# Phase 2. Transfer-Ready Process Package And Weak-Model Readiness

Status: blocked. The technical prerequisites are available, but human decision `D-015` pauses all implementation until the corrected, cleanly renumbered Phase 2 plan is accepted. The certification matrix and supported external reference runtime remain open planning decisions.

> **For implementation workers:** REQUIRED SKILL: use `phase-step-runner` to execute exactly one work item, or `phase-full-runner` only when the human explicitly requests the whole phase. Each completed work item follows scenario-first TDD, passes its reviewer/architecture/verification gates, updates evidence and documentation, and ends with an intentional commit.

## Goal

Build and externally certify a reusable release candidate for the deterministic NIS-aligned `minor | major | hotfix` SDD process so the corporate environment requires only verified environment inventory, real project/owner/path/workflow configuration, approved integration wiring, thin Qwen/DeepSeek/GigaCode adapter configuration, and a monitored real pilot.

Phase 2 does not perform the real corporate pilot. It produces the accepted release candidate and the adaptation/pilot package consumed by Phase 3.

## Planning Boundary

- The plan is gate-based and intentionally contains no delivery dates or calendar deadlines.
- External development owns all reusable schemas, deterministic checks, workflow entry points, package/bootstrap/update/rollback behavior, role instructions, read packs, certification fixtures, release evidence, and runbooks.
- Corporate work owns only real non-secret configuration, approved secret references, environment-specific standard-tool wiring, thin AI adapter configuration, and pilot evidence.
- Reusable gaps found in the corporate environment return to the external canonical source through OpenSpec; long-lived internal forks are rejected.
- AI-disabled operation is the first delivery requirement and permanent fallback. Under `D-014`, later accepted changes are expected to automate bounded workflow orchestration, drafting, evidence assembly, routing, monitoring, tool coordination, and permitted transition preparation; AI is not a gate, approval owner, waiver approver, merge owner, archive owner, or canonical-state owner unless a future explicit human decision changes that authority contract.
- Jira task automation, Confluence publication, QA/AT proposal generation, role inboxes, deploy, Zephyr integration, graph databases, and broad project-memory automation remain outside Phase 2.

## Dependency Gate

Status: accepted.

- Phase 0 is `closed`.
- Phase 1 is `closed`; its 8 accepted specs pass strict validation.
- No Phase 1 item is `pending_acceptance` or blocks Phase 2.
- The human owner accepted the release-candidate boundary and the removal of schedule dates from project planning artifacts.
- Active proposed change `define-transfer-ready-process-package` contains proposal, design, two capability deltas, and implementation tasks.
- Active proposed change `adopt-nis-corporate-process-governance` contains proposal, design, twelve capability deltas, and the implementation backlog for `D-013`.
- Product and technical prerequisites are available, but the human planning gate is closed under `D-015`. Work item 2.1 and the rest of Phase 2 must not start until the corrected plan replaces the defective `2.3A-2.8` mapping and the two open decisions below are accepted.

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
- `docs/planning/NIS_CORPORATE_PROCESS_ADOPTION_PLAN_2026-07-13.md`
- `docs/audits/NIS_V1_6_ARCHITECTURE_COMPATIBILITY_AUDIT_2026-07-13.md`
- `openspec/specs/repo-topology-config/spec.md`
- `openspec/specs/documentation-governance/spec.md`
- `openspec/specs/change-package-foundation/spec.md`
- `openspec/specs/change-lifecycle/spec.md`
- `openspec/specs/change-artifact-contracts/spec.md`
- `openspec/specs/traceability-contract/spec.md`
- `openspec/specs/waiver-policy/spec.md`
- `openspec/changes/define-transfer-ready-process-package/`
- `openspec/changes/adopt-nis-corporate-process-governance/`
- Existing `templates/change/`, `scripts/validate_change.py`, and `tests/test_validate_change.py`

## OpenSpec And Acceptance Mapping

Affected accepted requirements:

- `openspec/specs/repo-topology-config/spec.md`: central topology, config discovery, versioned package distribution, OpenSpec pin, owner registry, and bounded read-pack workflow.
- `openspec/specs/documentation-governance/spec.md`: scenario-first verification, human feedback memory, source ownership, derived-artifact metadata, and weak-model authority labels.
- `openspec/specs/change-package-foundation/spec.md`: copyable template, deterministic validator, pre-commit entry point, and placeholder validation.
- `openspec/specs/change-lifecycle/spec.md`: accepted six-state lifecycle and human-owned transitions; the NIS adoption change proposes class-aware DoR/DoD and external-delivery separation.
- `openspec/specs/change-artifact-contracts/spec.md`: historical accepted thin/full behavior; the NIS adoption change proposes replacement by minor/major/hotfix matrices.
- `openspec/specs/traceability-contract/spec.md`: review/archive evidence and AI-advisory traceability.
- `openspec/specs/waiver-policy/spec.md`: human-owned waiver approval and prohibited bypasses.

Active proposed change:

- `openspec/changes/define-transfer-ready-process-package/`
  - new capability `transfer-readiness`;
  - new capability `weak-model-guardrails`.
- `openspec/changes/adopt-nis-corporate-process-governance/`
  - new capabilities `corporate-change-classification`, `readiness-completion-gates`, `tech-lead-workflow`, and `corporate-flow-controls`;
  - modified package, artifact, lifecycle, traceability, waiver, topology/config, and Confluence-boundary capabilities.

Acceptance scenarios:

- A clean supported environment can bootstrap and validate the synthetic central `team-specs` reference without AI.
- Config, package, OpenSpec version, ownership, release manifest, and compatibility failures are rejected deterministically.
- The packaged flow covers deterministic minor/major/hotfix classification, migration, create, validate, Spec PR, DoR, human approval, implementation controls, DoD, applicable release/transfer readiness, archive support, and traceability evidence.
- Package update and rollback preserve canonical OpenSpec history.
- A deterministic launcher supplies one bounded role operation and an authority-labelled read pack.
- Missing context, conflicting sources, fabricated evidence, forbidden approval, skipped stop point, invalid transition, adapter failure, and context-limit failure are visible and safe.
- Actual Qwen-class and DeepSeek-class runs are recorded for minor, major, hotfix, analyst, developer, QA, and Tech Lead workflows plus negative authority cases.
- Every gated action passes an AI-disabled walkthrough.
- Release manifest and transfer runbook contain no corporate or private values.
- Corporate adaptation templates limit work to real configuration, approved wiring, thin adapters, and pilot evidence.

Verification evidence expected before Phase 2 completion:

- Focused TDD tests for each schema, validator, workflow entry point, read-pack builder, certification rule, release manifest, and rollback behavior.
- Full Python test suite.
- Synthetic clean-bootstrap rehearsal.
- Packaged minor/major/hotfix positive and negative walkthroughs, including migration, under-classification, pseudo-hotfix, hold/resume, and hotfix reconciliation.
- AI-disabled certification for every gated operation.
- Actual Qwen-class and DeepSeek-class certification evidence for analyst, developer, QA, and Tech Lead roles.
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
    classification-policy.schema.json
    change-v2.schema.json
    readiness-completion.schema.json
    regression-matrix.schema.json
    flow-control-record.schema.json
    release-package.schema.json
    pilot-evidence.schema.json
  templates/
    change/
  validators/
    validate_change.py
    validate_config.py
    validate_release.py
  roles/
    analyst-change.md
    developer-change.md
    qa-change.md
    tech-lead-change.md
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
  test_classification_migration.py
  test_change_flow_entrypoints.py
  test_readiness_completion.py
  test_tech_lead_workflow.py
  test_corporate_flow_controls.py
  test_pilot_safety_and_failed_runs.py
  test_build_read_pack.py
  test_weak_model_contract.py
  test_process_update_rollback.py
  test_release_certification.py

docs/runbooks/
  PROCESS_PACKAGE_SETUP.md
  PROCESS_PACKAGE_UPDATE_AND_ROLLBACK.md
  CORPORATE_ADAPTATION.md
  GOVERNED_CHANGE_PILOT.md
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
Verification impact: Requires clean bootstrap, packaged class-aware flow, AI-disabled execution, actual Qwen and DeepSeek certification, negative safety cases, release/rollback evidence, and human release acceptance.
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

```text
Idea: Adopt the real NIS corporate process as target behavior, including the flat minor/major/hotfix classification, readiness and completion criteria, Tech Lead automation, regression/scope/stop/release controls, role verification, pilot safety, and failed-run retention.
Source: Human correction and explicit choice after the NIS v1.6 architecture audit.
Type: scope_refinement, architecture_change, data_contract_change, new_feature, verification_change, documentation_change
Decision: create_openspec_change
Reason: The accepted Phase 1 thin/full baseline does not yet represent the real corporate workflow. The human owner selected the NIS process and explicitly chose its flat classification model; implementing the transfer release without this adoption would certify the wrong target.
Affected specs: New active change `adopt-nis-corporate-process-governance` modifies package, artifact, lifecycle, traceability, waiver, topology/config, and Confluence-boundary capabilities and adds classification, readiness/completion, Tech Lead, and corporate-flow capabilities.
Affected architecture: Preserves Git/OpenSpec canonical ownership, the six lifecycle states, deterministic/AI-disabled gates, human decisions, external-release boundary, and no-fork rule while adding corporate business gates and Tech Lead governance.
Data contract impact: Adds schema version 2, `classification: minor|major|hotfix`, migration from legacy mode, readiness/completion, regression, flow-control, release-package, decision/AI evidence, pilot-safety, and failed-run records.
Verification impact: Requires class and migration fixtures, DoR/DoD and hotfix negative cases, Tech Lead authority cases, stop/resume and reconciliation evidence, failed-run retention, pilot safety, AI-disabled operation, actual Qwen/DeepSeek certification, and human review.
Status: accepted planning direction under `D-013`. The OpenSpec change is documentation-complete but remains unimplemented; its tasks will receive unique owners in the corrected `2.3-2.14` matrix, and the old 2.3A ownership claim is superseded by `D-015`.
```

```text
Idea: Create one presentation-ready report that clearly separates what already matches NIS, what is borrowed, and what is adapted or rejected.
Source: Human request for a concise acceptance summary and a durable full report for a future presentation.
Type: documentation_change
Decision: adopt_now
Reason: The comparison already exists across the evidence audit, adoption plan, and OpenSpec change, but a presentation audience needs one clearly labelled read model without changing normative behavior.
Affected specs: None. The report references `D-013` and `adopt-nis-corporate-process-governance`; OpenSpec remains the normative owner.
Affected architecture: None. The report preserves source ownership and explicitly distinguishes accepted direction, proposed behavior, and current implementation.
Data contract impact: None.
Verification impact: Cross-check the report against the NIS audit, 22-file source-coverage appendix, active OpenSpec change, task count, and current implementation status; keep the NIS package ignored and untracked.
Status: closed. The report is stored in `docs/audits/NIS_V1_6_PRESENTATION_COMPARISON_REPORT_2026-07-13.md`.
```

```text
Idea: Remove all process-effectiveness measurement material from project documentation and OpenSpec while retaining failed-run evidence.
Source: Human correction after reviewing the measurement terminology.
Type: scope_refinement, verification_change, documentation_change
Decision: adopt_now
Reason: The target process should govern correctness, safety, roles, and delivery flow without introducing an effectiveness-evaluation program. Failed attempts must still remain visible for traceability and incident diagnosis.
Affected specs: Remove the proposed `process-measurement-pilot` capability; update `corporate-flow-controls`, `traceability-contract`, and `repo-topology-config` deltas.
Affected architecture: Removes historical/control/experimental comparison design, independent comparison assurance, contamination accounting, missing-measurement-data rules, sample/decision thresholds, and effectiveness/scale conclusions. Keeps DoR/DoD, QA ownership, operational stop/hold rules, pilot safety, and failed-run retention.
Data contract impact: Removes metric-definition and comparison records; retains source-linked failed-run and pilot-safety records.
Verification impact: Strict OpenSpec validation, documentation-wide forbidden-term scan, failed-run-retention scenario check, and documentation-sync audit are required.
Status: accepted and applied to the active documentation/OpenSpec proposal on 2026-07-13.
```

```text
Idea: Deliver the process in two automation horizons: first a complete AI-disabled deterministic process, then progressive AI automation of bounded process work after the process and pilot are stable.
Source: Human clarification on 2026-07-14.
Type: architecture_change, scope_refinement, verification_change, documentation_change
Decision: adopt_now
Reason: The AI-disabled path is the reliability foundation and fallback, but the intended product direction is not permanently AI-minimal. Future automation must be planned explicitly without weakening deterministic checks or silently transferring accountable human authority.
Affected specs: Current Phase 2 transfer and weak-model contracts retain AI-disabled certification; later automation capabilities require future OpenSpec changes after the governed pilot.
Affected architecture: Establishes deterministic verification as the control plane and progressive AI automation as a later execution layer.
Data contract impact: None in Phase 2 beyond keeping evidence and authority boundaries explicit; future automation contracts are out of current scope.
Verification impact: Phase 2 must prove every gate without AI. Later automation must prove equivalent or stronger deterministic evidence and safe fallback behavior.
Status: accepted as `D-014` and recorded in project and presentation-facing documentation.
```

```text
Idea: Repair the Phase 2 work-item plan before implementation.
Source: Human selections 1A, 2A, 3A, 6A, and 7A on 2026-07-14 after the Phase 2 completeness audit.
Type: planning_change, data_contract_clarification, verification_change, documentation_change
Decision: queue_current_phase
Reason: The old `2.3A-2.8` mapping has circular and duplicate task ownership. Clean sequential renumbering, a pre-implementation acceptance gate, explicit evidence storage, and a named final human acceptor remove ambiguity without changing accepted product scope.
Affected specs: Both active OpenSpec changes stay open through the Phase 3 pilot. NIS task 8.7 is split so Phase 2 stops at external release acceptance and Phase 3 owns real corporate configuration and pilot execution.
Affected architecture: No change to canonical ownership or the external/corporate boundary.
Data contract impact: Normalized synthetic evidence, manifests, and hashes are committed to Git; raw certification outputs live in a versioned release artifact and are referenced by manifest/checksum.
Verification impact: The human owner makes final Phase 2 release-candidate acceptance using mandatory Tech Lead, QA, and security evidence when applicable.
Status: blocked. The listed `D-015` choices are accepted, but implementation remains blocked while the exact certification matrix and supported external reference runtime are open; after those choices, the plan will replace `2.3A-2.8` with clean work items `2.3-2.14` and an exact one-owner task matrix.
```

## Work Items

Planning warning: the existing entries `2.3A-2.8` below document the audited draft only and are not executable. They will be replaced, not patched in place, by clean sequential work items `2.3-2.14` after the two open human decisions are resolved. No task may be started from the draft mapping.

### 2.1 Process Package And Synthetic Central Topology

Status: blocked.

Dependency status: human-planning-gate. Phase 1 and technical prerequisites are complete, but `D-015` explicitly pauses implementation until the corrected whole-phase plan is accepted.

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

### 2.3A NIS Corporate Governance And Classification Migration

Status: superseded. Replaced by the clean `2.3-2.14` decomposition required by `D-015`; the replacement details wait for the two open decisions.

Dependency status: superseded. This draft dependency must not be used for implementation.

Objective:

- Implement `D-013`: schema-versioned minor/major/hotfix classification, conservative deterministic rules, legacy migration, class artifact matrices, DoR/DoD, Tech Lead governance, corporate flow controls, release handoff, pilot safety, and failed-run retention.

OpenSpec source:

- Complete active change `adopt-nis-corporate-process-governance`, including its eleven capability deltas and task groups 1-8.
- Planning rationale and source-to-target matrix in `docs/planning/NIS_CORPORATE_PROCESS_ADOPTION_PLAN_2026-07-13.md`.

Expected files/modules:

- schema version 2 and classification policy/matrix schemas
- classification and migration check/apply entry points
- readiness/completion, regression, stop/escalation, release-package, decision/AI evidence, pilot-safety, and failed-run schemas
- deterministic class, DoR/DoD, Tech Lead, traceability, workflow-mapping, pilot-safety, and failed-run reports
- minor, major, hotfix, migration, hold/resume, and reconciliation fixtures/tests
- updated templates, compatibility wrappers, role instructions, runbooks, and certification matrix

Verification:

- Start each requirement scenario with a failing focused test or fixture.
- Prove `thin -> minor`, `full -> major`, no automatic hotfix, idempotency, conflict refusal, preserved metadata, and no archive rewriting.
- Prove minor all-conditions, major any-trigger, harm-based hotfix, under-classification/lower-class-waiver rejection, audited source correction and recalculation, and stricter-route selection.
- Prove DoR, implementation complete, DoD, release ready, archive ready, archived, and external delivered/Done remain distinct.
- Prove hotfix cannot bypass human ownership, minimum verification, required risk decisions, rollback/hold, traceability, or reconciliation.
- Prove Tech Lead automation is source-linked decision support and AI cannot approve, waive, resume, or close.
- Prove all core gates in AI-disabled mode; later certification adds actual Qwen/DeepSeek evidence.

Documentation updates:

- Replace target thin/full language while preserving clearly marked historical/migration evidence.
- Update setup, migration, governed-flow, Tech Lead, release, corporate-adaptation, and pilot runbooks.
- Keep NIS-derived role views linked to canonical policy/spec IDs.

Recommended subagents:

- worker: one task group at a time.
- reviewer: classification/gate correctness and migration safety.
- architecture-checker: source ownership, authority, transfer, and no-fork boundaries.
- verification-checker: negative cases, AI-disabled evidence, pilot safety, and failed-run retention.

Exit criteria:

- All OpenSpec tasks for `adopt-nis-corporate-process-governance` are complete, strict validation and tests pass, migration/reconciliation evidence is reproducible, and no target surface still offers thin/full as current routes.

### 2.3 Packaged Deterministic Class-Aware Flow

Status: superseded. This draft item will be redefined in the clean `2.3-2.14` plan required by `D-015`.

Dependency status: superseded. This draft dependency must not be used for implementation.

Objective:

- Make the minor, major, and hotfix flow consumable from the versioned process package while preserving a bounded legacy-reader/migration contract and the root compatibility entry point.

OpenSpec source:

- Accepted change-package-foundation, lifecycle, artifact, traceability, and waiver baseline plus the corresponding deltas in `adopt-nis-corporate-process-governance`.
- Tasks 2.1-2.5 in `define-transfer-ready-process-package` and relevant classification/gate tasks in the NIS adoption change.

Expected files/modules:

- `process/templates/change/**`
- `process/validators/validate_change.py`
- root compatibility wrapper `scripts/validate_change.py`
- `scripts/bootstrap_team_specs.py`
- `scripts/create_change.py`
- `scripts/prepare_spec_pr.py`
- `scripts/prepare_archive.py`
- `scripts/update_process_package.py`
- focused and end-to-end tests

Verification:

- Preserve all existing 34 validator tests before expanding behavior.
- Add red-green tests for bootstrap, create, PR evidence, archive evidence, update, and rollback.
- Prove AI-disabled minor, major, and hotfix flows on the synthetic reference setup.
- Verify no entry point approves, merges, waives, or archives without human evidence.

Documentation updates:

- setup, governed-flow, classification migration, update, and rollback runbooks
- current audit evidence

Recommended subagents:

- worker, reviewer, architecture-checker, verification-checker.

Exit criteria:

- The complete reference class-aware flow is reproducible from the packaged assets, deterministic gates remain AI-independent, migration is safe, and rollback preserves accepted history.

### 2.4 Weak-Model Operating Contracts And Role Kit

Status: superseded. This draft item will be redistributed in the clean `2.3-2.14` plan required by `D-015`.

Dependency status: superseded. No parallel work is authorized before the corrected whole-phase plan is accepted.

Parallel independence rationale:

- It does not independently define lifecycle/artifact behavior; it consumes the active NIS governance contracts.
- It consumes canonical IDs and paths from 2.1.
- It cannot accept release readiness before 2.3 and 2.5 close.

Objective:

- Implement deterministic task selection, authority-labelled bounded read packs, evidence output, explicit blocked behavior, and analyst/developer/QA/Tech Lead role instructions for weak models.

OpenSpec source:

- Active `weak-model-guardrails` requirements.
- Active `tech-lead-workflow`, `corporate-change-classification`, `readiness-completion-gates`, and `corporate-flow-controls` requirements.
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

Status: superseded. This draft item will be redistributed in the clean `2.3-2.14` plan required by `D-015`.

Dependency status: superseded. This draft dependency must not be used for implementation.

Objective:

- Build repeatable certification fixtures and record actual Qwen-class, DeepSeek-class, and AI-disabled evidence for all three classes and the first pilot roles.

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
- Cover minor, major, hotfix, analyst, developer, QA, and Tech Lead flows.
- Cover missing context, source conflict, fabricated evidence, under-classification, pseudo-hotfix, forbidden approval, unsafe resume, unresolved reconciliation, invalid transition, adapter failure, and context-limit failure.
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

- Both model families and the AI-disabled path have reproducible class/role evidence; fluent but non-compliant or authority-violating outputs fail certification.

### 2.6 Release Manifest, Transfer Runbook, And Rehearsal

Status: superseded. This draft item will be redistributed in the clean `2.3-2.14` plan required by `D-015`.

Dependency status: superseded. This draft dependency must not be used for implementation.

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

Status: superseded. This draft item will be redistributed in the clean `2.3-2.14` plan required by `D-015`.

Dependency status: superseded. This draft dependency must not be used for implementation.

Objective:

- Provide non-secret environment inventory, real-config, pilot-selection/entry, monitored-pilot safety, failed-run evidence, privacy, rollback/hold, hotfix reconciliation, and no-fork feedback templates for Phase 3.

OpenSpec source:

- Active `transfer-readiness` corporate-boundary, pilot, evidence, and later-layer exclusion requirements.
- Active tasks 6.1-6.4.

Expected files/modules:

- `docs/runbooks/CORPORATE_ADAPTATION.md`
- `docs/runbooks/GOVERNED_CHANGE_PILOT.md`
- environment inventory and pilot evidence templates
- internal-fork detection or package-version mismatch checks

Verification:

- Walk through the templates using synthetic values.
- Confirm every real fact is an explicit input.
- Confirm secrets are referenced, never embedded.
- Confirm reusable gaps route to external OpenSpec.
- Confirm Jira/Confluence/QA/AT/broad role-inbox layers are not pilot prerequisites while Tech Lead evidence remains available through deterministic files/reports.
- Confirm failed attempts remain visible after retries and that the pilot stops or holds when safety, access, evidence integrity, or rollback requirements fail.

Documentation updates:

- Phase 3 dependency and entry-gate text in roadmap
- context and audit boundaries

Recommended subagents:

- worker, reviewer, architecture-checker, verification-checker.

Exit criteria:

- Phase 3 can start from an accepted candidate without designing reusable process behavior inside the corporate environment.

### 2.8 External Release Candidate Acceptance Review

Status: superseded. This draft item will be redistributed in the clean `2.3-2.14` plan required by `D-015`.

Dependency status: superseded. This draft dependency must not be used for implementation.

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
- Clean bootstrap, legacy migration, and packaged minor/major/hotfix rehearsal.
- AI-disabled, Qwen-class, and DeepSeek-class certification for analyst, developer, QA, and Tech Lead authority cases.
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

## Superseded OpenSpec Task Mapping

The table below records the audited draft mapping only. It is retained for traceability and must be replaced by an exact one-owner mapping in the corrected plan.

| Phase 2 work item | OpenSpec task groups |
|---|---|
| 2.1 | 1.1-1.2 |
| 2.2 | 1.3 |
| 2.3A | `adopt-nis-corporate-process-governance` task groups 1-8 |
| 2.3 | `define-transfer-ready-process-package` 2.1-2.5 plus the class/gate integration tasks from 2.3A |
| 2.4 | 3.1-3.5 |
| 2.5 | 4.1-4.5 |
| 2.6 | 5.1-5.4 |
| 2.7 | 6.1-6.4 |
| 2.8 | 7.1-7.4 |

OpenSpec task 7.5 belongs to Phase 3 because it requires successful real corporate adaptation and pilot evidence.

## Phase Gate

Status: blocked. The gate criteria will be finalized with the clean `2.3-2.14` plan after the two open decisions close.

Phase 2 can move to `pending_acceptance` only when:

- work items 2.1-2.7 and 2.3A are closed;
- work item 2.8 verification is complete;
- the external release candidate and manifest are reproducible;
- all deterministic gates pass without AI;
- actual Qwen-class and DeepSeek-class certification evidence exists for minor, major, hotfix, analyst, developer, QA, and Tech Lead flows;
- legacy migration, DoR/DoD separation, under-classification, hotfix safety/reconciliation, Tech Lead authority, stop/resume, release-package, privacy, pilot-safety, and failed-run-retention scenarios pass;
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
- `D-013` accepts the flat NIS target model `minor|major|hotfix`, legacy mapping `thin -> minor` and `full -> major`, class-aware DoR/DoD, Tech Lead governance, corporate flow controls, pilot safety, and failed-run retention. Process-effectiveness measurement is excluded.
- `D-014` accepts two automation horizons: Phase 2 first proves a complete AI-disabled deterministic process; later accepted changes progressively automate bounded process work while deterministic checks remain the control plane and accountable human authority stays explicit.
- `D-015` selects clean sequential renumbering from `2.3`, requires plan acceptance before any Phase 2 implementation, and keeps both active OpenSpec changes open through the Phase 3 pilot.
- Certification evidence storage uses normalized synthetic evidence, manifests, and hashes in Git, with raw outputs in a versioned release artifact referenced by checksum and manifest.
- The human owner makes final Phase 2 release-candidate acceptance using mandatory Tech Lead, QA, and security evidence when applicable.

Open decisions that block the corrected plan and all implementation:

- Certification coverage matrix: choose how actual Qwen-class and DeepSeek-class runs cover three change classes and four roles without either leaving material gaps or requiring an unnecessarily large Cartesian test suite.
  - **A — risk-oriented pairwise matrix (recommended):** eight positive role/model walkthroughs so each model family performs analyst, developer, QA, and Tech Lead work once; distribute minor, major, and hotfix so each class is exercised by both model families; run the critical authority, fabricated-evidence, unsafe-resume, and hotfix-reconciliation negatives on both. This gives direct model/role and model/class evidence with materially less repetition than a full Cartesian matrix.
  - **B — full Cartesian matrix:** 24 positive walkthroughs (`2 model families x 4 roles x 3 classes`) plus the negative suite on both. This gives the strongest direct coverage but increases execution, review, artifact-storage, and maintenance cost substantially.
  - **C — minimal smoke matrix:** one end-to-end governed change per model family, with some roles/classes covered only by AI-disabled fixtures. This is cheapest, but it does not satisfy the current requirement for actual role certification without changing the OpenSpec contract and leaves model-specific gaps.
- Supported external reference runtime: choose the exact clean environment for which Phase 2 promises reproducible bootstrap and certification. Corporate environment compatibility remains a separate Phase 3 responsibility.
  - **A — one pinned Windows reference environment (recommended):** certify the current external workstation family with exact Windows, PowerShell, Python, OpenSpec, Git, and package dependency versions recorded after inventory. This is the narrowest honest support promise and is closest to the expected corporate desktop while leaving real corporate compatibility to Phase 3.
  - **B — Windows and Linux reference matrix:** certify clean bootstrap and the deterministic package on both operating-system families. This improves portability confidence but nearly doubles environment setup, compatibility testing, troubleshooting, and release evidence.
  - **C — container-only reference runtime:** certify one pinned container image. This maximizes reproducibility but may prove little about a restricted Windows corporate desktop where containers or required network/package access are unavailable, so an additional Phase 3 compatibility burden remains.

The old `2.3A-2.8` mapping must not be used for implementation. Once these two decisions are accepted, the plan must be rewritten as `2.3-2.14`, checked for one-owner task coverage and acyclic dependencies, and explicitly accepted before 2.1 can return to `ready`.

Mandatory later evidence, not current design decisions:

- Exact Qwen and DeepSeek model/runtime identifiers used for certification.
- Actual corporate runtime, network, artifact distribution, MCP, and integration capabilities.
- Real Jira/workflow mappings, owner/Tech Lead delegates, security approvers, evidence-retention/privacy rules, and pilot candidate.
- Human acceptance of the external release candidate before Phase 3.
