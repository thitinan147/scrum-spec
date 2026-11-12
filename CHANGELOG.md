# Changelog

Versions below 1.0 may change the document format (markers, headings, file names, config keys). Each such change is listed here. From 1.0, a format change bumps the major version and comes with upgrade notes.

## 0.1.0 - first release

- `/scrum-spec` drafts a Scrum team's spec documents step by step: story map (step 0), input (1), requirements and acceptance criteria (2), Sprint Goal (`plan-goal`), spec review (3), technical design (4), tasks with a readiness check (5), tester handoff (6) and sprint close (7).
- Three ways in: a whole board or flow, a single backlog card, or a card already in the Sprint.
- Three tracks: small, large and bug.
- The AI proposes and people decide: every decision, approval and "To decide" result records a person's name, role and date.
- `scripts/check.py` checks every document folder: tables, first-line marker, cited paths, decision and AC references, approvals, summary counts, and readability. `--status` shows every piece of work, what blocks it, and the next step.
- Markers, headings and table columns are in English; the drafted text follows the language of the input.
- Project settings in `scrum-spec/config.md`; personal roles in `scrum-spec/config.local.md` (gitignored).
- Human-only: `disable-model-invocation` (Claude Code), `allow_implicit_invocation: false` (Codex), and a `HUMAN-ONLY COMMAND.` description prefix (other agents).
