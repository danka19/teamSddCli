# Roadmap

This roadmap is the working development plan for teamSddCli. It is phase-level; detailed implementation plans belong in `docs/phases/`.

## Current Roadmap Validation

- Current phase: Phase 1 Discovery And Requirements.
- Planning from this roadmap alone is forbidden. Detailed phase plans must reconcile roadmap intent, current docs, current implementation, environment evidence, audit findings, and human decisions.
- `sdd CLI` behavior, SDD workflow requirements, proposed process changes, artifact contracts, and acceptance criteria belong in OpenSpec artifacts under `openspec/` when SDD applies.
- New ideas during active phase work must go through change intake before they alter scope or plans.
- Accepted architecture critique decisions from 2026-07-03 narrow the first MVP to a thin change flow before Jira, QA/AT, Confluence publication, and role inbox automation.
- Update this file when phase status, gates, or scope changes.

## Phase 0. Project Foundation

Status: complete.

Goal: prepare repository rules, documentation, environment notes, baseline product decisions, OpenSpec expectations, and verification habits from `sdd_final_architecture.md`.

Quality gate:

- `AGENTS.md`, docs map, roadmap, audit, verification checklist, and phase template exist.
- Secrets and private-data rules are clear.
- OpenSpec expectations and phase change-intake routing are documented.
- Another agent can continue without chat history.

## Phase 1. Discovery And Requirements

Status: in progress.

Goal: turn the architecture into concrete product requirements, user/role workflows, CLI command acceptance criteria, integration constraints, and OpenSpec artifacts.

Likely scope:

- Define accepted CLI personas: analyst, developer, QA, API AT, mobile AT, tech lead, CI owner, and product/business stakeholder.
- Decide the first supported repository topology and configuration format.
- Create initial OpenSpec specs for change lifecycle, artifact contracts, traceability, waiver behavior, and documentation governance.
- Define `thin change` and `full change package` modes, including which artifacts are required for each mode.
- Specify the Confluence feedback loop before implementing publication: responsible owner, service expectation, unresolved feedback, and accepted/rejected comment handling.
- Define the first pilot as a thin flow and explicitly keep Jira task automation, QA/AT proposal commands, Confluence publication, and role inboxes out of MVP unless re-scoped by the human owner.

Detailed plan:

- `docs/phases/PHASE_1_DISCOVERY_AND_REQUIREMENTS.md`

Current work:

- First deterministic artifact: `templates/change/`, `scripts/validate_change.py`, and `.pre-commit-config.yaml`, tracked by OpenSpec change `add-change-template-validation`.

## Phase 2. Architecture And Data Model

Status: not planned in detail yet.

Goal: define the first stable CLI architecture, core entities, storage boundaries, local state, schemas, and integration contracts.

Likely scope:

- Model `change.yaml`, `traceability.yaml`, owners registry, projects registry, quality policy, and local `~/.sdd` state.
- Decide implementation language/runtime for `sdd CLI`.
- Define adapters for OpenSpec CLI, Git, and PR creation first; defer Bitbucket/Jenkins/Confluence/Jira write integrations until the thin flow is stable.
- Define CLI mutation contracts: dry-run behavior, idempotency, machine-readable JSON output, and auditable action logs.
- Establish validation gates for thin Spec PR/archive first, then broaden to Code PR, QA PR, and AT PR gates in later work.

## Phase 3. First Usable Workflow

Status: not planned in detail yet.

Goal: implement the smallest end-to-end pilot flow that proves SDD automation value.

Likely scope:

- `sdd change new`
- `sdd change validate`
- `sdd change pr`
- `sdd change archive`
- Basic `traceability.yaml` validation.
- Supporting setup or doctor behavior only where required to make the thin flow usable.

Explicitly deferred from the first MVP:

- `sdd publish confluence --preview`
- `sdd tasks plan` / `sdd tasks create`
- `sdd qa propose`
- `sdd at propose`
- `sdd inbox`

## Phase 4. Hardening And Pilot Readiness

Status: not planned in detail yet.

Goal: improve reliability, safety, command usability, process operations, and acceptance evidence for pilot usage.

Likely scope:

- Waiver policy and evidence requirements.
- Confluence preview/final publication after the feedback loop contract is specified.
- Jira task planning/creation after thin change archive works.
- Role inbox hardening after task/status sources are stable.
- QA/AT proposal and skeleton generation after scenario and traceability contracts are validated.
- Drift detection for generated Confluence blocks.
- Bitbucket Code Insights or equivalent reporting.
- Read-only MCP exploration only after CLI/API flow is working.

## Phase Planning Rule

When a phase is too large for one iteration, create or update a detailed plan under `docs/phases/` before implementation starts. Follow `docs/phases/PHASE_PLAN_TEMPLATE.md`.
