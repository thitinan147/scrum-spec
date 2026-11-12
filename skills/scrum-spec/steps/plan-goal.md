# Plan-goal · Sprint Goal and item selection

`<command> plan-goal sprint=<sprint>` · Use during: start of Sprint Planning (topic 1 Why and topic 2 What) · `<ac_owner>` proposes the value and chooses the Goal · the team agrees on the Goal · devs choose the items they can take on · the skill prepares data and proposals. It does not choose for them

## Before drafting

1. **Collect the items that can be chosen:**
   - stories in `<backlog_root>/*/`, in the order of each flow's `00-map.md`, and single backlog cards in `<backlog_root>/<card>/`
   - tickets in `<docs_root>/` with no Sprint yet, or left over from the previous Sprint
   - items the user adds
2. **Data for each item (facts only):** from `check.py --status` (approve, blocking questions, waiting on whom), shown in chat. Do not store these numbers in the Sprint file, because they go stale when someone answers · Track, size signals from `00-map.md`, and items that must be done first
3. **Definition of Done:** read `<definition_of_done>` · If it is `–`, ask once where the team's DoD lives, or whether there is none yet (do not draft a DoD yourself)
4. If `<docs_root>/sprint-<sprint>.md` already exists, use it as the base

## Rules

- **Sprint Goal** is a 1–2 sentence outcome that says why this Sprint has value. It is not a task list
- Propose 2–3 Goals from the available items, with reasons · They are proposals until `<ac_owner>` chooses
- **Do not calculate capacity, add points, or say the team can take it on** · Ask the devs which items they take
- **Readiness is information for the team, not a gate:** an item whose AC is not approved yet or that still has open questions can be chosen, but state the risk in the table column
- Editing "Sprint / Ticket ID" and "Related Sprint Goal" in `01-input.md` does not change the scope, so it does not turn an existing approve back to ❌

## Template

Save to `<docs_root>/sprint-<sprint>.md` with first line `<!-- scrum-spec goal · plan-goal · <YYYY-MM-DD> -->`

```markdown
## Sprint <sprint> · Goal

**Summary:** <n> items chosen · for the latest status run `<command> status`

**approve:** ❌ not yet · waiting for <ac_owner> (Goal)

**approve:** ❌ not yet · waiting for Team (chosen items)

### Sprint Goal

(1–2 sentences `<ac_owner>` chose · if not chosen yet, put `[ask: Sprint Goal · <ac_owner>]`)

### Proposed Goals

| # | Proposed Goal | Items it serves | Reason |
|---|---|---|---|
| G1 | | | |

### Chosen items

| Item | ticket | Track | Risk when chosen | Do first |
|---|---|---|---|---|
| `<flow>/<story>` or `<ticket>` | | small / large / bug | (e.g. AC not approved yet, 2 questions blocking design · as of the day chosen) | – |

### Not in this Sprint

- (item) — (reason the team gave)

### Definition of Done

- (path of the DoD or `[ask: DoD · Team]`)
```

## After drafting

1. Save, then run `check.py` on `<docs_root>`
2. Ask per item 6 of `SKILL.md` in this order: Goal (`<ac_owner>`) → items the devs take (Team) → ticket name of each story per `ticket_format`, and the Sprint / Ticket ID value
3. **Move stories into the Sprint:** show every `git mv <backlog_root>/<flow>/<story> <docs_root>/<ticket>` (or `git mv <backlog_root>/<card> <docs_root>/<ticket>`) line that will run, and ask again · Move only when the user agrees
4. After moving, update `01-input.md` of every chosen item: "Sprint / Ticket ID" and "Related Sprint Goal" · Then run `check.py` on each ticket folder
5. If a flow has no stories left in the backlog, say that `sprint-close` will propose deleting that flow's `00-map.md`

## Output

- **Who confirms:** `<ac_owner>` chooses the Goal · the team (devs) chooses the items · **Post on `<board>`:** ✅
- In chat, add the line `Moved into Sprint: <n> stories` before the "Next" line
- "Next" for each ticket by track: small and bug tracks `5 · <command> plan-tasks ticket=<ticket>` · large track `3 · <command> plan-review ticket=<ticket>`
