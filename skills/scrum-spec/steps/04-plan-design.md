# 4. Draft the Technical Design + API Contract

`<command> plan-design` · Use during: section 1.2 · large track only · Pick the simplest approach that passes every AC. Reuse what the repo already has before building something new.

## Before drafting

1. If Open Questions in `02-ac.md` still has an open question whose "Needed before" is design, ask it first per item 6 of `SKILL.md`. If the user says to go on with the proposal, record it as an assumption in `00-decisions.md` with the name of the person who said so (item 6.3 of `SKILL.md`). Then draft and warn that the design must be redone if the answer changes · If no one said so, draft only the parts that do not depend on that question.
2. Read the code the AC touches in every path of `code_roots`, `<api_spec>` and `<project_rules>`. If an AC conflicts with the current code, ask which side to follow, then update the AC to match.
3. For every screen that a permission AC mentions, find every place in the code that has that button/menu/route.

## Rules

- Files / Components are for review and for avoiding clashes with other tickets. They do not dictate how to build it · Change = files a task must edit · Affected = not edited, but behavior may change and must be retested
- The design must not conflict with `<project_rules>`. If it does, say so and name the rule it breaks.
- In the "Agreed?" column, put "❌ not yet" on every row for the team to confirm, except endpoints that do not change, which get "➖ existing" · If there is no API to agree on, add a single row saying "➖ not relevant"
- Decisions holds only items that are hard to reverse, have real alternatives, and would make a later reader ask why · Every item is a proposal until the file's approve line is ✅ · The "Agreed?" column of the API Contract turns ✅ only when `<api_owner>` approves per "Who approves" in `SKILL.md`
- If data you need is not in the response (for example, you must filter by permission but there is no field), say it must be done on the `<api_owner>` side and put it in the API Contract.

## Template

```markdown
## 1.2 Technical Design

**Summary:** change <n> files · affected <n> files · new/changed API <n> endpoints (agreed <n>)

**approve:** ❌ not yet · waiting for <api_owner> (API Contract) and Team (design)

### Approach

(2–3 bullets)
-

### Files / Components

(one file per bullet · if there are several repos, group them, e.g. "Change (FE)", "Change (BE)")
- **Change**
  - `path` — short reason (AC…)
- **Affected (not edited · retest)**
  - `path` — short reason (AC…)

### Data Model

(only if it changes)

### Decisions

- **<topic>**
  - Options: …
  - Chosen: …
  - Because: …

### API Contract

| Method | Endpoint | New / Changed | Agreed with <api_owner>? |
|---|---|---|---|
| | `/path` | (1 sentence, e.g. "Changed: add `field`") | ❌ not yet |

(put the request / response of each new or changed endpoint under the table, one json code block per endpoint, only the relevant fields, with the error status codes)
```

## Output

- **Who confirms:** `<api_owner>` confirms the API Contract · someone reviews the design · **Post on `<board>`:** ✅
