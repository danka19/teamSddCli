# Context

This is the active glossary and domain-boundary file for teamSddCli.

## Canonical Terms

| Term | Meaning | Notes |
|---|---|---|
| SDD | Spec-driven development workflow where requirements, design, tasks, tests, and traceability are driven from structured spec artifacts. | In this project the SDD workflow is OpenSpec/Markdown-first. |
| OpenSpec/Markdown-first | Architecture choice where structured OpenSpec and Markdown files in Git are canonical. | Confluence is generated from this source, not edited as the source. |
| `team-specs` | Central repository expected to store requirements, OpenSpec changes, living specs, QA/AT plans, traceability, registry, templates, publishing config, and schemas. | It is described by the architecture document; this repository currently contains the CLI project foundation, not the real `team-specs` repo. |
| `sdd CLI` | Team-owned command-line process interface over OpenSpec, Git, Bitbucket, Jenkins, Jira/tracker, Confluence, and local AI tools. | It should automate workflow transitions, not replace OpenSpec CLI entirely. |
| Change package | Per-change folder under `team-specs/openspec/changes/<change-id>/` with metadata, proposal, design, tasks, spec deltas, QA artifacts, automation plan, and traceability. | Central process object. |
| Living specs | Accepted current requirements after a change is archived. | Updated from approved changes, not manually edited in generated Confluence blocks. |
| Traceability | Explicit links between requirement, scenario, dev task, QA task, test case, and automated test. | A change should not close while required links are missing without a waiver. |
| Role inbox | CLI view of relevant work for a role such as analyst, developer, QA, API AT, or mobile AT. | Local AI sessions do not monitor background state; `sdd inbox` does. |
| Context pack | Focused local bundle of relevant change/task/spec/design/test context prepared for a local AI tool. | One task or change should map to one context pack. |
| Waiver | Reviewed exception to a required artifact or verification rule with reason, evidence, and approver. | Not free text without owner/evidence. |
| Generated Confluence page | Readable publication built from OpenSpec/Markdown artifacts. | Comments are allowed; requirement edits must be moved back into Git/OpenSpec. |

## Boundary Rules

- Raw source artifacts such as specs, tracker exports, Confluence comments, repository metadata, and CI results must be preserved separately from derived values.
- Review-required proposals are not accepted decisions.
- LLM or heuristic output is proposal evidence only unless the project explicitly defines a reviewed acceptance workflow.
- Git/OpenSpec is the canonical engineering source; Confluence is a generated view.
- Jira or another tracker is workflow/status, not the source of product requirements.
- Bitbucket PRs are review/audit surfaces; Jenkins owns deterministic validation/automation gates.
- AI may draft proposals, checks, skeletons, and context packs; humans remain responsible for approve, merge, correctness, and final decisions.
- Avoid bidirectional synchronization between Confluence and Git unless a later accepted decision explicitly changes the architecture.
- Do not infer real corporate repository URLs, owners, credentials, Confluence spaces, Jira projects, or Jenkins jobs from examples in the architecture document.
