# Document format for easy reading

Read this file every time before writing a file in `<docs_root>/<ticket>/`, `<backlog_root>/` or the glossary. Every item applies to every step. If it conflicts with a step's Template, follow the Template

People open these documents quickly on a git host (GitLab, GitHub) or a board to find what they must do. So put the summary first, and make it easy to scan

## Contents
- 1. Summary first, detail later
- 2. Headings
- 3. Lists
- 4. Tables
- 5. Numbers and status
- 6. References
- 7. Sentences
- 8. Check before saving

## 1. Summary first, detail later

- The first line after an H2 heading is what the reader must know, such as the result, the counts or what is open, per the "Summary" field in the Template
- Open items ([ask], failed, waiting for a role) must show in the summary, not hide in the middle of a table
- Detail opened only when in doubt (e.g. paths, code evidence) goes at the end of the item, or in a "Details" section under the table

## 2. Headings

- Use `##` for section names from the Template (one per file) and `###` for sub-groups · never a whole bold line instead of a heading
- Keep headings short, with no explanation in parentheses (explanations in the Template are instructions to the AI, not output)
- Leave a blank line before and after headings, lists, tables and code blocks

## 3. Lists

- 1 bullet = 1 topic, at most about 2 lines on screen (about 200 characters); if longer, split it into sub-bullets
- Use ` · ` at most 2 times per line; with more, split into sub-bullets (except `**Summary:**` and `**Result:**` lines that list numbers in a row)
- For a topic with several parts, write the topic in bold on the parent bullet, then put the detail in sub-bullets that all start with the same kind of label, e.g. `Problem:`, `Change to:`, `Source:`
- Steps to do in order use a numbered list, one step per line, each starting with a verb such as "Open", "Click", "Check" · never write "1. … 2. …" on one line
- Things with no order use bullets, and every item in one list has the same shape
- Nest at most 2 levels, indented 2 spaces per level
- Never break a line mid-sentence (diffs get hard to read, and some languages have no spaces between words) · 1 sentence or 1 bullet = 1 line

## 4. Tables

- Use a table when each row has 3 or more cells the reader compares across rows; with fewer, use a list
- Each cell is at most 1 sentence (about 120 characters); if longer, move the detail under the table into `### Details` and refer to it by the row's ID, e.g. `**FE-01**`
- Never put `<br>`, lists, or several paths in one cell (at most 1 path per cell)
- A cell with no value gets `–`; never leave it empty, except cells the Template says the team fills in
- The table in `00-decisions.md`, the AC table in `02-ac.md` and the Tasks table in `05-tasks.md` use the Template's columns only · never add, remove or reorder columns, because `scripts/check.py` reads them by column position
- Use `\|` when a cell needs the `|` character

## 5. Numbers and status

- Status in tables uses the Template's own words, led by the same icon in every file:
  - ✅ = pass / Clear / agreed / answered
  - ⚠️ = partial / Partial / using an assumption
  - ❌ = fail / Missing / not yet
  - ➖ = not relevant
- Keep fixed values in English even when the content is in another language, because `scripts/check.py` reads them: tracks `small` / `large` / `bug`, decision types `decided` / `assumption` / `out of scope`, "Needed before" `design` / `start` / `later`, `❌ open`, `✅ answered (D<n>)`, `❌ not yet · waiting for <role>`, `not in a Sprint yet`, and `**Summary:**` lines as written in the Template
- Write counts as digits, e.g. "3", "35/35"
- Dates use `YYYY-MM-DD`

## 6. References

- Paths, field names, function names, values to type and URLs go in backticks, e.g. `src/x.ts:12`, `is_completed`
- A cited path must exist (`check.py` checks) · a file that will be created gets `(new)` after it, e.g. `src/room-list.tsx` (new) · a folder ends with `/` · an API endpoint starts with `/`
- Text the user sees on screen goes in "quotes", exactly as written
- Cite D, AC, EC and Task in parentheses at the end of the sentence, e.g. `(D9, AC23)`; never in the middle of a sentence
- Put paths at the end of a bullet or in the "Details" section, not in the middle of a sentence
- Do not repeat in another file what is already recorded in `00-decisions.md`; cite the D number instead

## 7. Sentences

- Short sentences with a subject and a verb · 1 sentence = 1 point
- Use the glossary's words, and the same word throughout the ticket (e.g. once you write "meeting room", do not switch to "room" or another word)
- No long connectives or filler such as "in this regard", "however", "with respect to"

## 8. Check before saving

- [ ] The first line after each H2 gives the result or what is open
- [ ] No bullet or table cell longer than items 3–4 allow (`scripts/check.py` reports them under "Hard to read" when a cell is over 160 characters, a line is over 300 characters, or ` · ` appears more than 2 times)
- [ ] Every set of steps is a numbered list, one step per line
- [ ] Status uses the icons in item 5
- [ ] The columns of the tables `check.py` reads are still in their places
