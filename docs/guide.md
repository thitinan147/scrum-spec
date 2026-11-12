# Guide

This guide is for the people on a team who use `scrum-spec`. The agent follows [`SKILL.md`](../skills/scrum-spec/SKILL.md); this page explains the same rules for people.

## Why it exists

Scrum work waits on people: the PO writes AC from a blank page, dev rebuild context at Planning, the tester waits for code to know what to test. The skill drafts each of those from the input and the real code, so people review and decide instead of writing from scratch.

## Principles

- **The AI proposes, people decide.** Every statement is a fact with a source, a proposal marked "Proposal:", or a question in the Questions table. Decisions carry a person's name and date; `check.py` fails an approval or decision given by an AI.
- **Facts come from the code.** Before asking, the skill reads every repo in `code_roots`. People are asked only for decisions and for what is not in the repo.
- **No one has to run the skill to answer.** Write in the Answer cell of the Questions table, or edit the approve line. The next run records it as a decision.
- **Approval informs, it does not block.** The PO approves AC; a change that follows a decision keeps the approval, any other change to rules or AC resets it.
- **Never estimates, prioritises, assigns owners, writes code, commits or deletes.**

## Usage

```text
/scrum-spec split <flow>        a whole flow → story map + one folder per story
/scrum-spec ac <work>           story, rules, acceptance criteria, questions
/scrum-spec tasks <work>        tasks pointing at real files, every AC covered
/scrum-spec handoff <work>      test steps for the tester on day one
/scrum-spec                     the next step of the work in this conversation
/scrum-spec help                short usage
```

Paste the card, bug or flow text after the command, or give a path to a PDF or image.

```
Refinement                         Sprint Planning
split <flow> (optional)            tasks <work>
→ ac <story> per story              → handoff <work>
  PO answers questions, approves AC
```

## Files

Everything for one story is in `<docs_root>/<work>/spec.md` (default `docs_root` is `scrum-spec`), in this order: Story · Rules · Acceptance Criteria · Questions · Decisions · Tasks · Test steps. A flow from `split` also has `<docs_root>/<flow>/map.md`.

Commit `spec.md` with the code. When the ticket is done, delete the folder; git keeps the history.

`scrum-spec/config.md` is optional:

```
docs_root: scrum-spec
code_roots: ., ../api
roles: PO, BE, UX, QA
task_prefixes: FE, BE
```

## Check documents with the script

```bash
python3 -I <skill_dir>/scripts/check.py scrum-spec/
```

- **Exit 1:** missing first-line marker, a broken table row, an approval or decision without a person and date or given by an AI, a reference to an AC/EC or D that does not exist, a path in Tasks or Source that does not exist (add `(new)` for files to create)
- **Reported:** approval status, open and blocking questions, answers not yet recorded, AC/EC with no task

## Measure whether it helps

Note these for 1–2 Sprints before and after, then ask at the retro:

| Measure | From |
|---|---|
| Time from getting a card to AC approved | git log of `spec.md` |
| Length of Sprint Planning | noted at the meeting |
| Questions found after the Sprint started | Decisions dated after the Sprint start |
| Blocking questions open at Sprint start | `check.py` |

**Signs it is not working:** people approve without reading, the PO is buried in questions, Planning does not get shorter, dev still ask the same questions.
