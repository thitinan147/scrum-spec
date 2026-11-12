<!-- scrum-spec 06 · sprint-handoff · 2026-01-08 -->
## 4 · Handoff to Tester

Sent to QA: 2026-01-08

**Summary:** AC 4 · EC 3 · Questions that affect testing 2

### Data and accounts

- **Has permission:** admin · `role = admin` · sees and can book the large meeting room
- **No permission:** staff · `role = staff` · does not see the large meeting room
- **Definition of Done:** –
- **Data to prepare:**
  - AC4, EC2: one PDF of 4 MB and one PDF of 6 MB (below and above the maximum size) · QA
  - EC3: a booking of room A tomorrow 10:00–11:00 made in advance · BE

### Test steps

#### Booking

- **AC1** "Book" button can be pressed
  1. Log in as staff
  2. Pick a date, time and a free room
  - Expected result: the "Book" button can be pressed
- **AC2** New booking shows in "My bookings"
  1. Fill in every field
  2. Press "Book"
  - Expected result: the new booking is in the "My bookings" list
- **AC3** "Book" disabled without a room
  1. Leave the room empty
  - Expected result: the "Book" button is disabled
- **EC3** Room already booked
  1. Pick room A tomorrow 10:00–11:00, which is already booked
  2. Press "Book"
  - Expected result: "This room is already booked"

#### Agenda

- **AC4** Attach an agenda
  1. Attach a 4 MB PDF
  - Expected result: the file name and size are shown
- **EC2** File too large
  1. Attach a 6 MB PDF (over 5 MB)
  - Expected result: an error under the field, and the "Book" button is disabled

#### Permissions

- **EC1** Large meeting room hidden from staff
  1. Log in as staff
  2. Open the room list
  - Expected result: the large meeting room is not listed

### Focus areas

1. **"My bookings" list** — must show the new booking created from this page
2. **Two people press "Book" for the same room at once** — one of them must get 409

### Out of scope, do not test

- Editing and cancelling a booking (RB-13)
- Email notifications

### Assumptions not yet confirmed

- A booking cannot span two days (D2)

### Known Issues

- –
