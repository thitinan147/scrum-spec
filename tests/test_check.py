"""Tests for skills/scrum-spec/scripts/check.py against the fixture folders in evals/files/.

Run: python3 -m unittest discover -s tests
Uses only the standard library.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CHECK = REPO / "skills" / "scrum-spec" / "scripts" / "check.py"
FIXTURES = REPO / "evals" / "files"


def run(name: str) -> tuple[int, str]:
    return run_path(FIXTURES / name)


def run_path(*folders: Path | str) -> tuple[int, str]:
    result = subprocess.run(
        [sys.executable, "-I", str(CHECK), *map(str, folders)],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.returncode, result.stdout


CONFIG = """<!-- scrum-spec config -->
docs_root: scrum-spec/sprint
backlog_root: scrum-spec/backlog
glossary_root: scrum-spec/glossary
code_roots: ., ../api
"""


DECISIONS = """<!-- scrum-spec decisions · t-1 -->
## Decisions

| # | Topic | Decision | Type | Decided by · date | Confirmed by · date | Files updated |
|---|---|---|---|---|---|---|
| D1 | How many days ahead can people book | 30 days | decided | Alex (PO) · 2026-01-03 | – | 02-ac (AC1) |
| D2 | Until when can a booking be cancelled | 1 hour before it starts | decided | Sam (BE) · 2026-01-04 | – | 02-ac (EC1) |
"""

QUESTIONS_HEADER = (
    "| # | Question | Ask (PO / BE) | Needed before | Proposal | Status |\n"
    "|---|---|---|---|---|---|\n"
)


def make_project(base: Path, ac: str, extra: dict[str, str] | None = None) -> Path:
    """A tiny project with a config, one source file in each code root, and one ticket holding `ac` (plus `extra` files)."""
    (base / "app" / "scrum-spec").mkdir(parents=True)
    (base / "app" / "scrum-spec" / "config.md").write_text(CONFIG, encoding="utf-8")
    (base / "app" / "src").mkdir()
    (base / "app" / "src" / "booking.ts").write_text("", encoding="utf-8")
    (base / "api" / "docs").mkdir(parents=True)
    (base / "api" / "docs" / "openapi.yaml").write_text("", encoding="utf-8")
    ticket = base / "app" / "scrum-spec" / "sprint" / "t-1"
    ticket.mkdir(parents=True)
    (ticket / "02-ac.md").write_text("<!-- scrum-spec 02 · refine-ac · 2026-01-01 -->\n" + ac, encoding="utf-8")
    for name, body in (extra or {}).items():
        (ticket / name).write_text(body, encoding="utf-8")
    return ticket


class CheckTest(unittest.TestCase):
    def test_full_ticket_passes_with_full_coverage(self):
        code, out = run("demo-room-booking")
        self.assertEqual(code, 0, out)
        self.assertIn("## Errors (0)", out)
        self.assertIn("(100% · 7/7)", out)

    def test_assumptions_and_questionnaire_answers_are_reported(self):
        _, out = run("demo-room-booking")
        self.assertIn("## Assumptions in 00-decisions.md (1)", out)
        self.assertIn("## Questionnaire answers (1)", out)
        self.assertIn("## Open [ask] (0)", out)

    def test_no_tasks_file_hides_coverage(self):
        code, out = run("small-room-note")
        self.assertEqual(code, 0, out)
        self.assertNotIn("Coverage", out)
        self.assertIn("## Open [ask] (1)", out)

    def test_bug_track_ac_and_ec_rows_are_covered(self):
        code, out = run("bug-double-booking")
        self.assertEqual(code, 0, out)
        self.assertIn("(100% · 3/3)", out)

    def test_structural_errors_fail_the_run(self):
        code, out = run("bad")
        self.assertEqual(code, 1, out)
        self.assertIn("## Errors (4)", out)
        self.assertIn("01-input.md:1 missing first line", out)
        self.assertIn("<!-- scrum-spec 01 · <command> · <YYYY-MM-DD> -->", out)
        self.assertIn("broken table", out)
        self.assertIn("leftover substitution text: <docs_root>", out)
        self.assertIn("cites D7 but 00-decisions.md has no such row", out)
        self.assertNotIn("cites D1", out)

    def test_hard_to_read_lines_are_reported_but_do_not_fail(self):
        code, out = run("hard-to-read")
        self.assertEqual(code, 0, out)
        self.assertIn("## Hard to read (4)", out)
        self.assertIn("02-ac.md:8 line is", out)
        self.assertIn("02-ac.md:9 has ' · ' 3 times", out)
        self.assertIn("02-ac.md:19 cell 4 is", out)
        self.assertIn("02-ac.md:20 cell 4 has ' · ' 3 times", out)

    def test_summary_lines_and_code_blocks_are_not_reported(self):
        _, out = run("hard-to-read")
        self.assertNotIn("02-ac.md:4 ", out)
        self.assertNotIn("02-ac.md:12 ", out)

    def test_readable_ticket_has_no_readability_section(self):
        _, out = run("bug-double-booking")
        self.assertNotIn("## Hard to read", out)

    def test_cited_paths_must_exist_in_a_code_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            ticket = make_project(Path(tmp), (
                "- Files: `src/booking.ts:12` and `docs/openapi.yaml`\n"
                "- New file: `src/room-list.tsx` (new)\n"
                "- Not paths: `/api/bookings`, `application/json`, `<flow>/x/`\n"
                "- Wrong: `src/missing.ts`\n"
            ))
            code, out = run_path(ticket)
        self.assertEqual(code, 1, out)
        self.assertIn("## Errors (1)", out)
        self.assertIn("02-ac.md:5 cites a path that does not exist: src/missing.ts", out)

    def test_paths_are_not_checked_outside_document_folders(self):
        _, out = run("demo-room-booking")
        self.assertIn("Cited paths · not checked", out)

    def test_approval_needs_a_person_with_role_and_date(self):
        with tempfile.TemporaryDirectory() as tmp:
            ticket = make_project(Path(tmp), (
                "**approve:** ✅ Alex (PO) · 2026-01-02\n"
                "**approve:** ✅ PO\n"
                "**approve:** ✅ Claude (AI) · 2026-01-02\n"
                "**approve:** ❌ not yet · waiting for PO\n"
            ))
            code, out = run_path(ticket)
        self.assertEqual(code, 1, out)
        self.assertIn("## Errors (2)", out)
        self.assertIn("02-ac.md:3 approval must read ✅ <name> (<role>) · YYYY-MM-DD", out)
        self.assertIn("02-ac.md:4 approval must come from a person, not an AI", out)

    def test_approval_keeps_decisions_the_owner_made_later(self):
        with tempfile.TemporaryDirectory() as tmp:
            ticket = make_project(Path(tmp), "**approve:** ✅ Alex (PO) · 2026-01-02 (incl. D1 · 2026-01-03)\n",
                                  {"00-decisions.md": DECISIONS})
            code, out = run_path(ticket)
        self.assertEqual(code, 0, out)

    def test_approval_note_must_cite_an_existing_decision(self):
        with tempfile.TemporaryDirectory() as tmp:
            ticket = make_project(Path(tmp), "**approve:** ✅ Alex (PO) · 2026-01-02 (incl. D2, D9 · 2026-01-04)\n",
                                  {"00-decisions.md": DECISIONS})
            code, out = run_path(ticket)
        self.assertEqual(code, 1, out)
        self.assertIn("## Errors (1)", out)
        self.assertIn("02-ac.md:2 cites D9 but 00-decisions.md has no such row", out)

    def test_summary_line_counting_questions_is_not_a_question(self):
        with tempfile.TemporaryDirectory() as tmp:
            ticket = make_project(Path(tmp), "x\n", {"06-handoff.md": (
                "<!-- scrum-spec 06 · sprint-handoff · 2026-01-05 -->\n"
                "**Summary:** AC 2 · EC 1 · [ask] that affect testing 0\n"
                "- [ask: which account to test with · QA]\n"
            )})
            code, out = run_path(ticket)
        self.assertEqual(code, 0, out)
        self.assertIn("## Open [ask] (1)", out)
        self.assertIn("06-handoff.md:3 ", out)
        self.assertNotIn("06-handoff.md:2 ", out)

    def test_open_questions_still_marked_open_are_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            ticket = make_project(Path(tmp), QUESTIONS_HEADER + (
                "| Q1 | Show the booker's name | PO | later | show it | ❌ open |\n"
                "| Q2 | How many days ahead | PO | design | 30 days | ✅ answered (D1) |\n"
            ))
            code, out = run_path(ticket)
        self.assertIn("## Open Questions still open in 02-ac.md (1)", out)
        self.assertIn("Q1 Show the booker's name", out)
        self.assertNotIn("Q2 How many days", out)

    def test_story_map_decisions_need_a_person(self):
        code, out = run("backlog/room-booking-flow")
        self.assertEqual(code, 0, out)

    def test_story_map_result_by_an_ai_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            flow = Path(tmp)
            (flow / "00-map.md").write_text(
                "| # | Topic | Proposal | Who decides | Result |\n|---|---|---|---|---|\n"
                "| T1 | How to split | by workflow step | PO | ✅ by workflow step · Claude (AI) · 2026-01-02 |\n"
                "| T2 | First slice | book a small room | PO | ✅ PO |\n",
                encoding="utf-8",
            )
            code, out = run_path(flow)
        self.assertEqual(code, 1, out)
        self.assertIn("T1 result must be decided by a person, not an AI", out)
        self.assertIn("T2 result must read ✅ <what was decided> · <name> (<role>) · YYYY-MM-DD", out)

    def test_ai_deciders_are_reported_but_do_not_fail(self):
        code, out = run("demo-room-booking")
        self.assertEqual(code, 0, out)
        self.assertIn("## Decided by an AI (1)", out)

    def test_summary_counts_must_match_the_tables(self):
        with tempfile.TemporaryDirectory() as tmp:
            ticket = make_project(Path(tmp), (
                "**Summary:** AC 2 · EC 0 · Open Questions 0\n"
                "| # | Given | When | Then | Verified by |\n|---|---|---|---|---|\n"
                "| AC1 | a | b | c | – |\n| EC1 | a | b | c | – |\n"
            ), {"05-tasks.md": (
                "<!-- scrum-spec 05 · plan-tasks · 2026-01-05 -->\n"
                "**Summary:** 1 task · Coverage AC/EC 2/2 · can start now: FE-01\n"
                "| Task | Summary | AC | Owner | Est. | Depends on |\n|---|---|---|---|---|---|\n"
                "| FE-01 | Build the page | AC1 | | | – |\n"
            )})
            code, out = run_path(ticket)
        self.assertEqual(code, 1, out)
        self.assertIn("## Errors (2)", out)
        self.assertIn("02-ac.md:2 **Summary:** does not match the table (says AC 2 · EC 0 but the table has AC 1 · EC 1)", out)
        self.assertIn("05-tasks.md:2 **Summary:** does not match the table (says 1 tasks · Coverage 2/2 but the files have 1 tasks · Coverage 1/2)", out)

    def test_several_folders_print_one_block_each_and_skip_files(self):
        code, out = run_path(FIXTURES / "demo-room-booking", FIXTURES / "bad", FIXTURES / "bad" / "01-input.md")
        self.assertEqual(code, 1, out)
        self.assertIn("demo-room-booking · Errors 0 · open questions", out)
        self.assertIn("bad · Errors 4", out)
        self.assertNotIn("## Coverage", out)

    def test_status_shows_track_approvals_questions_and_next_step(self):
        code, out = run_path("--status", FIXTURES / "backlog" / "room-booking-flow" / "book-small-room",
                             FIXTURES / "backlog" / "room-booking-flow" / "approve-large-room", FIXTURES / "bug-double-booking")
        self.assertEqual(code, 0, out)
        self.assertIn("| Work | Track | Files | approve | Blocking | Later | Waiting on | Next | Errors |", out)
        self.assertIn("| book-small-room | small · backlog | 01 02 | 01✅ 02✅ | 0 | 0 | – | plan-goal | 0 |", out)
        self.assertIn("| approve-large-room | large · backlog | 01 | 01✅ |", out)
        self.assertIn("| 2 · refine-ac | 0 |", out)
        self.assertIn("| bug-double-booking |", out)

    def test_status_finds_work_folders_under_roots_without_shell_globs(self):
        code, out = run_path("--status", FIXTURES / "backlog")
        self.assertEqual(code, 0, out)
        self.assertIn("| room-booking-flow/book-small-room | small · backlog |", out)
        self.assertIn("| room-booking-flow/approve-large-room | large · backlog |", out)
        self.assertIn("## Questions blocking the next step\n- none", out)

    def test_status_lists_blocking_questions_but_not_later_ones(self):
        with tempfile.TemporaryDirectory() as tmp:
            ticket = make_project(Path(tmp), QUESTIONS_HEADER + (
                "| Q1 | Show the booker's name | PO | later | show it | ❌ open |\n"
                "| Q2 | How many days ahead | PO | design | 30 days | ❌ open |\n"
            ))
            code, out = run_path("--status", ticket)
        self.assertIn("| t-1 | ? | 02 | – | 1 | 1 | PO 2 | 1 · refine-intake | 0 |", out)
        self.assertIn("## Questions blocking the next step", out)
        self.assertIn("Q2 How many days ahead · ask PO · before design", out)
        self.assertNotIn("Q1 Show the booker", out)

    def test_summary_open_questions_count_must_match_table(self):
        with tempfile.TemporaryDirectory() as tmp:
            ticket = make_project(Path(tmp), "**Summary:** AC 0 · EC 0 · Open Questions 1\n\n" + QUESTIONS_HEADER + (
                "| Q1 | Show the booker's name | PO | later | show it | ✅ answered |\n"
                "| Q2 | How many days ahead | PO | design | 30 days | ❌ open |\n"
            ))
            code, out = run_path(ticket)
        self.assertEqual(code, 1, out)
        self.assertIn("says Open Questions 1 but the table has 2", out)

    def test_question_left_in_input_after_ac_is_an_error_not_a_second_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            ticket = make_project(Path(tmp), QUESTIONS_HEADER + (
                "| Q1 | How many days ahead | PO | design | 30 days | ❌ open |\n"
            ), {"01-input.md": "<!-- scrum-spec 01 · refine-intake · 2026-01-01 -->\n"
                                "- [ask: how many days ahead · PO]\n"})
            code, out = run_path("--status", ticket)
        self.assertIn("| t-1 | ? | 01 02 | – | 1 | 0 | PO 1 |", out)
        self.assertIn("01-input.md:2 has [ask] but 02-ac.md exists", out)

    def test_single_backlog_card_is_found_one_level_down(self):
        with tempfile.TemporaryDirectory() as tmp:
            card = Path(tmp) / "backlog" / "export-bookings"
            card.mkdir(parents=True)
            (card / "01-input.md").write_text(
                "<!-- scrum-spec 01 · refine-intake · 2026-01-01 -->\n"
                "- **Sprint / Ticket ID:** not in a Sprint yet\n"
                "- **Track:** small · reason: an existing API\n",
                encoding="utf-8",
            )
            code, out = run_path("--status", Path(tmp) / "backlog")
        self.assertEqual(code, 0, out)
        self.assertIn("| export-bookings | small · backlog | 01 |", out)

    def test_other_languages_in_content_do_not_break_markers(self):
        with tempfile.TemporaryDirectory() as tmp:
            ticket = make_project(Path(tmp), (
                "**Summary:** AC 1 · EC 0 · Open Questions 1\n"
                "| # | Given | When | Then | Verified by |\n|---|---|---|---|---|\n"
                "| AC1 | ผู้ใช้เข้าสู่ระบบแล้ว | กดจอง | เห็นการจอง | – |\n\n" + QUESTIONS_HEADER +
                "| Q1 | จองล่วงหน้าได้กี่วัน | PO | design | 30 วัน | ❌ open |\n"
            ))
            code, out = run_path(ticket)
        self.assertEqual(code, 0, out)
        self.assertIn("Q1 จองล่วงหน้าได้กี่วัน", out)

    def test_missing_folder_exits_2(self):
        code, _ = run("does-not-exist")
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
