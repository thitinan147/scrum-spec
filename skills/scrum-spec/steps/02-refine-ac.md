# 2. Draft Requirement & Acceptance Criteria

`<command> refine-ac` · Use during: section 1.1 · Refinement (story in the backlog) or Planning (ticket) · Write only the What (what the system must do). Do not include how to implement it

Business Rules are the rules, the AC table holds examples of the rules, and Open Questions are what cannot be answered yet (in the style of Example Mapping) · Every rule should have at least 1 example in the AC

The main readers are `<ac_owner>` and the flow owner, who may not read the code

Open Questions is the single question list for this work. Step 3 adds its questions here · An answered question changes its status to `✅ answered (D<n>)`. Do not delete it

## Rules

- AC table: 1 row = 1 behavior · Given, When, Then in separate cells, 1 sentence per cell · Then must be visible or checkable. If there are several outcomes, split them into several rows
- **Business language:** Problem → Outcome, User Flow, Business Rules and Given / When / Then use words the user sees on screen. No paths, field names, function names or endpoints · Evidence from code goes in `### Evidence from code` at the end of the file
- AC1, AC2… = main flow · EC1, EC2… = edge cases (empty data, over size, no permission, system failure, double submit)
- **Verified by** (Unit / Integration / Manual) is for the devs and `<tester>`: during Refinement put `–` and fill it in at step `plan-tasks` · For a ticket drafted during Planning, a dev can fill it in right away
- If AC already exist, keep them and add only what is missing
- If code for the ticket already exists, compare the AC with the code. For any difference, ask which side to follow
- Examples in the AC must not conflict with the Business Rules
- **Move questions from `01-input.md`:** put every `[ask]` in `01-input.md` into Open Questions (do not add ones already there again), then delete them from `01-input.md` · This deletion does not change the approve of `01-input.md` · If any remain, `check.py` reports an error
- What is not done in this ticket goes in Out of Scope · If an AC is cut later, do not renumber. Put the cut number in Out of Scope (e.g. "was EC4")
- **Screens:** If the input has screens (`<design_source>`, PDF or images), go through every screen and every visible part (buttons, columns, input fields, print/export) into the "Screens" table · Every row must have an AC/EC, be in Out of Scope, or be `[ask]` · Also go through the states the user can meet: empty data, failed to load, no permission, text too long · If there are no screens, put `–`
- Bug track: use the **Bug** heading instead of **Problem → Outcome** and **User Flow** · AC = correct behavior · EC = what must not change

## Template

```markdown
## 1.1 Requirement & Acceptance Criteria

**Summary:** AC <n> · EC <n> · Open Questions <n>

**approve:** ❌ not yet · waiting for <ac_owner>

### Problem → Outcome

(1–2 lines on how the result is measured once done)

### User Flow

1.

(the bug track uses this heading instead of the 2 headings above)
### Bug

- **Current behavior:** (what happens)
  1. (steps to reproduce, one step per line)
- **Correct behavior:**
- **Must not change:**

### Business Rules

(validation, permissions, conditions · the parent bullet is the group name in bold, rules are sub-bullets, one rule per item)
- **<group name>**
  -

### Out of Scope

(include the AC/EC numbers that were cut)
-

### Screens

(every part seen in the design or input · if there are no screens, put `–`)

| Screen / part | States to support | AC / EC |
|---|---|---|
| | normal / empty / error / no permission | AC1 or Out of Scope or `[ask]` |

### Acceptance Criteria

| # | Given | When | Then | Verified by |
|---|---|---|---|---|
| AC1 | … | … | … | – |
| EC1 | … | … | … | – |

### Open Questions

| # | Question | Ask (<roles>) | Needed before | Proposal | Status |
|---|---|---|---|---|---|
| Q1 | | | design / start / later | | ❌ open |

### Evidence from code

(for devs · one topic per bullet, cite the rule or AC number · if none, put `–`)
- (AC1) `path` — what was found
```

## After drafting · small and bug tracks

These tracks have no step 3, so a short spec review happens in this step
1. Go through the check categories in `steps/03-plan-review.md` and the `<tester>` view (how each AC is tested, which EC are missing). Find at most 5 points where 2 devs could read it and build different things
2. Fix them directly in the AC table and Open Questions. Do not add new headings
3. Ask per item 6 of `SKILL.md`, then create `questions-<slug>.md` for the items still waiting on other people
4. If you find that a new API must be agreed or the scope is unclear, propose upgrading to the large track

## After drafting · all tracks

- **Story too big:** If Business Rules have more than 4 groups, or many Open Questions block the main AC, propose splitting the story with a split method per `steps/00-refine-split.md`, and ask · If it is a story in the backlog and the user agrees, also update the flow's `00-map.md` · Do not split it yourself

## Output

- **Who confirms:** `<ac_owner>` confirms the AC · **Post on `<board>`:** ✅
