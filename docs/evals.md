# Evals

`evals/evals.json` holds scenarios that check how the agent behaves with the skill, in the format of the [skill-creator](https://code.claude.com/docs/en/skills.md#run-evals-with-skill-creator) plugin. Each scenario has a `query` (what the user types), the `files` it needs, and the `expected_behavior` to grade against. The fixture files in `evals/files/` double as the fixtures of the `check.py` unit tests.

Run the scenarios before the team relies on a change, and after every change to `SKILL.md`, `steps/` or `references/`.

## Run a scenario by hand

1. Create a scratch git repo and set `git config user.name`.
2. Install the skill there (see the README), or point your agent at your working copy.
3. Copy the scenario's `files` into place:
   - `evals/files/configs/<name>.md` → `scrum-spec/config.md`
   - `evals/files/glossary/` → `<glossary_root>/`
   - a ticket folder → `<docs_root>/<folder name>/`
   - `evals/files/backlog/<flow>/` → `<backlog_root>/<flow>/`
4. Run the `query` in a new session, answer follow-up questions as the scenario says, then grade the result against every `expected_behavior` line.
5. Try every model the team uses, and run each scenario at least twice. If results differ a lot between runs, the rule is not clear enough yet.

## With skill-creator

`evals/evals.json` follows the skill-creator format. skill-creator looks for it inside the skill folder, which this repo keeps free of test files, so copy or link `evals/` next to `skills/scrum-spec/SKILL.md` in a scratch checkout before running it. See its documentation for the commands.
