# scrum-spec

**Let your coding agent draft the spec documents a Scrum team shares, from a story map to a tester handoff, while every decision stays with a person.**

`scrum-spec` is an [Agent Skill](https://agentskills.io/) that writes a team's shared spec docs one step at a time: split a flow into stories, draft rules and acceptance criteria, propose a Sprint Goal, review the spec, design the API contract, break work into tasks, and share the test plan with the tester. At Sprint end it keeps what future work needs in a glossary and deletes the rest.

*The AI proposes. People decide.*

## Why

- **Nothing is guessed.** Every statement in a document is a fact with a source (a path or a decision number), a proposal marked as one, or an open question `[ask: … · <role>]`.
- **Every decision has a name on it.** Decisions, "To decide" results and `**approve:**` lines record `<name> (<role>) · <date>`. An AI can never be the one who decided, and a script checks it.
- **Facts come from the code.** Before asking, the skill searches your repos, API spec and fixtures. People are asked only for decisions and for what is not in the repo.
- **A script checks every document.** [`check.py`](skills/scrum-spec/scripts/check.py) fails on broken tables, cited paths that do not exist, references to decisions or AC that do not exist, approvals without a person, and summary counts that drift from their tables.
- **Plain files in your repo.** Everything lives under `scrum-spec/` as Markdown. No service, no account, no dependencies beyond `git` and Python.

## Install

Pick **one** method. Installing both gives you the skill twice.

**Any agent (Claude Code, Codex, Cursor, ...)** with [skills.sh](https://skills.sh/) (not tested yet; please report how it goes):

```bash
# Pin a release so later changes cannot reach you unreviewed (recommended)
npx skills add thitinan147/scrum-spec#v0.1.0

# Or follow the default branch
npx skills add thitinan147/scrum-spec
```

Add `-g` to install for all your projects instead of the current one.

**Claude Code plugin:**

```text
# Pinned to a release (recommended)
/plugin marketplace add thitinan147/scrum-spec#v0.1.0
/plugin install scrum-spec@scrum-spec
```

Installed as a plugin, the command is `/scrum-spec:scrum-spec` instead of `/scrum-spec`.

You need Python 3.9+ and git. To read large PDFs exported from a board, also install poppler (macOS: `brew install poppler` · Debian/Ubuntu: `poppler-utils`).

## Quick start

```text
/scrum-spec setup                               create scrum-spec/config.md (guesses from your repo, asks the rest)
/scrum-spec refine-intake ticket=abc-123-book   then paste the card's text, or a path to a PDF or image
/scrum-spec                                     run the next step of the work in progress
/scrum-spec status                              where every piece of work is, what blocks it, what to do next
/scrum-spec help                                short usage with input forms and examples
```

The skill runs only when you type the command. It writes files into your repo and asks questions as it goes, so the model never starts it by itself.

## Three ways in

| You have | Start with | Goes to |
|---|---|---|
| A whole board or flow, not yet split | `refine-split flow=<flow>` (step 0) | `<backlog_root>/<flow>/<story>/` per story |
| A single card in the backlog, not in a Sprint yet | `refine-intake` (step 1) | `<backlog_root>/<card>/` |
| A card already in the Sprint | `refine-intake ticket=<ticket>` (step 1) | `<docs_root>/<ticket>/` |

Backlog work enters the Sprint through `plan-goal`, which moves the folders with `git mv` after the team confirms.

## How it works

| # | Command | What it does | Who confirms |
|---|---|---|---|
| 0 | `refine-split` | Splits a whole flow into vertical-slice stories on a story map | Product Owner confirms stories, slices and order |
| 1 | `refine-intake` | Summarises one card or bug and picks a track | Product Owner confirms scope |
| 2 | `refine-ac` | Drafts rules and acceptance criteria | Product Owner confirms AC |
| – | `plan-goal` | Proposes a Sprint Goal, shows each item's readiness, moves chosen stories into the Sprint | Product Owner picks the Goal · dev pick the items |
| 3 | `plan-review` | Finds ambiguity in the spec, including the tester's view | The roles asked |
| 4 | `plan-design` | Drafts the technical design and API contract | API owner confirms the API · team reviews the design |
| 5 | `plan-tasks` | Breaks work into tasks per the Definition of Done and says how ready it is to start | Dev approve the breakdown, add Owner and Estimate |
| 6 | `sprint-handoff` | Shares the test plan (personas, test data, steps, risks) | Sent to the tester |
| 7 | `sprint-close` | Checks the DoD, keeps what future work needs in the glossary, deletes finished folders | Team confirms before anything is deleted |

Each ticket follows one track:

| Track | Steps | Use when |
|---|---|---|
| small (default) | 1 → 2 → 5 → 6 | Most work, including a new screen on an existing API |
| large | 1 → 2 → 3 → 4 → 5 → 6 | A new or changed API must be agreed before coding, or the scope is unclear |
| bug | 1 → 2 → 5 → 6 | Behavior does not match what was agreed, or it worked and broke |

Markers, headings and table columns are always English, because the checker reads them. The text the skill drafts follows the language of your input, so a team that writes in Thai, Japanese or Spanish gets its documents in that language.

The [guide](docs/guide.md) covers the principles, where each result lives, the checker, and how to measure whether the skill helps your team.

## Platform support

| | Status |
|---|---|
| Claude Code on macOS | Tested with the plugin installed from a local path: `help`, `status` and `refine-intake` |
| Claude Code on Linux | Expected to work, not tested yet |
| Codex, Cursor and other Agent Skills clients | Expected to work, not tested yet. The human-only rule relies on `agents/openai.yaml` (Codex) and the description prefix (others) |
| Windows | Not tested. Use WSL |

## Security

The skill reads your repos and writes Markdown into the project. `check.py` reads files only, runs no commands and makes no network calls. See [SECURITY.md](SECURITY.md).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Run the tests with `python3 -m unittest discover -s tests`.

## License

[MIT](LICENSE)
