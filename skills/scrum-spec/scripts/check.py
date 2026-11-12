#!/usr/bin/env python3
"""Deterministic checks for a scrum-spec document folder
(a ticket, a story, a flow, the glossary or the sprint docs root).

Usage:
  python3 -I check.py <folder>                 full report of one folder
  python3 -I check.py <folder> <folder> ...    one block per folder: errors and open counts only
  python3 -I check.py --status <folder> ...    one table row per work folder found in or under each
                                               folder (two levels deep, e.g. docs_root and backlog_root):
                                               track, files, approvals, open questions, who to ask,
                                               next step, then the questions that block the next step

Exits 1 when a structural error is found (broken table, leftover
substitution text or config placeholder, missing header line, task or
decision reference that does not exist, a cited file path that does not
exist, an approval without a person or given by an AI, a **Summary:** count
that does not match its table). Open questions, assumptions, questionnaire
answers, AI deciders, AC coverage and hard-to-read lines are reported but
never fail the run. Arguments that are not folders are skipped when more
than one is given (so shell globs such as scrum-spec/sprint/* work).

Cited paths are checked only when the folder sits inside docs_root,
backlog_root or glossary_root of a project config
(scrum-spec/config.md found in the folder or a parent).
Read-only: never edits files. Needs Python 3.9 or newer.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Config keys that step prompts write as <key>; one left in a document means a missed substitution.
PLACEHOLDERS = (
    "skill_dir", "command", "roles", "docs_root", "backlog_root", "glossary_root", "domain_source",
    "definition_of_done",
    "code_roots", "project_rules", "api_spec", "ac_owner", "api_owner", "tester",
    "layers", "task_prefixes", "estimation", "review_term", "board", "design_source",
    "input_sources", "personas", "ticket_format", "aliases",
)
STRAY = [r"\\[0-9]", r"\$[0-9]", r"\{\{[^}]*\}\}", r"<(?:" + "|".join(PLACEHOLDERS) + r")>"]
HEADER = re.compile(r"^<!-- scrum-spec ")
PARENS = re.compile(r"\(([^()]*)\)")
DECISION_ID = re.compile(r"\bD([0-9]+)\b")
SEPARATOR = re.compile(r"^\|[\s:|-]+\|\s*$")
QUOTE = re.compile(r"^\s*>\s?(.*)$")
ANSWER_LABEL = re.compile(r"^Answer:\s*")
FENCE = re.compile(r"^\s*```")
ASK = re.compile(r"\[ask[:\]]")

# Readability limits from references/format.md (characters, not bytes).
MAX_CELL = 160
MAX_LINE = 300
MAX_DOTS = 2
DOT = " · "
SHOW_READABILITY = 20
SUMMARY = re.compile(r"^\*\*(?:Summary|Result|approve):\*\*")  # summary lines list counts with " · " on purpose

# Cited paths and approvals.
CONFIG_FILE = Path("scrum-spec") / "config.md"
PATH_TOKEN = re.compile(r"`([^`\s]+)`(\s*\(new\))?")
PATH_SUFFIX = re.compile(r"(:[0-9]+(-[0-9]+)?|#L[0-9]+(-L?[0-9]+)?)$")
FILE_LIKE = re.compile(r"(\.[A-Za-z0-9]{1,8}|/)$")
NOT_A_PATH = re.compile(r"[<>*{}$|]|://")
AI_NAME = re.compile(r"\b(?:Claude|AI|GPT|Copilot|Gemini|Codex)\b", re.IGNORECASE)
APPROVE_LINE = re.compile(r"^\*\*approve:\*\*\s*(.*)$")
APPROVED_BY = re.compile(r"^✅ .+ \(.+\) · [0-9]{4}-[0-9]{2}-[0-9]{2}")
# Counts written on **Summary:** lines, checked against the tables they summarise.
SUMMARY_AC = re.compile(r"^\*\*Summary:\*\*\s*AC ([0-9]+) · EC ([0-9]+)(?: · Open Questions ([0-9]+))?")
SUMMARY_TASKS = re.compile(r"^\*\*Summary:\*\*\s*([0-9]+) tasks? · Coverage AC/EC ([0-9]+)/([0-9]+)")
ASK_ROLE = re.compile(r"\[ask[^\]]*·\s*([^\]·]+?)\s*\]")
STEP_FILES = {"01": "refine-intake", "02": "refine-ac", "03": "plan-review", "04": "plan-design",
              "05": "plan-tasks", "06": "sprint-handoff"}
TRACKS = {"large": ["01", "02", "03", "04", "05", "06"], "small": ["01", "02", "05", "06"], "bug": ["01", "02", "05", "06"]}
DECIDED_BY = re.compile(r"^✅ .+ · .+ \(.+\) · [0-9]{4}-[0-9]{2}-[0-9]{2}")
NOT_IN_SPRINT = "not in a Sprint yet"


def step_of(name: str) -> str | None:
    """The step number a file belongs to, or None when it is not a step file."""
    return name[:2] if name[:2] in STEP_FILES and name[2:3] == "-" else None


def cells(line: str) -> int:
    return line.count("|") - line.count("\\|")


def check_tables(path: Path, lines: list[str], errors: list[str]) -> None:
    i = 0
    while i < len(lines):
        if lines[i].startswith("|") and i + 1 < len(lines) and SEPARATOR.match(lines[i + 1]):
            want = cells(lines[i])
            j = i + 2
            while j < len(lines) and lines[j].startswith("|"):
                got = cells(lines[j])
                if got != want:
                    errors.append(f"{path.name}:{j + 1} broken table: this row has {got - 1} cells, the header has {want - 1}")
                j += 1
            i = j
        else:
            i += 1


def table_rows(lines: list[str], first_col: re.Pattern) -> list[list[str]]:
    rows = []
    for line in lines:
        if line.startswith("|") and not SEPARATOR.match(line):
            parts = [c.strip() for c in line.strip().strip("|").split("|")]
            if parts and first_col.fullmatch(parts[0]):
                rows.append(parts)
    return rows


def quoted_answers(lines: list[str]) -> list[tuple[int, str]]:
    """Non-empty answers in a questionnaire: each run of '>' lines, without the 'Answer:' label."""
    found = []
    i = 0
    while i < len(lines):
        if not QUOTE.match(lines[i]):
            i += 1
            continue
        start, parts = i, []
        while i < len(lines) and QUOTE.match(lines[i]):
            text = ANSWER_LABEL.sub("", QUOTE.match(lines[i]).group(1).strip())
            if text:
                parts.append(text)
            i += 1
        if parts:
            found.append((start + 1, " ".join(parts)))
    return found


def split_cells(line: str) -> list[str]:
    return [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]


def check_readability(path: Path, lines: list[str], notes: list[str]) -> None:
    in_code = False
    for n, line in enumerate(lines, 1):
        if FENCE.match(line):
            in_code = not in_code
            continue
        if in_code or n == 1 or SEPARATOR.match(line):
            continue
        if line.startswith("|"):
            for k, cell in enumerate(split_cells(line), 1):
                if len(cell) > MAX_CELL:
                    notes.append(f"{path.name}:{n} cell {k} is {len(cell)} characters (over {MAX_CELL}) · move the detail below the table")
                elif cell.count(DOT) > MAX_DOTS:
                    notes.append(f"{path.name}:{n} cell {k} has ' · ' {cell.count(DOT)} times · split the cell or move it below the table")
        elif len(line) > MAX_LINE:
            notes.append(f"{path.name}:{n} line is {len(line)} characters (over {MAX_LINE}) · split it into sub-bullets")
        elif line.count(DOT) > MAX_DOTS and not SUMMARY.match(line):
            notes.append(f"{path.name}:{n} has ' · ' {line.count(DOT)} times · split it into sub-bullets")


def read_config(folder: Path) -> tuple[Path, dict[str, str]] | None:
    """Project root and key/value pairs of the nearest project config, if any."""
    for base in [folder, *folder.parents]:
        cfg = base / CONFIG_FILE
        if cfg.is_file():
            values = {}
            for line in cfg.read_text(encoding="utf-8").splitlines():
                found = re.match(r"^([a-z_]+):\s*(.*)$", line)
                if found:
                    values[found.group(1)] = found.group(2).strip()
            return base, values
    return None


def path_roots(folder: Path) -> list[Path] | None:
    """Folders a cited path may be relative to, or None when the folder is not a project document folder."""
    found = read_config(folder)
    if not found:
        return None
    root, conf = found
    doc_dirs = [
        (root / conf[key]).resolve()
        for key in ("docs_root", "backlog_root", "glossary_root")
        if conf.get(key, "–") not in ("", "–")
    ]
    if not any(folder == d or d in folder.parents for d in doc_dirs):
        return None
    roots = [root, folder, *doc_dirs]
    code_roots = conf.get("code_roots", "–")
    if code_roots not in ("", "–"):
        roots += [(root / r.strip()).resolve() for r in code_roots.split(",") if r.strip()]
    return list(dict.fromkeys(roots))


def check_paths(path: Path, lines: list[str], roots: list[Path], errors: list[str]) -> None:
    in_code = False
    for n, line in enumerate(lines, 1):
        if FENCE.match(line):
            in_code = not in_code
            continue
        if in_code:
            continue
        for found in PATH_TOKEN.finditer(line):
            token, is_new = found.group(1), found.group(2)
            cited = PATH_SUFFIX.sub("", token).rstrip(",.;")
            if is_new or "/" not in cited or cited.startswith(("/", "~")):
                continue
            if NOT_A_PATH.search(cited) or not FILE_LIKE.search(cited):
                continue
            if not any((r / cited).exists() for r in roots):
                errors.append(
                    f"{path.name}:{n} cites a path that does not exist: {token} "
                    "(add (new) after a file that will be created · otherwise fix the path or remove it)"
                )


def check_approvals(path: Path, lines: list[str], errors: list[str]) -> None:
    for n, line in enumerate(lines, 1):
        found = APPROVE_LINE.match(line.strip())
        if found:
            value = found.group(1)
            if AI_NAME.search(value):
                errors.append(f"{path.name}:{n} approval must come from a person, not an AI: {value[:80]}")
            elif value.startswith("✅") and not APPROVED_BY.match(value):
                errors.append(f"{path.name}:{n} approval must read ✅ <name> (<role>) · YYYY-MM-DD: {value[:80]}")
    for row in table_rows(lines, re.compile(r"T[0-9]+")):
        result = row[4] if len(row) > 4 else ""
        if AI_NAME.search(result):
            errors.append(f"{path.name} {row[0]} result must be decided by a person, not an AI")
        elif result.startswith("✅") and not DECIDED_BY.match(result):
            errors.append(f"{path.name} {row[0]} result must read ✅ <what was decided> · <name> (<role>) · YYYY-MM-DD")


def id_key(ref: str) -> tuple[str, int]:
    return ref[:2], int(re.sub(r"\D", "", ref))


def field(lines: list[str], label: str) -> str:
    """Value of a '- **<label>:** value' line, or ''."""
    for line in lines:
        found = re.match(r"^\s*-\s*\*\*" + re.escape(label) + r":\*\*\s*(.*)$", line)
        if found:
            return found.group(1).strip()
    return ""


def check_counts(text: dict[str, list[str]], defined: set[str], covered: dict[str, list[str]],
                 task_rows: list[list[str]], errors: list[str]) -> None:
    """**Summary:** counts are written by hand, so they drift when AC or tasks change later."""
    for n, line in enumerate(text.get("02-ac.md", []), 1):
        found = SUMMARY_AC.match(line.strip())
        if found and defined:
            ac = sum(1 for d in defined if d.startswith("AC"))
            ec = len(defined) - ac
            if (int(found.group(1)), int(found.group(2))) != (ac, ec):
                errors.append(f"02-ac.md:{n} **Summary:** does not match the table (says AC {found.group(1)} · EC {found.group(2)} "
                              f"but the table has AC {ac} · EC {ec}) · count again")
        if found and found.group(3) is not None:
            q = len(table_rows(text["02-ac.md"], re.compile(r"Q[0-9]+")))
            if int(found.group(3)) != q:
                errors.append(f"02-ac.md:{n} **Summary:** says Open Questions {found.group(3)} "
                              f"but the table has {q} · count again")
        if found:
            break
    for n, line in enumerate(text.get("05-tasks.md", []), 1):
        found = SUMMARY_TASKS.match(line.strip())
        if found:
            want = (len(task_rows), len(set(covered) & defined) if defined else int(found.group(2)),
                    len(defined) if defined else int(found.group(3)))
            got = tuple(int(g) for g in found.groups())
            if got != want:
                errors.append(f"05-tasks.md:{n} **Summary:** does not match the table (says {got[0]} tasks · Coverage {got[1]}/{got[2]} "
                              f"but the files have {want[0]} tasks · Coverage {want[1]}/{want[2]}) · count again")
            break


def analyze(folder: Path) -> dict:
    roots = path_roots(folder.resolve())
    files = sorted(folder.glob("*.md"))
    errors: list[str] = []
    questions: list[str] = []
    asked: list[str] = []  # role of each open question, for "who to ask"
    answers: list[str] = []
    readability: list[str] = []
    text: dict[str, list[str]] = {}

    # Once 02-ac.md has a numbered Open Questions table, questions live there and not in 01-input.md.
    ac_file = folder / "02-ac.md"
    has_ac = ac_file.is_file() and bool(re.search(r"^\| Q[0-9]+ \|", ac_file.read_text(encoding="utf-8"), re.M))
    for path in files:
        lines = path.read_text(encoding="utf-8").split("\n")
        text[path.name] = lines
        if re.match(r"^[0-9]{2}-", path.name) and not HEADER.match(lines[0] if lines else ""):
            step = path.name[:2]
            errors.append(
                f"{path.name}:1 missing first line <!-- scrum-spec ... --> "
                f"(put back <!-- scrum-spec {step} · <command> · <YYYY-MM-DD> -->)"
            )
        check_tables(path, lines, errors)
        check_readability(path, lines, readability)
        check_approvals(path, lines, errors)
        if roots:
            check_paths(path, lines, roots, errors)
        for n, line in enumerate(lines, 1):
            for pat in STRAY:
                found = re.search(pat, line)
                if found:
                    errors.append(f"{path.name}:{n} leftover substitution text: {found.group(0)}")
            if ASK.search(line) and path.name == "01-input.md" and has_ac:
                errors.append(f"01-input.md:{n} has [ask] but 02-ac.md exists "
                              f"· move it to Open Questions in 02-ac.md (if not there yet) and delete it from 01-input.md")
            elif ASK.search(line) and not path.name.startswith(("03-", "questions-")) and not SUMMARY.match(line.strip()):
                questions.append(f"{path.name}:{n} {line.strip()[:120]}")
                asked.extend(r.strip() for r in ASK_ROLE.findall(line))
        if path.name.startswith("questions-"):
            answers.extend(f"{path.name}:{n} {a[:120]}" for n, a in quoted_answers(lines))

    # AC defined in 02-ac
    defined = {r[0] for r in table_rows(text.get("02-ac.md", []), re.compile(r"(AC|EC)[0-9]+[a-z]?"))}

    # AC referenced by tasks
    task_rows = table_rows(text.get("05-tasks.md", []), re.compile(r"[A-Z]+-[0-9]+"))
    covered: dict[str, list[str]] = {}
    for row in task_rows:
        ac_col = row[2] if len(row) > 2 else ""
        for ref in re.findall(r"\b(?:AC|EC)[0-9]+[a-z]?\b", ac_col):
            covered.setdefault(ref, []).append(row[0])
            if defined and ref not in defined:
                errors.append(f"05-tasks.md {row[0]} cites {ref} but 02-ac.md has no such row")
    check_counts(text, defined, covered, task_rows, errors)

    # decisions: every D<n> written inside parentheses must exist in 00-decisions.md
    has_decisions = "00-decisions.md" in text
    dec_rows = table_rows(text.get("00-decisions.md", []), re.compile(r"D[0-9]+"))
    dec_ids = {r[0] for r in dec_rows}
    assumptions = [f"{r[0]} {r[1]} → {r[2]}" for r in dec_rows if len(r) > 3 and "assumption" in r[3].lower()]
    open_rows = [r for r in table_rows(text.get("02-ac.md", []), re.compile(r"Q[0-9]+")) if "❌" in r[-1]]
    open_questions = [f"{r[0]} {r[1]}" for r in open_rows]
    later = sum(1 for r in open_rows if len(r) > 3 and "later" in r[3].lower())
    blocking = [f"{r[0]} {r[1]} · ask {r[2]} · before {r[3]}" for r in open_rows if len(r) > 3 and "later" not in r[3].lower()]
    asked.extend(r[2] for r in open_rows if len(r) > 2)
    ai_deciders = [f"{r[0]} {r[1]} · {r[4]}" for r in dec_rows if len(r) > 4 and AI_NAME.search(r[4])]
    for name, lines in text.items():
        for n, line in enumerate(lines, 1):
            for group in PARENS.findall(line):
                for num in DECISION_ID.findall(group):
                    if not has_decisions:
                        errors.append(f"{name}:{n} cites D{num} but there is no 00-decisions.md")
                    elif f"D{num}" not in dec_ids:
                        errors.append(f"{name}:{n} cites D{num} but 00-decisions.md has no such row")

    return {
        "folder": folder, "roots": roots, "text": text, "errors": errors, "questions": questions,
        "asked": asked, "answers": answers, "readability": readability,
        "defined": defined, "covered": covered, "assumptions": assumptions,
        "open_questions": open_questions, "later": later, "blocking": blocking, "ai_deciders": ai_deciders,
    }


def print_report(r: dict) -> None:
    errors, questions, defined, covered = r["errors"], r["questions"], r["defined"], r["covered"]
    print(f"# check · {r['folder']}")
    print(f"\n## Errors ({len(errors)})")
    print("\n".join(f"- {e}" for e in errors) or "- none")

    if defined and "05-tasks.md" in r["text"]:
        uncovered = sorted(defined - set(covered), key=id_key)
        pct = round(100 * (len(defined) - len(uncovered)) / len(defined))
        print(f"\n## Coverage AC/EC → task ({pct}% · {len(defined) - len(uncovered)}/{len(defined)})")
        for ac in sorted(defined, key=id_key):
            print(f"- {ac}: {', '.join(covered.get(ac, [])) or 'no task'}")

    print(f"\n## Open [ask] ({len(questions)})")
    print("\n".join(f"- {q}" for q in questions) or "- none")
    if r["open_questions"]:
        print(f"\n## Open Questions still open in 02-ac.md ({len(r['open_questions'])})")
        print("\n".join(f"- {q}" for q in r["open_questions"]))
    print(f"\n## Assumptions in 00-decisions.md ({len(r['assumptions'])})")
    print("\n".join(f"- {a}" for a in r["assumptions"]) or "- none")
    if r["ai_deciders"]:
        print(f"\n## Decided by an AI ({len(r['ai_deciders'])}) · no person approved these rows, ask before using them")
        print("\n".join(f"- {a}" for a in r["ai_deciders"]))
    if r["roots"] is None:
        print("\n## Cited paths · not checked (folder is not inside docs_root, backlog_root or glossary_root of a config)")
    if r["answers"]:
        print(f"\n## Questionnaire answers ({len(r['answers'])}) · check they are recorded in 00-decisions.md")
        print("\n".join(f"- {a}" for a in r["answers"]))

    readability = r["readability"]
    if readability:
        print(f"\n## Hard to read ({len(readability)}) · fix per references/format.md, only in the files of the step being run")
        print("\n".join(f"- {x}" for x in readability[:SHOW_READABILITY]))
        if len(readability) > SHOW_READABILITY:
            print(f"- … {len(readability) - SHOW_READABILITY} more")


def print_compact(r: dict) -> None:
    errors = r["errors"]
    open_n = len(r["questions"]) + len(r["open_questions"])
    print(f"## {r['folder']} · Errors {len(errors)} · open questions {open_n} · questionnaire answers {len(r['answers'])}")
    for e in errors:
        print(f"- {e}")


def status_row(r: dict) -> str | None:
    """One row of the status table, or None when the folder holds no step files."""
    text = r["text"]
    step_names = {step_of(name): name for name in sorted(text) if step_of(name)}
    steps = sorted(step_names)
    if not steps:
        return None
    intake = text.get("01-input.md", [])
    track_value = field(intake, "Track").lower()
    track = next((t for t in TRACKS if track_value.startswith(t)), "")
    in_backlog = NOT_IN_SPRINT in field(intake, "Sprint / Ticket ID")
    approvals = []
    for step in steps:
        name = step_names[step]
        line = next((x for x in text[name] if APPROVE_LINE.match(x.strip())), "")
        if line:
            approvals.append(f"{step}{'✅' if '✅' in line else '❌'}")
    block = len(r["questions"]) + len(r["open_questions"]) - r["later"]
    who: dict[str, int] = {}
    for role in r["asked"]:
        who[role] = who.get(role, 0) + 1
    wanted = TRACKS.get(track, TRACKS["small"])
    missing = [s for s in wanted if s not in steps]
    if in_backlog and "02" in steps:
        nxt = "plan-goal"
    elif missing:
        nxt = f"{int(missing[0])} · {STEP_FILES[missing[0]]}"
    else:
        nxt = "7 · sprint-close at Sprint end"
    return (f"| {r.get('name', r['folder'].name)} | {track or '?'}{' · backlog' if in_backlog else ''} | {' '.join(steps)} "
            f"| {' '.join(approvals) or '–'} | {block} | {r['later']} "
            f"| {', '.join(f'{k} {v}' for k, v in sorted(who.items())) or '–'} | {nxt} | {len(r['errors'])} |")


def work_folders(base: Path) -> list[tuple[Path, str]]:
    """Folders holding step files at or up to two levels under `base`, with a name relative to it."""
    def has_steps(d: Path) -> bool:
        return any(step_of(f.name) for f in d.glob("*.md"))
    if has_steps(base):
        return [(base, base.name)]
    found = []
    for child in sorted(d for d in base.iterdir() if d.is_dir()):
        if has_steps(child):
            found.append((child, child.name))
        else:
            found += [(g, f"{child.name}/{g.name}") for g in sorted(child.iterdir()) if g.is_dir() and has_steps(g)]
    return found


def main() -> int:
    args = sys.argv[1:]
    status = "--status" in args
    args = [a for a in args if a != "--status"]
    if not args:
        print(__doc__)
        return 2
    many = status or len(args) > 1
    folders = [Path(a) for a in args if Path(a).is_dir()]
    if not many and not folders:
        print(f"folder not found: {args[0]}")
        return 2
    if status:
        named = [w for f in folders for w in work_folders(f)]
        results = [dict(analyze(f), name=name) for f, name in named]
    else:
        results = [analyze(f) for f in folders]
    if status:
        print("| Work | Track | Files | approve | Blocking | Later | Waiting on | Next | Errors |")
        print("|---|---|---|---|---|---|---|---|---|")
        rows = [row for row in (status_row(r) for r in results) if row]
        print("\n".join(rows) or "| no work | | | | | | | | |")
        blocking = [(r, r["blocking"] + [q.split(" ", 1)[1].lstrip("-* ") for q in r["questions"]]) for r in results]
        blocking = [(r, items) for r, items in blocking if items]
        print("\n## Questions blocking the next step")
        if not blocking:
            print("- none")
        for r, items in blocking:
            print(f"- **{r.get('name', r['folder'].name)}**")
            print("\n".join(f"  - {i[:160]}" for i in items))
        bad = [r for r in results if r["errors"]]
        for r in bad:
            print()
            print_compact(r)
    elif many:
        for r in results:
            print_compact(r)
    else:
        print_report(results[0])
    return 1 if any(r["errors"] for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())
