# handoff · Test steps for the tester

`<command> handoff <work>` · right after `tasks`, so the tester starts on day one of the Sprint, in parallel with dev · readers know the product, not the code

## Before drafting

1. Find the test users or personas in the code (fixtures, seed data, a test user picker). A name that does not match its real permission goes in Watch out
2. Risky places: files several tasks change, screens that share the changed code, and the EC
3. Rerun after an AC changed: edit only the steps of the AC that a newer D changed, and say in chat which ones

## Rules

- One `###` per AC or EC with numbered steps starting with a verb. The AC's Then is the expected result; add `- Also check:` only for what Then does not say
- Out of scope and `assumption:` decisions are listed so the tester does not report them as bugs, or reports a mismatch citing the D

## Template

```markdown
## Test steps

- **Accounts:** (persona with permission · persona without)
- **Data to prepare:** (one thing per line, or –)
- **Do not report:** (Out of scope items and assumptions, citing D numbers, or –)

### AC1 (short name)

1. Open …
2. Click …

### Watch out

1. (at most 5 places likely to break · why · how to check)
```

## After drafting

- Next: none; the story's spec is complete. Suggest starting a new conversation for the next story
