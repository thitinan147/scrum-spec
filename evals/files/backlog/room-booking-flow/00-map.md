<!-- scrum-spec 00 · refine-split · 2026-02-02 -->
## Story Map · End-to-end meeting room booking

**Summary:** 2 stories · first slice 1 story · Not now 1 · To decide 2 (open 0) · open questions 0

### To decide

| # | Topic | Proposal | Who decides | Result |
|---|---|---|---|---|
| T1 | Can staff request the large meeting room? | Yes, the manager approves; replaces the old rule that only admin can book | PO | ✅ Yes, the manager approves · Alex (PO) · 2026-02-02 |
| T2 | Defer email notifications | Defer, because they do not block booking | PO | ✅ Defer · Alex (PO) · 2026-02-02 |

### Backbone

1. Search for a free room — staff
2. Book the room — staff
3. Approve the large meeting room — manager

### Stories

| Story | Slice | Backbone | Pattern | Size signal | Track |
|---|---|---|---|---|---|
| `book-small-room` | 1 | 1–2 | Workflow steps | Uses the existing booking API | small |
| `approve-large-room` | 2 | 2–3 | Business rule variations | Needs a new approval API | large |

### Details

- **`book-small-room`** Staff book a small meeting room
  - As a staff member I want to book a small meeting room myself so that I do not have to wait for admin
  - Once delivered, the user gets: book a small room right away
  - INVEST: ✅ pass
- **`approve-large-room`** Manager approves large meeting room bookings
  - As a manager I want to approve or reject requests for the large meeting room so that the large room is used for work that needs it
  - Once delivered, the user gets: staff can book the large room without going through admin
  - INVEST: ✅ pass

### Not now

- Email notifications — do not block booking (T2)
