# Roadmap

This roadmap is the working development plan for teamSddCli. It is phase-level; detailed implementation plans belong in `docs/phases/`.

## Current Roadmap Validation

- Current phase: Phase 0 Project Foundation.
- Planning from this roadmap alone is forbidden. Detailed phase plans must reconcile roadmap intent, current docs, current implementation, environment evidence, audit findings, and human decisions.
- `sdd CLI` behavior, SDD workflow requirements, proposed process changes, artifact contracts, and acceptance criteria belong in OpenSpec artifacts under `openspec/` when SDD applies.
- New ideas during active phase work must go through change intake before they alter scope or plans.
- Update this file when phase status, gates, or scope changes.

## Phase 0. Project Foundation

Status: in progress.

Goal: prepare repository rules, documentation, environment notes, baseline product decisions, OpenSpec expectations, and verification habits from `sdd_final_architecture.md`.

Quality gate:

- `AGENTS.md`, docs map, roadmap, audit, verification checklist, and phase template exist.
- Secrets and private-data rules are clear.
- OpenSpec expectations and phase change-intake routing are documented.
- Another agent can continue without chat history.

## Phase 1. Discovery And Requirements

Status: not planned in detail yet.

Goal: turn the architecture into concrete product requirements, user/role workflows, CLI command acceptance criteria, integration constraints, and OpenSpec artifacts.

Likely scope:

- Define accepted CLI personas: analyst, developer, QA, API AT, mobile AT, tech lead, CI owner, and product/business stakeholder.
- Decide the first supported repository topology and configuration format.
- Create initial OpenSpec specs for documentation governance, change package lifecycle, traceability, and core CLI commands.
- Define what the first pilot must prove and what remains explicitly out of scope.

## Phase 2. Architecture And Data Model

Status: not planned in detail yet.

Goal: define the first stable CLI architecture, core entities, storage boundaries, local state, schemas, and integration contracts.

Likely scope:

- Model `change.yaml`, `traceability.yaml`, owners registry, projects registry, quality policy, and local `~/.sdd` state.
- Decide implementation language/runtime for `sdd CLI`.
- Define adapters for OpenSpec CLI, Git, Bitbucket, Jenkins, Confluence, Jira/tracker, and optional local AI context-pack generation.
- Establish validation gates for Spec PR, Code PR, QA PR, and AT PR.

## Phase 3. First Usable Workflow

Status: not planned in detail yet.

Goal: implement the smallest end-to-end pilot flow that proves SDD automation value.

Likely scope:

- `sdd init`
- `sdd doctor`
- `sdd change new`
- `sdd change validate`
- `sdd change pr`
- `sdd publish confluence --preview`
- `sdd tasks plan` or `sdd tasks create`
- `sdd inbox`

## Phase 4. Hardening And Pilot Readiness

Status: not planned in detail yet.

Goal: improve reliability, safety, command usability, process operations, and acceptance evidence for pilot usage.

Likely scope:

- Waiver policy and evidence requirements.
- Drift detection for generated Confluence blocks.
- Role inbox hardening.
- QA/AT proposal and skeleton generation.
- Bitbucket Code Insights or equivalent reporting.
- Read-only MCP exploration only after CLI/API flow is working.

## Phase Planning Rule

When a phase is too large for one iteration, create or update a detailed plan under `docs/phases/` before implementation starts. Follow `docs/phases/PHASE_PLAN_TEMPLATE.md`.
