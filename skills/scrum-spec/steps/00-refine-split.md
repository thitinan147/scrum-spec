# 0. Refine · Split a flow into stories

`<command> refine-split flow=<flow>` · Use during: Product Backlog Refinement · Mainly run by `<ac_owner>` or the person who owns the flow's details · Input is a whole flow not yet split into stories · Readers are people who do not read the code

This step prepares options for `<ac_owner>` to decide. It does not decide for them: how to split, which slice comes first, and what is cut are a "proposal" until `<ac_owner>` confirms.

## Prepare input

- Follow `references/input.md` before summarising (every Backbone item must point back to the input)
- Name `<flow>` in lowercase with `-` between words and no Sprint number. If the user did not give one, propose a name and ask
- If `<backlog_root>/<flow>/00-map.md` already exists, use it as the base and change only the parts with new information

## Before drafting

1. Read the glossary and search `<backlog_root>/` and `<docs_root>/` for flows or tickets that touch the same screens or rules · Flag a glossary rule that conflicts with the input right away
2. Find facts in every path of `code_roots` and in `<api_spec>`: does each step of the flow already have a screen, route or API? · Use them as size signals and as evidence for the proposal
3. If the input conflicts with the code (for example, the flow says one role can do it but the code lets another role do it), point to it with the path and ask which side to follow. Do not choose yourself

## How to split

1. **Backbone:** List the user's activities in flow order, from the input only. One activity per item, with who does it and where it comes from in the input
2. **Walking skeleton:** Propose the thinnest slice that works end to end as the first slice
3. **Split into stories:** Go through the patterns in this order. Use the first one that fits, and split along 1 axis at a time
   1. Workflow steps: build the straight path end to end first, then add middle steps and special cases later
   2. Operation: create / edit / cancel as separate stories
   3. Varying business rules: one story per rule
   4. Varying data: start with simple data, add other kinds later
   5. Data entry method: simple UI first, more convenient UI later
   6. Major effort in the first part: build the first part, then choose the next part
   7. Simple / complex: simple case first, complex case as a separate story
   8. Split performance or non-functional work from "make it work"
   9. Spike: last resort, only when you really do not know how to build it, with a clear time box
4. **Vertical slice:** Every story, once delivered, must let the user see a result or use something. Do not split by layer or component (for example, a story "build the API" or "build the screen"). `<api_owner>` work belongs in the story that uses that API, and becomes a separate task in step 5
5. **INVEST:** Check every story is Independent, Negotiable, Valuable, Estimable, Testable · Merge a story that has no value on its own into another story. Do not split it further
6. **Choose how to split:** If there are several ways to split, choose the one that shows low-value parts that can be cut, or that gives stories of similar size. Offer the other ways as options in "To decide"
7. **Nothing dropped:** Every backbone activity must be in some story, or in "Not now"

## Rules

- **Size signals are facts only**, for example "uses an existing screen", "needs a new API", "5 rules". Do not add points, S/M/L or days, because devs estimate size
- **The proposed order is a proposal.** `<ac_owner>` sets the order. The order in the Stories table follows what `<ac_owner>` has confirmed. If not confirmed yet, put it in "To decide"
- **Business language:** The main sections have no paths, file names or function names · Evidence from code goes only in the `Source:` line of `### Details`
- **Only as detailed as needed:** Stories that `<ac_owner>` says are close to a Sprint get full details. Stories that are further away get only a name and a 1-line user story · If not told yet, give full details only for the first slice, and put this in "To decide"
- Story names are lowercase with `-` between words and no Sprint number (the Sprint number and Ticket ID are added when the story enters a Sprint)
- Flow-level decisions (how to split, slices, order, what is cut) are recorded in the "To decide" table of this file. Do not create a flow-level `00-decisions.md` · Decisions that change the spec of one story go in `00-decisions.md` in that story's folder
- Ask `<ac_owner>` about scope, order and cuts · Ask the role that "Answers about" that topic in the Roles table about flow details, business rules and data (if none, ask `<ac_owner>`)

## Template

```markdown
## Story Map · <flow name>

**Summary:** <n> stories · first slice <n> stories · Not now <n> · To decide <n> (open <n>) · open questions <n>

### To decide

| # | Topic | Proposal | Who decides | Result |
|---|---|---|---|---|
| T1 | (the choice to make, 1 line) | (recommended option + short reason) | (role that owns the topic) | ❌ not yet |

### Backbone

1. (activity) — (who does it) · (source in input)

### Stories

(in the order `<ac_owner>` confirmed, or the proposed order if not confirmed yet)

| Story | Slice | Backbone | Pattern | Size signal | Track |
|---|---|---|---|---|---|
| `<story>` | 1 | 1–3 | Workflow steps | (fact, 1 sentence) | small / large |

### Details

- **`<story>`** <short story name>
  - As a … I want … so that …
  - Once delivered, the user gets: …
  - INVEST: ✅ pass / ⚠️ <what fails · reason>
  - Source: `path`

### Not now

- (topic) — (reason · result of T<n> if any)
```

- "Result" column: the person in the "Who decides" column can edit it in the file directly · `❌ not yet` or `✅ <what was decided> · <name> (<role>) · YYYY-MM-DD` · Once someone answers, it becomes ✅ right away whatever their role, recording the name and role of who answered (the "Who decides" column is a proposal of who to ask)
- `[ask: … · <role>]` can go in any section, and counts toward "open questions" in the summary line

## After drafting

1. Save `<backlog_root>/<flow>/00-map.md` and run `check.py` on `<backlog_root>/<flow>`
2. Ask per item 6 of `SKILL.md`, asking "To decide" first, starting with how to split and the first slice
3. **Before creating story folders:** show the list of stories to create and ask. Create only the stories the user confirms
4. For every confirmed story, create `<backlog_root>/<flow>/<story>/01-input.md` per the Template in `steps/01-refine-intake.md`, with first line `<!-- scrum-spec 01 · refine-split · <YYYY-MM-DD> -->`:
   - **approve:** ✅ if the person who confirmed the story list is `<ac_owner>` (`<name> (<ac_owner>) · date`), otherwise `❌ not yet · waiting for <ac_owner> (confirm scope)`
   - **Sprint / Ticket ID:** `not in a Sprint yet`
   - **Related Sprint Goal:** `–`
   - **Track:** from the "Track" column, with the reason
   - **Out of Scope:** related other stories in the flow, and the topics in "Not now"
   - **Reference:** `<backlog_root>/<flow>/00-map.md` and the stories that must be done first
   - Then run `check.py` on each story folder
   - Stories whose folder already exists: if the scope in the map changed, summarise what will change in `01-input.md` and ask before editing · For a story cut from the map, do not delete its folder. Tell the user
5. For questions still waiting on other people, create `<backlog_root>/<flow>/questions-<slug>.md` per `references/shared-files.md`

## Output

- **Who confirms:** `<ac_owner>` confirms the story list, slices and order · the role that owns the flow answers the details · devs look at the size signals and estimate during refinement · **Post on `<board>`:** ✅
- In chat, add the line `To decide: <n>, open <n> · who to ask` before the "Next" line
- "Next" is `2 · <command> refine-ac story=<flow>/<first story in the order>`
