---
name: scrum-spec
description: HUMAN-ONLY COMMAND. Drafts a Scrum team's shared spec docs one step at a time, from Product Backlog Refinement through Sprint Planning to tester handoff and sprint close. Starts from a whole board, a single backlog card, or a card already in the Sprint. Splits a flow into vertical-slice stories on a story map, drafts rules and acceptance criteria, proposes a Sprint Goal and its items, then per ticket runs a spec review, technical design and API contract, task breakdown with a readiness check, and a tester handoff; at sprint end keeps what future work needs in a glossary and deletes finished folders. Finds facts in the code, proposes options but never decides for the team, asks when something is unclear, and records who approved each decision. Settings live in scrum-spec/config.md (created by setup). Type /scrum-spec, e.g. "split this flow into stories", "draft AC", "set the Sprint Goal", "break into tasks", "write the tester handoff".
license: MIT
compatibility: Claude Code, Codex, Cursor and other Agent Skills clients. Needs git and Python 3.9+ (standard library only). pdftotext and pdftoppm (poppler) are optional, for PDF input.
metadata:
  author: Thitinan
  version: "0.1.0"
  short-description: Draft Scrum spec docs step by step; the AI proposes, people decide
argument-hint: "<help | setup | status | board | 0-7 | refine-split|refine-intake|refine-ac|plan-goal|plan-review|plan-design|plan-tasks|sprint-handoff|sprint-close> [flow=<flow> | story=<flow>/<story> | ticket=<ticket> | sprint=<sprint>]"
allowed-tools: Bash(python3 -I ${CLAUDE_SKILL_DIR}/scripts/check.py *) Bash(git rev-parse *) Bash(git status *) Bash(git log *) Bash(git config user.name)
disable-model-invocation: true
---

# scrum-spec

Argument: `$ARGUMENTS` (if this still reads `$ARGUMENTS`, the argument is the text the user wrote after the command)

This skill writes the spec documents a team shares, from Refinement through Sprint Planning, until the test plan is shared with the tester, and closes the ticket when the Sprint ends · Doing the tasks (writing code, reviewing code, writing test cases) is up to each person

Documents exist so people decide the same thing, not to fill every heading. Write only what is needed. For what can be found in the code, API spec or design, cite the path instead of repeating it

## Rule: propose, never guess

Every statement written into a document must be one of these 3 kinds. A statement that fits none of them is a guess, and must not be written

| Kind | Means | Must have |
|---|---|---|
| Fact | Found in the input, code, API spec, glossary or decisions | Source (path or D number) |
| Proposal | The AI recommends it, but no person has decided yet | Marked as a proposal, with the reason and the alternatives |
| Unknown | No source and not enough to propose | `[ask: … · <role>]` |

- **Unclear means ask:** when the input is ambiguous, documents contradict each other, or the input contradicts the code, point at it with the path and ask · never pick a side yourself
- **People decide, the AI proposes:** `<ac_owner>` (Product Owner) decides value, scope and order · dev decides size, which items to take and how to build · the AI never fills in points, priority, capacity or Owner
- **Every decision needs a person's approval:** a row in `00-decisions.md`, a result in the "To decide" table and an `**approve:**` line must have `<name> (<role>)` and a date · never an AI · with no approval yet, keep it as a proposal, `[ask]` or `❌ not yet`
- **Who approves:** approval comes 3 ways: said in chat, answered in a questionnaire, or by editing the `**approve:**` line / "Result" cell in the file (git log shows who edited) · in chat use the name from `git config user.name` (if none, ask for the name once) · the user's role: read the `my_roles:` line in `scrum-spec/config.local.md` (a personal file, not committed · the value is role names separated by `,` or `all roles`) · if the file is missing, ask once, then offer to save it to that file, and add it to `.gitignore` if `git check-ignore` says it is not ignored yet · a user with several roles can answer those roles' questions in chat right away, recorded as `<name> (<role of the question>)` · **once a person decides, it is settled, whatever the role:** record the name and role of whoever answered, with no wait for another role to confirm or acknowledge (anyone who wants to know who decided what reads the D rows) · a questionnaire answer uses the name and role of the person who answered in that file
- **Assumptions exist only when a person orders them:** e.g. the user answers "use the proposal for now" (item 6.3)

## Values used

- `<skill_dir>` = `<this-skill-dir>`, the folder that holds this SKILL.md
- `<command>` = the command that runs the skill, usually `/scrum-spec` (installed as a plugin it is `/<plugin>:scrum-spec`)
- Other `<key>` such as `<docs_root>`, `<roles>`, `<ac_owner>`, `<board>` come from the project config; their meaning is in [references/config.md](references/config.md) · substitute them before following the files in `steps/` and `references/` · for a key that is `–`, follow the "If `–`" column in `references/config.md`

## Steps

| # | Command | Step file | Also read | Saved to |
|---|---|---|---|---|
| – | `help` | [references/help.md](references/help.md) | – | not saved · shown in chat |
| – | `setup` | [references/config.md](references/config.md) | – | `scrum-spec/config.md` |
| – | `status` | this file ("status" in Workflow) | – | not saved · shown in chat |
| – | `board` | this file ("board" in Workflow) | – | `<docs_root>/board.html` (rebuilt whole every time) |
| 0 | `refine-split` | [steps/00-refine-split.md](steps/00-refine-split.md) | [references/input.md](references/input.md) | `<backlog_root>/<flow>/00-map.md` and `01-input.md` of every confirmed story |
| 1 | `refine-intake` | [steps/01-refine-intake.md](steps/01-refine-intake.md) | [references/input.md](references/input.md) | `01-input.md` |
| 2 | `refine-ac` | [steps/02-refine-ac.md](steps/02-refine-ac.md) | review categories in [steps/03-plan-review.md](steps/03-plan-review.md) · splitting in [steps/00-refine-split.md](steps/00-refine-split.md) | `02-ac.md` |
| – | `plan-goal` | [steps/plan-goal.md](steps/plan-goal.md) | – | `<docs_root>/sprint-<sprint>.md` |
| 3 | `plan-review` | [steps/03-plan-review.md](steps/03-plan-review.md) | – | `03-spec-review.md` · questions go to Open Questions in `02-ac.md` |
| 4 | `plan-design` | [steps/04-plan-design.md](steps/04-plan-design.md) | – | `04-design.md` |
| 5 | `plan-tasks` | [steps/05-plan-tasks.md](steps/05-plan-tasks.md) | – | `05-tasks.md` |
| 6 | `sprint-handoff` | [steps/06-sprint-handoff.md](steps/06-sprint-handoff.md) | – | `06-handoff.md` |
| 7 | `sprint-close` | [steps/07-sprint-close.md](steps/07-sprint-close.md) | – | edits the glossary, then deletes folders that are done |

- Every step that writes a file: read [references/format.md](references/format.md) before writing, and read [references/shared-files.md](references/shared-files.md) before writing decisions, questionnaires or the glossary
- Command names start by phase: `refine-` = Refinement · `plan-` = Sprint Planning · `sprint-` = during and at the end of the Sprint · accept the number, the command name and codes in `aliases` of the config (case-insensitive)

**Work folders** for steps 1–7 come in 2 kinds, with the same files inside
- `<docs_root>/<ticket>/` · a ticket already in the Sprint
- `<backlog_root>/<flow>/<story>/` · a story from step 0 · or `<backlog_root>/<card>/` · a single backlog card · both not in a Sprint yet · steps 1 and 2 can use them; for other steps, warn that it is not in a Sprint yet and ask before doing it

**A story enters the Sprint:** through `plan-goal`, which runs `git mv` after the user confirms, or the user moves it · if "Sprint / Ticket ID" in `01-input.md` still reads `not in a Sprint yet`, ask for the value and fix it

**The approve line:** `01-input.md`, `02-ac.md`, `04-design.md`, `05-tasks.md` and the Sprint file have an `**approve:**` line per their Template
- It starts as `❌ not yet · waiting for <role>` · it becomes `✅ <name> (<role>) · <YYYY-MM-DD>` only when someone in that role approves by one of the 3 ways above · keep a ✅ that a person wrote in the file; never delete or overwrite it
- **Edits after ✅:** look at where the edit came from (while it is still ❌, edit freely; the approve line needs nothing):

  | Edit | approve line |
  |---|---|
  | Follows a D a person decided (any role, in chat or questionnaire · including the user agreeing to an edit the AI proposed, which must be recorded as a D) | keep ✅ and append `(incl. D<n> · <YYYY-MM-DD>)` · several become `(incl. D3, D5 · <YYYY-MM-DD>)` · do not ask for approval again |
  | design, task, path, code evidence, wording with the same meaning, "Verified by" cell, Open Questions, Sprint / Ticket ID | unchanged |
  | The AI changes scope, rules or AC itself with no D (e.g. finds AC that contradict and proposes a fix) | back to `❌ not yet · waiting for <role> (edited after approval <YYYY-MM-DD>)` · better: ask first to get a D, then use the first row |

  - If someone later decides differently, record a new D that replaces the old one, then fix the affected files again (item 6.2)
- **First approval request:** show a summary before asking, at most 10 lines: what it does / main rules / not included / what the code shows / open questions · asking again (after the AI edited it back to ❌) shows only what changed

## Tracks by type of work

Step 1 (or step 0 for a story) proposes a track, then records it in the "Track" field of `01-input.md` once the user picks

| Track | Steps | Use when |
|---|---|---|
| small (default) | 1 → 2 → 5 → 6 | most work, including a new screen on an existing API |
| large | 1 → 2 → 3 → 4 → 5 → 6 | a new or changed API must be agreed with `<api_owner>` before coding, or the scope is unclear |
| bug | 1 → 2 → 5 → 6 | behavior does not match what was agreed, or it used to work and broke |

- **Three ways in:** a whole board or flow: step 0 → step 2 per story → `plan-goal` → the story's track (skip step 1; step 0 already wrote `01-input.md`) · a single backlog card: step 1 in `<backlog_root>/<card>/` (write `not in a Sprint yet` in "Sprint / Ticket ID") → step 2 → `plan-goal` · a card already in the Sprint: step 1 in `<docs_root>/<ticket>/` → its track
- **Rhythm:** Refinement runs throughout the Sprint → at the start of Planning run `plan-goal` once per Sprint → steps 3–5 per ticket → step 6 right after, so `<tester>` writes test cases from the start of the Sprint → during the Sprint dev pick tasks themselves → step 7 at the end of the Sprint
- Step 0, `plan-goal` and step 7 do not count in a track's number of steps
- When unsure pick small; if it later turns out an API must be agreed or the scope is unclear, propose upgrading to large · if the user agrees, record a D, fix the track field, and the next step is step 3
- If the ticket's code is already done, use small and skip step 5 · small and bug: step 2 runs a short spec review itself, and step 5 finds the files from the code itself
- A step outside the track may still run: warn in one line and continue

Shared files (created when they get their first content · each piece of information lives in one place; see the "Where information lives" table in `references/shared-files.md`):

| File | Holds | Written by |
|---|---|---|
| `<work folder>/00-decisions.md` | decisions that change the spec of a ticket or story | every step, as soon as an answer comes in |
| `<work folder>/questions-<slug>.md` | a questionnaire for a role that must answer (only roles the Roles table gives a questionnaire) | steps 2, 3 · other steps when the user asks |
| `<backlog_root>/<flow>/questions-<slug>.md` | a flow-level questionnaire | step 0 |
| `<glossary_root>/<domain>.md` | terms, rules across tickets and carried-over items | every step, as soon as agreed · step 7 |

## Workflow

Copy this checklist and tick it item by item:

```
scrum-spec:
- [ ] 1. Load the config, then identify the step and work folder
- [ ] 2. Read the step file and the files in "Also read"
- [ ] 3. Gather input and find facts yourself
- [ ] 4. Draft the result from the Template
- [ ] 5. Save and check the result
- [ ] 6. Ask and fill in answers
- [ ] 7. Reply
```

- **`help`** (or `-h`): skip this checklist · read `references/help.md`, substitute `<command>` and the config keys (with no config keep `<key>` and add a last line saying to run `<command> setup`), then show the whole file in chat · no questions, no files written
- **`status`** (or questions like "what next", "what is blocked", "are we ready", "which step are we on"): skip this checklist · no files written, no questions
  1. Run `python3 -I <skill_dir>/scripts/check.py --status <docs_root> <backlog_root>` (the script finds the work folders inside itself; no `*` needed · if the user names one piece of work, pass only that folder)
  2. Show the table and "Questions blocking the next step" from the script (do not open the work files yourself), then 2 short headings: **Can do now without waiting** (work whose next step has no blocking question, and questions the user's role can answer) · **Next** (one recommended command with the full work name · pick work whose next step is not blocked; tickets in the Sprint come before backlog stories, and stories follow the order in `00-map.md`)
  3. All numbers come from the script and the files; never count yourself · if there are errors, say which step can fix them
- **`board`:** rebuild `<docs_root>/board.html` whole from the files in the repo every time; never patch it, so it always matches the files
  - Content: the `status` table · per ticket/story: what it does in 1–2 lines, Business Rules and AC in business language, open questions grouped by who must answer, approvals with names · readable by someone with no repo access, with no paths or field names
  - A single HTML file that loads nothing external · the first line is `<!-- scrum-spec board · built from files <YYYY-MM-DD> · do not edit -->` · if this session can publish a web page and the user has given a board URL before, update that URL
- **Step 7 `sprint-close`:** do items 1–2, then follow the step file instead of items 3–7

**1. Load the config, then identify the step and work folder**
- config: look for `scrum-spec/config.md` in this order, then read the whole file
  1. the root of the git repo cwd is in (`git rev-parse --show-toplevel`)
  2. if cwd is not in a git repo: cwd itself; if not there, look for `*/scrum-spec/config.md` one level down and ask which one to use
  3. not found: say so in one line, run `setup` first, then the step that was asked for

  paths in the config are relative to the folder that holds `scrum-spec/`; if a path in `code_roots` does not exist, warn once and use what exists
- step: the first argument
  - **No argument:** if this conversation has work in progress and the next step in its track is clear, say so in one line and do that step without asking · otherwise run `status`
  - **A work name** (ticket, story, flow, Sprint or path) or a free question: run `status` for that work · matches nothing: run `status` and say to type `<command> help` for usage
- work: step 0 uses `flow=` · `plan-goal` uses `sprint=` · other steps use `ticket=`, `story=<flow>/<story>` or `story=<card>` (a single backlog card) · also accept it without `key=`, e.g. `plan-review s1-x` or `plan-review=s1-x` → if none given, use the one used in this conversation → if none, ask (propose a name, or show the existing folders to pick from) · ticket names follow `ticket_format`
- track: read it from `01-input.md`; if that file does not exist yet, the track comes from step 0 or 1
- Tell the user in one line, e.g. `Step 5 · plan-tasks · ticket <ticket> · small track (3/4)` or `Step 2 · refine-ac · story <flow>/<story> · not in a Sprint yet` · the numbers in parentheses are position in the track / number of steps in the track; include them only for a ticket that has a track

**2. Read the step file and the files in "Also read"** from the "Steps" table, whole, and follow every item

**3. Gather input and find facts yourself** from these sources in this order
1. what the user gave in the argument or the conversation
2. `00-decisions.md`, filled-in answers in `questions-*.md` and the glossary · `00-decisions.md` and ✅ results in the "To decide" table of `00-map.md` win over older text in other files (including the glossary) · a questionnaire answer not yet in `00-decisions.md` is a new answer; record it per item 6.2
3. the result of the previous step, from this conversation; if absent, read it from the work folder · for a story, also read `<backlog_root>/<flow>/00-map.md`
4. the repo: search every path in `code_roots`

- **Proposals about UX, wording or standards:** use a pattern the repo already has (cite the path); if there is none, cite an official guideline or standard you found (name the source) · never propose from memory alone
- **Find facts yourself, ask people for decisions:** before writing `[ask]`, look in the code, fixtures, `<personas>`, config and documents first; if found, write what you found with the path · keep only decisions and information from outside the repo as questions
- **Files not yet following an existing decision** (a ✅ D or T that clearly covers the topic): fix them per item 6.2 and report; do not ask
- Files that contradict each other with no decision behind them (e.g. an AC example contradicts the Business Rules), or a user describing behavior that contradicts the code: flag it with the path and ask · if the conflict affects what you are about to draft, ask before drafting (ask right away per item 6.1) · if not, keep drafting and include it in the item 6 round of questions
- A previous step in the track has no result yet: warn in one line and continue · a required input is missing: ask; never make it up

**4. Draft the result** from the step's `## Template` only
- use only information from item 3 · every statement is a fact, a proposal or `[ask: … · <role>]` (`<role>` is one role name from `<roles>`)
- markers, headings, template labels, table columns and fixed values are always in English, exactly as in the Template · fixed values `check.py` reads: tracks `small` / `large` / `bug`, decision types `decided` / `assumption` / `out of scope`, "Needed before" `design` / `start` / `later`, statuses `❌ open` / `✅ answered (D<n>)` / `❌ not yet · waiting for <role>`, `not in a Sprint yet`, and the wording of `**Summary:**` lines
- the free text you draft (rules, AC, descriptions, questions) is in the language of the input or of the user's conversation; technical terms may stay in English · text in parentheses in the Template is an instruction, not output · a heading that does not apply gets `–`
- if the step's result file already exists, use it as the base: change only the parts with new information and keep what the team edited · Template headings missing from the old file need not be added when there is nothing to put in them · with no new information do not redraft; say what is needed before running it again

**5. Save and check the result**
- write the file from the "Steps" table; the first line is `<!-- scrum-spec <##> · <command> · <YYYY-MM-DD> -->` · before overwriting an existing file or editing another step's file, summarise what will change and ask before writing, **except** edits that follow a D just decided (item 6.2) or a decision already ✅ (item 3): make those and report them in item 7 · still ask first before overwriting a part a person edited (see `git diff` or `git log -p` of the file)
- run `python3 -I <skill_dir>/scripts/check.py <full path of the folder written>`
  - **exit 1:** broken table, leftover text (`\1`, `{{…}}`, an unsubstituted `<key>`), missing first line, a task citing an AC that does not exist, a `D<n>` that does not exist, **a cited path that does not exist**, an approval with no name, role and date, or by an AI · fix it and run again · add `(new)` after the path of a file that will be created · never guess another path for one that cannot be found; search the code or remove it
  - **report only:** coverage, `[ask]`, open Open Questions, assumptions, questionnaire answers, AI deciders in decision rows and "Hard to read" · fix "Hard to read" in this step's files before finishing
  - **the script cannot run:** tell the user with the error, then check the exit 1 list yourself file by file · never say it passed the script check
- check yourself as well (the script cannot):
  - every Template heading is present; no headings added (except `### Details` under a table)
  - every statement has a source, is a proposal or is `[ask]` · never say something is confirmed or passed without evidence · no ✅ written by the skill without a person approving in chat or in a questionnaire
  - no conflict with `00-decisions.md`, the glossary and earlier step files; if there is one, ask · if it conflicts with a glossary rule, ask whether to follow the rule, change the rule, or make an exception for this work
  - no secrets, tokens or customers' personal data (the documents will be committed)

**6. Ask and fill in answers** when the result has `[ask]`, proposals waiting for a person, or assumptions
1. **Ask now and keep asking until done:** save the result, then start asking in the same turn (if you stopped before drafting per item 3, ask right away the same way) · never end a turn with a list of `[ask]` and wait for the user to say "ask me" · the first round starts with a summary of at most 5 lines: what was drafted and how many questions there are · ask at most 4 at a time (or as the user asks, e.g. one at a time) until all are done
   - in chat ask only what the user's role can answer · other roles' questions go into `questions-<slug>.md` without asking (for a role the Roles table gives no questionnaire, keep it as `[ask]` or an Open Question in the file and say in item 7 who must be asked)
   - the user may answer "use all the recommendations" at any time: remaining questions with a recommended option are recorded as decided by the user · questions with no recommended option stay `[ask]`
   - order by impact × uncertainty · ask only what would change a story, AC, API or task if answered differently · small things go into the questionnaire
   - every question reads on its own, says what the answer will change, has a recommended option marked "(Recommended)" with a reason from the code or documents, and has the option "Don't know yet / wait for <role>"
   - questions that depend on another answer wait for the next round · information with no option to recommend (e.g. Sprint, business reasons) stays `[ask]`
2. **Write right away and fix everything affected in one round:** the user's answer counts as confirmation; do not ask for approval again (the approve line follows "Edits after ✅")
   - answers that change the spec go into `00-decisions.md` (step 0: into the "To decide" table of `00-map.md`) · terms and rules used across work go into the glossary, in one place; tickets cite the rule's name and do not copy it
   - **find every place affected, not only the work folder:** search (Grep) by the topic's key words, AC/EC numbers, field or endpoint names, and the old text being replaced, in the work folder, other ticket folders in the same Sprint, the Sprint file (`<docs_root>/sprint-<n>.md`), the flow's `00-map.md`, `<backlog_root>` and `<glossary_root>`
   - fix every place found in this round; never put it off to "when that step runs" · **replace the old conflicting text**; do not add a line repeating the meaning · recount `**Summary:**` counters that count what changed · in `sprint-<n>.md` fix only names, scope or tickets that changed; do not touch the "Risk when chosen" column (recorded on the day of choosing)
   - another ticket whose spec changes as a result: add a D row to that ticket's `00-decisions.md` whose "Decision" starts `per <source ticket> D<n>:` (not in parentheses), then apply "Edits after ✅" to that ticket's approve line
   - a D's "Files updated" lists every file actually edited · something affected that cannot be fixed this round (e.g. its owner must be asked first) is reported in item 7 as `Not fixed: <path> · because <reason>`
   - run `check.py` again, once, on every folder edited in this item (`check.py <folder> <folder> …`) and fix errors before replying
3. **Assumptions:** the AI never picks on its own · if the user orders using a proposal for now, record it as an "assumption" in `00-decisions.md` with "Decided by" as the person who ordered it, and say so in chat · if not ordered, it stays `[ask]` and the parts that depend on it are not drafted
4. Questions answered "don't know yet" stay `[ask]` and go out in `questions-<slug>.md` · something that does not belong to this work (e.g. a glossary rule that conflicts with the flow) goes into the glossary's "Carried over" table, so it is not lost in chat

**7. Reply** never show the full result in chat; reply in this format:
  ```
  ✅ Step <#> · <command> · <ticket … / story … / flow … / sprint …> · <track> track (<position in track>/<steps in track>)
  Saved to: <file path> (<key counts, e.g. AC 8 · EC 5>)
  New decisions <n> · other files updated: <every path actually edited>
  Not fixed: <path · because …>
  approve: <✅ name (role) · date (incl. D…) or ❌ not yet · waiting for role>
  Assumptions <n>:
    - <every one>
  [ask] <n>:
    - <every one · who to ask>
  Who confirms: <from ## Output> · posted on <board> <✅/❌>
  Next: <#> · <command> <step>
  ```
  - a line with no information says "none" · drop the "Not fixed" line if there is nothing · drop the approve line for a file with no approve line · when `board` is `–`, drop "· posted on …" · when a questionnaire was created or edited, add a line `Questionnaire: <path>` · extra lines from the step (e.g. `Ready to start:`) go before "Next"
  - "Next" is the next step in the track · if something must be fixed first, point at the first step that can fix it · for a story not in a Sprint yet, after step 2 it is the next story in `00-map.md` with no `02-ac.md`; if none is left, it is `plan-goal` at Planning · after step 6 it is `7 · <command> sprint-close` at the end of the Sprint · after step 6 of one ticket, when moving on to another ticket, recommend clearing the conversation first (`/clear` in Claude Code), since the state is in the files and a long conversation is slow

## Rules

- Never commit, push or open a `<review_term>` unless the user says so
- Delete files only in step 7 and move folders only in `plan-goal` · both only after the user confirms the list
- **The files in the repo are the source of truth:** `<board>` is a copy for the team to see · if someone edits on the board, ask for that edit and apply it to the repo files before the next step · if it is unclear which is newer, ask
- **approve and "Ready to start" are information for the team, not gates:** state the risk, but the team can always choose to continue
- **AC change during the Sprint:** run step 2 again → record a D whose "Files updated" names the AC numbers, e.g. `02-ac (AC5, EC3)` → fix `05-tasks.md` so every AC still has a task closing it → if a handoff exists, run step 6 again and tell `<tester>` which AC changed
- Never change the `<!-- scrum-spec ` marker on the first line; `scripts/check.py` uses it
- `scripts/check.py` reads fixed English markers such as `[ask`, `Answer:`, `(new)`, `**Summary:**`, so they stay in English whatever language the content is in · never write a project name, customer name, a role name that does not come from the config, or a path on any machine into this skill · project-specific values live only in `scrum-spec/config.md`
- `scripts/check.py` is read-only and never edits files
