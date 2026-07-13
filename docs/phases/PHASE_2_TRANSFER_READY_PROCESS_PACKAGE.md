# Phase 2. Transfer-Ready Process Package And Weak-Model Readiness

Status: ready. The human owner accepted the transfer boundary; work item 2.1 may start, and later items follow the dependency order below.

> **For implementation workers:** REQUIRED SKILL: use `phase-step-runner` to execute exactly one work item, or `phase-full-runner` only when the human explicitly requests the whole phase. Each completed work item follows scenario-first TDD, passes its reviewer/architecture/verification gates, updates evidence and documentation, and ends with an intentional commit.

## Goal

Build and externally certify a reusable release candidate for the deterministic thin-change SDD process so the corporate environment requires only verified environment inventory, real project/owner/path configuration, approved integration wiring, thin Qwen/DeepSeek/GigaCode adapter configuration, and a monitored real pilot.

Phase 2 does not perform the real corporate pilot. It produces the accepted release candidate and the adaptation/pilot package consumed by Phase 3.

## Planning Boundary

- The plan is gate-based and intentionally contains no delivery dates or calendar deadlines.
- External development owns all reusable schemas, deterministic checks, workflow entry points, package/bootstrap/update/rollback behavior, role instructions, read packs, certification fixtures, release evidence, and runbooks.
- Corporate work owns only real non-secret configuration, approved secret references, environment-specific standard-tool wiring, thin AI adapter configuration, and pilot evidence.
- Reusable gaps found in the corporate environment return to the external canonical source through OpenSpec; long-lived internal forks are rejected.
- AI is never a gate, approval owner, waiver approver, merge owner, archive owner, or canonical-state owner.
- Jira task automation, Confluence publication, QA/AT proposal generation, role inboxes, deploy, Zephyr integration, graph databases, and broad project-memory automation remain outside Phase 2.

## Dependency Gate

Status: accepted.

- Phase 0 is `closed`.
- Phase 1 is `closed`; its 8 accepted specs pass strict validation.
- No Phase 1 item is `pending_acceptance` or blocks Phase 2.
- The human owner accepted the release-candidate boundary and the removal of schedule dates from project planning artifacts.
- Active proposed change `define-transfer-ready-process-package` contains proposal, design, two capability deltas, and implementation tasks.
- Phase 2 is sequentially unblocked. Work item 2.1 is ready; other work items remain planned until their named dependencies close.

## Inputs To Read

- `AGENTS.md`
- `docs/README.md`
- `docs/00_FILE_STRUCTURE.md`
- `docs/ROADMAP.md`
- `docs/IMPLEMENTATION_STRATEGY.md`
- `docs/CONTEXT.md`
- `docs/DECISIONS.md`
- `docs/CURRENT_PROJECT_AUDIT.md`
- `docs/audits/TRANSFER_READINESS_STATUS_2026-07-13.md`
- `docs/AI_STEP_VERIFICATION_CHECKLIST.md`
- `docs/planning/PROJECT_MEMORY_AND_WEAK_MODEL_GUARDRAILS.md`
- `openspec/specs/repo-topology-config/spec.md`
- `openspec/specs/documentation-governance/spec.md`
- `openspec/specs/change-package-foundation/spec.md`
- `openspec/specs/change-lifecycle/spec.md`
- `openspec/specs/change-artifact-contracts/spec.md`
- `openspec/specs/traceability-contract/spec.md`
- `openspec/specs/waiver-policy/spec.md`
- `openspec/changes/define-transfer-ready-process-package/`
- Existing `templates/change/`, `scripts/validate_change.py`, and `tests/test_validate_change.py`

## OpenSpec And Acceptance Mapping

Affected accepted requirements:

- `openspec/specs/repo-topology-config/spec.md`: central topology, config discovery, versioned package distribution, OpenSpec pin, owner registry, and bounded read-pack workflow.
- `openspec/specs/documentation-governance/spec.md`: scenario-first verification, human feedback memory, source ownership, derived-artifact metadata, and weak-model authority labels.
- `openspec/specs/change-package-foundation/spec.md`: copyable template, deterministic validator, pre-commit entry point, and placeholder validation.
- `openspec/specs/change-lifecycle/spec.md`: human-owned transitions and first thin-flow capability boundary.
- `openspec/specs/change-artifact-contracts/spec.md`: thin/full package behavior and later-layer exclusions.
- `openspec/specs/traceability-contract/spec.md`: review/archive evidence and AI-advisory traceability.
- `openspec/specs/waiver-policy/spec.md`: human-owned waiver approval and prohibited bypasses.

Active proposed change:

- `openspec/changes/define-transfer-ready-process-package/`
  - new capability `transfer-readiness`;
  - new capability `weak-model-guardrails`.

Acceptance scenarios:

- A clean supported environment can bootstrap and validate the synthetic central `team-specs` reference without AI.
- Config, package, OpenSpec version, ownership, release manifest, and compatibility failures are rejected deterministically.
- The packaged thin flow covers create, validate, Spec PR support, human approval boundary, archive support, and traceability evidence.
- Package update and rollback preserve canonical OpenSpec history.
- A deterministic launcher supplies one bounded role operation and an authority-labelled read pack.
- Missing context, conflicting sources, fabricated evidence, forbidden approval, skipped stop point, invalid transition, adapter failure, and context-limit failure are visible and safe.
- Actual Qwen-class and DeepSeek-class runs are recorded for analyst, developer, and QA thin-change workflows.
- Every gated action passes an AI-disabled walkthrough.
- Release manifest and transfer runbook contain no corporate or private values.
- Corporate adaptation templates limit work to real configuration, approved wiring, thin adapters, and pilot evidence.

Verification evidence expected before Phase 2 completion:

- Focused TDD tests for each schema, validator, workflow entry point, read-pack builder, certification rule, release manifest, and rollback behavior.
- Full Python test suite.
- Synthetic clean-bootstrap rehearsal.
- Packaged thin-flow positive and negative walkthroughs.
- AI-disabled certification for every gated operation.
- Actual Qwen-class and DeepSeek-class certification evidence for analyst, developer, and QA roles.
- Secret/private-value scan over release assets and certification fixtures.
- Release-manifest validation and rollback rehearsal.
- `openspec list`, `openspec list --specs`, and `openspec validate --all --strict`.
- `git diff --check`.
- Human acceptance of the external release candidate before Phase 3 begins.

## Implementation File Structure

The implementation should converge on this responsibility split. Exact generated release output remains ignored or is stored as synthetic committed evidence only.

```text
process/
  VERSION
  package.yaml
  workflow.yaml
  schemas/
    sdd-config.schema.json
    projects.schema.json
    owners.schema.json
    project-adapter.schema.json
    process-package.schema.json
    read-pack.schema.json
    operation-evidence.schema.json
    release-manifest.schema.json
    certification-record.schema.json
  templates/
    change/
  validators/
    validate_change.py
    validate_config.py
    validate_release.py
  roles/
    analyst-thin-change.md
    developer-thin-change.md
    qa-thin-change.md
  adapters/
    qwen.md
    deepseek.md
    gigacode.md
  certification/
    fixtures/
    expected/
    negative-cases/

templates/
  team-specs/
    sdd.config.yaml
    projects.yaml
    owners.yaml
    openspec/
    traceability/
  project-adapter/
    .sdd-project.yaml

scripts/
  bootstrap_team_specs.py
  create_change.py
  validate_process_config.py
  build_read_pack.py
  prepare_spec_pr.py
  prepare_archive.py
  update_process_package.py
  certify_process_release.py

tests/
  test_validate_change.py
  test_validate_process_config.py
  test_bootstrap_team_specs.py
  test_thin_flow_entrypoints.py
  test_build_read_pack.py
  test_weak_model_contract.py
  test_process_update_rollback.py
  test_release_certification.py

docs/runbooks/
  PROCESS_PACKAGE_SETUP.md
  PROCESS_PACKAGE_UPDATE_AND_ROLLBACK.md
  CORPORATE_ADAPTATION.md
  THIN_CHANGE_PILOT.md
```

Compatibility rule:

- `process/` becomes the reusable package source.
- Existing root entry points remain thin compatibility wrappers until their removal is proposed and accepted separately.
- Canonical behavior is not duplicated between root wrappers and package modules.

## Change Intake

```text
Idea: Complete the reusable SDD tool externally as a transfer-ready release candidate, including preparation and certification for weak Qwen/DeepSeek-class models, so the corporate environment performs only real configuration, integration adaptation, and a pilot.
Source: Human confirmation after the transfer-readiness audit.
Type: scope_refinement, architecture_change, verification_change, documentation_change
Decision: adopt_now
Reason: Leaving process-package design, weak-model safeguards, or reusable workflow behavior for the constrained corporate environment would make correctness depend on weaker assistants and create a high risk of internal forks.
Affected specs: Active change `define-transfer-ready-process-package`; accepted repo-topology, documentation-governance, lifecycle, artifact, traceability, waiver, and change-package-foundation specs remain the baseline.
Affected architecture: Establishes an external reusable core, a thin corporate adaptation layer, separate external-release and corporate-pilot gates, and a no-fork feedback path.
Data contract impact: Adds proposed release manifest, read-pack, operation-evidence, certification-record, compatibility, and adaptation/pilot evidence contracts.
Verification impact: Requires clean bootstrap, packaged thin flow, AI-disabled execution, actual Qwen and DeepSeek certification, negative safety cases, release/rollback evidence, and human release acceptance.
Status: accepted. The boundary is captured in the active OpenSpec change, this Phase 2 plan, roadmap, decision log, audit, context, and verification guidance.
```

```text
Idea: Do not record delivery dates or calendar deadlines in the roadmap, OpenSpec change, or Phase 2 plan.
Source: Human confirmation after reviewing the recommended transfer plan.
Type: documentation_change, scope_refinement
Decision: adopt_now
Reason: The project should be controlled by evidence and acceptance gates; schedule commitments are managed outside these durable product/process contracts.
Affected specs: None; this is a planning/documentation boundary rather than SDD product behavior.
Affected architecture: None.
Data contract impact: None.
Verification impact: Phase planning review must confirm that no delivery schedule or deadline was introduced.
Status: accepted. Phase 2 and roadmap planning are gate-based and contain no delivery dates or deadlines.
```

## Work Items

### 2.1 Process Package And Synthetic Central Topology

Status: ready.

Dependency status: sequential-start. Phase 1 is closed and no earlier Phase 2 item is required.

Objective:

- Create the versioned `process/` source package and synthetic `team-specs`/project-adapter bootstrap templates using accepted topology and configuration names.

OpenSpec source:

- Accepted `repo-topology-config` requirements for first topology, config files, package distribution, OpenSpec pin, and owner registry.
- Active tasks 1.1-1.2 in `define-transfer-ready-process-package`.

Expected files/modules:

- `process/VERSION`
- `process/package.yaml`
- `process/workflow.yaml`
- `process/schemas/*.schema.json`
- `templates/team-specs/**`
- `templates/project-adapter/.sdd-project.yaml`
- schema and fixture tests

Verification:

- Write failing schema/fixture tests before each schema or template.
- Validate one complete synthetic central setup.
- Reject missing version pins, unsupported topology, invalid project/owner references, and production-looking placeholders.
- Run focused tests and `git diff --check`.

Documentation updates:

- `docs/00_FILE_STRUCTURE.md`
- setup-oriented docs only after paths exist
- Phase 2 evidence section

Recommended subagents:

- worker: package/config skeleton and tests.
- reviewer: schema completeness and placeholder/secret risks.
- architecture-checker: accepted topology and package-boundary compliance.
- verification-checker: fixture and negative-case evidence.

Exit criteria:

- Synthetic central topology is copyable, schemas are deterministic, package/config versions are explicit, and no corporate value is inferred.

### 2.2 Configuration Discovery And Compatibility Validation

Status: planned.

Dependency status: sequential. Starts after 2.1 is closed.

Objective:

- Implement central/project config discovery, schema validation, OpenSpec `1.4.1` pin checks, process-package compatibility checks, and safe diagnostics.

OpenSpec source:

- Accepted `repo-topology-config` scenarios for config discovery, version mismatch, supported topology, and owner mapping.
- Active task 1.3.

Expected files/modules:

- `process/validators/validate_config.py`
- `scripts/validate_process_config.py`
- `tests/test_validate_process_config.py`
- compatibility/rollback fixtures

Verification:

- TDD cases for central config, optional adapter, sibling checkout, missing registry, version mismatch, unsupported topology, secrets, and invalid owner/project references.
- Machine-readable and human-readable diagnostics must identify the exact failing field and source file.

Documentation updates:

- `docs/runbooks/PROCESS_PACKAGE_SETUP.md`
- configuration section in file structure/context if needed

Recommended subagents:

- worker, reviewer, architecture-checker, verification-checker.

Exit criteria:

- Configuration and compatibility state can be proven before any gated operation, with no AI inference required.

### 2.3 Packaged Deterministic Thin Flow

Status: planned.

Dependency status: sequential. Starts after 2.1 and 2.2 are closed.

Objective:

- Make the accepted thin flow consumable from the versioned process package while preserving the existing validator contract and root compatibility entry point.

OpenSpec source:

- Accepted change-package-foundation, lifecycle, artifact, traceability, and waiver requirements.
- Active tasks 2.1-2.5.

Expected files/modules:

- `process/templates/change/**`
- `process/validators/validate_change.py`
- thin root wrapper `scripts/validate_change.py`
- `scripts/bootstrap_team_specs.py`
- `scripts/create_change.py`
- `scripts/prepare_spec_pr.py`
- `scripts/prepare_archive.py`
- `scripts/update_process_package.py`
- focused and end-to-end tests

Verification:

- Preserve all existing 34 validator tests before expanding behavior.
- Add red-green tests for bootstrap, create, PR evidence, archive evidence, update, and rollback.
- Prove AI-disabled thin flow on the synthetic reference setup.
- Verify no entry point approves, merges, waives, or archives without human evidence.

Documentation updates:

- setup, thin-flow, update, and rollback runbooks
- current audit evidence

Recommended subagents:

- worker, reviewer, architecture-checker, verification-checker.

Exit criteria:

- The complete reference thin flow is reproducible from the packaged assets, deterministic gates remain AI-independent, and rollback preserves accepted history.

### 2.4 Weak-Model Operating Contracts And Role Kit

Status: planned.

Dependency status: parallel-after-foundation. May start after 2.1 closes because it depends on stable canonical paths and package metadata but not on completion of every thin-flow entry point.

Parallel independence rationale:

- It does not change accepted lifecycle/artifact behavior.
- It consumes canonical IDs and paths from 2.1.
- It cannot accept release readiness before 2.3 and 2.5 close.

Objective:

- Implement deterministic task selection, authority-labelled bounded read packs, evidence output, explicit blocked behavior, and analyst/developer/QA role instructions for weak models.

OpenSpec source:

- Active `weak-model-guardrails` requirements.
- Accepted documentation-governance source-ownership scenarios.
- Active tasks 3.1-3.5.

Expected files/modules:

- read-pack and operation-evidence schemas
- `scripts/build_read_pack.py`
- `process/roles/*.md`
- `process/adapters/*.md`
- `tests/test_build_read_pack.py`
- `tests/test_weak_model_contract.py`

Verification:

- TDD cases for authority labels, bounded context, missing sources, conflicting sources, stable IDs, private paths, evidence boundaries, forbidden authority, and stop points.
- Self-review role instructions for one-stage scope, concrete examples, negative cases, and deterministic fallback.

Documentation updates:

- `docs/planning/PROJECT_MEMORY_AND_WEAK_MODEL_GUARDRAILS.md`
- role and adapter ownership map

Recommended subagents:

- worker: role/read-pack implementation.
- reviewer: weak-model ambiguity and instruction-height review.
- architecture-checker: canonical-source and adapter boundaries.
- verification-checker: negative-case completeness.

Exit criteria:

- A model cannot select its own authority or silently proceed with missing context, and every assisted operation has an AI-disabled fallback.

### 2.5 Weak-Model And AI-Disabled Certification

Status: planned.

Dependency status: sequential. Starts after 2.3 and 2.4 are closed.

Objective:

- Build repeatable certification fixtures and record actual Qwen-class, DeepSeek-class, and AI-disabled evidence for the first pilot roles.

OpenSpec source:

- Active `weak-model-guardrails` certification requirements.
- Active tasks 4.1-4.5.

Expected files/modules:

- `process/certification/**`
- `scripts/certify_process_release.py`
- `tests/test_release_certification.py`
- committed synthetic certification summaries or evidence references

Verification:

- Record exact model/runtime and adapter identifiers rather than generic family claims.
- Cover analyst, developer, and QA thin flows.
- Cover missing context, source conflict, fabricated evidence, forbidden approval, skipped stop, invalid transition, adapter failure, and context-limit failure.
- Require deterministic validation of outputs.
- If either Qwen-class or DeepSeek-class actual execution is unavailable, mark this work item blocked; do not claim external release readiness without a new human scope decision.

Documentation updates:

- certification evidence index
- current audit limitations and results

Recommended subagents:

- worker: fixture/runner implementation.
- reviewer: instruction/evaluation bias and false-positive review.
- architecture-checker: AI/non-AI responsibility boundary.
- verification-checker: reproduce every claimed result.

Exit criteria:

- Both model families and the AI-disabled path have reproducible evidence; fluent but non-compliant outputs fail certification.

### 2.6 Release Manifest, Transfer Runbook, And Rehearsal

Status: planned.

Dependency status: sequential. Starts after 2.2, 2.3, and 2.5 are closed.

Objective:

- Assemble and validate the external release candidate, transfer manifest, compatibility inventory, clean bootstrap, update/rollback rehearsal, and secret/private-data safety evidence.

OpenSpec source:

- Active `transfer-readiness` release-content, bootstrap, external-gate, and evidence requirements.
- Active tasks 5.1-5.4.

Expected files/modules:

- release-manifest schema/template
- `process/validators/validate_release.py`
- release certification entry point
- `docs/runbooks/PROCESS_PACKAGE_UPDATE_AND_ROLLBACK.md`
- `docs/runbooks/CORPORATE_ADAPTATION.md`
- synthetic transfer rehearsal evidence

Verification:

- Rebuild from a clean supported location.
- Verify package/config/OpenSpec versions and evidence references.
- Scan release assets for secrets, internal URLs, private paths, and corporate data.
- Rehearse upgrade failure and rollback.
- Reject missing, stale, failed, or AI-only evidence.

Documentation updates:

- setup/update/rollback/adaptation runbooks
- audit release-readiness findings

Recommended subagents:

- worker, reviewer, architecture-checker, verification-checker.

Exit criteria:

- A reproducible candidate and manifest exist, rollback works, and no corporate fact was guessed or embedded.

### 2.7 Corporate Adaptation And Pilot Package

Status: planned.

Dependency status: sequential. Starts after 2.6 is closed; it prepares Phase 3 but does not execute the real pilot.

Objective:

- Provide non-secret environment inventory, real-config, pilot-entry, monitored-pilot, rollback/hold, and no-fork feedback templates for Phase 3.

OpenSpec source:

- Active `transfer-readiness` corporate-boundary, pilot, evidence, and later-layer exclusion requirements.
- Active tasks 6.1-6.4.

Expected files/modules:

- `docs/runbooks/CORPORATE_ADAPTATION.md`
- `docs/runbooks/THIN_CHANGE_PILOT.md`
- environment inventory and pilot evidence templates
- internal-fork detection or package-version mismatch checks

Verification:

- Walk through the templates using synthetic values.
- Confirm every real fact is an explicit input.
- Confirm secrets are referenced, never embedded.
- Confirm reusable gaps route to external OpenSpec.
- Confirm Jira/Confluence/QA/AT/role-inbox layers are not pilot prerequisites.

Documentation updates:

- Phase 3 dependency and entry-gate text in roadmap
- context and audit boundaries

Recommended subagents:

- worker, reviewer, architecture-checker, verification-checker.

Exit criteria:

- Phase 3 can start from an accepted candidate without designing reusable process behavior inside the corporate environment.

### 2.8 External Release Candidate Acceptance Review

Status: planned.

Dependency status: sequential-final. Starts after 2.1-2.7 are closed.

Objective:

- Reconcile implementation, specs, tasks, tests, certification, documentation, audit, release manifest, and rollback evidence; stop for human acceptance.

OpenSpec source:

- Active tasks 7.1-7.4.
- All proposed transfer-readiness and weak-model-guardrails scenarios.

Expected files/modules:

- Phase 2 acceptance evidence section
- updated roadmap/current audit/file structure/context/runbooks
- release manifest and certification index

Verification:

- Focused and full tests.
- Clean bootstrap and packaged thin-flow rehearsal.
- AI-disabled, Qwen-class, and DeepSeek-class certification.
- Secret/private-data scan.
- Rollback rehearsal.
- `openspec list`, `openspec list --specs`, `openspec validate --all --strict`, and `git diff --check`.
- Reviewer, architecture, and verification findings resolved or explicitly blocked.

Documentation updates:

- Mark Phase 2 gate `pending_acceptance` before asking the human.
- Mark it `accepted`/`closed` only after explicit human acceptance and full status reconciliation.
- Keep the OpenSpec change active for Phase 3 pilot evidence unless its accepted archive gate is explicitly revised by the human.

Recommended subagents:

- reviewer, architecture-checker, verification-checker; worker only for accepted fixes.

Exit criteria:

- Human accepts the exact external release candidate for corporate adaptation, with known limitations and rollback evidence visible.

## OpenSpec Task Mapping

| Phase 2 work item | OpenSpec task groups |
|---|---|
| 2.1 | 1.1-1.2 |
| 2.2 | 1.3 |
| 2.3 | 2.1-2.5 |
| 2.4 | 3.1-3.5 |
| 2.5 | 4.1-4.5 |
| 2.6 | 5.1-5.4 |
| 2.7 | 6.1-6.4 |
| 2.8 | 7.1-7.4 |

OpenSpec task 7.5 belongs to Phase 3 because it requires successful real corporate adaptation and pilot evidence.

## Phase Gate

Status: planned.

Phase 2 can move to `pending_acceptance` only when:

- work items 2.1-2.7 are closed;
- work item 2.8 verification is complete;
- the external release candidate and manifest are reproducible;
- all deterministic gates pass without AI;
- actual Qwen-class and DeepSeek-class certification evidence exists for analyst, developer, and QA thin flows;
- negative safety scenarios pass;
- clean bootstrap, update, rollback, and secret/private-data checks pass;
- corporate adaptation and pilot materials are complete;
- no later-layer integration became a hidden prerequisite;
- current docs, audit, roadmap, OpenSpec status, and phase statuses agree.

Phase 2 becomes `closed` only after explicit human acceptance of the external release candidate. Phase 3 must not install or pilot an unaccepted candidate.

## Human Decisions

Resolved:

- External transfer-ready release candidate is the required boundary before corporate adaptation.
- Reusable core and weak-model safeguards are completed externally.
- Corporate work is limited to real paths, projects, owners, approved secret references, integration wiring, thin model adapters, environment checks, and pilot evidence.
- The plan and roadmap contain no delivery dates or calendar deadlines.

No decision currently blocks work item 2.1.

Mandatory later evidence, not current design decisions:

- Exact Qwen and DeepSeek model/runtime identifiers used for certification.
- Actual corporate runtime, network, artifact distribution, MCP, and integration capabilities.
- Human acceptance of the external release candidate before Phase 3.
