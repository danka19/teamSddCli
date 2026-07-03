# teamSddCli

## Summary

teamSddCli is a local SDD automation project for a team workflow based on OpenSpec/Markdown, Git, Bitbucket, Jenkins, Confluence, Jira or another task tracker, local CLI commands, and local AI tools.

The project goal is to automate the end-to-end transition from analysis to development tasks, QA test cases, automated-test skeletons, verification, and archived living specs without introducing one centralized autonomous agent.

Current checkpoint:

> Project foundation from `sdd_final_architecture.md` is being converted into durable repository documentation. No implementation source code or executable CLI is present yet.

## Scope

In scope:

- OpenSpec/Markdown-first workflow where Git/OpenSpec is the canonical engineering source.
- `sdd CLI` process commands for change creation, validation, PR support, publication, task planning, QA/AT proposals, role inboxes, AI context packs, and archiving.
- Integration boundaries for Bitbucket, Jenkins, Confluence, Jira or an equivalent tracker, code repositories, QA repositories, and AT repositories.
- Change packages with proposal, design, tasks, spec deltas, QA plans, test cases, automation plans, and traceability.
- Local AI support for drafts, reviews, context packs, and test or automation skeletons.
- Phase-based delivery of a minimal pilot, task automation, QA/AT automation, and process hardening.

Out of scope:

- Treating Confluence as the editable source of truth for requirements.
- Bidirectional Git/Confluence synchronization.
- Letting AI approve, merge, own process state, or replace human accountability.
- Building a centralized background autonomous agent as the first architecture.
- Assuming concrete corporate credentials, project owners, repository URLs, or production deployment details before they are verified.

## Key Decisions

- 2026-07-03: Use the existing `sdd_final_architecture.md` as the initial project source document.
- 2026-07-03: Use OpenSpec/Markdown in Git as the canonical source and Confluence as a generated publication layer.
- 2026-07-03: Automate artifact state transitions through CLI/CI rather than centralizing control in one autonomous agent.
- 2026-07-03: Keep human ownership over approvals, merges, business decisions, correctness, and review outcomes.
- 2026-07-03: Use this starter-kit documentation set as the durable operating system for future Codex work.
- 2026-07-03: Narrow the first implemented MVP to a thin change flow: `sdd change new`, `sdd change validate`, `sdd change pr`, `sdd change archive`, and basic `traceability.yaml`; Jira task automation, QA/AT proposal commands, Confluence publication, and role inboxes are later layers unless explicitly re-scoped.
- 2026-07-03: Support two change modes in future requirements: a lightweight `thin change` path for small bugfix/refactor/small behavior patches and a `full change package` path for feature, API, mobile, cross-repo, or high-risk changes.
- 2026-07-03: The first product OpenSpec specs should focus on change lifecycle, artifact contracts, traceability, and waiver behavior before broad CLI/integration coverage.
- 2026-07-03: Confluence feedback handling must be explicitly specified before implementation: owner, service expectation, unresolved-feedback handling, and how comments become accepted deltas or rejected notes.
- 2026-07-03: Future mutating CLI/integration commands should be designed with dry-run behavior, idempotency, machine-readable JSON output, and auditable action logs.
- 2026-07-03: Gherkin is not mandatory for every QA artifact; every requirement needs at least a testable scenario, while Gherkin should be required only when a scenario is executable or exported to AT.

## Source Architecture

The initial product architecture is documented in `sdd_final_architecture.md`.

A recorded critique of that architecture, with evaluation criteria, external comparison, recommendations (REC-001..REC-007), and alternative lightweight solution paths, lives in `docs/audits/ARCHITECTURE_CRITIQUE_2026-07-03.md`. Its recommendations are proposed planning inputs; only items already listed under Key Decisions are accepted.

Important concepts from that document:

- Canonical source: `team-specs` repository with `openspec/` artifacts.
- Publication: generated Confluence pages from Markdown/OpenSpec.
- Review and audit: Bitbucket PRs with reviewer assignment from owners registry.
- Validation and automation: Jenkins pipelines.
- Workflow status: Jira or another task tracker.
- Local process interface: `sdd CLI`.
- Traceability path: requirement -> scenario -> dev task -> test case -> automated test.
- Minimal pilot: `team-specs`, OpenSpec CLI, core `sdd` commands, Jenkins Spec PR pipeline, Bitbucket reviewer assignment, Confluence preview, Jira task creation, and `traceability.yaml`.

## First Valuable Outcome

The first useful delivery should prove the smallest thin SDD change flow at pilot scale:

1. Create a change package from templates.
2. Validate structure, policy, and basic traceability locally.
3. Create a Spec PR.
4. Archive the completed change into living specs.
5. Preserve enough traceability to show requirement -> scenario -> change evidence.

Confluence publication, Jira task creation, QA/AT proposal generation, and role inboxes remain important, but they are not required for the first MVP unless the human owner explicitly re-scopes the pilot.

## Documentation Rules

- `AGENTS.md` is the canonical agent operating guide.
- `docs/00_FILE_STRUCTURE.md` is the repository map and must be updated when files or folders are added.
- `docs/CURRENT_PROJECT_AUDIT.md` is an active planning input and must be updated when findings are fixed or invalidated by evidence.
- Detailed phase plans live under `docs/phases/` and must use `docs/phases/PHASE_PLAN_TEMPLATE.md`.
- New human feedback that affects `sdd CLI` behavior, safety, command usability, SDD workflow, acceptance, or verification must be persisted in the correct durable document.
