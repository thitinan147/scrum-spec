# Changelog

Versions below 1.0 may change the document format (markers, headings, file names, config keys). Each such change is listed here. From 1.0, a format change bumps the major version and comes with upgrade notes.

## 0.2.0 - smallest useful skill

Breaking: a new document format. v0.1 documents are not read or migrated; finish them with v0.1 or copy their AC into a new `spec.md`.

- Four commands: `split`, `ac`, `tasks`, `handoff` (plus `help`). Removed: `refine-intake` (folded into `ac`), `plan-goal`, `plan-review` (a short review now runs inside `ac`), `plan-design` (an API to agree becomes a question that blocks tasks), `sprint-close`, `status`, `setup`, `board`.
- One `spec.md` per story instead of `01-input`, `02-ac`, `03-spec-review`, `04-design`, `05-tasks`, `06-handoff`, `00-decisions` and `questions-*.md`. Questions are answered in the file's Answer column.
- No backlog/Sprint folders, no tracks, no glossary, no `config.local.md`. `scrum-spec/config.md` is optional with 4 keys.
- One approval (the PO on AC). Decisions record a name and date.
- Each fact lives in one place: an answered question moves to Decisions and its row is deleted; test steps use the AC's Then as the expected result; a decision is applied to every section and to other specs with the same rule (`per <work> D<n>:`); other specs are grepped, not read whole.
- `check.py` cut from about 500 to about 230 lines: marker, table cells, person on approvals and decisions, AC/EC and D references, cited paths, task and test-step coverage, open questions, and assumptions (`⚠️ D<n>`) still waiting for the asked role. "AI" only matches in upper case, so a person nicknamed "Ai" passes.
- One run loads at most 1,500 words of instructions (`SKILL.md` + one step file), down from about 6,000.

## 0.1.0 - first release

- Nine steps from story map to sprint close, three tracks, glossary, questionnaires, `check.py` with `--status`.
