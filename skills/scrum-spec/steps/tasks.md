# tasks · Break the work into tasks

`<command> tasks <work>` · for Sprint Planning · readers are dev

The goal: dev start Planning from tasks that point at the real files, with every AC covered, instead of breaking work down from zero.

## Before drafting

1. Read the AC and every open question with Blocks `tasks`. If one is open, say so and ask it first; draft only what does not depend on it, unless someone says "use the proposal for now" (an `assumption:` decision)
2. Find the files each AC touches in every `code_roots` path. Every cited path must exist; a file to create gets `(new)` after it
3. Grep other specs in `<docs_root>` for the same files, tables or migrations; put them in Depends on, or say the order must be agreed
4. Personas or test users the AC need: check in the code that one can really log in as them; if not, add a task

## Rules

- 1 task ≈ 1 merge request that can be reviewed in one round · tests go in the same task as the code they test · a needed refactor is its own task
- Task IDs: a prefix from `task_prefixes` and two digits, e.g. `FE-01`
- Every AC and EC is in the AC column of at least one task; the checker lists any that are not
- Leave estimates and owners to the team; the table has no column for them
- A new or changed API: its own task for the API owner's side, and the contract (method, path, fields, errors) in that task's Do cell or in one line under the table

## Template

```markdown
## Tasks

| Task | Do | AC | Files | Depends on |
|---|---|---|---|---|
| FE-01 | (1 sentence) | AC1, EC2 | `path`, `path` (new) | – |
```

## After drafting

- In the reply, add one line before Next: `Ready: yes / with assumptions (D…) / not yet · <reason>`. It informs the team; it is not a gate
- Next: `handoff`
