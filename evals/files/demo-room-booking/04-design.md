<!-- scrum-spec 04 · design · 2026-01-06 -->
## 1.2 Technical Design

- **Approach:** Add a booking page with a single form that calls the new create-booking API, and reuse the existing room list while hiding the large meeting room from non-admin users
- **Files / Components:** (used for review and to avoid conflicts, not to dictate how to do it)
  - Change: `src/booking/booking-form.tsx` — booking form and validation
  - Change: `src/booking/agenda-upload.tsx` — attach the agenda
  - Change: `src/rooms/room-picker.tsx` — hide the large meeting room by permission
  - Change: `api/bookings/create.go` — create the booking and prevent double bookings
  - Change: `api/rooms/permission.go` — respond 403 when the user is not admin
  - Affected (not edited · retest): `src/booking/my-bookings.tsx` — shows the new booking
- **Data Model:** –
- **Decisions:** Prevent double bookings in BE with a unique constraint on room and time slot instead of checking in FE · because FE cannot handle two people pressing at the same time
- **Complexity Check:** no new library

**API Contract**

| Method | Endpoint / Request → Response | New / Changed | Agreed with BE? |
|---|---|---|---|
| POST | `/bookings` · room_id, start_at, end_at, agenda_file_id → 201 id · 409 if the room is booked · 403 for the large room if not admin | New | not yet |
