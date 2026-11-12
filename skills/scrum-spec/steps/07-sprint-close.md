# 7. Close the Ticket

`<command> sprint-close` · Use during: Sprint end, after `<tester>` finishes testing · every track · Move only what future work needs into the glossary, then delete the ticket folder, the story map of any flow with no stories left, and Sprint files that have done their job

## What to keep

Keep as little as possible. An outdated document is worse than no document. If unsure, do not keep it, because git has the history.
Keep it only when all 3 hold: it cannot be found in the code, tests, `<api_spec>`, `<design_source>` or commit messages · future tickets need to know it · it fits in the glossary (do not create new doc files outside the glossary)

| Item in the ticket | Goes to |
|---|---|
| Terms whose meaning was agreed | glossary · Terms |
| D that other tickets must follow, e.g. wording, permissions, statuses that must not change | glossary · Rules across tickets |
| Behavior that looks like a bug but is intended, e.g. "does not block X because Y" | glossary · Rules across tickets, with the reason in `### Details` |
| Assumptions, `[ask]` and questionnaire items with no answer yet, Known Issues, out-of-scope items to do later | glossary · Carried over |
| APIs used in practice but missing from `<api_spec>` | No doc · tell `<api_owner>` to add it to `<api_spec>` |
| Testing traps, e.g. a persona or fixture whose name does not match its real permissions | No doc · propose a fix to the fixture or `<personas>` |
| "Not now" items and unanswered questions in `00-map.md` of a flow with no stories left | glossary · Carried over |
| Everything else, e.g. AC, design, tasks, handoff, story map, Sprint files, Owner, Estimate, UI visible in the code or design | Do not keep |

- If the glossary already has it, add to "Source" instead of adding a duplicate row · For a rule this ticket changes, replace the old row · Delete rows that are no longer true
- Delete rows in "Carried over" that this ticket finished or answered, and move the result to Terms or Rules if it meets the criteria
- Every row must make sense without opening the ticket docs · Write the source as `<ticket>` followed by the D, AC or EC number if any (not in parentheses). If there is no number, use the file name, e.g. `<ticket>` questions-po · Items from a flow use `<flow>` T<n>
- This step does not write `00-decisions.md` because the folder will be deleted. Put new answers straight into the glossary.

## Steps

1. **Choose what to close:** if there is no `ticket=`, show every folder in `<docs_root>/`, every `<docs_root>/sprint-<sprint>.md` file whose Sprint tickets are all closed, and every flow in `<backlog_root>/` with no story folders left, then ask what to close. The user may pick several. Do them one at a time.
2. **Check it can be closed:**
   - If there is no handoff file yet, warn and ask whether to close now (for example, the ticket was cancelled) or wait. Do not decide yourself.
   - ticket: ask whether it has passed `<definition_of_done>` · If not, ask whether to close it or carry it to the next Sprint. Do not decide yourself.
   - Run `git status --porcelain -- <path to delete>`. If there are uncommitted files, say they cannot be recovered from git once deleted, and ask the user to commit first. Continue once committed, or once the user confirms they accept the loss.
3. **Gather:** run `check.py` on the folder to close, then read every file in it and the glossary of the related domain · Answers in a questionnaire that are not yet in `00-decisions.md` count as new answers
4. **Find links that will break:** search for the paths to delete in every path of `code_roots` (except the path itself) · Point other tickets' docs to the heading in the glossary instead · If the cited content is not going into the glossary, ask · For links in the code, list them in the plan. Do not edit them yourself.
5. **Ask** per item 6 of `SKILL.md`. Each assumption has the options confirmed / move to Carried over / no longer doing it. You may mark one (Recommended), but the user must choose. Do not decide yourself · "Don't know yet" counts as move to Carried over
6. **Show the plan and ask before acting**, in one message: glossary rows to add, edit or delete · links to fix · issues to fix at the source · the full list of files to delete
7. **Act once the user confirms:** edit the glossary per `references/shared-files.md` → fix links → delete the folders or files the user confirmed → run `check.py` on `<glossary_root>` and the folders where links were fixed. If it exits 1, fix and run again.
8. Do not commit, and do not edit code, fixtures or config yourself unless the user says so.

Reply in chat in this format:

```
✅ Step 7 · sprint-close · <ticket … / flow … / sprint …>
glossary: <glossary_root>/<domain>.md · Terms +<n> · Rules +<n> · Carried over +<n> / removed <n>
Links fixed: <file list or "none"> · Links in code to fix yourself: <list or "none">
Fix at the source:
  - <every item · to whom, or "none">
Deleted: <path> (<n> files) · History: git log -- <path>
Next: commit the glossary and the deletions
```

## Output

- **Who confirms:** the team confirms what to keep and which files to delete before deletion · **Post on `<board>`:** ❌
