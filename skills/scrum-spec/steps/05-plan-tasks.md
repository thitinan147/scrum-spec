# 5. Break Down Tasks and Check Readiness

`<command> plan-tasks` · Use during: section 1.3 · last planning step of every track

## Before drafting

1. **No `04-design.md`** (small track, bug, or a large track that skipped step 4): find the files to change from the code in every path of `code_roots` based on the AC, and put them in the "Files:" line of each task.
2. Search other tickets in `<docs_root>/` that change the same files, the same tables or migrations, or the same seed data. If you find any, put them in Depends on and say which ticket creates the migration or seed (it must run whichever ticket finishes first), or say in chat that the order must be agreed.
3. In the AC table of `02-ac.md`, fill any "Verified by" cell that is still `–` from the task tests (Unit / Integration / Manual) without asking, then say in chat how many you filled · Do not overwrite values a person filled in · Filling this column does not turn the AC approve back to ❌
4. **Personas used by the AC must really work:** find the persona in `<personas>`, then check in the code that you can actually log in as that persona in the app (for example, a test user picker), not just that it exists in a fixture · If not, add a task or ask.
5. Read `<definition_of_done>` and put the work the DoD requires (for example, tests, docs) in the same task as the code · If it is `–` and you have not asked in this conversation yet, ask once where the team keeps its DoD. Do not draft a DoD yourself.

## Rules

- 1 task ≈ 1 `<review_term>` that can be reviewed in one round · A needed refactor is its own task · Tests go in the same task as the code they test
- Task IDs use a prefix from `<task_prefixes>` followed by a 2-digit number, e.g. FE-01
- Leave Owner and Est. blank for the team to fill in · Team estimation method: `<estimation>`. If the team estimates the whole ticket, no per-task Est. is needed
- Put [P] in front of the Summary cell if the task can run in parallel with other tasks (no shared files). If files overlap, use Depends on instead.
- Every AC / EC must have a task that covers it, and every file in the "Change" group of the Design must be in at least 1 task. If not, flag it below the table.

## Template

```markdown
## 1.3 Tasks

**Summary:** <n> tasks · Coverage AC/EC <n>/<n> · Can start now: <Task IDs whose Depends on is –>

**approve:** ❌ not yet · waiting for Team (dev confirms the task breakdown)

| Task | Summary | AC | Owner | Est. | Depends on |
|---|---|---|---|---|---|
| FE-01 | (1 sentence, no path) | | | | – |

### Details

- **FE-01** <short task name>
  - Do: (what must change, 1 sentence; if there are several things, start a new `Do:` line)
  - Files: `path`, `path`
  - test: (tests to add or change)

**AC / EC with no task yet:** –

**Files in the Design "Change" group not in any task:** – (small track and bug: put "not relevant")
```

## After drafting · Readiness check

This is not a gate. It says how far work can start and where the risks are. The team can always choose to start · Do not write a separate file.
1. Use the `check.py` results (coverage, `[ask]`, open Open Questions, assumptions) and your own check from item 5 of `SKILL.md` (documents that conflict) · Passing the script does not mean ready.
2. Pick 1 result, and add it in chat on top of the usual format as the line `Ready to start: <result> · <1-line reason>`
   - **Can start:** coverage is complete, no open question blocks the work, and `02-ac.md` is approved (large track: `04-design.md` too)
   - **Can start on assumptions (D…):** there are still open questions, but every one that blocks the work has an assumption someone ordered, and the AC is approved
   - **Fix first (recommended):** coverage is incomplete, documents still conflict, an open question blocks the main work with no assumption, no one has approved the AC, a large track whose API Contract or design is not approved, or the work is too big for the Sprint (propose how to split the ticket or cut scope)
3. If there is an `[ask]` still waiting for someone else, create or update `questions-<slug>.md`

## Output

- **Who confirms:** dev approves the task breakdown · the team fills in Owner and Est. at Planning · **Post on `<board>`:** ✅
