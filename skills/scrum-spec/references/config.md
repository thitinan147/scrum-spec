# Project config

Read this file when running `setup`, when editing the config, or when unsure what a key means

## Contents
- Where the file lives
- File format
- Keys
- Roles
- Placeholders in `steps/`
- setup
- Personal file (not committed)

## Where the file lives

`scrum-spec/config.md` at the project root · commit it so the whole team uses the same values · the `scrum-spec/` folder also holds the documents by default (`scrum-spec/sprint/`, `scrum-spec/backlog/`, `scrum-spec/glossary/`)

The skill looks for the config in this order
1. the root of the git repo cwd is in (`git rev-parse --show-toplevel`) · this works in a worktree, because committed files are in the worktree too
2. if cwd is not in a git repo (e.g. a folder that holds several repos): look for `scrum-spec/config.md` in cwd first; if not there, look for `*/scrum-spec/config.md` one level down and ask which one to use
3. not found: run `setup` first, then the step that was asked for

Paths in the config are relative to the folder that holds `scrum-spec/` (the project root)
In a worktree, count `code_roots` from the main checkout (the parent folder of `git rev-parse --git-common-dir`), because sibling repos sit next to the main checkout, not next to the worktree
If a path does not exist, warn once and use what exists

## File format

One `key: value` per line · several values are separated by `, ` · a value that is absent or unused gets `–` · never use `|` in a value

```markdown
<!-- scrum-spec config -->
# scrum-spec config

version: 1
docs_root: scrum-spec/sprint
backlog_root: scrum-spec/backlog
glossary_root: scrum-spec/glossary
domain_source: src/modules/*
code_roots: ., ../api
project_rules: AGENTS.md, CLAUDE.md
definition_of_done: docs/definition-of-done.md
api: yes
api_spec: ../api/docs/openapi.yaml
ac_owner: PO
api_owner: BE
tester: QA
layers: FE, BE
task_prefixes: FE, BE, INT, TEST
estimation: points per task
review_term: PR
board: Miro (sections 0–4 of the ticket board)
design_source: Figma
input_sources: issue text, PDF exported from the board
personas: test/fixtures/users.ts
ticket_format: <ticket-id>-<short-name> in lowercase joined by -, e.g. abc-123-room-booking
aliases: input=1, ac=2, tasks=5

## Roles

| Name | slug | Answers about | Questionnaire |
|---|---|---|---|
| PO | po | scope, order, confirming AC, wording | ✅ |
| BA | ba | flow detail, business rules, data | ✅ |
| BE | be | API, server-side permissions | ✅ |
| UX | ux | design, mobile | ✅ |
| QA | qa | test cases, edge cases | ❌ |
| Team | team | decisions inside the team | ❌ |
```

## Keys

| key | Used for | If `–` |
|---|---|---|
| `version` | version of the config format; currently 1 | – |
| `docs_root` | folder that holds tickets (`<docs_root>/<ticket>/`) | must have a value |
| `backlog_root` | folder that holds flows and stories from step 0, and single backlog cards, before they enter a Sprint (`<backlog_root>/<flow>/<story>/`, `<backlog_root>/<card>/`) | no step 0 and no backlog cards |
| `glossary_root` | folder of the glossary | no glossary |
| `domain_source` | how glossary domains are named, e.g. folders in `src/modules/*` | one file, `<glossary_root>/index.md` |
| `code_roots` | every repo to search for code (supports FE and BE in separate repos) | use `.` |
| `project_rules` | files with the project's constraints and rules that step plan-design must read | no constraints to check |
| `definition_of_done` | the team's Definition of Done file (used in plan-goal, plan-tasks, sprint-handoff, sprint-close) | ask once where the team's DoD is; never draft one |
| `api` | does the project have an API to agree on (`yes` / `no`) | – |
| `api_spec` | the Swagger / OpenAPI file that step plan-design must read | ask, or use response examples from the code |
| `ac_owner` | the role acting as Product Owner: decides value, scope, order, Sprint Goal and confirms AC | use "Team" |
| `api_owner` | the role that agrees the API Contract | use "Team" |
| `tester` | the role that writes test cases and receives the handoff | use "Team" |
| `layers` | layers where rules are enforced, e.g. FE, BE (used in step plan-review) | use "System" |
| `task_prefixes` | prefixes of Task IDs | use `T` (T-01, T-02, …) |
| `estimation` | how the team estimates, e.g. `points per task` or `points per ticket` (used in step plan-tasks) | do not check Estimate |
| `review_term` | the name of a code review unit, `MR` or `PR` | use "MR/PR" |
| `board` | where the team posts results together, e.g. Figma, Miro, Confluence (the "posted on …" line) | drop the "posted on …" line |
| `design_source` | where the UX design lives (steps plan-review and sprint-close) | assume there is no design to cite |
| `input_sources` | input the team usually gives in steps 0 and 1, e.g. issue text, PDF from a board | ask the user |
| `personas` | file to find personas / test users in, e.g. fixtures | search the code yourself |
| `ticket_format` | the ticket folder name format, with an example | follow the folders already in `<docs_root>` · if there are none, ask, proposing `<ticket-id>-<short-name>` (with an issue number) and `s<Sprint number>-<short-name>` (no issue number), lowercase joined by `-` |
| `aliases` | other codes the team uses for steps, e.g. `S0=1, S1=2` or command names `input=1, ac=2` | none |

## Roles

A table with the columns `Name | slug | Answers about | Questionnaire`
- **Name:** used in `[ask: … · who to ask]` and in the option "Don't know yet / wait for <name>"
- **slug:** lowercase English letters, used to name `questions-<slug>.md`
- **Answers about:** helps pick whom to ask
- **Questionnaire:** ✅ = create `questions-<slug>.md` for this role · ❌ = do not (e.g. the team itself, or a role that only reviews)

`<roles>` is every role name in the table, separated by ` / `

## Placeholders in `steps/`

Files in `steps/` and `references/` write values that differ per project as `<key>` · substitute the config's values before following them

| placeholder | Comes from |
|---|---|
| `<skill_dir>` | the skill's path ("Values used" in `SKILL.md`) |
| `<command>` | the command the user runs the skill with ("Values used" in `SKILL.md`) |
| `<roles>` | every role name in the Roles table, separated by ` / ` |
| other `<key>` such as `<docs_root>`, `<board>`, `<review_term>`, `<project_rules>`, `<ac_owner>`, `<api_owner>`, `<tester>` | the config key of the same name |

If one is left unsubstituted and written into a document, `scripts/check.py` reports it as an error

## setup

Used when the user runs `<command> setup`, or when a step runs and there is no config yet

1. **Where to write:** the root of the git repo cwd is in · if cwd is not in a git repo, ask first whether to write in cwd (a workspace-level config) or in which repo · never write outside a git repo without asking
2. **If a config already exists:** show the current values, ask which keys to change, show what will change, then ask before writing · never overwrite the whole file
3. **Guess values from the repo before asking:**

   | key | Guess from |
   |---|---|
   | `review_term` | `git remote get-url origin`: a host with `gitlab` → MR · `github.com` → PR · other hosts: ask |
   | `project_rules` | files that exist at the root, e.g. `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md` |
   | `definition_of_done` | a file whose name has `definition-of-done` or `dod`, or a "Definition of Done" heading in the repo's documents · not found: ask · never use a constraints file as the DoD yourself |
   | `docs_root`, `ticket_format` | a folder that already holds `01-input.md` files, and the ticket folder names in it · none: propose `scrum-spec/sprint` |
   | `backlog_root` | a folder that already holds `00-map.md` files · none: propose `scrum-spec/backlog` |
   | `glossary_root`, `domain_source` | an existing glossary folder (none: propose `scrum-spec/glossary`) · domain or module folders in the code |
   | `task_prefixes` | Task IDs in existing `05-tasks.md` files · if none, see whether the repo splits FE / BE |
   | Roles, `ac_owner`, `api_owner`, `tester` | the end of `[ask … · X]` and the "Who confirms" lines in existing documents |
   | `code_roots` | sibling repos in the parent folder with similar names, e.g. `-fe` and `-be`, or `web` and `api` |
   | `api`, `api_spec` | `swagger.*` or `openapi.*` files in `code_roots` |
   | `personas` | fixtures, seeds or mock users / profiles in the code |
   | `estimation` | Tasks tables in existing documents |

4. **Ask the rest in one round** per item 6 of `SKILL.md` · guessed values are the first option with "(Recommended)" and say where they were found
5. **Write `scrum-spec/config.md`** in the format above, then tell the user to commit it
6. **If `code_roots` has a path outside the repo:** tell the user the agent may ask permission every time it reads that path (in Claude Code, fix it with `/add-dir` or `permissions.additionalDirectories` in settings)
7. If setup ran because the user asked for another step, do that step right after

## Personal file (not committed)

`scrum-spec/config.local.md` holds each person's own values · it has one value for now:

```
my_roles: PO, BA      # or: all roles
```

- The skill uses this value instead of asking for the role every conversation, and in chat asks only these roles' questions
- It must be in `.gitignore` (one line: `scrum-spec/*.local.md`) · with no file, the skill asks once and offers to create it
