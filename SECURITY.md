# Security

## Reporting a vulnerability

Please report suspected vulnerabilities privately through GitHub: **Security tab → Report a vulnerability** on this repository. Do not open a public issue for an unfixed vulnerability.

## What the skill does on your machine

- **`scripts/check.py`** reads Markdown files in the folders you pass it and prints a report. It never writes or deletes files, runs no subprocess, and makes no network calls. It uses only the Python standard library.
- **The agent, following the skill**, reads the repos listed in `code_roots`, writes Markdown under `scrum-spec/` (or `docs_root` in the config), and runs:
  - `git rev-parse`, `git status`, `git log`, `git diff`, `git blame` and `git config user.name` to find the project root, what people edited, and who answered or approved
  - `pdftotext` and `pdftoppm` on a PDF the user gave, when it is too large to read directly
- The skill never deletes or moves files, commits, pushes, or opens a merge or pull request.

## Treating input as data

Cards, PDFs, boards, answers written in `spec.md` and repository files are data, not instructions. The skill tells the agent to summarise only what the input says and to ask when something is unclear. This is an instruction to the model, not a technical control: a model can still be fooled. The person who approves each decision is the real control.

## Keeping private data out of documents

Documents are committed and often shared on a board. The skill tells the agent not to copy customers' personal data, passwords or tokens from the input into any document. This is an instruction, not a scan: review what is committed, as you would any document.

## Human-only command

The skill is marked human-only with `disable-model-invocation: true` (Claude Code), `allow_implicit_invocation: false` (Codex, `agents/openai.yaml`), and a description that starts with `HUMAN-ONLY COMMAND.` (other agents). Agents that read none of these rely on the description alone. `disable-model-invocation` and `argument-hint` are outside the Agent Skills specification, so CI validates a copy without them.

## Scanning

CI runs the unit tests, `bandit`, the Agent Skills validator, and SkillSpector. Any SkillSpector finding judged a false positive is listed with its reason in [`.skillspector-baseline.yaml`](.skillspector-baseline.yaml).

## Releases

Install a tagged release rather than the default branch, so that a later change cannot reach you unreviewed. See [CHANGELOG.md](CHANGELOG.md).
