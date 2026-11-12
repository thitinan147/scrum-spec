# Guide

This guide is for the people on a team who use `scrum-spec`. The agent follows [`SKILL.md`](../skills/scrum-spec/SKILL.md); this page explains the same rules for people.

## Principles: the AI proposes, people decide

- **Never guess:** every statement in a document is a fact with a source, a proposal clearly marked as one, or `[ask]` · cited paths must exist (`check.py` checks)
- **Unclear means ask:** when the input is ambiguous, documents contradict each other, or the input contradicts the code, the skill points at it and asks; it never picks a side
- **Every decision needs a person's approval:** decisions, the "To decide" table and `**approve:**` lines carry a name, role and date · an AI can never be the one who decided (`check.py` checks)
  - approval comes 3 ways: said in chat, answered in a questionnaire, or by editing the `**approve:**` line in the file (so the Product Owner never has to run the skill)
  - in chat, the name comes from `git config user.name`, and the skill asks once which role you answer as (saved in `scrum-spec/config.local.md`) · once a person decides, it is settled, whatever the role
  - edits after approval: an edit that follows a decision a person made keeps ✅ and appends the D number · an edit the AI made with no decision goes back to ❌
  - after an answer, the skill fixes every affected file in one round, including other tickets, the Sprint file, the story map and the glossary
- **Assumptions exist only when a person orders them:** e.g. answering "use the proposal for now"
- **Scrum roles:** the Product Owner (`ac_owner` in the config) decides value, scope, order and the Sprint Goal · dev estimate size, pick the items they take, and choose how to build · the AI never fills in points, priority, capacity or Owner
- **approve and "Ready to start" are not gates:** they show the team the risk, and the team can always choose to continue
- **Refinement documents use business language:** the story map, rules and AC read without knowing the code · code evidence sits at the end of the file for dev · the "Verified by" cell of each AC is filled in by dev or the tester at Planning
- **The handoff is not a hand-over after the code is done:** it shares the test plan with the tester at the start of the Sprint, so testing runs alongside development

## Set up a project

```text
/scrum-spec setup
```

`setup` guesses from the repo first (git host → MR or PR, the project's rules files, existing document folders, sibling repos, OpenAPI files, fixtures, Definition of Done) and asks only what it cannot guess. If you run a step with no config, the skill runs setup first.

Values you can set include:
- where documents live (`docs_root`), the backlog before the Sprint (`backlog_root`) and the glossary
- the repos to search for code (FE and BE in separate repos are supported)
- the project's rules files and Definition of Done (`definition_of_done`)
- the roles that answer questions, the Product Owner (`ac_owner`), the API owner and the tester
- MR or PR, the board where the team posts results, where the UX design lives
- Task ID prefixes, how the team estimates, and the team's own step codes (`aliases`)

Every key, and how setup guesses it, is in [`references/config.md`](../skills/scrum-spec/references/config.md). Commit `scrum-spec/config.md` so the whole team uses the same values, and add `scrum-spec/*.local.md` to `.gitignore`.

## Usage

Run a step by number, command name, or a code in the config's `aliases`, e.g. `/scrum-spec 4` = `/scrum-spec plan-design`.

```text
/scrum-spec help                                 short usage with input forms and examples
/scrum-spec                                      the next step of the work in progress; with none, status
/scrum-spec status                               which step, blocking questions, what can be done now, next step (add a work name)
/scrum-spec board                                rebuild the HTML board from the files, for people without the repo
/scrum-spec setup                                create or edit the project config
/scrum-spec refine-split flow=<flow>             paste the whole flow, or add a PDF path
/scrum-spec refine-ac story=<flow>/<story>       draft rules and AC for a backlog story
/scrum-spec refine-intake ticket=<ticket>        one card at a time, or a bug
/scrum-spec plan-goal sprint=<sprint>            start of Planning: Sprint Goal and chosen items
/scrum-spec plan-tasks ticket=<ticket>           break into tasks at Planning
/scrum-spec sprint-handoff                       share the test plan with the tester
/scrum-spec sprint-close                         close work at Sprint end (without ticket= you can pick several)
```

The rhythm, when you start from a whole flow:

```
Refinement (ongoing)            Sprint Planning                       During / end of Sprint
0 refine-split                  plan-goal: Goal + choose items        dev pick tasks themselves
→ 2 refine-ac per story          → move stories into the Sprint        6 sprint-handoff (start of Sprint)
  <backlog_root>/<flow>/         → the story's track (3 → 4 →) 5        7 sprint-close (end of Sprint)
```

- Step 0 writes `01-input.md` for every story, so step 1 is skipped
- `plan-goal` runs once per Sprint · folders move with `git mv` only after the team confirms
- When unsure pick the small track; if an API turns out to need agreement, the skill proposes upgrading to large
- If the code is already done, use the small track and skip step 5
- The small and bug tracks run a short spec review in step 2 · the bug track writes AC as the correct behavior and EC as what must not change

**If AC change during the Sprint:** run step 2 again. The skill records a D that names the AC numbers, fixes the tasks so every AC is still covered, and, if a handoff exists, updates only the test steps of the AC that changed.

## Where results live

Refinement saves to `<backlog_root>/<flow>/` (or `<backlog_root>/<card>/`) · Sprint Planning saves the Goal to `<docs_root>/sprint-<sprint>.md` · during the Sprint, results go to `<docs_root>/<ticket>/` · chat shows only a summary, the `[ask]` items and what must be decided.

**The files in the repo are the source of truth.** The board is a copy for the team. If someone edits on the board, bring the edit back into the repo files before the next step (paste it in chat and tell the skill).

Each piece of information lives in one place (the "Where information lives" table in [`references/shared-files.md`](../skills/scrum-spec/references/shared-files.md)):

| File | What it is |
|---|---|
| `<backlog_root>/<flow>/00-map.md` | the flow's story map and its flow-level "To decide" table |
| `<docs_root>/sprint-<sprint>.md` | Sprint Goal, chosen items and the Definition of Done used |
| `<work folder>/00-decisions.md` | decisions that change the spec · other files cite them as `D<n>` · when documents conflict, this file wins |
| Open Questions in `02-ac.md` | the one list of questions for the work |
| `<work folder>/questions-<slug>.md` | a questionnaire for a role that must answer · send it as is · the skill reads filled-in answers on the next run |
| `<glossary_root>/<domain>.md` | the one permanent file: terms, rules across work, and "Carried over" |

**Closing (step 7):** after the Sprint most documents have done their job. This step keeps only what future work needs in the glossary, then deletes the ticket folders, story maps with no stories left, and the Sprint file.
- Keep as little as possible, because an outdated document is worse than none · keep only what the code, tests, API spec or design cannot tell and future work needs
- No new documents outside the glossary · the skill asks before every delete · see history with `git log -- <path>`

## Check documents with the script

```bash
python3 -I <skill_dir>/scripts/check.py <folder>                    # a ticket, story, flow, glossary or <docs_root>
python3 -I <skill_dir>/scripts/check.py <folder> <folder> …         # several folders · errors and open-question counts only
python3 -I <skill_dir>/scripts/check.py --status scrum-spec/sprint scrum-spec/backlog   # the status table; finds work folders inside
```

- **Exit 1:** a broken table, leftover substitution text (including an unsubstituted `<key>`), a missing first line, a task citing an AC that does not exist, a `D<n>` that does not exist, a cited path that does not exist (add `(new)` after a file that will be created), an approval with no name, role and date or by an AI, `**Summary:**` counts in `02-ac.md` (AC, EC, Open Questions) and `05-tasks.md` that do not match their tables, and `[ask]` left in `01-input.md` once `02-ac.md` has Open Questions
- **Report only:** AC → task coverage, `[ask]`, assumptions, questionnaire answers, decision rows decided by an AI, and "Hard to read" · a `**Summary:**` line never counts as `[ask]`
- Paths are checked only when the folder sits inside `docs_root`, `backlog_root` or `glossary_root` of the config

The script is read-only. The skill runs it at every step, and you can run it yourself before committing.

## Measure whether it helps

AI amplifies how a team already works, the good parts and the problems. Measure before and after.
1. **Before using it, for 1–2 Sprints:** note the baseline below
2. **Pilot on one flow for 1–2 Sprints:** note the same values and compare
3. **At the retro:** ask the Product Owner, dev and tester whether it helped, then adjust from what you saw

| Measure | From |
|---|---|
| Time from getting a flow to ready for Planning | the dates on the first line of `00-map.md` → `sprint-<sprint>.md` |
| Length of Sprint Planning | noted at the meeting |
| Questions found after the Sprint started | D rows in `00-decisions.md` dated after the Sprint start |
| Items not done in the Sprint (carry-over) | the board or `sprint-<sprint>.md` |
| `[ask]` still open when the Sprint starts | `check.py` of each ticket |

**Signs it is not working:** people approve without reading, so many questions that the Product Owner becomes the bottleneck instead, documents get longer but Planning does not get shorter, dev still ask the same questions back.
