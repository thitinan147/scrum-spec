# scrum-spec · How to use

Helps a Scrum team write spec docs one step at a time: Refinement → Sprint Planning → share the test plan → close the ticket
**AI proposes, people decide:** the skill finds facts in the code itself, asks about anything unclear, and every decision needs a person to approve it

## First time

1. Look at what kind of work you got, then pick a command from the table "What each command needs"
2. Type the command, followed by the work's details (text, path of a PDF or image) · Not sure what to include? Type just the command and the skill will ask for what is missing
3. Answer the skill's questions · Every step ends with a `Next:` line that tells you what to type next

## For the Product Owner and flow owners: preparing refinement

| When | What | Command |
|---|---|---|
| 2–3 days before refinement | Split the flow into stories · `<ac_owner>` answers "To decide" (first slice, order, what to cut) | `refine-split flow=<name>` |
| 1–2 days before refinement | Draft rules and AC per story, starting from the first slice · send questionnaires to other roles | `refine-ac story=<flow>/<story>` |
| When answers arrive | Run the same command again. The skill reads the questionnaire answers itself | Same as above |
| Before the meeting | `<ac_owner>` approves the AC that look good | Type "approve AC" or edit the approve line in the file |

- **Walk into refinement ready:** story map, draft rules and AC, open questions, and size signals for dev to estimate · The meeting is for deciding and editing, not writing from scratch
- **No code knowledge needed:** the story map, rules and AC are written in business language. Evidence from the code sits at the end of the file for dev
- **No need to fill in** the "Verified by" column in the AC table, points or Owner · dev and `<tester>` fill them in at Planning
- **`<ac_owner>` does not have to run the skill:** approve by editing the line in the file to `**approve:** ✅ <name> (<ac_owner>) · <YYYY-MM-DD>`, or answer in the questionnaire

## Command format

```
<command> <step> <work name> <details>
```

| Part | What to put | Can you leave it out? |
|---|---|---|
| `<step>` | Step name, e.g. `refine-split`, or number, e.g. `0` | If left out, the skill runs the next step of the current work. If there is none, it shows `status` |
| `<work name>` | `flow=<name>` · `story=<flow>/<story>` · `ticket=<ticket>` · `sprint=<number>`, or just the name, e.g. `plan-review s1-x` | Yes. The skill proposes a name or lets you pick from existing folders · No need to repeat it in the same conversation |
| `<details>` | Text, path of a PDF or image, after the command or pasted in the next message | Yes, for steps that read the files of earlier steps (see the table below) |

`flow` and `story` names are lowercase, separated by `-`, with no Sprint number, e.g. `room-booking` · `ticket` names follow the project config

## What each command needs

★ = required · the rest means fewer questions

| What you got | Command | You provide | The skill reads itself from |
|---|---|---|---|
| A whole flow, not split yet | `refine-split flow=<name>` | ★ Flow content (use the "Flow form") | Code, API spec, glossary |
| A backlog story that needs AC | `refine-ac story=<flow>/<story>` | Extra rules or examples (if any) | The story's `01-input.md`, story map |
| A single card already in the Sprint | `refine-intake ticket=<ticket>` | ★ Card content (use the "Card form") | Code, glossary |
| A single card in the backlog, not in a Sprint yet | `refine-intake story=<card>` | ★ Card content (use the "Card form") · say it is not in a Sprint yet | Code, glossary |
| A bug | `refine-intake ticket=<ticket>` | ★ Symptoms (use the "Bug form") | Code, glossary |
| Start of Sprint Planning | `plan-goal sprint=<number>` | – (`<ac_owner>` picks the Goal · dev picks items when answering questions) | Existing stories and tickets, Definition of Done |
| Spec review (large track) | `plan-review ticket=<ticket>` | – | `01-input.md`, `02-ac.md` |
| Design + API (large track) | `plan-design ticket=<ticket>` | API already agreed with `<api_owner>` (if any) | `02-ac.md`, code, API spec |
| Task breakdown | `plan-tasks ticket=<ticket>` | – | `02-ac.md`, `04-design.md`, code, DoD |
| Share the test plan | `sprint-handoff ticket=<ticket>` | – | `02-ac.md`, `05-tasks.md`, personas |
| Sprint end | `sprint-close` | What to close (leave it out to pick several) | Every file in what is being closed |

## Input forms

Copy, fill in, and paste after the command. Leave blank anything you don't know. The skill will ask or find it in the code

**Flow form** (`refine-split`)

```
★ Users:       what <role> can do (one role per line)
★ Steps:       1. <who> <does what> on the <screen> screen
               2. …
  Rules:       conditions, statuses, who can do what
★ This Sprint: do … · not now …
  Agreed:      APIs already discussed, screens already done
  Attach:      path of a PDF or image
```

**Card form** (`refine-intake`)

```
★ Sprint / Ticket ID:
★ What is needed:  As a … I want … so that … (or 1–2 sentences)
  Do / Don't:      …
  Attach:          path of a PDF or image
```

**Bug form** (`refine-intake`)

```
★ What happens now:
★ How to reproduce:  1. … 2. …
★ What should happen:
  Used to work:      when, or which <review_term> broke it
```

## How to give input

- **Text:** type or paste after the command; multi-line paste is fine · Or type the command first and paste the details when the skill asks
- **PDF or image:** give the file path, e.g. `~/Downloads/flow.pdf`, or drag the file into the terminal · Large PDFs need poppler (macOS `brew install poppler` · Debian/Ubuntu package `poppler-utils`)
- **Design tool links (e.g. Figma, Miro):** the skill cannot open them. Export to PDF or an image first
- **No need to include:** anything in the code or API spec (e.g. whether this API exists yet). The skill finds it
- **Never include:** passwords, tokens or customer personal data, because the docs will be committed

## Answering questions and approving

- **The skill keeps asking until done.** No need to type "ask me" · Want one question at a time? Just say so · Answer "use all the recommendations" to settle every remaining question that has a recommended option
- **Answering:** pick an option, type your own answer, or answer "Don't know yet / wait for <role>" (it goes into the questionnaire `questions-<role>.md`)
- **"Use the proposal for now":** that item becomes an assumption, with your name recorded as the person who ordered it · If you don't say so, the skill will not choose for you
- **3 ways to approve:** type in chat, e.g. "approve AC", "approve goal" or "approve tasks" (the skill records `✅ <name from git config user.name> (<role>) · <date>`) · answer in the questionnaire · or edit the `**approve:**` line in the file yourself
- **Role:** put `my_roles: PO, BA` or `my_roles: all roles` in `scrum-spec/config.local.md` (a personal file, not committed) and the skill stops asking. If the file is missing, the skill asks once and offers to save it · Questions for roles you don't hold go into the questionnaire, not to you · Once decided, it's settled whatever the role. The skill records your name and role in the D row
- **Edits after approval:** no need to re-approve every time
  - Someone decided (any role): keep ✅ and append `(incl. D<n> · <date>)`
  - Edits to design, tasks, paths or wording with the same meaning: no effect
  - The AI changes scope, rules or AC on its own with no one deciding: back to ❌
- **Docs follow your answers at once:** the skill edits every affected file, including other tickets, Sprint files, `00-map.md` and the glossary, in one round, then says which files it edited and which it could not edit and why
- **approve and "Ready to start" are information for the team, not gates.** The team can always go on
- **Someone else answered the questionnaire:** have them write under `> Answer:` in the file, then run the same step again. The skill reads the answers itself

## Example: a full cycle, from flow to Sprint end

A made-up meeting room booking system · skill messages are cut down to the key parts

**1. Refinement · split the flow**

```
You:   <command> refine-split flow=room-booking
       ★ Users:       Employee = books rooms · Manager = approves large rooms
       ★ Steps:       1. Employee searches for free rooms  2. Books a room  3. Large rooms need manager approval
                      4. Email when approved  5. Employee can cancel
       ★ This Sprint: do items 1–3 · not now: email
skill: Which role are you answering as?  → <ac_owner>
skill: T1 Make "book a small room" the first slice? (uses the existing booking API)
         ● Yes (Recommended)  ○ Large room first  ○ Don't know yet / wait for <ac_owner>   → Yes
skill: I will create 3 story folders: book-small-room, approve-large-room, cancel-booking · OK?  → OK
skill: ✅ Step 0 · refine-split · flow room-booking
       Saved to: <backlog_root>/room-booking/00-map.md (3 stories · first slice 1 story)
       Next: 2 · <command> refine-ac story=room-booking/book-small-room
```

**2. Refinement · draft AC, then approve**

```
You:   <command> refine-ac story=room-booking/book-small-room
skill: Q1 How many days ahead can people book?  ● 30 days (Recommended · per the value in the code)  ○ No limit  ○ Don't know yet / wait for <ac_owner>
You:   Use the proposal for now
skill: Q2 Up to how many hours before the start can people cancel?  → Don't know yet, wait for <ac_owner>
skill: ✅ Step 2 · refine-ac · story room-booking/book-small-room · not in a Sprint yet
       Saved to: .../02-ac.md (AC 5 · EC 3)
       approve: ❌ not yet · waiting for <ac_owner>
       Assumptions 1: D1 book up to 30 days ahead (ordered by <name> (<ac_owner>))
       [ask] 1: up to how many hours before can people cancel → Questionnaire: .../questions-<slug>.md
You:   approve AC
skill: approve: ✅ <name> (<ac_owner>) · <date>
```

**3. Sprint Planning · set the Goal and pick items**

```
You:   <command> plan-goal sprint=5
skill: G1 "Employees can book small rooms themselves without going through an admin" ← book-small-room (AC approved)
       G2 "Managers can approve large rooms" ← approve-large-room (AC not approved · needs a new API)
       Which Goal? (<ac_owner>)  → G1
skill: Which items does dev take?  → book-small-room
skill: I will run git mv <backlog_root>/room-booking/book-small-room <docs_root>/s5-book-small-room · OK?  → OK
skill: ✅ plan-goal · sprint 5 · Saved to: <docs_root>/sprint-5.md
       Moved into Sprint: 1 story
       Next: 5 · <command> plan-tasks ticket=s5-book-small-room
```

**4. Sprint Planning · dev breaks down tasks**

```
You:   <command> plan-tasks ticket=s5-book-small-room
skill: ✅ Step 5 · plan-tasks · ticket s5-book-small-room · small track (3/4)
       Saved to: .../05-tasks.md (4 tasks · Coverage AC/EC 8/8)
       Ready to start: Can start on assumptions (D1) · AC approved
       Next: 6 · <command> sprint-handoff
You:   approve tasks
```

**5. Share the test plan, then dev picks up work**

```
You:   <command> sprint-handoff
skill: ✅ Step 6 · sprint-handoff · Saved to: .../06-handoff.md (AC 5 · EC 3)
dev:   (in their own Claude Code) read <docs_root>/s5-book-small-room/ and do FE-01
```

**6. A bug**

```
You:   <command> refine-intake ticket=s5-fix-double-booking
       ★ What happens now:    two people can book the same room at the same time
       ★ How to reproduce:    1. user A books room 1 at 10:00  2. user B books room 1 at 10:00
       ★ What should happen:  user B sees a message that this time is already booked
skill: I propose the bug track, because it used to work and then broke · OK?  → OK
skill: Next: 2 · <command> refine-ac
```

**7. Sprint end**

```
You:   <command> sprint-close ticket=s5-book-small-room
skill: Has it passed the Definition of Done?  → Yes
skill: Plan: glossary Rules +1 · Carried over +1 (up to how many hours before can people cancel) · delete 6 files · OK?  → OK
skill: ✅ Step 7 · sprint-close · Next: commit the glossary and the deletions
```

## Track of each ticket

| Track | Steps | Use when |
|---|---|---|
| small (default) | intake → ac → tasks → handoff | Most work, using existing APIs |
| large | intake → ac → review → design → tasks → handoff | A new API must be agreed with `<api_owner>`, or the scope is unclear |
| bug | intake → ac → tasks → handoff | It used to work and broke, or it does not match what was agreed |

The skill proposes a track and you choose · Stories from `refine-split` skip intake because they already have `01-input.md` · `plan-goal` runs once per Sprint

## By role

- **`<ac_owner>` and flow owners:** `refine-split`, then `refine-ac` per story · answer "To decide" (order, slice, scope) · approve AC · pick the Sprint Goal in `plan-goal`
- **dev:** pick the items you take in `plan-goal` · `plan-review`, `plan-design`, `plan-tasks` · fill in Owner and points yourselves · pick up tasks and work any way you like. You can hand the ticket folder to your own AI as context
- **`<tester>`:** read `06-handoff.md` from the start of the Sprint and write test cases in parallel with dev
- **Everyone:** answer questions in `questions-<role>.md` under `> Answer:`

## What the skill does not do

- Does not set points, priority, capacity or Owner
- Does not commit, push or open a `<review_term>` itself
- Does not move or delete files without asking
- Does not write code

## All commands

| # | Command | Phase |
|---|---|---|
| 0 | `refine-split` | Refinement |
| 1 | `refine-intake` | Refinement / Planning |
| 2 | `refine-ac` | Refinement / Planning |
| – | `plan-goal` | Start of Sprint Planning |
| 3 | `plan-review` | Planning (large track) |
| 4 | `plan-design` | Planning (large track) |
| 5 | `plan-tasks` | Planning |
| 6 | `sprint-handoff` | Start of Sprint |
| 7 | `sprint-close` | Sprint end |
| – | `status` | Any phase · writes no files |
| – | `board` | Any phase · rebuilds `board.html` from the files |

- Type the number or the command name, e.g. `<command> 5` = `<command> plan-tasks` · Other team codes can be set in `aliases` in the config
- `<command>` alone runs the next step of the current work · `<command> status`, or asking "what's next?" or "what's blocking?", gives a status table, blocking questions, what you can do now, and the next step
- After finishing a ticket, type `/clear` before starting the next one. The state is in the files, and a short conversation is faster
- `<command> help` shows this page · `<command> setup` creates or edits the project config
- The files in the repo are the source of truth. If someone edits on the board, paste that edit in chat before running the next step
- More details are in the skill's `README.md`
