<!-- scrum-spec config -->
# scrum-spec config

version: 1
docs_root: docs/sprint
backlog_root: docs/backlog
glossary_root: docs/glossary
domain_source: src/*
code_roots: ., ../room-api
project_rules: AGENTS.md
definition_of_done: –
api: yes
api_spec: ../room-api/docs/openapi.yaml
ac_owner: PO
api_owner: BE
tester: QA
layers: FE, BE
task_prefixes: FE, BE, INT, TEST
estimation: points per task
review_term: MR
board: Figma (sections 0–4 of the ticket board)
design_source: Figma
input_sources: ticket text, PDF exported from FigJam
personas: src/test/personas.ts
ticket_format: <ticket-id>-<short-name> in lowercase joined by -, e.g. demo-room-booking
aliases: –

## Roles

| Name | slug | Answers about | Questionnaire |
|---|---|---|---|
| PO | po | scope, order, confirming AC, wording | ✅ |
| BA | ba | flow detail, business rules, data | ✅ |
| BE | be | API, server-side permissions | ✅ |
| UX | ux | design, mobile | ✅ |
| QA | qa | test cases, edge cases | ❌ |
| Team | team | decisions inside the team | ❌ |
