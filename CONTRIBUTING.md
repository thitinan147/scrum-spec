# Contributing

Thanks for helping. Issues and pull requests are welcome.

## Report a problem

- **Bug or unclear behaviour:** open an issue and include your agent (Claude Code, Codex, ...), OS, Python version, the step you ran, and the `check.py` output. Remove names, customer data and internal paths first.
- **Security problem:** do not open a public issue. See [SECURITY.md](SECURITY.md).
- **Tested on another agent or on Windows?** Tell us in an issue. The README lists what is tested.

## Change the skill

1. Fork, then branch from `main`.
2. Run the tests: `python3 -m unittest discover -s tests` (Python 3.10+, standard library only).
3. Keep the skill dependency-free. `check.py` uses only the standard library and never edits files.
4. Keep it small: `SKILL.md` plus any one step file stays under 1,500 words (a test checks it). Add a command or a section only when a team asked for it.
5. If you change a heading, table column, marker or config key, update the step's template, `check.py`, the fixtures in `evals/files/`, and `CHANGELOG.md`, and add or adjust a test. `tests/test_skill_contracts.py` fails when `check.py` relies on a marker no prompt writes.
6. If you add or rename a command, update the "Commands" table in `SKILL.md`, `references/help.md`, `README.md` and `evals/evals.json`.
7. Behaviour changes: run the affected scenarios in `evals/evals.json` (see [docs/evals.md](docs/evals.md)) before and after, and say in the pull request what changed.
8. Open a pull request that says what changed and why. CI runs the tests, `bandit`, Agent Skills spec validation, and a SkillSpector scan. Any new SkillSpector suppression in `.skillspector-baseline.yaml` needs a written reason.

Commit messages follow `type(scope): summary` (for example `fix(check): ...`).
