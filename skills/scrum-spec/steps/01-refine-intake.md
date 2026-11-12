# 1. Summarise the ticket Input

`<command> refine-intake` · Use during: section 0 · When you get one ticket at a time, or a bug (Refinement or Planning) · If you get a whole flow, use step 0 · Summarise from the input only. Do not write new requirements

## Prepare input

- Follow `references/input.md` before summarising
- Where to write: a card already in the Sprint goes to `<docs_root>/<ticket>/` · a single card not in a Sprint yet goes to `<backlog_root>/<card>/` with "Sprint / Ticket ID" set to `not in a Sprint yet` · if unclear, ask which one
- If the input is a whole flow not yet split into tickets (several screens or several user activities) and `backlog_root` is not `–`, propose step 0 `refine-split` instead, and ask before going on

## Before drafting

1. Read the glossary in `<glossary_root>` and search other tickets in `<docs_root>/` and stories in `<backlog_root>/` that mention the same screen, menu or term. If found, add them to Reference with the path · If a rule conflicts with the note, flag it right away
   - Rows in "Carried over" that relate to this ticket: add them to Reference and tell the user this ticket may close that row
   - Rows whose "Added" date is older than 6 weeks: ask the user whether to keep or delete them. Delete only when the user answers · Except rows this ticket is working on: no need to ask
2. Check whether code for this ticket already exists, then propose a track per the "Tracks by type of work" table in `SKILL.md`, with a reason from the scope, and ask the user

## Rules

- Track: small (default) / large when a new or changed API must be agreed with `<api_owner>` before writing code, or the scope is not clear yet / bug when behavior does not match what was agreed, or used to work and broke
- Fields not in the input become `[ask]`. Do not make them up

## Template

```markdown
## 0 · Input

**approve:** ❌ not yet · waiting for <ac_owner> (confirm scope)

- **Sprint / Ticket ID:**
- **Feature Name:**
- **Track:** small / large / bug · reason:
- **Related Sprint Goal:**
- **User Story:** As a … I want … so that …
- **Business Context:** (1–2 sentences)
- **In Scope:** (if there are several screens or flows, group them · the first sub-bullet is the group name in bold, one topic per item)
  -
- **Out of Scope:** (one topic per item)
  -
- **Reference:**
  - (source in the input, e.g. page, frame or note · links · other tickets that touch the same screen or rule)
```

## Output

- **Who confirms:** the person who takes the ticket summarises · `<ac_owner>` confirms scope · the team helps fill in `[ask]` · **Post on `<board>`:** ✅
