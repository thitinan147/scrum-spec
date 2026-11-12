"""Tests for skills/scrum-spec/scripts/board.py against fixtures and maps.

Run: python3 -m unittest discover -s tests
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BOARD = REPO / "skills" / "scrum-spec" / "scripts" / "board.py"
FIXTURES = REPO / "evals" / "files"


class BoardTests(unittest.TestCase):
    def test_generate_board_from_fixture(self) -> None:
        fixture_dir = FIXTURES / "room-booking" / "scrum-spec"
        with tempfile.TemporaryDirectory() as tmp:
            out_file = Path(tmp) / "board.html"
            res = subprocess.run(
                [sys.executable, "-I", str(BOARD), str(fixture_dir), "-o", str(out_file)],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(res.returncode, 0, res.stderr)
            self.assertTrue(out_file.exists())
            html = out_file.read_text(encoding="utf-8")

            # Check that stories are included
            self.assertIn("rb-12-book-room", html)
            self.assertIn("rb-13-cancel-booking", html)
            self.assertIn("RB-12", html)
            self.assertIn("RB-13", html)

            # Check ACs are rendered
            self.assertIn("AC1", html)
            self.assertIn("EC1", html)

            # Check Decision D1
            self.assertIn("A booking lasts at most 4 hours", html)

            # Check Blocker question
            self.assertIn("BLOCKS DEV", html)

    def test_generate_board_with_map(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            map_file = root / "map.md"
            map_file.write_text("""<!-- scrum-spec -->
# Story map · room-booking

**approve:** ❌ waiting for PO

## Steps

1. Find a room — Staff · PO note
2. Pick date and time — Staff · PO note

## Stories

| Story | Steps | Once done, the user can | Size signal |
|---|---|---|---|
| `rb-12-book-room` | 1–2 | Book a room | existing screen |

## Not now

- Email notifications — postponed

## Questions

| # | Question | Ask | Blocks | Answer |
|---|---|---|---|---|
| Q1 | Proposal: first slice is rb-12 | PO | stories | |
""", encoding="utf-8")

            spec_file = root / "rb-12-book-room" / "spec.md"
            spec_file.parent.mkdir(parents=True, exist_ok=True)
            spec_file.write_text("""<!-- scrum-spec -->
# rb-12-book-room

## Story

- **Ticket:** RB-12
- **Story:** As a user I want to book a room
- **In scope:**
  - Pick room
- **Out of scope:**
  - Email

## Rules

- Max 2 hours

## Acceptance Criteria

**approve:** ✅ Alex · 2026-11-03

| # | Given | When | Then |
|---|---|---|---|
| AC1 | Room free | Click Book | Booked |

## Questions

| # | Question | Ask | Blocks | Answer |
|---|---|---|---|---|

## Decisions

- **D1** Max 2 hours · Alex · 2026-11-03

## Test steps

- **Accounts:** Alex
- **Data to prepare:** none
- **Do not report:** none

### AC1 Booked

1. Click book
""", encoding="utf-8")

            out_file = root / "board.html"
            res = subprocess.run(
                [sys.executable, "-I", str(BOARD), str(root), "-o", str(out_file)],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(res.returncode, 0, res.stderr)
            self.assertTrue(out_file.exists())
            html = out_file.read_text(encoding="utf-8")

            # Check steps
            self.assertIn("Step 1", html)
            self.assertIn("Find a room", html)
            self.assertIn("Step 2", html)

            # Check not now
            self.assertIn("Email notifications", html)

            # Check story & correlated map step
            self.assertIn("Steps 1–2", html)
            self.assertIn("rb-12-book-room", html)
