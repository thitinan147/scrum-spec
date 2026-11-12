# 6. Write the Handoff to the Tester

`<command> sprint-handoff` · Use during: section 4 · right after step 5, to share the test plan with `<tester>` from the start of the Sprint, not to hand work over after the code is done · `<tester>` is part of the team and works in parallel with dev · The reader does not know the code details

## Before drafting

1. **Personas:** find them in `<personas>` and in the repo itself (for example, a test user picker, fixtures, mock profiles). If the personas in different places give different roles, or a name does not match its real permissions, put it in "Focus areas" and propose a fixture fix in chat.
2. **Focus areas:** from the "Affected" group of Files in `04-design.md` (if any), the EC in `02-ac.md`, and "Must not change" for the bug track
3. **Rerun after the AC changes:** use the existing file as the base. Edit the test steps only for the AC/EC that D rows in `00-decisions.md` cite after the date it was last sent, then tell `<tester>` in chat which AC changed.

## Rules

- Test steps are converted from Given / When / Then and grouped by flow · One bold bullet per AC. Steps are a numbered list starting with a verb
- Leave out `<review_term>`, build and env. `<tester>` gets those from the `<review_term>` · Known Issues lists only what is already known

## Template

```markdown
## 4 · Handoff to Tester

Sent to <tester>: <YYYY-MM-DD>

**Summary:** AC <n> · EC <n> · Questions that affect testing <n>

### Data and accounts

- **Has permission:** (persona · role or field that decides the permission)
- **No permission:**
- **Definition of Done:** (path of `<definition_of_done>` or `–`)
- **Data to prepare:** (who prepares it · one thing per item, grouped by AC)
  -

### Test steps

#### <group name, e.g. Edit>

- **AC1** <short name>
  1. Open …
  2. Click …
  - Expected result: …

### Focus areas

(at most 5 places likely to break or affect other screens)
1. **<area>** — why it is risky and how to check it (1–2 lines)

### Out of scope, do not test

(from Out of Scope and Decisions of type "out of scope" · if you see this behavior, do not report it as a bug)
-

### Assumptions not yet confirmed

(from Decisions of type "assumption" · if it does not match what the user expects, report it and cite the D number)
-

### Known Issues

-
```

## Output

- **Who confirms:** sent to `<tester>` to write test cases and test · **Post on `<board>`:** ✅
