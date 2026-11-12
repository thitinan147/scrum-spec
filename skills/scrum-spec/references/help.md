# scrum-spec · How to use

Drafts a Scrum team's spec into one `spec.md` per story, so nobody waits on a blank page. **The AI proposes, people decide:** it reads the code, asks only for decisions, and puts a person's name on each one.

## Commands

```
<command> split <flow>     a whole flow → story map + one folder per story   (Refinement)
<command> ac <work>        story, rules, acceptance criteria, questions        (Refinement)
<command> tasks <work>     tasks pointing at real files, every AC covered      (Planning)
<command> handoff <work>   test steps for the tester, on day one of the Sprint (Planning)
<command>                  the next step of the work in this conversation
```

Paste the text after the command, or give a path to a PDF or image. Leave out what you don't know; the skill asks.

**Card:** what is needed (As a … I want … so that …), do / don't, ticket ID if any
**Bug:** what happens now, how to reproduce, what should happen
**Flow:** who does what on which screen, step by step, and what is in this Sprint

## Answering

- In chat: pick an option, type your own, "Don't know / ask <role>", or "use the recommendations"
- In the file, without running the skill: write in the Answer cell of the Questions table. The PO approves AC by editing the line to `**approve:** ✅ <name> · <YYYY-MM-DD>`
- The next run records each answer as a decision with your name, removes the question, and updates every section and other spec it affects

## Files

- `<docs_root>/<work>/spec.md`, one per story or ticket. Commit it with the code; delete the folder when the ticket is done (git keeps history)
- Optional `scrum-spec/config.md`: `docs_root`, `code_roots`, `roles`, `task_prefixes`

## It does not

Estimate, set priority or owners, write code, commit, push, or delete files.
