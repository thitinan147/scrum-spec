# Glossary · booking

## Terms

| Term | Meaning | In code / data | Source |
|---|---|---|---|
| Large meeting room | A room for more than 20 people; only admin can book it | `room.size = large` | `demo-room-booking` EC1 |

## Rules across tickets

| Rule | Applies to | Source |
|---|---|---|
| Show times in 24-hour format, e.g. 13:30 | Every page that shows booking times | `demo-room-booking` D3 |
| Only admin can book the large meeting room | Booking page, room list, booking API | `demo-room-booking` EC1 |

## Carried over

| Topic | Type | Ask / owner | Added | Source |
|---|---|---|---|---|
| Room timeline page showing all of a day's bookings in one view | deferred | PO | 2025-06-01 | `demo-room-booking` 01-input |
