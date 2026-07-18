# Phase 2.13 Corporate Adaptation Package Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build deterministic, non-secret corporate-adaptation and pilot templates that Phase 3 can populate without inventing reusable behavior or forking the external OpenSpec workflow.

**Architecture:** Add four closed JSON Schema contracts and one validation module for environment inventory, configuration/pilot-entry checklists, pilot evidence, and no-fork assessments. Ship blank templates plus one fully synthetic pilot example inside the versioned process package, expose a check-only JSON-capable CLI, and keep real values outside the repository. Schema validation owns structure; semantic checks own secret/privacy rejection, pilot readiness, and reusable-gap routing.

**Tech Stack:** Python 3.11+, PyYAML, jsonschema Draft 2020-12, pytest, JSON Schema, YAML, OpenSpec 1.4.1.

## Global Constraints

- This work creates templates and synthetic fixtures, not real corporate configuration or pilot evidence.
- No model execution is required or permitted as acceptance evidence for 2.13.
- Inline secrets, private values, production URLs, internal repository exports, real owners, and real project identifiers must not enter the release package.
- Unknown environment facts remain explicit as `unresolved`; they are never inferred from examples.
- Reusable gaps route to the external canonical OpenSpec workflow; internal process-package forks are rejected.
- AI-disabled deterministic gates, rollback/hold, and human decisions remain mandatory.
- The existing immutable `phase-2-12-rc7` evidence is historical and must not be rewritten.

---

### Task 1: Environment Inventory Contract

**Files:**
- Create: `process/schemas/corporate-environment-inventory.schema.json`
- Create: `process/templates/corporate-adaptation/environment-inventory.yaml`
- Create: `tests/fixtures/corporate-adaptation/valid/environment-inventory.yaml`
- Create: `tests/fixtures/corporate-adaptation/invalid/environment-inventory-missing-mcp.yaml`
- Create: `tests/test_corporate_adaptation.py`

**Interfaces:**
- Produces schema id `corporate-environment-inventory.schema.json` and template kind `environment-inventory`.
- Covers OS/shell/runtime, Git/OpenSpec, package distribution, network, Bitbucket/Jenkins/Jira/Confluence, MCP, and AI model/adapter availability.

- [x] Write a failing test that loads the inventory template, validates its exact required sections, and rejects the fixture without MCP inventory.
- [x] Run `python -m pytest tests/test_corporate_adaptation.py -k environment_inventory -v` and confirm failure because the schema/template do not exist.
- [x] Add the closed schema and non-secret unresolved template.
- [x] Re-run the focused test and confirm it passes.

### Task 2: Configuration And Pilot-Entry Contracts

**Files:**
- Create: `process/schemas/corporate-adaptation-checklist.schema.json`
- Create: `process/templates/corporate-adaptation/configuration-checklist.yaml`
- Create: `process/templates/corporate-adaptation/pilot-entry-checklist.yaml`
- Create: `tests/fixtures/corporate-adaptation/valid/configuration-checklist.yaml`
- Create: `tests/fixtures/corporate-adaptation/valid/pilot-entry-checklist.yaml`
- Create: `tests/fixtures/corporate-adaptation/invalid/configuration-inline-secret.yaml`
- Create: `tests/fixtures/corporate-adaptation/invalid/pilot-entry-missing-fallback.yaml`

**Interfaces:**
- Produces one conditional schema for `configuration` and `pilot-entry` checklist kinds.
- Requires installed-package evidence, project/owner mappings, approved secret references, integration wiring, rollback, external acceptance, privacy, and AI-disabled fallback as applicable.

- [x] Add failing positive/negative tests for both checklist kinds, mandatory fields, and inline-secret rejection.
- [x] Run `python -m pytest tests/test_corporate_adaptation.py -k checklist -v` and confirm the intended missing-contract failures.
- [x] Add the checklist schema, templates, and fixtures with `verified | unresolved | not-applicable` evidence states.
- [x] Re-run the focused tests and confirm they pass.

### Task 3: Pilot Evidence Contract And Synthetic Example

**Files:**
- Create: `process/schemas/corporate-pilot-evidence.schema.json`
- Create: `process/templates/corporate-adaptation/pilot-evidence.yaml`
- Create: `process/examples/corporate-adaptation/pilot-evidence-synthetic.yaml`
- Create: `tests/fixtures/corporate-adaptation/invalid/pilot-evidence-missing-human-decisions.yaml`

**Interfaces:**
- Produces template kind `pilot-evidence` and one `evidence_kind: synthetic-example` instance.
- Records selection/class rationale, change/requirement/scenario IDs, DoR/DoD/release evidence, PR/tests, decisions, installed adapters/runtime, failures/interventions/deviations, privacy, rollback/hold, and follow-up changes.

- [x] Add a failing test that validates the blank template and complete synthetic example and rejects missing human decisions.
- [x] Run `python -m pytest tests/test_corporate_adaptation.py -k pilot_evidence -v` and confirm failure because the contract is absent.
- [x] Add the closed schema, blank template, synthetic example, and negative fixture.
- [x] Re-run the focused tests and confirm they pass.

### Task 4: No-Fork Contract And Validator

**Files:**
- Create: `process/schemas/corporate-no-fork-assessment.schema.json`
- Create: `process/templates/corporate-adaptation/no-fork-assessment.yaml`
- Create: `process/examples/corporate-adaptation/no-fork-routed-synthetic.yaml`
- Create: `tests/fixtures/corporate-adaptation/invalid/no-fork-internal-reusable-change.yaml`
- Create: `process/corporate_adaptation.py`
- Create: `scripts/validate_corporate_adaptation.py`

**Interfaces:**
- Produces `validate_document(document, kind, process_root, external_package=False)` and `validate_package_templates(process_root)`.
- Emits stable diagnostics for schema errors, inline secrets, private external-package values, unready pilot entry, and reusable findings not routed to an external OpenSpec change.

- [x] Add failing contract tests for routed reusable gaps, forbidden internal forks, privacy detection, deterministic JSON output, and no file mutation.
- [x] Run `python -m pytest tests/test_corporate_adaptation.py -k "no_fork or privacy or cli" -v` and confirm the intended missing-validator failures.
- [x] Implement the minimal pure validator and check-only CLI, reusing `secret_diagnostics` for credential detection.
- [x] Re-run the focused tests and confirm they pass.

### Task 5: Package Integration And Documentation

**Files:**
- Modify: `process/package.yaml`
- Modify: `process/release-allowlist.yaml`
- Modify: `process/release_candidate.py`
- Create: `docs/runbooks/CORPORATE_ADAPTATION_AND_PILOT.md`
- Modify: `docs/00_FILE_STRUCTURE.md`
- Modify: `docs/phases/PHASE_2_EVIDENCE_INDEX.md`
- Modify: `docs/CURRENT_PROJECT_AUDIT.md`
- Modify: `openspec/changes/define-transfer-ready-process-package/tasks.md`

**Interfaces:**
- Registers all four schemas, template/example roots, CLI, and runbook in the versioned release contract.
- Maps tests to the Corporate adaptation boundary, Corporate pilot entry and acceptance, and Release evidence and auditability scenarios.

- [x] Add failing package-closure and public-CLI smoke tests before updating package metadata/allowlist.
- [x] Run the focused package tests and confirm failures identify the missing registered assets.
- [x] Register the new assets, write the runbook, and update durable status/evidence documents without changing `phase-2-12-rc7`.
- [x] Run `python -m pytest tests/test_corporate_adaptation.py tests/test_process_package.py tests/test_release_candidate.py -v` and confirm the integrated slice passes.

### Task 6: Combined Verification And Final Review

**Files:**
- Modify after review only: files with accepted batch findings.
- Modify at closure: `docs/phases/PHASE_2_TRANSFER_READY_PROCESS_PACKAGE.md`, `docs/ROADMAP.md`, `docs/README.md`, `docs/CURRENT_PROJECT_AUDIT.md`, and `openspec/changes/define-transfer-ready-process-package/tasks.md` as required by verified status.

**Interfaces:**
- Produces one combined completion gate and one final independent reviewer report.

- [x] Run the corporate-adaptation focused suite, schema/template package validation, privacy scan, and representative CLI positive/negative fixtures.
- [x] Run the complete pytest suite, strict OpenSpec validation, roadmap/OpenSpec validator, whitespace check, and `git diff --check`.
- [x] Dispatch exactly one final reviewer after implementation stabilizes; collect all actionable findings before changing files.
- [x] Apply accepted reviewer fixes in one batch and repeat focused plus affected full checks once.
- [x] Re-run phase-status-audit, set 2.13 `closed` only with complete evidence, update tasks 6.1-6.4, and create one intentional commit.
