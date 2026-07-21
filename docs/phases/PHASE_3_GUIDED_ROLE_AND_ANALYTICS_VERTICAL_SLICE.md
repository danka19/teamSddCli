# Phase 3. Guided Role And Analytics Vertical Slice

Status: in_progress.

## Goal

Deliver a local, deterministic, MCP-free P3 vertical slice that fails closed on unknown roles, requires trusted human acceptance bound to a shown spec revision, and persists/validates a sanitized typed analytics package with read-only previews.

## Inputs To Read

- `AGENTS.md`, `docs/README.md`, `docs/00_FILE_STRUCTURE.md`, `docs/ROADMAP.md`
- `docs/CURRENT_PROJECT_AUDIT.md`, `docs/AI_STEP_VERIFICATION_CHECKLIST.md`
- `docs/audits/GIGACODE_ROLE_ACCEPTANCE_AND_FRAMEWORK_READINESS_AUDIT_2026-07-21.md`
- `docs/DECISIONS.md` (`D-024`–`D-026`)
- `docs/planning/ANALYTIC_TEMPLATE_STRUCTURE_AND_MIGRATION_PLAN_2026-07-06.md`
- both active P3 changes under `openspec/changes/`

## OpenSpec And Acceptance Mapping

- Affected accepted requirements: `change-lifecycle`, `change-artifact-contracts`, `traceability-contract`.
- Active proposed changes: `harden-role-aware-guided-workflow`, `add-typed-analytics-artifact-framework`.
- Acceptance scenarios: unknown role blocks; Analyst has no implementation CTA; UI `Да` is rejected; trusted evidence is revision-bound; incomplete DoR blocks; valid typed fixtures preview locally; passive integrations never invoke external systems.
- Verification evidence: focused pytest, one final relevant pytest run, `openspec validate --all --strict`, roadmap/OpenSpec validation, `git diff --check`, and synthetic GigaCode/AI-disabled walkthrough.

## Change Intake

```text
Idea: Local end-to-end P3 role/acceptance and typed analytics vertical slice.
Source: Human request on 2026-07-21; D-024–D-026 and GigaCode readiness audit.
Type: bug_fix, scope_refinement, data_contract_change, verification_change, documentation_change.
Decision: adopt_now.
Reason: The audit identifies critical fail-open authority/evidence gaps and absent P3 artifacts; deferral would make the guided workflow unsafe and readiness unprovable.
Affected specs: change-lifecycle, change-artifact-contracts, traceability-contract; two new P3 changes.
Affected architecture: local process-package validators/templates/read-only previews only; no corporate integration boundary change.
Data contract impact: trusted acceptance event and seven typed YAML artifact contracts.
Verification impact: negative authority/evidence/readiness tests plus synthetic local walkthrough.
Status: in_progress.
```

## Work Items

### 3.1 Role-aware acceptance and readiness gate

Objective:

- Implement fail-closed role selection, trusted revision-bound acceptance, and DoR-preserving guided integrity validation.

Expected files/modules:

- guided catalog/schema/module, acceptance schema/template, integrity validator/summary, roles/read-pack/runbook, package registry, tests.

Verification:

- Focused guided and integrity pytest tests, catalog/runbook validator, synthetic negative/positive walkthrough.

Exit criteria:

- A route cannot offer an unauthorized CTA or begin implementation without valid role, readiness, trusted human event, and matching revision digest.

### 3.2 Typed analytics artifact framework

Objective:

- Add seven YAML artifact contracts, templates, deterministic validation, and local read-only preview with a sanitized example.

Expected files/modules:

- analytics schemas/templates/validator/preview, package registry, read-pack/roles, tests and synthetic fixture.

Verification:

- Focused analytics pytest tests and CLI preview for the sanitized fixture.

Exit criteria:

- Every artifact is schema/semantic validated, traceable, free of placeholders, and previewed without integrations or product payment screens.

### 3.3 Package and sandbox transfer

Objective:

- Version/package the reusable assets and update the sandbox only through the existing controlled mechanism without touching its dirty OpenSpec paths.

Verification:

- Source package tests, package update `check`/`update`, sandbox focused tests, and separate commits.

Exit criteria:

- Sandbox package equals the validated source candidate; its existing uncommitted `enforce-guided-process-integrity` deletions remain untouched.

## Phase Gate

- Local deterministic evidence is complete; no MCP/tool invocation, credential, live integration, product payment UI, or corporate adaptation is introduced. Human acceptance of the P3 changes remains a separate lifecycle decision.
