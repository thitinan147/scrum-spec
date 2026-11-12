---
name: scrum-spec
description: HUMAN-ONLY COMMAND. Drafts a Scrum team's spec, one spec.md per story - stories from a flow, acceptance criteria and open questions, tasks grounded in the code, test steps for the tester. Finds facts in the code, asks people only for decisions, records who decided. Type /scrum-spec, e.g. /scrum-spec ac rb-12-book-room.
license: MIT
compatibility: Claude Code, Codex, Cursor and other Agent Skills clients. Needs git and Python 3.10+ (standard library only). poppler is optional, for large PDFs.
metadata:
  author: Thitinan
  version: "0.2.0"
  short-description: Draft Scrum specs from the code; the AI proposes, people decide
argument-hint: "<help | split | ac | tasks | handoff> [<work>] [text or path of a PDF or image]"
allowed-tools: Bash(python3 -I ${CLAUDE_SKILL_DIR}/scripts/check.py *) Bash(git rev-parse *) Bash(git status *) Bash(git log *) Bash(git diff *) Bash(git blame *) Bash(git config user.name)
disable-model-invocation: true
---

# scrum-spec

Argument: `$ARGUMENTS` (if unreplaced: the text the user wrote after the command)

Goal: remove waiting. The PO edits a draft instead of a blank page, dev start from tasks grounded in the code, the tester has test steps on day one. Write only what someone will act on; each fact lives in one place, cited elsewhere.

## Rules

- **Fact, proposal or question, never a guess.** A fact has a source (path, input page, D number); a proposal says "Proposal:" and why; anything else is a row in Questions.
- **People decide.** The PO decides scope, rules and AC; dev decide how to build. Never fill in points, priority, owner or capacity.
- **Every decision has a person's name:** `git config user.name` for chat answers; for answers in the file, the name written there, else `git blame`, else ask. Never an AI.
- **Ask before** overwriting text a person wrote (`git diff`). Never commit, push, delete or move files.
- **Language:** headings, labels, columns and markers stay as in the templates (`check.py` reads them); other text follows the file, or the input for a new file.
- No passwords, tokens or customer personal data in documents.

## Commands

| Command | Step file | Writes |
|---|---|---|
| `help` | [references/help.md](references/help.md) | nothing; show it with values filled in |
| `split` | [steps/split.md](steps/split.md) | `<docs_root>/<flow>/map.md`, then a `spec.md` per confirmed story |
| `ac` | [steps/ac.md](steps/ac.md) | Story, Rules, Acceptance Criteria, Questions in `spec.md` |
| `tasks` | [steps/tasks.md](steps/tasks.md) | Tasks in `spec.md` |
| `handoff` | [steps/handoff.md](steps/handoff.md) | Test steps in `spec.md` |

- `<command>`: `/scrum-spec`, or `/scrum-spec:scrum-spec` as a plugin
- No command: run the next missing section's command for the work in this conversation, saying so in one line. No work either: run `check.py <docs_root>` and ask which spec to continue
- Input from a PDF or image: also read [references/input.md](references/input.md)

## Where files live

- `<docs_root>/<work>/spec.md` per story or ticket (`<flow>/<story>` from `split`); `<work>` is lowercase-with-dashes, ticket ID first
- `scrum-spec/config.md` at the git root is optional. Keys, one per line, with these defaults:

```
docs_root: scrum-spec
code_roots: .
roles: PO, Dev, QA
task_prefixes: FE, BE
```

`code_roots`: every repo to search (e.g. `., ../api`); `roles` fill the Ask column.

`spec.md` starts with `<!-- scrum-spec -->` and `# <work>`, then `## Story`, `## Rules`, `## Acceptance Criteria`, `## Questions`, `## Decisions`, `## Tasks`, `## Test steps`, in this order.

## Workflow

1. **Find the work:** the name given, else the one in this conversation, else ask, listing existing folders. Read the whole step file and the existing `spec.md`.
2. **Gather facts yourself:** the input, then every `code_roots` path (screens, routes, APIs, permissions, fixtures); grep other specs instead of reading them whole. Ask people only for decisions and facts not in the repo. A contradiction: cite the path and ask.
3. **Write only this command's sections,** plus edits a decision requires (item 6). An existing section is the base: change only what has new information. If a person's edit to Rules or AC left Tasks or Test steps behind, update them and say so. Headings and columns exactly as the template; text in parentheses is an instruction.
4. **Check:** run `python3 -I <skill_dir>/scripts/check.py <folder>` (`<skill_dir>` holds this file). Fix every `ERROR`, rerun; if it cannot run, say so.
5. **Ask** in the same turn, never ending on a bare list:
   - at most 4 at a time, most impact first, only ones that change scope, an AC, an API or a task; the rest wait in the table for the next round
   - each stands alone, says what it changes, offers a "(Recommended)" option with its reason, and "Don't know / ask <role>"
   - ask only questions for the user's role (from this conversation, else ask it with the first questions); other roles' questions and "Don't know" stay in Questions for anyone to answer later in the Answer cell
   - "use the recommendations" accepts every recommended option
6. **Apply answers at once** (from chat, or an Answer cell someone filled in):
   - add `- **D<n>** <what was decided> · <name> · <YYYY-MM-DD>` to Decisions and delete the question's row
   - fix every section it affects, replacing the old text; grep other specs in `<docs_root>` for the same rule and fix them too, each with its own D starting `per <work> D<n>:`
   - approval: a change that follows a D keeps a ✅ and appends `(incl. D<n>)`. Any other change to Rules or AC sets `**approve:** ❌ waiting for PO (changed <YYYY-MM-DD>)`
   - "use the proposal for now": start the D with `assumption:` and keep the row with Answer `⚠️ D<n>` until the asked role confirms
7. **Reply** in this format plus any line the step adds, never the whole document:

```
✅ <command> · <work> · saved <path>
Added: <e.g. AC 5 · EC 3 · Questions 2 (blocking 1)>
Decisions: <D numbers, or none> · approve: <✅ name · date / ❌ waiting for PO>
Waiting on: <role: Q numbers, or none>
Next: <command> <next command> <work>, or none
```
