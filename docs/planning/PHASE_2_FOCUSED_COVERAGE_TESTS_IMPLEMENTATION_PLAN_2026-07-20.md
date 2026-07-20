# Phase 2 Focused Coverage Tests Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Record the accepted first-MVP integration boundary and close the four residual selectors whose underlying template or topology behavior already exists but lacks an exact test.

**Architecture:** This is an evidence-only successor-source change. Tests inspect the canonical templates, bootstrap output, and central/project topology boundaries directly; no production behavior or schema is added. `SCENARIO_COVERAGE` remains source-owned beside each exercising test, and `evidence-manifest.yaml` changes from gap metadata to exact pytest/manual references only after the focused tests pass.

**Tech Stack:** Python 3, pytest, PyYAML, existing process-package helpers, OpenSpec 1.4.1.

## Global Constraints

- Do not modify `process/release/` or any immutable `phase-2-14-rc4` evidence.
- Do not weaken a test to make an unimplemented invariant pass; reclassify the selector as a product gap if existing behavior does not satisfy it.
- Do not change accepted OpenSpec behavior, schemas, public CLI behavior, or package data contracts in this bounded change.
- Keep all examples synthetic and free of corporate values or secrets.
- A new release claim requires a successor candidate and candidate-bound certification; this plan does not freeze one.

---

### Task 1: Bind the accepted first-MVP boundary

**Files:**
- Modify: `docs/DECISIONS.md`
- Modify: `docs/phases/PHASE_2_TRANSFER_READY_PROCESS_PACKAGE.md`
- Modify: `process/certification/evidence-manifest.yaml`
- Test: `tests/test_certification.py`

**Interfaces:**
- Consumes: human direction dated 2026-07-20 and transfer-readiness scenario `Later integrations do not block transfer readiness`.
- Produces: decision `D-019` and `manual:docs/DECISIONS.md` coverage evidence.

- [ ] Change the coverage regression expectation from one human-boundary gap to no human-boundary gap and from `284/18/32` to `285/17/32`.
- [ ] Run `python -m pytest tests/test_certification.py::test_residual_gap_review_routes_later_phases_and_governance_exactly -q`; expect failure because the manifest still contains the gap.
- [ ] Replace only that selector's gap record with `manual:docs/DECISIONS.md`.
- [ ] Re-run the focused test; expect pass.

### Task 2: Add exact artifact-height tests

**Files:**
- Modify: `tests/test_validate_change.py`
- Modify: `process/certification/evidence-manifest.yaml`
- Test: `tests/test_validate_change.py`

**Interfaces:**
- Consumes: `templates/change/proposal.md`, `templates/change/tasks.md`, `process/templates/change/proposal.md`, and `process/templates/change/tasks.md`.
- Produces: `test_proposal_templates_stay_business_and_scope_focused` and `test_task_templates_are_executable_and_parseable`.

- [ ] Point both selectors at the named, not-yet-existing pytest nodes and run the coverage regression; expect `coverage.unknown-pytest`.
- [ ] Add the two tests. Proposal assertions allow only business/scope/acceptance headings and reject implementation/code fences. Task assertions require unique stable `TASK-*` IDs, unchecked Markdown task syntax, and substantive action text in both canonical templates.
- [ ] Add exact accepted-spec selector rows to the local `SCENARIO_COVERAGE` mapping.
- [ ] Run the two pytest nodes and the coverage regression; expect pass.

### Task 3: Add exact distribution and repository-split tests

**Files:**
- Modify: `tests/test_packaged_flow.py`
- Modify: `tests/test_process_package.py`
- Modify: `process/certification/evidence-manifest.yaml`
- Test: `tests/test_packaged_flow.py`, `tests/test_process_package.py`

**Interfaces:**
- Consumes: `bootstrap_team_specs`, `templates/team-specs/sdd.config.yaml`, `templates/team-specs/projects.yaml`, and `templates/project-adapter/.sdd-project.yaml`.
- Produces: `test_bootstrap_reuses_one_versioned_package_without_policy_fork` and `test_central_specs_and_project_implementation_truth_stay_separate`.

- [ ] Point both selectors at the named, not-yet-existing pytest nodes and run the coverage regression; expect `coverage.unknown-pytest`.
- [ ] Add a bootstrap test that proves one sibling `process` package is referenced by `team-specs`, while no copied policy/process tree appears under canonical team-specs.
- [ ] Add a topology test that proves central canonical paths contain spec/evidence surfaces, repository records and adapters own `src`/`tests`, and no implementation root becomes a central canonical path.
- [ ] Add exact accepted-spec selector rows to the local `SCENARIO_COVERAGE` mappings.
- [ ] Run the two pytest nodes and the coverage regression; expect pass.

### Task 4: Reconcile evidence and verify the bounded change

**Files:**
- Modify: `docs/audits/PHASE_2_RESIDUAL_GAP_SELECTOR_REVIEW_2026-07-20.md`
- Modify: `docs/ROADMAP.md`
- Modify: `docs/CURRENT_PROJECT_AUDIT.md`
- Modify: `docs/phases/PHASE_2_EVIDENCE_INDEX.md`
- Modify: `docs/phases/PHASE_2_TRANSFER_READY_PROCESS_PACKAGE.md`

**Interfaces:**
- Consumes: four passing pytest nodes plus `D-019`.
- Produces: working-source coverage `289 covered / 13 gaps / 32 future_work`, with all remaining gaps routed to product OpenSpec intake.

- [ ] Update the dated audit without rewriting its historical review result: append the accepted boundary and focused-test remediation outcome.
- [ ] Update current roadmap/audit/evidence summaries while keeping rc4 at `204/110/20` and the successor source explicitly uncertified.
- [ ] Run the four focused nodes, certification coverage test, changed-file suite, full pytest suite, `openspec validate --all --strict`, and roadmap/OpenSpec validator.
- [ ] Require `git diff --check` and an empty diff under `process/release/`.
- [ ] Commit the bounded implementation separately from the later product-gap intake.

## Self-review

- Spec coverage: all four focused selectors and the separate human boundary selector have an exact task and evidence target.
- Placeholder scan: no `TBD`, `TODO`, or unspecified implementation step remains.
- Type consistency: all named test nodes are exact Python function names and all evidence references use the existing `pytest:` or `manual:` contract.
- Scope: no product-gap behavior is implemented here; six product groups remain for the next `phase-change-intake` step.
