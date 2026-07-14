# NIS v1.6 Architecture Compatibility Audit

Date: 2026-07-13
Status: completed and updated after the human scope correction.
Target: local git-ignored `docs/NIS_Clean_v1.6_Approved_Package/` versus accepted teamSddCli architecture and active changes.

## Decision Addendum

The human owner accepted NIS as primary corporate-process input and selected the flat target classification `minor | major | hotfix`, with deterministic legacy migration `thin -> minor` and `full -> major`. Hotfix is never inferred automatically.

The accepted adoption boundary includes business gates, Tech Lead governance, quality/regression ownership, fixed-input and scope-drift control, stop/hold/escalation/resume, release-package handoff, role-understanding evidence, pilot safety, and failed-run retention.

The human owner later removed the entire process-effectiveness evaluation layer from the target and from current project documentation. This audit therefore contains no metric definitions, comparison-group design, independent comparison-assurance design, comparison-contamination accounting, missing-measurement-data rules, sample rules, outcome thresholds, or scale-decision protocol. Failed-run retention is the sole preserved rule from that material.

## Executive Verdict

The NIS package is not a replacement architecture. It combines useful corporate process behavior with organization-specific structure, project-layout assumptions, unsafe AI-only ideas, and an evaluation program that the project does not adopt.

The compatible integration boundary is:

1. Keep teamSddCli architecture and source ownership.
2. Promote portable NIS business-process behavior through OpenSpec.
3. Correct AI authority, manual fallback, safety, and transfer assumptions.
4. Exclude PPRB organization and NIS project structure.
5. Exclude the evaluation layer.
6. Retain failed-run evidence as ordinary traceability and safety evidence.

## Audit Boundary

### Included

- current `AGENTS.md`, roadmap, context, decisions, implementation strategy, Phase 2 plan, current audit, and verification checklist;
- accepted specs in `openspec/specs/`;
- active changes `define-transfer-ready-process-package` and `adopt-nis-corporate-process-governance`;
- all files in the local NIS v1.6 package, including the executive deck render used for visual cross-checking;
- current implementation/test evidence only to distinguish accepted baseline from proposed target behavior.

### Explicitly excluded

- PPRB team performance or organization suitability;
- real corporate identities, repositories, credentials, tracker values, or production configuration;
- NIS repository layout as a target design;
- process-effectiveness evaluation design or conclusions;
- implementation claims for the still-unapplied governance change.

### Criteria

The audit compares:

- canonical source ownership;
- role and authority boundaries;
- classification and lifecycle semantics;
- readiness, completion, release, archive, and delivery separation;
- quality and regression ownership;
- stop, rollback, privacy, and security behavior;
- portability and corporate transfer boundary;
- traceability and failed-run integrity;
- documentation maintainability for humans and weak assistants.

## Evidence Reviewed

### Canonical project sources

- `AGENTS.md`;
- `docs/README.md` and `docs/00_FILE_STRUCTURE.md`;
- `docs/ROADMAP.md`;
- `docs/IMPLEMENTATION_STRATEGY.md`;
- `docs/CONTEXT.md` and `docs/DECISIONS.md`;
- `docs/CURRENT_PROJECT_AUDIT.md`;
- `docs/AI_STEP_VERIFICATION_CHECKLIST.md`;
- `docs/phases/PHASE_2_TRANSFER_READY_PROCESS_PACKAGE.md`;
- accepted and active OpenSpec artifacts.

### NIS source package

The package contains 22 reviewed files/categories: its README, standard, portfolio/team and Tech Lead guides, role-understanding guide, evaluation-oriented files, implementation and decision documents, selection file, pilot/execution/decision/checklist templates, executive deck in PPTX/PDF form, and the verified deck montage.

Evaluation-oriented content was inspected to establish the source boundary but is not reproduced in this current audit. File-by-file dispositions are maintained in `docs/planning/NIS_CORPORATE_PROCESS_ADOPTION_PLAN_2026-07-13.md`.

### Repository treatment

The NIS package remains ignored by `.gitignore` and is not tracked. Its role is evidence input only.

## Accepted Architecture Baseline

The project baseline remains:

- Git/OpenSpec owns canonical behavior;
- Confluence is a generated publication/read model;
- Jira/tracker owns workflow/status, not specification truth;
- Bitbucket PR owns review/audit evidence;
- Jenkins and deterministic scripts own reproducible checks;
- AI prepares drafts, questions, checks, and packs but cannot approve;
- lifecycle, waiver, archive, release, and traceability decisions remain human-owned;
- a reusable externally certified release candidate precedes real corporate adaptation;
- corporate work is real configuration, approved wiring, thin adapters, environment checks, and one bounded pilot;
- reusable corrections return to external OpenSpec instead of forming an internal fork.

## What Directly Aligns

| ID | Alignment | Project anchor |
|---|---|---|
| A-01 | Git-centered, reconstructable process evidence | `D-004`, traceability contract |
| A-02 | Named human responsibilities | owner registry and waiver/lifecycle contracts |
| A-03 | AI execution separated from accountable decisions | `D-003`, transfer-readiness boundary |
| A-04 | Scenario and verification orientation | documentation governance |
| A-05 | Stop and escalation when continuation is unsafe | corporate-flow proposal |
| A-06 | Release handoff needs reproducible evidence | transfer-readiness and release-package proposal |
| A-07 | Role understanding must be demonstrated, not asserted | weak-model certification and role walkthroughs |
| A-08 | Failed attempts must remain visible after retry | traceability and corporate-flow deltas |
| A-09 | Organization-specific details require local mapping | central package plus project adapter architecture |
| A-10 | Reusable process must work without AI | `D-012` and AI-disabled certification |

## What Usefully Complements The Project

| ID | NIS addition | Adopted treatment |
|---|---|---|
| E-01 | Flat `minor|major|hotfix` classification | Canonical target enum with conservative rules |
| E-02 | Preliminary initiative triage | Structured proceed/hold/split/redirect/reject record |
| E-03 | Definition of Ready | Class-aware implementation-entry gate |
| E-04 | Implementation complete versus Definition of Done | Separate engineering and completion checkpoints |
| E-05 | Release/transfer readiness | Separate package and receiver evidence |
| E-06 | First-class Tech Lead workflow | Bounded human authority plus deterministic decision support |
| E-07 | Fixed input and material scope-drift handling | Approved baseline plus mandatory reassessment |
| E-08 | Quality strategy and regression matrix | QA/test-owner sufficiency and result disposition |
| E-09 | Structured stop/hold/escalation/resume | Source-linked records and canonical safety triggers |
| E-10 | Role-understanding walkthroughs | Positive, negative, authority, and AI-disabled scenarios |
| E-11 | Portfolio WIP and pilot selection | Operational prioritization and bounded entry record |
| E-12 | Failed-run integrity | Failure evidence survives retry |

## What Conflicts With Accepted Decisions

| ID | Conflict | Project decision |
|---|---|---|
| C-01 | AI-only production process | Reject; deterministic and human/manual paths remain |
| C-02 | AI-generated decision treated as approval | Reject; named humans own decisions |
| C-03 | Mandatory LLM/MCP dependency | Reject for gates; integrations remain optional/adapted |
| C-04 | Manual authoring or testing forbidden | Reject; manual evidence remains valid where policy allows |
| C-05 | Separate AI checker treated as sufficient quality proof | Reject; QA/test ownership and deterministic evidence remain |
| C-06 | PPRB hierarchy copied as universal role model | Reject; keep portable responsibilities only |
| C-07 | NIS repository/project structure copied | Reject; existing topology remains authoritative |
| C-08 | “Zero production risk” wording | Reject; use explicit risk, residual risk, stop, and rollback |
| C-09 | Broad rollout after a bounded pilot | Reject; later expansion needs a new accepted change |
| C-10 | Duplicated normative rules across guides, decks, and templates | Reject; write once in OpenSpec/policy and reference many |
| C-11 | Process-effectiveness evaluation program | Exclude by human decision |

## Key Findings

### NIS-AUD-001: Foundation boundaries substantially agree

Severity: pass.

Both approaches value traceability, role ownership, controlled transitions, release evidence, and reconstructable work. This supports selective process adoption without replacing the architecture.

### NIS-AUD-002: The NIS production constitution requires safety correction

Severity: high if copied directly.

AI-only and no-manual assumptions conflict with deterministic/AI-disabled guarantees and human correctness ownership. The project explicitly rejects those assumptions.

### NIS-AUD-003: Classification and business gates fill real process gaps

Severity: high opportunity.

The legacy thin/full vocabulary does not model the selected corporate process. The accepted target is flat minor/major/hotfix plus explicit DoR, implementation-complete, DoD, release, archive, and external delivery evidence.

### NIS-AUD-004: Tech Lead must be first-class but bounded

Severity: high opportunity.

Tech Lead responsibilities are useful for classification, readiness, architecture/risk, dependencies, stop/resume, completion, and release recommendation. They must not absorb QA, product, security, release, merge, archive, or tracker authority.

### NIS-AUD-005: QA ownership remains ordinary process governance

Severity: medium.

Quality strategy and regression results require a configured QA/test owner. No separate comparison-control or comparison-assurance role is added.

### NIS-AUD-006: Transfer readiness remains a prerequisite

Severity: high.

The real corporate pilot cannot begin before the reusable package is externally certified, AI-disabled, migration-safe, rollback-capable, and accepted by the human owner.

### NIS-AUD-007: Failed-run retention is independently valuable

Severity: high opportunity.

Successful retry must not erase a failed validation, AI, adapter, integration, or workflow attempt. This becomes normal traceability and pilot-safety evidence, not an evaluation score.

### NIS-AUD-008: Evaluation content is outside target scope

Severity: resolved human decision.

The project does not create data contracts, tasks, gates, or future-phase commitments for process-effectiveness evaluation. Current documentation may state the exclusion but must not retain the removed methodology or values.

### NIS-AUD-009: Documentation must be canonicalized for weak assistants

Severity: high.

Rules repeated independently across role guides, templates, dashboards, and presentations will drift. OpenSpec/policy remains canonical and all derived surfaces must carry source metadata.

### NIS-AUD-010: Organizational conclusions are intentionally not assessed

Severity: excluded.

PPRB is another team. This audit does not judge its staffing, hierarchy, or performance and does not use its project layout as architecture input.

## Recommended Integration Boundary

### Adopt

- minor/major/hotfix classification and legacy migration;
- preliminary triage and approved input;
- DoR, implementation complete, DoD, release, archive, and external Done separation;
- Tech Lead governance and deterministic support;
- QA-owned quality strategy and regression matrix;
- scope-drift, stop/hold/escalation/resume, deviation, and waiver records;
- release/transfer package and receiver acceptance;
- role-understanding and AI-disabled certification;
- portfolio WIP and bounded pilot safety;
- failed-run retention.

### Adapt

- cadence as configuration rather than universal calendar rules;
- roles as portable responsibilities rather than PPRB hierarchy;
- real system mappings as ignored corporate configuration;
- pilot selection as a qualitative operational record rather than a formula;
- generated views as references to canonical OpenSpec/policy.

### Reject Or Exclude

- AI-only production and AI approval;
- prohibition on manual authoring/testing;
- mandatory LLM/MCP gates;
- zero-risk claims;
- NIS project/repository structure;
- PPRB organization structure;
- separate comparison assurance;
- the process-effectiveness evaluation layer;
- automatic broad rollout.

## Sequencing

### Phase 2

Implement package/config foundations, classification migration, business gates, Tech Lead support, corporate flow records, failed-run integrity, pilot-safety templates, deterministic verification, actual Qwen/DeepSeek certification, AI-disabled walkthroughs, update/rollback, release manifest, and transfer acceptance.

### Phase 3

Supply real ignored configuration, wire approved standard integrations, choose one bounded real change, verify rollback/hold and pilot safety, execute the governed flow, preserve failed attempts, and return reusable gaps to external OpenSpec.

### Later work

Add only separately accepted product/process layers. No effectiveness-evaluation phase is planned by this audit.

## Residual Risks And Unknowns

- The governance change is proposed but unimplemented.
- Current validators and accepted specs still reflect the legacy baseline until promotion.
- Real corporate Jira states, owners, integrations, model/runtime identifiers, evidence-retention rules, security approvers, and pilot candidate remain unknown external inputs.
- Actual Qwen-class and DeepSeek-class certification has not yet been run for the expanded process.
- The NIS package may contain organization-specific assumptions not suitable for portable adoption; source coverage therefore remains explicit.

## Remediation Decision

Resolved by the human owner on 2026-07-13 and remapped on 2026-07-14: adopt the repaired NIS corporate process through `adopt-nis-corporate-process-governance` and exact Phase 2 work items 2.3-2.14, using the flat NIS classification and the corporate governance controls above. Exclude process-effectiveness evaluation. Preserve failed-run retention as traceability and safety evidence.
