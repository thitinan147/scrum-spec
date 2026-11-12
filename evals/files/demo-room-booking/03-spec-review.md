<!-- scrum-spec 03 · spec-review · 2026-01-06 -->
## Spec Review

**Spec completeness**

| Category | Status | Note |
|---|---|---|
| 1. Scope and main behavior | Clear | |
| 2. Data and fields | Partial | Not yet known whether a booking can span two days |
| 3. Flow and UX | Clear | |
| 4. Non-functional | Missing | Mobile is not mentioned |
| 5. Permissions | Clear | Large meeting room: FE hides it · BE responds 403 |
| 6. Integration and API | Partial | There is no create-booking API yet |
| 7. Edge cases and errors | Partial | No case for a room booked by someone else before "Book" is pressed |
| 8. Constraints and exclusions | Clear | |
| 9. Terms | Clear | |
| 10. Testability of AC | Clear | |

**Issues found** (at most 5, ordered from most to least impact)
1. Issue: no case for a room booked by someone else while filling in the form · Fixed AC: EC3

**Questions · needed before design**

| # | Question | Why it matters | Ask (PO / BE / UX / QA / Team) | Proposed assumption |
|---|---|---|---|---|
| Q1 | Can a booking span two days? | Changes validation and the API | PO | No → assumption (D2) |

**Questions · can wait until ready**

| # | Question | Why it matters | Ask (PO / BE / UX / QA / Team) | Proposed assumption |
|---|---|---|---|---|
| Q2 | Are agenda file types other than PDF supported? | Changes file validation | PO | Accept PDF only |
