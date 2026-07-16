# Phase 2. Transfer-Ready Process Package And Weak-Model Readiness

Status: in_progress.

Work items 2.1-2.10 are closed after implementation, review hardening, and coordinator verification; work item 2.11 is `in_progress` after adapter `2.1` produced Qwen 2/5 and DeepSeek 0/5 preflight results with zero retries and no matrices. The 2026-07-17 ambiguity audit routes the next bounded remediation through planned change `determinize-weak-model-operational-decisions`. Work item 2.12 remains planned and blocked by 2.11.

> **For implementation workers:** REQUIRED SKILL: use `phase-step-runner` for exactly one work item, or `phase-full-runner` only when the human explicitly requests the whole phase. Within one active work item, independent subtasks may use parallel workers only when dependencies, owners, non-overlapping write scopes, evidence, and integration responsibility are explicit. Every completed work item follows scenario-first TDD, passes review/architecture/verification gates, updates evidence and documentation, and ends with an intentional commit.

## Goal

Build and externally certify a reusable release candidate for the deterministic NIS-aligned `minor | major | hotfix` SDD process. The package must provide equivalent governed behavior on Windows, Linux, and macOS with documented Python, Node.js/OpenSpec, Git, MCP, shell, and package dependencies.

Reliability increases through broader risk-oriented positive and negative test coverage plus end-to-end traceability from requirements and scenarios to tasks, executions, decisions, failures, and verification evidence. Delivery speed increases through AI-assisted decomposition and safe parallel execution of explicitly independent tasks. AI-disabled execution remains the required foundation and fallback; AI never gains approval or accountable human authority by implication.

Phase 2 produces the accepted external release candidate and the adaptation/pilot package. It does not configure real corporate values or execute the Phase 3 pilot.

## Planning Boundary

- Planning is gate-based and contains no delivery dates or calendar deadlines.
- External development owns reusable schemas, deterministic checks, workflow entry points, package/bootstrap/update/rollback behavior, role instructions, read packs, safe-parallel contracts, certification fixtures, cross-platform evidence, release evidence, and runbooks.
- Corporate adaptation owns real non-secret configuration, approved secret references, environment-specific standard-tool wiring, thin AI adapters, and monitored pilot evidence.
- Reusable gaps found during corporate adaptation return to the external OpenSpec workflow; long-lived internal behavior forks are rejected.
- Windows, Linux, and macOS are supported full desktop hosts. Provisioned prerequisites do not replace clean-bootstrap and equivalence evidence on each host.
- Normalized synthetic evidence, manifests, and hashes are stored in Git. Raw certification outputs are stored in a versioned release artifact and referenced by manifest and checksum.
- Both active OpenSpec changes remain open through the Phase 3 pilot. Phase 2 stops at external release-candidate acceptance.
- Jira task automation, Confluence publication, QA/AT proposal generation, role inboxes, deploy, Zephyr integration, graph databases, and broad project-memory automation remain outside Phase 2.

## Dependency Gate

Status: accepted.

- Phase 0 and Phase 1 are `closed`; eight accepted Phase 1 specs are present.
- The external release-candidate boundary, NIS target behavior, two-horizon AI direction, evidence-storage policy, human acceptance owner, certification matrix, and Windows/Linux/macOS host matrix are accepted in `D-012` through `D-016`.
- Active change `define-transfer-ready-process-package` owns the reusable package, weak-model, parallel-execution, coverage, portability, release, and transfer contracts.
- Active change `adopt-nis-corporate-process-governance` owns the NIS-aligned classification, gates, Tech Lead, flow-control, traceability, safety, migration, and acceptance contracts.
- Planned change `determinize-weak-model-operational-decisions` owns the post-`2.1` operational-ambiguity remediation without rewriting the blocked adapter `2.1` history.
- Technical prerequisites and planning acceptance are complete. Work items 2.1-2.10 are closed; work item 2.11 is `in_progress` for bounded weak-model remediation, and 2.12 is blocked by 2.11.

## Planning Acceptance Gate

Status: accepted. Human acceptance is recorded in `D-017` on 2026-07-14.

Acceptance confirms:

- clean sequential work-item numbering `2.1-2.14`;
- exact one-owner mapping for the then-current 33 transfer-package tasks and all 43 NIS-governance tasks;
- no circular Phase 2 dependencies;
- `define-transfer-ready-process-package` task 7.5 and `adopt-nis-corporate-process-governance` task 8.8 remain Phase 3 work;
- safe parallelism is limited to independent subtasks inside an active work item unless a later plan explicitly marks cross-item work `parallel-independent`;
- Phase 2 implementation starts with work item 2.1 after this accepted gate.

The adopted 2026-07-16 change intake adds transfer tasks 4.7-4.9 under work item 2.11. The current exact one-owner mapping therefore covers 36 transfer-package tasks and all 43 NIS-governance tasks without altering the historical planning-acceptance evidence.

## Inputs To Read

- `AGENTS.md`
- `docs/README.md`
- `docs/00_FILE_STRUCTURE.md`
- `docs/ROADMAP.md`
- `docs/IMPLEMENTATION_STRATEGY.md`
- `docs/CONTEXT.md`
- `docs/DECISIONS.md`
- `docs/CURRENT_PROJECT_AUDIT.md`
- `docs/AI_STEP_VERIFICATION_CHECKLIST.md`
- `docs/audits/PHASE_2_PLAN_COMPLETENESS_AUDIT_2026-07-13.md`
- `docs/planning/NIS_CORPORATE_PROCESS_ADOPTION_PLAN_2026-07-13.md`
- accepted specs under `openspec/specs/`
- both active changes under `openspec/changes/`
- existing `templates/change/`, `scripts/validate_change.py`, and `tests/test_validate_change.py`

## OpenSpec And Acceptance Mapping

Accepted baseline:

- `repo-topology-config`: central topology, configuration, package distribution, OpenSpec pin, and owners.
- `documentation-governance`: scenario-first verification, source ownership, durable human feedback, and AI read-pack boundaries.
- `change-package-foundation`, `change-lifecycle`, `change-artifact-contracts`, `traceability-contract`, and `waiver-policy`: current Phase 1 behavior that must be migrated without rewriting accepted history.

Active proposed behavior:

- `define-transfer-ready-process-package`: `transfer-readiness` and `weak-model-guardrails`.
- `adopt-nis-corporate-process-governance`: NIS-aligned classification, gates, Tech Lead governance, flow controls, traceability, safety, migration, certification, and release acceptance.

Phase acceptance evidence must prove:

- deterministic bootstrap, validation, update, rollback, and class-aware governed flow on Windows, Linux, and macOS;
- `thin -> minor`, `full -> major`, no inferred hotfix, no archive rewrite, and safe rollback;
- DoR, implementation-complete, DoD, release readiness, archive readiness, archived, and external Done remain distinct;
- broader positive and negative verification coverage with requirement/scenario-to-evidence mapping and visible residual gaps;
- every gate works with AI disabled;
- the accepted risk-oriented Qwen/DeepSeek certification matrix passes or routes limitations explicitly;
- concurrent AI work is allowed only for independent write scopes and passes focused plus combined integration checks;
- release assets contain no secrets, corporate values, or private source material;
- the human owner accepts the release candidate using Tech Lead and QA evidence plus security evidence when applicable.

## Target Implementation Structure

```text
process/
  VERSION
  package.yaml
  workflow.yaml
  schemas/
  templates/change/
  validators/
  roles/
  adapters/
  certification/fixtures/
  certification/expected/
  certification/negative-cases/

templates/team-specs/
templates/project-adapter/

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
docs/runbooks/
```

Compatibility rules:

- `process/` becomes the reusable package source.
- Existing root entry points remain thin compatibility wrappers until their removal is proposed separately.
- Canonical behavior is not duplicated between wrappers, role instructions, generated views, and OpenSpec.
- Cross-platform differences stay in thin launch/path/shell adapters; policy and evidence contracts remain shared.

## Change Intake

```text
Idea: Close the eight uncovered deterministic NIS feedback/publication-boundary scenarios with focused policy/config validation and exact scenario evidence.
Source: Work item 2.10 second independent review.
Type: bug_fix, verification_change
Decision: adopt_now
Reason: NIS task 8.1 and transfer-package task 4.6 already own focused positive/negative coverage; leaving these scenarios as aggregate gaps makes work item 2.10 acceptance evidence incorrect.
Affected specs: Existing adopt-nis-corporate-process-governance confluence-feedback-loop delta; no new requirement or capability.
Affected architecture: Add only a pure deterministic policy/config boundary and synthetic fixtures; do not implement Confluence integration, publication, remote access, or corporate generated-view selection.
Data contract impact: Add a closed synthetic feedback-policy/evaluation contract with explicit SLA enable/disable, defaults/overrides, dispositions/follow-up, evidence-boundary, source-mode, and generated-view ownership fields.
Verification impact: Eight exact pytest nodes bind one-to-one to the eight delta scenarios, plus negative privacy/schema/package regression and the combined certification coverage gate.
Status: adopted and reconciled through work item 2.10 hardening. The earlier independent review findings were closed, and final semantic remapping and verification were completed by the coordinator after the human requested no further subagent work.
```

```text
Idea: Bind Tech Lead control decisions, time semantics, checkpoints, and finding output to canonical evidence after architecture review.
Source: Phase 2 work item 2.6 architecture findings on 2026-07-14.
Type: bug_fix, architecture_change, data_contract_change, verification_change, documentation_change
Decision: adopt_now
Reason: Leaving any invalid authoritative record able to return clear, comparing timestamp strings/local dates, accepting self-asserted checkpoints, or ignoring the locked finding contract would make the active safety/control work item architecturally incorrect.
Affected specs: adopt-nis-corporate-process-governance tech-lead-workflow delta.
Affected architecture: Check-only Tech Lead validator and its resolved policy/config snapshot; no mutation, daemon, calendar, or inbox boundary changes.
Data contract impact: UTC cutoff provenance, checkpoint owner binding, locked checkpoint definitions, and compiled finding fields.
Verification impact: Adversarial fail-closed, timezone offset/order/tie/cutoff, checkpoint mismatch, and policy-tampering tests plus existing Phase 2 regression gates.
Status: adopted and reconciled through the closed work item 2.6 evidence; no separate scope change remains pending.
```

```text
Idea: Deliver a reusable externally certified process package before corporate adaptation.
Source: Human transfer-readiness decision and D-012.
Type: scope_refinement, architecture_change, verification_change
Decision: adopt_now
Reason: Reusable correctness cannot be left to a constrained corporate environment or weaker assistants.
Affected specs: define-transfer-ready-process-package and accepted Phase 1 baseline.
Affected architecture: External reusable core, thin corporate adaptation, no-fork feedback path.
Data contract impact: Release manifest, read pack, operation evidence, certification, compatibility, and pilot evidence.
Verification impact: Clean bootstrap, AI-disabled and weak-model certification, update/rollback, privacy, and human acceptance.
Status: accepted.
```

```text
Idea: Replace the Phase 1 thin/full target with the real NIS minor/major/hotfix process.
Source: Human decision D-013.
Type: scope_refinement, architecture_change, data_contract_change, verification_change
Decision: create_openspec_change
Reason: Certifying the historical baseline would certify the wrong corporate process.
Affected specs: adopt-nis-corporate-process-governance and modified accepted capabilities.
Affected architecture: Adds class-aware gates, Tech Lead governance, flow controls, safety, and failed-run retention without changing canonical ownership.
Data contract impact: Schema v2, classification, gates, flow, release, decision, AI execution, safety, and failed-run records.
Verification impact: Positive/negative class, migration, gate, authority, stop/resume, hotfix, and release evidence.
Status: accepted.
```

```text
Idea: Repair the Phase 2 plan with clean numbering, exact task ownership, no circular dependencies, and a pre-implementation human gate.
Source: Phase 2 completeness audit and human decision D-015.
Type: planning_change, verification_change, documentation_change
Decision: adopt_now
Reason: The former 2.3A-2.8 draft duplicated ownership and mixed Phase 2 acceptance with Phase 3 pilot work.
Affected specs: Both active changes remain open; task 7.5 and task 8.8 are assigned to Phase 3.
Affected architecture: No scope expansion beyond accepted boundaries.
Data contract impact: Normalized Git evidence plus raw versioned-artifact references/checksums.
Verification impact: Exact one-owner matrix and acyclic dependency audit.
Status: accepted through `D-017`; the corrected plan replaces the former draft mapping.
```

```text
Idea: Support Windows, Linux, and macOS with all required runtimes, dependencies, and MCP provisioned.
Source: Human platform clarification on 2026-07-14.
Type: scope_refinement, architecture_change, verification_change
Decision: adopt_now
Reason: Portability is a release contract, not a best-effort assumption from one workstation.
Affected specs: transfer-readiness portability scenario and release tasks.
Affected architecture: Shared policy/core with thin platform launch/path/shell adapters.
Data contract impact: Manifest records OS, architecture, shell, Python, Node.js/OpenSpec, Git, MCP, dependencies, and limitations.
Verification impact: Equivalent bootstrap, flow, update, rollback, and evidence on all three hosts.
Status: accepted.
```

```text
Idea: Improve reliability through broader tests and traceability, and improve speed through parallel AI work on independent tasks.
Source: Human goal clarification on 2026-07-14; D-016.
Type: architecture_change, verification_change, documentation_change
Decision: adopt_now
Reason: Speed must come from safe decomposition and concurrency while reliability comes from explicit coverage and reconstructable evidence.
Affected specs: weak-model-guardrails safe-parallel requirement; transfer-readiness coverage scenario.
Affected architecture: Concurrent workers use separate task IDs, scopes, evidence, and integration responsibility; shared mutations serialize.
Data contract impact: Parallel task plan/evidence records and requirement/scenario coverage report.
Verification impact: Focused tests per output plus deterministic combined integration checks; uncovered scenarios remain visible with risk and owner.
Status: accepted. This does not reintroduce the process-effectiveness measurement program excluded by D-013.
```

```text
Idea: Repair the pre-existing machine-readable roadmap/OpenSpec ownership contract exposed by the mandatory Phase 2 status audit.
Source: phase-status-audit after work item 2.2 reconciliation.
Type: documentation_change, verification_change
Decision: adopt_now
Reason: The status gate requires zero roadmap/OpenSpec governance-validator errors before sequential Phase 2 execution continues; the repair changes metadata and consumer syntax only.
Affected specs: Metadata only for all eight accepted capability specs and both active proposals.
Affected architecture: None.
Data contract impact: None.
Verification impact: Preserve the 33-error RED baseline, require zero governance-validator errors, run native strict OpenSpec validation, verify status consistency, and run the Git diff check.
Status: accepted for bounded repair. Product behavior, acceptance criteria, implementation tasks, lifecycle states, phase scope, and work-item states remain unchanged.
```

## Work Items

### 2.1 Process Package And Synthetic Central Topology

Status: closed. Implementation, independent task review, architecture review, and fresh verification passed; evidence is recorded in `docs/phases/PHASE_2_EVIDENCE_INDEX.md`.

Dependency status: sequential-start. Phase 1 and the Phase 2 planning gate are accepted; no earlier Phase 2 work item is required.

Objective:

- Create the versioned `process/` skeleton, package/workflow metadata, synthetic central `team-specs` bootstrap, and project-adapter templates.

OpenSpec source: transfer-package tasks 1.1-1.2 and accepted `repo-topology-config`.

Expected files: `process/VERSION`, `process/package.yaml`, `process/workflow.yaml`, base schemas, `templates/team-specs/**`, `templates/project-adapter/**`, and fixture tests.

Verification: schema-first tests; valid clean synthetic topology; negative missing-version, invalid-reference, secret/private-value, and production-looking-placeholder cases.

Parallelization: after the shared package naming and schema conventions are fixed, independent schema/fixture pairs may be assigned to separate workers; one integration owner validates the assembled topology.

Documentation: file structure, setup notes, phase evidence index.

Exit criteria: the synthetic topology is reproducible, versioned, deterministic, and contains no inferred corporate values.

### 2.2 Configuration Discovery And Compatibility Validation

Status: closed. Deterministic implementation, independent task review, architecture review, and fresh verification passed; evidence is recorded in `docs/phases/PHASE_2_EVIDENCE_INDEX.md`.

Dependency status: sequential after 2.1.

Objective: implement central/project configuration discovery, schema validation, OpenSpec `1.4.1` pin checks, package compatibility, and secret rejection.

OpenSpec source: transfer-package task 1.3 and accepted `repo-topology-config` scenarios.

Expected files: config validators, compatibility fixtures, `tests/test_validate_process_config.py`, and thin root entry point.

Verification: central/adapter/sibling layouts, missing registry, invalid owner/project, version mismatch, unsupported topology, private value, and human/JSON diagnostic tests.

Parallelization: positive discovery fixtures and independent negative compatibility fixtures may run in parallel after the discovery precedence contract is fixed.

Documentation: process-package setup and compatibility inventory.

Exit criteria: every gated command can prove compatible configuration before mutation without AI inference.

### 2.3 Policy Schema V2 And Class Foundation

Status: closed.

Implementation, independent task review, architecture review, and fresh verification passed; evidence is recorded in `docs/phases/PHASE_2_EVIDENCE_INDEX.md`.

Dependency status: sequential after 2.2.

Objective: define schema-v2 change metadata and canonical policies for classification, gates, regression, flow controls, release, pilot safety, and failed runs.

OpenSpec source: NIS tasks 1.1-1.4.

Expected files: versioned policy/change schemas plus valid and invalid minor/major/hotfix fixtures.

Verification: schema-first positive/negative tests, policy discovery, unknown/conflicting input, and non-configurable-minimum weakening cases.

Parallelization: independent policy schemas and fixture families may use parallel workers after shared IDs/versioning are fixed; combined schema validation is mandatory.

Documentation: schema inventory, compatibility rules, context terminology.

Exit criteria: one deterministic schema/policy foundation exists for all later class-aware work.

### 2.4 Classification And Legacy Migration

Status: closed.

Dependency status: sequential after 2.3.

Objective: implement conservative minor/major/hotfix classification and idempotent legacy `thin/full` migration without inferring hotfix or rewriting archives.

OpenSpec source: NIS tasks 2.1-2.6.

Expected files: classifier, reports, migration check/apply commands, updated current-facing templates/diagnostics, and migration fixtures/tests.

Verification: minor all-conditions, major any-trigger, harm-based hotfix, under-classification refusal, evidence correction/recalculation, stricter route, check/apply idempotency, conflict refusal, metadata preservation, and no archive rewrite.

Parallelization: classifier reports and migration fixtures may proceed independently after the classification decision contract is tested; apply logic waits for check-mode acceptance.

Documentation: migration runbook and explicit historical-only thin/full references.

Exit criteria: current surfaces offer only minor/major/hotfix and legacy migration is safe and reversible.

### 2.5 Artifact Matrices And Lifecycle Gates

Status: closed.

Dependency status: sequential after 2.4.

Objective: implement class-aware artifact matrices, review readiness, DoR, implementation-complete, DoD, release readiness, archive readiness, and guarded lifecycle transitions.

OpenSpec source: NIS tasks 3.1-3.6.

Expected files: matrix/gate validators, reports, fixtures, and lifecycle transition tests.

Verification: substantive-content, conditional N/A, waiver, hotfix deferral, placeholder, stale evidence, skipped state, unresolved reconciliation, Jira Done, deployment, and AI-completion negative cases.

Parallelization: class-specific matrix fixtures may run in parallel; shared lifecycle-transition logic remains single-owner and integrates all matrices.

Documentation: governed-flow and gate semantics.

Exit criteria: every transition reports exact blocking/advisory evidence and keeps human approval explicit.

### 2.6 Tech Lead Governance

Status: closed.

Dependency status: sequential after 2.5.

Objective: implement Tech Lead ownership, review packs, deterministic reports, stop/hold/escalate/resume records, scheduled/event-driven views, and authority-limit evidence.

OpenSpec source: NIS tasks 4.1-4.6.

Expected files: owners schema extensions, Tech Lead pack/report builders, flow-control validators, role instruction source, and certification fixtures.

Verification: owner/delegate conflicts, under-classification, missing context, unsafe continuation, AI resume/approval prohibition, completion/release recommendation, waiver expiry, and AI-disabled operation.

Parallelization: report views and role fixtures may run in parallel after owner authority and stop/resume schemas close; authority validation has one integration owner.

Documentation: Tech Lead operating guide and escalation model.

Exit criteria: Tech Lead automation reduces evidence search without impersonating decisions or other roles.

### 2.7 Corporate Flow Controls, Safety, And Failed Runs

Status: closed.

Dependency status: sequential after 2.6.

Objective: implement initiative triage, baseline/scope drift, quality/regression, decision/AI evidence, release handoff, role map, WIP, pilot safety, and failed-run retention records.

OpenSpec source: NIS tasks 5.1-5.7 and 6.1-6.2.

Expected files: flow-control, regression, release-package, role-map, WIP, safety, and failed-run schemas/validators/fixtures.

Verification: proceed/hold/split/redirect/reject; scope reassessment; QA coverage gaps; waiver/deferral expiry; stop/resume; external evidence chain; missing-owner AI substitution; WIP hold; privacy/secrets; retry cannot erase failure.

Parallelization: independent record families may use parallel workers after shared IDs and evidence references are fixed; cross-record traceability and stop-trigger integration are serialized.

Documentation: quality, flow-control, release-handoff, pilot-safety, and failed-run guidance.

Exit criteria: governed work is reconstructable from source-linked records and unsafe continuation is deterministically blocked.

### 2.8 Packaged Deterministic Governed Flow

Status: closed.

Dependency status: sequential after 2.7 and requires 2.1-2.2.

Objective: package templates/validators and implement bootstrap, create, Spec PR, archive preparation, update, rollback, traceability, external mapping, and AI-disabled fallbacks.

OpenSpec source: transfer-package tasks 2.1-2.5 and NIS tasks 7.1-7.4.

Expected files: `process/templates/change/**`, packaged validators, root wrappers, workflow scripts, traceability schemas, and end-to-end tests.

Verification: existing 34 tests remain green; red-green entry-point tests; minor/major/hotfix flows; migration; DoR/DoD; update/rollback; unknown external mappings; unavailable Jira/Confluence/model/MCP fallback; no human authority substitution.

Parallelization: command entry points with non-overlapping modules may use parallel workers after shared workflow/state contracts are fixed; one end-to-end integration gate validates the complete flow.

Documentation: setup, governed flow, update/rollback, and integration-boundary runbooks.

Exit criteria: the complete core flow is usable from the versioned package and remains fully executable with AI disabled.

### 2.9 Weak-Model Role Kit And Safe Parallel Execution

Status: closed.

Dependency status: sequential after 2.8.

Objective: implement deterministic role launch/read packs, bounded role instructions/adapters, evidence boundaries, authority checks, and safe parallel-task planning.

OpenSpec source: transfer-package tasks 3.1-3.6.

Expected files: read-pack/evidence/parallel-task schemas, builder/launcher, analyst/developer/QA/Tech Lead instructions, adapters, and negative tests.

Verification: missing/conflicting context, source authority, stop points, unsupported completion, forbidden approval/transition, non-canonical derived output, overlapping write scope, unresolved dependency, separate evidence, and combined integration-gate cases.

Parallelization: role instructions and adapter templates may use separate workers after launcher/read-pack contracts close; shared-source mutation and policy decisions are explicitly serialized.

Documentation: weak-model operating kit and parallel-execution safety guide.

Exit criteria: AI can accelerate bounded independent work while deterministic launch, ownership, evidence, and integration controls prevent races and overreach.

### 2.10 Certification Fixtures, Coverage, And Runner

Status: closed.

Dependency status: sequential after 2.9.

Objective: build synthetic fixtures, golden results, negative cases, certification runner/evidence, and requirement/scenario coverage reporting.

OpenSpec source: transfer-package tasks 4.1-4.3 and 4.6; NIS task 8.1.

Expected files: synthetic repos, role/class/platform fixtures, negative cases, runner, evidence manifest, coverage report, and deterministic tests.

Verification: every applicable scenario maps to an automated test or manual evidence; gaps record owner/risk/compensation/follow-up; raw outputs remain in versioned artifacts; normalized evidence/hashes remain in Git; secrets/private values are absent.

Parallelization: independent class, role, platform, and negative-case fixture families are preferred parallel worker slices; runner and coverage schema have single owners and one combined validation pass.

Documentation: certification evidence format and evidence-storage policy.

Exit criteria: certification is repeatable, source-linked, privacy-safe, and exposes rather than hides verification gaps.

### 2.11 AI-Disabled And Weak-Model Certification

Status: in_progress.

Dependency status: sequential after 2.10.

Objective: preserve the completed AI-disabled and first weak-model baseline, implement the approved bounded Qwen/DeepSeek adapter remediation, and execute new gated certification without weakening deterministic validation.

OpenSpec source: transfer-package tasks 4.4-4.5 and 4.7-4.9; NIS tasks 8.2-8.3.

Expected files: normalized results, manifests/hashes, raw versioned release artifacts, limitation/fallback records, and phase evidence index entries.

Verification: every gate works AI-disabled; role-specific schemas expose only supplied source IDs and global reason codes; reasoning and final output remain separate; normalization cannot repair semantics; at most one structural retry is retained append-only; each family must pass the same-adapter 5/5 preflight before its 15/15 matrix may start; all existing authority, evidence, source, stop, and lifecycle checks remain unchanged.

Parallelization: independent model/role/class runs may execute concurrently when isolated workspaces and evidence paths are declared; shared fixture mutation and final result disposition are serialized.

Documentation: exact model/runtime/adapter versions, interventions, limitations, and fallbacks.

Exit criteria: Qwen and DeepSeek each pass 5/5 preflight and 15/15 matrix with the approved adapter boundary, or the exact residual incompatibility is recorded and returned for a new human disposition; fallback-only acceptance is not the current approved route.

Historical baseline evidence on 2026-07-15: all 11 AI-disabled walkthrough records passed. Frozen non-leading Qwen-family bytes passed 0/5 preflight and 1/15 matrix cases; frozen DeepSeek-family bytes passed 0/5 preflight and 0/15 matrix cases. Every failure retains deterministic validation plus a catalog-owned case-specific human owner and concrete disposition action. Transfer task 4.5 and NIS task 8.3 remain checked as execution-complete historical baseline work and are not reopened or rewritten.

Adapter `2.1` outcome on 2026-07-16: decision-dependent `draft` and `block`
branches, restricted model check results, version-bound runtime evidence,
exclusive result creation, and immutable adapter `1.0`/`2.0` compatibility were
implemented and reviewed before execution. With Ollama `0.30.11`, frozen
`qwen3.5:9b` passed 2/5 preflight cases and frozen `deepseek-r1:8b` passed 0/5.
All ten responses were structurally valid on attempt 1, so no retry was allowed;
both gates failed and neither matrix ran. The fresh AI-disabled regression
passed 11/11. Transfer progress remains 22/36; task 4.9 remains open,
fallback-only acceptance remains superseded, and the exact outcome is recorded
in
`docs/audits/PHASE_2_WORK_ITEM_2_11_ADAPTER_2_1_AUDIT_2026-07-16.md`.

#### Phase Change Intake: Weak-Model Adapter Remediation

```text
Idea: Remediate the weak-model adapter so Qwen- and DeepSeek-family assistants can reliably produce bounded role output without weakening deterministic authority or safety checks.
Source: Human rejection of fallback-only acceptance after Phase 2 work item 2.11 certification results, confirmed on 2026-07-16.
Type: scope_refinement, architecture_change, data_contract_change, verification_change, documentation_change
Decision: adopt_now
Reason: Accepting the current fallback dispositions would leave the internal AI layer ineffective and would make the intended work item 2.11 outcome incorrect for the human's stated product goal.
Affected specs: Existing define-transfer-ready-process-package weak-model-guardrails delta and its certification tasks; no independent capability is introduced.
Affected architecture: Add a thin model-family generation adapter, role-specific constrained response contracts, reasoning/final separation, and mechanical normalization ahead of the unchanged deterministic validator.
Data contract impact: Replace the model-facing all-role compact envelope with a generated common decision envelope plus one role-specific payload; preserve the existing normalized operation-evidence contract downstream.
Verification impact: Require adapter-focused TDD, negative authority/evidence/source tests, append-only retry evidence, 5/5 preflight for each model family before its matrix, and 15/15 matrix completion for both families.
Status: adopted; adapter `2.0` and `2.1` implementations were reviewed before execution. Task 4.9 remains open after adapter `2.1` produced Qwen 2/5 and DeepSeek 0/5 with no matrices, and work item 2.11 remains `in_progress`.
```

#### Phase Change Intake: Deterministic Operational Decision Plan

```text
Idea: Reduce Phase 2.11 operational error by moving deterministic policy and routing metadata out of weak-model generation.
Source: Human request on 2026-07-17 and docs/audits/PHASE_2_WORK_ITEM_2_11_OPERATIONAL_AMBIGUITY_AUDIT_2026-07-17.md.
Type: architecture_change, data_contract_change, verification_change, documentation_change
Decision: create_openspec_change
Reason: Adapter 2.1 made the JSON shape unambiguous, but the current gate still contains hidden exact policy labels, source-manifest repetition, ambiguous draft sufficiency, and a field-blind authority heuristic. Another prompt-only revision would not isolate or minimize operational error.
Affected specs: New weak-model-operational-decision-plan capability; existing transfer-readiness weak-model objectives remain active.
Affected architecture: Add an identity-bound deterministic operation plan before the model call; model produces only source-grounded draft content or a planned block explanation.
Data contract impact: Launcher owns action, artifact kind, reason codes, required source inventory, and human action codes; model content uses a smaller branch-specific schema.
Verification impact: Add ambiguity regression fixtures, deterministic policy-projection evidence, field-scoped authority tests, actual Qwen/DeepSeek 5/5 then 15/15 gates, and AI-disabled 11/11.
Status: planned in openspec/changes/determinize-weak-model-operational-decisions/.
```

#### Planned Work Item 2.11 Remediation Slice

OpenSpec source:

- `openspec/changes/determinize-weak-model-operational-decisions/`

Objective:

- make the supported weak-model operation deterministic before generation;
- remove model ownership of machine reason codes, full source inventory,
  artifact routing, and human action codes;
- preserve claim-level source grounding and all authority/evidence safety gates;
- rerun the same frozen Qwen and DeepSeek proxies without increasing the model.

Implementation order:

1. Reproduce the ambiguity findings with focused RED tests.
2. Add the smallest operation-plan schema and predicates for the frozen
   supported catalog; unknown cases fail to the named human.
3. Replace policy-selection output with `draft_content` or `blocked_summary`.
4. Scope authority validation to structured action fields and model-authored
   claims; attach launcher provenance mechanically.
5. Run deterministic verification, then append-only 5/5 preflight and gated
   15/15 matrices, followed by AI-disabled 11/11.
6. Reconcile work item 2.11 from actual evidence.

Explicitly rejected as disproportionate:

- semantic retries or self-critique loops;
- another classifier agent;
- fuzzy or embedding-based semantic acceptance;
- expanding the reason-code taxonomy;
- a new maintained role/process documentation hierarchy;
- a general-purpose policy rules engine.

Exit criteria:

- identical verified inputs produce byte-stable operation policy metadata;
- every model-owned acceptance obligation is visible and locally diagnosed;
- zero accepted unsafe continuation, fabricated evidence, model-owned authority,
  canonical mutation, or operation-plan override;
- safe descriptions of pending human approval/resume/release/archive decisions
  do not trigger false authority failures;
- each family passes 5/5 preflight before 15/15 matrix, and AI-disabled remains
  11/11;
- otherwise work item 2.11 remains `in_progress` with exact residual
  incompatibility and fallback evidence.

### 2.12 Cross-Platform Release Candidate And Rollback

Status: planned.

Dependency status: blocked by in-progress work item 2.11; sequential after 2.11 and requires 2.2 and 2.8.

Objective: generate/validate the release manifest, automate acceptance checks, rehearse migration/update/rollback, and prove equivalent Windows/Linux/macOS behavior.

OpenSpec source: transfer-package tasks 5.1-5.4; NIS task 8.4.

Expected files: release-manifest generator/validator, platform launch adapters, setup/update/rollback runbooks, platform evidence, checksums, and release artifact.

Verification: clean bootstrap, deterministic flow, MCP connectivity, OpenSpec/Git/Python/Node dependencies, migration, idempotency, update, rollback/hold, no archive rewrite, evidence equivalence, and missing/stale/failed/private/AI-only evidence rejection on all three hosts.

Parallelization: Windows, Linux, and macOS rehearsals may run concurrently from the same immutable candidate; candidate construction and final manifest acceptance remain single-owner.

Documentation: installation, platform inventory, compatibility, update, rollback, secrets, adapters, and no-fork feedback.

Exit criteria: one immutable candidate produces equivalent governed results on all supported hosts and can be rolled back safely.

### 2.13 Corporate Adaptation And Pilot Package

Status: planned.

Dependency status: sequential after 2.12.

Objective: prepare non-secret environment inventory, real-configuration/pilot-entry checklists, monitored-pilot evidence template, and external feedback/no-fork checks without executing the pilot.

OpenSpec source: transfer-package tasks 6.1-6.4.

Expected files: corporate inventory, adaptation, pilot-entry, pilot-evidence, rollback/hold, and no-fork templates/runbooks.

Verification: templates cover runtimes, package distribution, network, Bitbucket/Jenkins/Jira/Confluence, MCP, models/adapters, owners/projects, secrets, rollback, AI-disabled gates, failures, interventions, privacy, and follow-up changes.

Parallelization: inventory, entry checklist, and pilot evidence template may use separate workers against one accepted schema/source map; final no-fork and completeness review is combined.

Documentation: corporate adaptation and governed pilot runbooks.

Exit criteria: Phase 3 can configure and pilot without inventing reusable behavior or storing real corporate values in the external package.

### 2.14 Documentation, Final Verification, And Human Acceptance

Status: planned.

Dependency status: sequential-final after 2.1-2.13.

Objective: reconcile documentation/statuses, run complete verification, assemble the acceptance packet, complete review gates, and stop for human-owner acceptance.

OpenSpec source: transfer-package tasks 7.1-7.4; NIS tasks 8.5-8.7.

Expected files: current docs/audit/roadmap, phase evidence index, manifest, runbooks, review records, coverage/traceability report, limitations, and acceptance packet.

Verification: focused/full tests; package/config/template validation; coverage/traceability; Windows/Linux/macOS evidence; AI-disabled and weak-model certification; privacy/secret scan; documentation-sync audit; `openspec list`; `openspec list --specs`; `openspec validate --all --strict`; `git diff --check`; worker/reviewer/architecture/verification gates.

Parallelization: documentation review, architecture review, and verification evidence audit may run concurrently against the frozen candidate; fixes serialize through one integration owner and require re-verification.

Documentation: all affected project, role, setup, operations, roadmap, audit, and presentation-facing material.

Exit criteria: the human owner accepts or rejects the exact external candidate using mandatory Tech Lead and QA evidence plus security evidence when applicable. No corporate pilot begins before acceptance.

## Exact OpenSpec Task Mapping

| Phase 2 work item | `define-transfer-ready-process-package` | `adopt-nis-corporate-process-governance` |
|---|---|---|
| 2.1 | 1.1-1.2 | - |
| 2.2 | 1.3 | - |
| 2.3 | - | 1.1-1.4 |
| 2.4 | - | 2.1-2.6 |
| 2.5 | - | 3.1-3.6 |
| 2.6 | - | 4.1-4.6 |
| 2.7 | - | 5.1-5.7, 6.1-6.2 |
| 2.8 | 2.1-2.5 | 7.1-7.4 |
| 2.9 | 3.1-3.6 | - |
| 2.10 | 4.1-4.3, 4.6 | 8.1 |
| 2.11 | 4.4-4.5, 4.7-4.9 | 8.2-8.3 |
| 2.12 | 5.1-5.4 | 8.4 |
| 2.13 | 6.1-6.4 | - |
| 2.14 | 7.1-7.4 | 8.5-8.7 |
| Phase 3 | 7.5 | 8.8 |

Coverage check:

- Transfer-package tasks: 36 total; 35 map exactly once to Phase 2 and task 7.5 maps exactly once to Phase 3.
- NIS-governance tasks: 43 total; 42 map exactly once to Phase 2 and task 8.8 maps exactly once to Phase 3.
- No task group is owned by more than one Phase 2 work item.
- No Phase 2 work item depends on Phase 3 evidence for closure.

## Dependency Sequence

```text
Planning acceptance
  -> 2.1 -> 2.2 -> 2.3 -> 2.4 -> 2.5 -> 2.6 -> 2.7
  -> 2.8 -> 2.9 -> 2.10 -> 2.11 -> 2.12 -> 2.13 -> 2.14
  -> human release-candidate acceptance
  -> Phase 3 adaptation and pilot
```

This sequence controls canonical work-item integration. It does not forbid safe parallel workers inside an active item where the item explicitly identifies independent slices.

## Phase Gate

Status: planned.

Phase 2 can move to `pending_acceptance` only when:

- work items 2.1-2.13 are `closed` and 2.14 verification is complete;
- the exact immutable release candidate, manifest, raw artifact, hashes, and rollback reference are reproducible;
- Windows, Linux, and macOS clean-host evidence proves equivalent governed behavior;
- all deterministic gates pass with AI disabled;
- risk-oriented Qwen/DeepSeek certification and negative authority/safety cases are complete;
- broader positive/negative coverage is linked to requirements/scenarios and residual gaps are explicit;
- safe parallel-execution contracts and combined integration gates pass positive and negative cases;
- migration, gates, Tech Lead authority, flow controls, hotfix reconciliation, privacy, safety, and failed-run retention pass;
- adaptation/pilot materials are complete and contain no real corporate values;
- roadmap, audit, phase status, OpenSpec status, docs, tests, and evidence agree.

Phase 2 becomes `closed` only after explicit human acceptance of the external release candidate. Both active OpenSpec changes remain open for Phase 3 pilot evidence; Phase 3 must not use an unaccepted candidate.

## Human Decisions

Resolved:

- `D-012`: external transfer-ready candidate before corporate adaptation; no delivery dates in durable phase planning.
- `D-013`: NIS-aligned minor/major/hotfix target, migration, gates, Tech Lead governance, flow/safety controls, failed-run retention, and no process-effectiveness measurement program.
- `D-014`: deterministic/AI-disabled foundation first, progressive bounded AI automation later.
- `D-015`: clean numbering, plan-first acceptance, both changes open through Phase 3, normalized/raw evidence split, human-owner final acceptance, risk-oriented certification matrix, and Windows/Linux/macOS support with provisioned prerequisites and MCP.
- `D-016`: reliability through broader tests and traceability; speed through safe parallel AI work on independent tasks.
- `D-017`: the human owner accepts this corrected Phase 2 plan and authorizes sequential implementation beginning with work item 2.1.

The AI-disabled, Qwen-family, and actual DeepSeek-family runtime/matrix execution from 2026-07-15 remains the immutable first baseline. The adapter `2.0` remediation and adapter `2.1` follow-up are also append-only evidence. Adapter `2.1` produced Qwen 2/5 and DeepSeek 0/5 with zero retries and no matrices, so 2.11 remains `in_progress` and 2.12 remains planned and blocked.

Mandatory later evidence, not design decisions:

- Any later append-only Qwen-class and DeepSeek-class remediation evidence: 5/5 frozen preflight before each 15/15 matrix, with a new human-approved remediation scope required before another run.
- Exact supported Windows, Linux, and macOS versions/architectures and dependency versions used for certification.
- Actual corporate configuration, network/artifact distribution, MCP and integration capabilities, owners/delegates/security approvers, retention/privacy values, and pilot candidate.
- Human acceptance of the external release candidate before Phase 3.
