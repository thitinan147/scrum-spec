# scrum-spec

**Let your coding agent draft the spec documents a Scrum team shares, from a story map to a tester handoff, while every decision stays with a person.**

`scrum-spec` is an [Agent Skill](https://agentskills.io/) that removes the waiting in Scrum: the PO gets a draft of the stories and acceptance criteria instead of a blank page, dev get AC with the code they touch already found, and the tester gets test steps on the first day of the Sprint. Everything for one story lives in one `spec.md`.

*The AI proposes. People decide.*

## Why

- **Nothing is guessed.** Every statement is a fact with a source, a proposal marked as one, or a question in the Questions table, addressed to a role.
- **Every decision has a name on it.** Decisions and the AC approval record a person and a date. A script fails any approval or decision given by an AI.
- **Facts come from the code.** Before asking, the skill reads your repos. People are asked only for decisions.
- **No one has to run the skill to answer.** The PO writes in the Answer column or edits the approve line; the next run records it.
- **Small.** Three commands, one file per story, no required config, and one run loads at most 1,500 words of instructions.

## Install

Pick **one** method. Installing both gives you the skill twice.

**Any agent (Claude Code, Codex, Cursor, ...)** with [skills.sh](https://skills.sh/) (not tested yet; please report how it goes):

```bash
# Pin a release so later changes cannot reach you unreviewed (recommended)
npx skills add thitinan147/scrum-spec#v0.3.0

# Or follow the default branch
npx skills add thitinan147/scrum-spec
```

Add `-g` to install for all your projects instead of the current one.

**Claude Code plugin:**

```text
# Pinned to a release (recommended)
/plugin marketplace add thitinan147/scrum-spec#v0.3.0
/plugin install scrum-spec@scrum-spec
```

Installed as a plugin, the command is `/scrum-spec:scrum-spec` instead of `/scrum-spec`.

You need Python 3.10+ and git. To read large PDFs exported from a board, also install poppler (macOS: `brew install poppler` · Debian/Ubuntu: `poppler-utils`).

## Quick start

```text
/scrum-spec ac rb-12-book-room     then paste the card's text, or a path to a PDF or image
/scrum-spec handoff rb-12-book-room  once no question blocks the AC
/scrum-spec split room-booking     optional: a whole flow → a story map and one folder per story
/scrum-spec help
```

The skill runs only when you type the command. It writes `scrum-spec/<work>/spec.md` and asks questions as it goes.

| Command | What it writes in `spec.md` | Who decides |
|---|---|---|
| `split` | `map.md`: steps, vertical-slice stories, what is not now | PO confirms stories and order |
| `ac` | Story, Rules, Acceptance Criteria, Questions (with a short ambiguity review) | PO answers and approves AC |
| `handoff` | Test steps, accounts, data, what not to report, risky areas | The tester starts writing tests |

Headings and table columns stay in English because the checker reads them. The text follows the language of your input, so a team that writes in Thai gets its documents in Thai.

The [guide](docs/guide.md) covers the principles, the file layout, the checker and how to measure whether it helps.

## Platform support

| | Status |
|---|---|
| Claude Code on macOS | v0.1 tested with the plugin from a local path; v0.3 not tested end to end yet |
| Claude Code on Linux | Expected to work, not tested yet |
| Codex, Cursor and other Agent Skills clients | Expected to work, not tested yet. The human-only rule relies on `agents/openai.yaml` (Codex) and the description prefix (others) |
| Windows | Not tested. Use WSL |

## Security

The skill reads your repos and writes Markdown into the project. `check.py` reads files only, runs no commands and makes no network calls. See [SECURITY.md](SECURITY.md).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Run the tests with `python3 -m unittest discover -s tests`.

## License

[MIT](LICENSE)
