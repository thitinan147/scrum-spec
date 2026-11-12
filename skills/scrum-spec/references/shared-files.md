# Shared file formats

Read this file when creating or editing `00-decisions.md`, `questions-<slug>.md` or the glossary

## Contents
- Where information lives
- Decisions
- Questionnaire
- Glossary

## Where information lives

Each piece of information lives in one place · other places cite it by number instead of repeating it

| Information | Lives in | Cited as |
|---|---|---|
| A decision that changes the spec of a ticket or story | `00-decisions.md` | `(D<n>)` |
| A flow-level decision (how to split, slices, order) | the "To decide" table in `00-map.md` | `T<n>` |
| Open questions of a ticket or story | Open Questions in `02-ac.md` (before `02-ac.md` exists, use `[ask]` in the file · once `02-ac.md` exists, move them into Open Questions and delete them from `01-input.md`) | `Q<n>` |
| Questions sent to another role to answer | `questions-<slug>.md` (a copy of the open questions that need that role's answer) | – |
| Who approved which file | that file's `**approve:**` line | – |
| Sprint Goal and chosen items | `<docs_root>/sprint-<sprint>.md` | – |
| Terms, rules across work, items left open after closing | glossary | – |

## Decisions (`00-decisions.md`)

```markdown
<!-- scrum-spec decisions · <ticket or story> -->
## Decisions

| # | Topic | Decision | Type | Decided by · date | Confirmed by · date | Files updated |
|---|---|---|---|---|---|---|
| D1 | <topic to decide> | <what was decided> | decided | <name> (<role>) · YYYY-MM-DD | – | 02-ac, 04-design |
| D2 | <topic no one has answered yet> | <the proposal the user ordered to use for now> | assumption | <name of who ordered it> (<role>) · YYYY-MM-DD | – | 02-ac |
| D3 | <topic cut out> | not done in this ticket | out of scope | <name> (dev) · YYYY-MM-DD | – | 01-input, 02-ac |
| D4 | <AC changed during the sprint> | <what changed> | decided | <name> (<role>) · YYYY-MM-DD | – | 02-ac (AC5, EC3), 05-tasks |
```

- Record only decisions that change the spec (scope, AC, permissions, API, wording) · do not record work management such as the Sprint Goal, Owner, Estimate, reviewer or readiness results
- Type: `decided` / `assumption` / `out of scope`
- Every row needs a person's approval: "Decided by" is `<name> (<role>)` per "Who approves" in `SKILL.md` (the name from `git config user.name` or from the questionnaire) · never an AI · once a person decides it is settled whatever the role; no wait for another role · "Confirmed by" is for an assumption someone confirms later; otherwise `–` · an assumption exists only when the user orders using a proposal for now
- An assumption becomes decided only when a person confirms it · never change it yourself
- A row whose "Decided by" is an AI counts as not approved by a person · `check.py` reports it · ask when the step being run needs that row
- Other step files cite a row by number in parentheses, e.g. `(D1)` or `(D1, D4)`, instead of repeating the date and decider
- When AC change, name the AC numbers in the "Files updated" column, e.g. `02-ac (AC5, EC3)` · step 6 uses it to find which test steps must change
- "Files updated" lists every file actually edited, including files outside the work folder, e.g. `sprint-s1`, `00-map`, `glossary/booking` or `<other ticket>/02-ac (AC2)` (find them all per item 6.2 of `SKILL.md`)
- A D that also changes another ticket's spec: that ticket gets its own D row whose "Decision" starts `per <source ticket> D<n>:`, with the same "Decided by" as the source · never put another ticket's `(D<n>)` in parentheses, because `scripts/check.py` checks it against `00-decisions.md` in the same folder
- Never add or remove columns, because `scripts/check.py` reads them by column position
- Keep the table easy to read (`references/format.md` item 4):
  - "Topic" is a question or short title of at most 1 line, with no path
  - "Decision" is at most 2 sentences with at most 1 path · other evidence stays in the step file that uses it and cites back by D number
  - a cell with no value gets `–`

## Questionnaire (`questions-<slug>.md`)

The slug comes from the Roles table in the config · create one only for roles the table gives a questionnaire

```markdown
# Questions for <role> · <ticket, story or flow>

- **From:** <team / user> · **To:** <role> · **What the answers are for:** <e.g. fix AC before design starts>
- **Answered by:** <name> (<role>) · used to record who approved · AC or scope can be approved in this file, e.g. by answering "approve AC"
- **Context:** <so someone who was not in Planning understands · 1 short paragraph, or with several topics, one sub-bullet per topic>
- **How to answer:** answer under each question · answering some, or saying you are not sure, is fine · answers needed before <step/date>

## Needed before <step it blocks>
1. <one question, not nested, 1–2 lines>
   - Assumption in use: <if any>
   - _Why it matters: <only for a question that may be answered wrongly or vaguely>_

   > Answer:

## Can wait
…

## Anything else?
> 
```

- Order from most to least important · the person answering may read it only once
- Context and evidence (paths, lines of code) go in **Context** above, or as a sub-bullet of the question, not appended to the question itself · split context into sub-bullets by topic when there is more than 1
- The person answering writes after `> Answer:` or on the next `>` line
- Once answered, the user pastes the answers in chat or edits this file, then runs the related step again · the skill reads the filled-in answers and records them in `00-decisions.md` (`scripts/check.py` also reports the filled-in answers)

## Glossary (`<glossary_root>/<domain>.md`)

`<domain>` is named per `domain_source` in the config · if `domain_source` is `–`, use one file, `<glossary_root>/index.md`

```markdown
# Glossary · <domain>

## Terms

| Term | Meaning | In code / data | Source |
|---|---|---|---|
| <term> | <the agreed meaning in 1 line> | <field / type / value in code that matches this term> | `<ticket>` D<n> |

## Rules across tickets

| Rule | Applies to | Source |
|---|---|---|
| <a rule other tickets must follow too, e.g. wording or permissions> | <screen / part of the system> | `<ticket>` D<n> or `<ticket>` AC<n> |

## Carried over

| Topic | Type | Ask / owner | Added | Source |
|---|---|---|---|---|
| <something not finished, 1 sentence> | waiting for answer / assumption / deferred / known issue | <role> | YYYY-MM-DD | `<ticket>` D<n> |
```

- The "Terms" table holds terms only, not specs or implementation decisions
- Rules across tickets live in the glossary only · a ticket's `02-ac.md` and `00-decisions.md` do not copy the rule; they cite its name, e.g. "per the glossary rule: <rule>" · a rule that changes is fixed in one place
- The "Rules across tickets" table holds rules every ticket in the domain must follow (e.g. words used on screen, or who may do what), not how to implement them, and only once the rule was decided in some ticket
- Behavior that looks like a bug but the team wants it this way (e.g. "can delete even when … because …") goes in "Rules across tickets", with the reason in `### Details`, because the code cannot tell whether it was intended or forgotten
- Write the current state, not history · a rule that changes: edit the old row and append to "Source" · delete rows that are no longer true
- Never add what can be found in the code, tests, API spec or design, because it would duplicate and go stale
- The "Carried over" table is written by step 7 when a ticket closes, to keep what is not finished · when some ticket finishes it or gets the answer, delete that row when closing that ticket, and move the result to Terms or Rules if it applies across tickets
- "Added" is used to find rows left open a long time · step 1 asks about rows open more than 6 weeks whether to keep or delete them
- Every row must read on its own without opening the ticket's documents, because the folder of a closed ticket is deleted (history: `git log -- <docs_root>/<ticket>/`)
- "Source" is `<ticket>` followed by a D, AC or EC number, or `<flow>` followed by a T number (if there is no number, the file name) · not in parentheses, because `scripts/check.py` checks `(D<n>)` against `00-decisions.md` in the same folder
- If a ticket's D conflicts with a rule in this table, ask whether to follow the rule, change the rule, or record an exception for that ticket (if a ✅ decision already clearly covers it, change the rule without asking), then say so in chat
- When the user or a document uses a word that conflicts with the glossary, flag it right away and ask which meaning is meant
- For ambiguous words (e.g. "their own data"), propose a clear meaning with example boundaries, then ask
