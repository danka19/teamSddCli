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
- the active analytics change under `openspec/changes/` and the archived role-aware/operation-catalog P3 change packages under `openspec/changes/archive/`

## OpenSpec And Acceptance Mapping

- Affected accepted requirements: `change-lifecycle`, `change-artifact-contracts`, `traceability-contract`.
- Active proposed change: `add-typed-analytics-artifact-framework`. The role-aware workflow and operation catalog/dispatcher requirements are accepted living specs.
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
State detail: role-aware and operation-catalog work is accepted, while the active analytics change awaits human acceptance.
```

## Work Items

### 3.1 Role-aware acceptance and readiness gate

Status: accepted.

OpenSpec mapping: archived `openspec/changes/archive/2026-07-23-harden-role-aware-guided-workflow/`; accepted spec `role-aware-guided-workflow`.

Progress evidence:

- [x] Fail-closed interactive role policy and readiness-validation baseline are implemented and transferred in package `0.3.4`.
- [x] Implement the human decision-card and confirmation-event contract documented in the archived accepted change; the record remains non-authoritative and bound to the shown change and revision.
- [x] Implement proactive discovery recommendations and their negative transcript checks; silence remains unresolved.
- [x] Add the non-authoritative operation-confirmation binding contract; it prepares future review only and cannot enable `sdd run`.
- [x] Validate the completed successor flow and transfer it through the controlled package mechanism as part of P3.3.

Objective:

- Implement fail-closed role selection, trusted revision-bound acceptance, and DoR-preserving guided integrity validation.

Expected files/modules:

- guided catalog/schema/module, acceptance schema/template, integrity validator/summary, roles/read-pack/runbook, package registry, tests.

Verification:

- Focused guided and integrity pytest tests, catalog/runbook validator, synthetic negative/positive walkthrough.

Verification evidence (2026-07-23):

- Relevant guided/package/release suite: `137 passed, 1 skipped`; controlled-update evidence suite: `20 passed`.
- `openspec validate --all --strict`: `18 passed, 0 failed`; roadmap validator: `0 errors` and `2` unrelated historical lifecycle warnings.
- AI-disabled CLI walkthrough blocked an `existing-change` request without `human_role` and reported no lifecycle or external mutation; route/confirmation/discovery transcript negatives are covered by the focused guided tests.
- The real source-to-sandbox `update_process_package check` was intentionally fail-closed as `package-contract-invalid` before an accepted successor candidate existed; sandbox status remained limited to its pre-existing untracked paths. P3.3 owns the later successful check/update/rollback and separate sandbox commit.
- The role-aware change was accepted into `openspec/specs/role-aware-guided-workflow/` and archived by commit `2038c93`; its operation-confirmation boundary remains non-authoritative and `sdd run` remains fail-closed.

Exit criteria:

- A route cannot offer an unauthorized CTA or begin implementation without valid role, readiness, trusted human event, and matching revision digest.

### 3.2 Typed analytics artifact framework

Status: in_progress.

OpenSpec mapping: `add-typed-analytics-artifact-framework`.

Progress evidence:

- [x] The OpenSpec contract and initial failing validation fixture are defined.
- [x] Implement typed schemas, templates, validators, and deterministic previews.
- [x] Add the sanitized end-to-end fixture and focused verification.
- [x] Transfer the validated successor package through the controlled package mechanism as part of P3.3.

Objective:

- Add seven YAML artifact contracts, templates, deterministic validation, and local read-only preview with a sanitized example.

Expected files/modules:

- analytics schemas/templates/validator/preview, package registry, read-pack/roles, tests and synthetic fixture.

Verification:

- Focused analytics pytest tests and CLI preview for the sanitized fixture.

Verification evidence (2026-07-23): `python scripts/preview_analytics.py process/examples/analytics/sanitized --json` returned a valid read-only preview with no integration actions; the relevant P3/package/release/dispatcher suite passed `147` tests with `1` skip, and `openspec validate --all --strict` passed `18` checks.

Exit criteria:

- Every artifact is schema/semantic validated, traceable, free of placeholders, and previewed without integrations or product payment screens.

### 3.3 Package and sandbox transfer

Status: pending_acceptance.

OpenSpec mapping: the accepted role-aware baseline and the active `add-typed-analytics-artifact-framework` change; this work item packages their validated successor implementation without accepting the active analytics change.

Baseline evidence:

- [x] Package `0.3.4` was transferred through the controlled mechanism before these successor changes.
- [x] Package and transfer the successor after work items 3.1 and 3.2 meet their verification gates.

Objective:

- Version/package the reusable assets and update the sandbox only through the existing controlled mechanism without touching its dirty OpenSpec paths.

Verification:

- Source package tests, package update `check`/`update`, sandbox focused tests, and separate commits.

Exit criteria:

- Sandbox package equals the validated source candidate; its existing uncommitted `enforce-guided-process-integrity` deletions remain untouched.

Transfer evidence (2026-07-23): immutable `p3-analytics-v0.3.6-rc2` validated with payload SHA-256 `b4b9f97be4eada905a65acffa3d24f1a98c2cdfe8fa38bd90d2a2296c282db57`. Source verification returned `89 passed` for the P3/package/update/catalog suite and `83 passed, 1 skipped` for `tests/test_release_candidate.py`. The controlled sandbox sequence `check -> update -> rollback -> final update` moved `0.3.4 -> 0.3.6`, proved the retained rollback snapshot, and left package/config at `0.3.6`. `git diff --check` passed after the final update. The existing dirty OpenSpec paths were neither changed nor staged. This work item is ready for human review; it does not accept or archive the active analytics change.

### Change Intake — P3.1 pre-transfer boundary (2026-07-23)

```text
Idea: separate the P3.1 role-aware verification evidence from the real sandbox update.
Source: accepted P3.3 dependency gate and the then-active change task wording.
Type: verification_change, documentation_change.
Decision: adopt_now.
Reason: the pre-transfer check isolated role-aware verification from a real sandbox update. A later owner-authorized controlled transfer was recorded under P3.3 without treating it as analytics acceptance.
Affected specs: no product behavior change; role-aware-guided-workflow verification wording only.
Affected architecture: none; the controlled update mechanism remains the only transfer path.
Data contract impact: none.
Verification impact: P3.1 performs a deterministic pre-transfer check and records the constraint; P3.3 performs check/update/rollback, sandbox parity, and separate commits.
Status: closed.
State detail: its transfer boundary is evidenced by P3.3, while analytics acceptance remains separate.
```

### Change Intake — operation-confirmation binding (2026-07-23)

```text
Idea: extend the role-aware confirmation contract with trusted role, operation ID, input digest, revision digest, and expiry for future dispatcher mutations.
Source: explicit owner decision after reviewing the implemented P3 decision-card contract.
Type: architecture_change, data_contract_change, verification_change, documentation_change.
Decision: adopt_now.
Reason: the existing decision card is not sufficient to authorize a specific operation and input; leaving that gap would make a future mutation gate ambiguous.
Affected specs: role-aware-guided-workflow; related dispatcher dependency only.
Affected architecture: typed non-authoritative request/event and validator; no execution enablement.
Data contract impact: role, operation ID, canonical input digest, card revision digest, trusted event chain, and expiry.
Verification impact: missing/mismatch/expiry/argv negatives; valid artifact still blocked at `sdd run`; external mutation permanently forbidden.
Status: closed.
State detail: `harden-role-aware-guided-workflow` was accepted and archived in `openspec/changes/archive/2026-07-23-harden-role-aware-guided-workflow/`. The contract remains non-authoritative.
```

### 3.4 Operation catalog and thin dispatcher

Status: accepted.

OpenSpec mapping: archived `openspec/changes/archive/2026-07-23-add-operation-catalog-and-dispatcher/`; accepted specs `operation-catalog` and `guided-operation-dispatcher` (P3 primary; P4/P5 related).

Objective:

- Convert the existing 30 local script entrypoints into one versioned operation catalog and give humans/AI a local situation-first `sdd` entry point without building a separate CLI platform or changing direct script compatibility.

Boundaries and dependencies:

- `operations.yaml` is the only operation registry; README, release allowlist and guided routes become validated derived views under `D-CAT-1`.
- Direct `python scripts/<name>.py` remains a supported contract under `D-CAT-2`.
- Read-only, prepare and non-authoritative request paths are delivered locally. The accepted confirmation contract is validated, while every P3 `mutate_*` run remains fail-closed; execution enablement requires a future separately accepted change under `D-CAT-3`.
- Weak-model/certification operations are internal, analytics preview is public, and raw certification writers are high risk under `D-CAT-4`.
- No MCP, credentials, network calls, external mutations or corporate configuration are allowed.

Verification:

- Catalog coverage/drift negatives, generated README equality, direct-script compatibility, four guided situations, AI-disabled fallback, and P3 mutation fail-closed evidence.

Exit criteria:

- A person can discover the next permitted action and its human decision boundary without knowing a script filename; no unregistered script or divergent derived list can pass validation.

Implementation and acceptance evidence (2026-07-23): all 16 tasks are complete; catalog schema/validator/derived artifacts, the local dispatcher, four guided walkthroughs, and the P3 fail-closed mutation boundary are verified. The catalog/dispatcher/package suite passed 138 tests with 1 skip; the owned suite passed 776 tests with 4 skips before the final catalog package integration fixes. The role-aware dependency was accepted and archived in `2038c93`; the operation catalog/dispatcher change was accepted, promoted into living specs, and archived in `d070007`. A valid confirmation artifact is validated but still returns `confirmation-contract-pending`; it never enables a mutation.
### Change Intake — единый operation catalog и dispatcher (2026-07-22)

```text
Idea: Превратить разрозненные локальные scripts в catalog-defined operations и дать человеку/AI situation-first local dispatcher.
Source: Architecture review plus accepted D-CAT-1, D-CAT-2, D-CAT-3 and D-CAT-4.
Type: scope_refinement, new_feature, architecture_change, data_contract_change, verification_change, documentation_change.
Decision: create_openspec_change.
Reason: Изменение вводит новый CLI/artifact contract, производные registry rules, automation authority boundary and acceptance scenarios; docs-only запись была бы недостаточна.
Affected specs: new operation-catalog and guided-operation-dispatcher; modified documentation-governance and repo-topology-config.
Affected architecture: versioned `operations.yaml` becomes the single registry; thin dispatcher delegates to preserved scripts; one existing confirmation mechanism remains authoritative.
Data contract impact: operation records, operation IDs in guided routes, generated README table and future confirmation binding fields.
Verification impact: complete script coverage, drift negatives, direct compatibility, AI-disabled routes and fail-closed mutation negatives.
Status: closed.
State detail: the change was accepted, promoted into `operation-catalog` and `guided-operation-dispatcher` living specs, and archived in `openspec/changes/archive/2026-07-23-add-operation-catalog-and-dispatcher/`.
```
## Phase Gate

- Local deterministic evidence is complete; no MCP/tool invocation, credential, live integration, product payment UI, or corporate adaptation is introduced. The remaining P3 lifecycle decision is human acceptance of the active analytics change and its transfer evidence.

### Change Intake — human-confirmed decisions and proactive discovery (2026-07-21)

```text
Idea: Let a colleague record a decision in ordinary chat without allowing GigaCode to invent words, acceptance, DoR or a transition; require proactive depth recommendations in ordinary intake.
Source: Human decision after PAY-AUD-001 through PAY-AUD-005.
Type: bug_fix, scope_refinement, architecture_change, data_contract_change, verification_change, documentation_change.
Decision: adopt_now.
Reason: Current AI-write acceptance evidence and premature sufficiency inference make the role-aware P3 gate unsafe.
Affected specs: role-aware-guided-workflow; change-lifecycle; traceability-contract.
Affected architecture: local typed decision-draft/confirmation-event and discovery-map contracts; no network, MCP, credentials or corporate integration.
Data contract impact: DEC code, active-card state, two verbatim human messages, revision binding, expiry and discovery-resolution rows.
Verification impact: transcript negatives for invented words/authority and completeness negatives for silent defaults.
Status: closed.
State detail: the role-aware workflow and its contract-only extension were accepted and archived in `openspec/changes/archive/2026-07-23-harden-role-aware-guided-workflow/`.
```

### Change Intake — справочный каталог скриптов (2026-07-22)

```text
Idea: Сохранить в проектной справке человекочитаемый перечень всех существующих локальных скриптов с назначением и ситуацией запуска, пока отдельный архитектор детально прорабатывает единый operation catalog и guided CLI.
Source: Human request in the active P3 discussion.
Type: documentation_change.
Decision: adopt_now.
Reason: Таблица не меняет поведение процесса, но устраняет потерю уже проверенного инвентаря и даёт человеку одну видимую точку ориентации.
Affected specs: operation-catalog and guided-operation-dispatcher (new); documentation-governance and repo-topology-config (modified) in `add-operation-catalog-and-dispatcher`.
Affected architecture: approved single operation catalog and thin local dispatcher; no external integration or autonomous authority.
Data contract impact: none.
Verification impact: сверка с перечнем `scripts/` и таблицей в проектном аудите от 2026-07-22.
Status: closed.
State detail: D-CAT-1…4 are implemented through the accepted and archived operation-catalog/dispatcher change. P3 mutation execution remains intentionally fail-closed.
```
