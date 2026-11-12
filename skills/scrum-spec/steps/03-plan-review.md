# 3. Review the Spec for ambiguity

`<command> plan-review` · Use during: after drafting the AC · Large track only (small and bug tracks do a short review in step 2)

Find points where 2 devs could read it and build different things, and points where `<tester>` cannot tell how to test. If none are found, answer "none found". Do not invent issues to fill the list

## Categories to check

Give every category a status: Clear / Partial / Missing / Not relevant
1. Scope and main behavior
2. Data and fields (accepted values, required, format, defaults)
3. Flow and UX (navigation, screen states, messages)
4. Non-functional (mobile, accessibility, performance, security)
5. Permissions (who can do it, which `<layers>` enforce it, buttons/URLs/APIs)
6. Integration and API (endpoints, errors, external systems)
7. Edge cases and errors (empty data, lots of data, double submit, data already edited or deleted by someone else)
8. Does Out of Scope conflict with other parts?
9. Terms (the same word used with different meanings, vague words such as "fast", "own")
10. Are the AC checkable? (Then is checkable, examples do not conflict with the rules, which EC are missing)

Put the questions found in Open Questions of `02-ac.md` (the single question list of the work), with the "Needed before" cell set by impact:
- **Needed before design:** if the answer would force design / tasks / API to be redone (scope, which frames are in the ticket, permissions, `<api_owner>` work)
- **Later:** does not change the structure (messages, minor numbers, order)

## Template

```markdown
## Spec Review

**Summary:** ✅ <n> · ⚠️ <n> · ❌ <n> categories · issues <n> · new questions <n> (needed before design <n>)

### Spec completeness

| Category | Status | Note |
|---|---|---|
| 1. Scope and main behavior | ✅ Clear / ⚠️ Partial / ❌ Missing / ➖ Not relevant | (1 sentence) |

### Issues found

(at most 5, ordered from most to least impact)
1. **<short issue name>**
   - Issue: …
   - Fixed AC: …
```

## After drafting

1. Propose all edits to `02-ac.md` at once: AC per "Fixed AC" and new questions in Open Questions · Ask before editing. If the user agrees, edit right away (and `01-input.md` if the scope changes)
2. Ask per item 6 of `SKILL.md`, asking the questions needed before design first · Answered questions change their status in Open Questions to `✅ answered (D<n>)`
3. Group the still-open questions by role and create `questions-<slug>.md`
4. If questions needed before design are still open, say in the "Next" line that going to step 4 now may mean redoing the design

## Output

- **Who confirms:** the roles asked answer the open questions · `<tester>` reviews the added EC · **Post on `<board>`:** ✅ only the questions still open
