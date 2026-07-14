# NIS v1.6 Presentation Comparison Report

Date: 2026-07-13
Status: updated on 2026-07-14 for the two-horizon automation, corrected Phase 2 plan, cross-platform target, and reliability/parallel-throughput goal; presentation-ready current comparison.
Normative owner: `D-013`, `D-014`, `D-015`, `D-016`, and the two active OpenSpec changes.

## 1. Executive Summary

NIS does not replace the teamSddCli architecture. Git/OpenSpec remains canonical, Confluence remains a generated publication surface, Jira remains workflow/status, Bitbucket PR remains review/audit, and Jenkins remains deterministic verification.

The automation strategy has two horizons. First, the complete governed process must work without AI; this makes deterministic checks and human decisions the reliability foundation and permanent fallback. After the process and pilot are stable, AI is expected to progressively automate bounded orchestration, drafting, evidence assembly, routing, monitoring, tool coordination, and permitted transition preparation. AI does not gain independent approval, waiver, merge, release, archive, or risk-acceptance authority through that evolution.

The practical target joins reliability and speed. Reliability increases through broader risk-oriented positive and negative testing and end-to-end traceability from requirements and scenarios to tasks, executions, decisions, failures, and evidence. Speed increases when AI decomposes work and executes genuinely independent tasks in parallel with explicit ownership, non-overlapping write scopes, separate evidence, and a deterministic integration gate.

NIS strengthens the operating process with corporate practices that were previously incomplete:

- flat `minor | major | hotfix` classification;
- explicit criteria for when work may start and when it is complete;
- first-class Tech Lead governance and automation support;
- quality strategy and regression ownership;
- scope-drift, stop, hold, escalation, and resume controls;
- release/transfer-package handoff;
- separation of archive, release, and external Done;
- role-understanding evidence;
- bounded pilot safety;
- retention of failed attempts after retry.

The project does not borrow the NIS process-effectiveness evaluation layer. The future process contains no effectiveness scorecard, comparison groups, separate comparison-assurance role, comparison-contamination records, missing-measurement-data rules, sample rules, or outcome thresholds.

## 2. One-Slide Decision

| Question | Decision |
|---|---|
| Does NIS become the architecture? | No. Existing teamSddCli architecture remains authoritative. |
| Does NIS become primary corporate-process input? | Yes. |
| Which classification is accepted? | Flat `minor | major | hotfix`. |
| How is legacy metadata migrated? | `thin -> minor`, `full -> major`; hotfix is never inferred. |
| What is the main operational addition? | Business gates, Tech Lead governance, quality/regression, stop/release controls, and role evidence. |
| What evaluation material is adopted? | None. |
| What single rule is retained from that material? | Failed attempts remain visible after successful retry. |
| Is the NIS team/project structure copied? | No. PPRB organization and NIS repository layout are excluded. |
| Is AI-disabled operation the final product state? | No. It is the first required delivery state and permanent fallback; later accepted changes progressively automate bounded process execution with AI. |
| What is the reliability goal? | Broader risk-oriented tests plus reconstructable requirement/scenario-to-evidence traceability. |
| What is the speed goal? | Safe parallel AI work on independent tasks; conflicting or dependent work remains serialized. |
| Which desktop hosts are supported? | Windows, Linux, and macOS with documented prerequisites and MCP provisioned. |

## 3. What Was Already The Same

| Area | Existing teamSddCli direction | NIS alignment |
|---|---|---|
| Canonical source | Git/OpenSpec owns behavior | Git-centered process and reconstructable evidence |
| Human authority | Humans approve, merge, waive, release, and archive | Named role ownership and decision records |
| AI boundary | The process works without AI; AI may draft and check but cannot own gates | Later AI automation can expand bounded execution while accountable decisions and deterministic verification stay explicit |
| Traceability | Requirement/scenario/change/implementation/test links | End-to-end reconstructability |
| Quality | Scenario-first checks and deterministic validation | Quality strategy and regression discipline |
| Safety | Stop points, waivers, rollback, secret/private-data boundaries | Explicit stop and release controls |
| Portability | Reusable external package before corporate adaptation | Repeatable process package and role guidance |
| Corporate systems | Jira/Confluence/PR/CI remain distinct systems | Cross-system operating flow |

The strongest agreement is architectural: process guarantees cannot depend on one AI model, and accountable humans remain visible.

## 4. What Is Borrowed From NIS

### 4.1 Flat change classification

The target enum is:

```text
minor | major | hotfix
```

#### Minor

Minor is permitted only when all low-impact conditions are known and satisfied. Unknown impact is not minor.

Minor must remain local and small, have simple rollback, and avoid user-scenario, SLA, security/compliance, integration, data-model, component, public-API, cross-repository, reliability, performance, operations, governed-test, governed-documentation, and architecture impact.

#### Major

Major is required when any major trigger exists: feature/business logic, user scenario, component interaction, governed test/documentation obligations, API/integration/data/security/compliance/SLA, dependency/cross-repository, reliability/performance/operations, material regression risk, difficult rollback, or architecture decision.

A major trigger cannot be waived down to minor. Only corrected source evidence followed by recalculation, a stricter route, or a separate accepted policy change can alter the result.

#### Hotfix

Hotfix is justified only when delay increases concrete harm. It accelerates sequence and waiting, not responsibility.

It retains named ownership, minimum scenario/regression/safety evidence, security/compliance checks, rollback/hold, traceability, release-package evidence when releasable, and mandatory reconciliation before closure.

### 4.2 Business gates

The project adopts distinct checkpoints:

1. Preliminary triage.
2. Review ready.
3. Definition of Ready.
4. Implementation complete.
5. Definition of Done.
6. Release/transfer ready when applicable.
7. Archive ready.
8. Archived.
9. External Delivered/Done as an independent external state.

This prevents one word such as “done” from hiding missing verification, release, archive, or receiver acceptance.

### 4.3 Tech Lead governance and automation

The Tech Lead becomes a first-class human role for:

- classification and source-correction review;
- readiness and missing-context control;
- architecture/risk review;
- owner/repository/dependency mapping;
- scope-drift review;
- stop/hold/escalation/resume;
- engineering-completion review;
- release-readiness recommendation;
- waiver expiry and hotfix follow-up.

Automation may generate source-linked review packs, gap reports, stop/resume records, completion/release views, and configurable scheduled or event-driven control reports. It may not approve or impersonate another role.

### 4.4 Corporate flow controls

Borrowed controls include:

- preliminary initiative triage;
- approved input baseline;
- material scope-drift reassessment;
- class-aware quality strategy;
- deterministic regression matrix;
- QA/test-owner sufficiency and result disposition;
- structured deviation, waiver, deferral, stop, hold, escalation, and resume evidence;
- human decision log separated from AI execution evidence;
- versioned release/transfer package;
- receiver acceptance/deviation record;
- portfolio WIP prioritization;
- bounded pilot selection and safety;
- no-fork feedback to the external canonical package.

### 4.5 Portable role model

The reusable role map keeps responsibilities without copying PPRB hierarchy:

| Responsibility | Target owner |
|---|---|
| Business value and scope | Business/product owner |
| Requirements and scenarios | Analyst/product role |
| Engineering design, classification, stop/resume | Tech Lead within authority |
| Implementation and developer verification | Developer |
| Quality strategy and regression disposition | QA/test owner |
| Release/transfer/support | Release or support owner |
| Specialized risk | Architecture, security, or compliance owner when applicable |

Missing human ownership is a blocker; AI cannot fill it.

### 4.6 Failed-run integrity

When validation, AI, adapter, integration, or workflow execution fails, the failed attempt remains source-linked after a successful retry. Both attempts stay identifiable, and required disposition remains visible.

This rule supports traceability, diagnosis, and safety. It is not used to score productivity or process value.

## 5. What Is Adapted Rather Than Copied

| NIS idea | Why direct copying is unsafe | Project adaptation |
|---|---|---|
| NIS as a complete standard | It mixes business process, organization, project layout, and unsafe AI assumptions | Extract portable process behavior into OpenSpec |
| Hard-coded daily/weekly Tech Lead routine | Corporate cadence varies | Configurable scheduled or event-driven checkpoints |
| One team hierarchy | PPRB is a different team | Portable responsibilities plus local owner mapping |
| NIS repository structure | Project topology was already decided | Keep existing central package/config architecture |
| No manual production work | Removes deterministic/human fallback | Human-authored and manual verification remain supported |
| Universal release sequence | Archive and delivery order varies by system | Link the states but do not infer one from the other |
| Project-selection formula | Fixed weights do not transfer safely | Qualitative class/risk/readiness/rollback/privacy selection record |
| Broad rollout sequence | External certification and local safety come first | Phase 2 release candidate, then one bounded Phase 3 pilot |

## 6. What Does Not Match And Is Rejected

### Architecture conflicts

- AI-only production constitution.
- AI approval or correctness authority.
- Mandatory LLM/MCP dependency for process gates.
- PPRB organization and reporting lines as universal roles.
- NIS repository/project layout as target structure.
- Confluence/Jira copies becoming canonical rules.

### Safety conflicts

- “Zero risk” claims.
- Manual work or testing forbidden in production.
- Client delivery without explicit release/rollback ownership.
- Busiest-project-first pilot as a universal default.
- Automatic broad rollout after one bounded pilot.

### Evaluation material excluded by human decision

- process-effectiveness or productivity scoring;
- historical, control, or experimental comparison cohorts;
- separate comparison-assurance ownership;
- comparison-contamination records;
- missing-measurement-data treatment;
- sample, analysis, decision, or rollout thresholds;
- scorecards and outcome-based scale decisions.

Failed-run retention is the sole preserved rule from this excluded material.

## 7. Presentation-Ready Comparison Matrix

| Topic | Already aligned | Borrowed or strengthened | Excluded or corrected |
|---|---|---|---|
| Architecture | Git/OpenSpec canonical, human decisions | Cross-system evidence chain | NIS topology and PPRB hierarchy |
| Classification | Risk-aware change handling | Flat minor/major/hotfix and legacy migration | Lower-class waiver |
| Readiness | Spec Review and approvals | Explicit DoR | AI readiness approval |
| Completion | Verification and archive evidence | Implementation complete, DoD, release, archive, Delivered separation | One overloaded Done state |
| Tech Lead | Human architecture/risk ownership | First-class packs, reports, stop/resume, follow-ups | AI approval impersonation |
| QA | Scenario and evidence orientation | Quality strategy and regression ownership | Separate comparison-control role |
| Release | Traceability and rollback direction | Versioned release package and receiver acceptance | Zero-risk claim |
| Pilot | External release before corporate use | Bounded safety/risk/rollback package | Evaluation program and automatic scale decision |
| Execution history | Source-linked evidence | Failed attempts survive retry | Hiding failed runs |

## 8. Suggested Future Presentation Structure

### Slide 1: Why NIS matters

NIS reflects real corporate delivery and fills gaps in classification, readiness, completion, Tech Lead operations, release handoff, and pilot safety.

### Slide 2: Two automation horizons

Show the near horizon as a complete AI-disabled deterministic process and permanent fallback. Show the later horizon as progressive AI automation of bounded orchestration, evidence assembly, routing, monitoring, and transition preparation, with deterministic verification and human authority retained.

### Slide 3: Reliability and speed target

Show reliability as broader positive/negative coverage plus end-to-end evidence traceability. Show speed as AI-assisted decomposition and parallel execution of independent tasks with separate ownership/evidence and one deterministic integration gate.

### Slide 4: What was already the same

Git/OpenSpec source ownership, human authority, deterministic gates, traceability, and an AI-disabled foundation that later supports bounded AI automation.

### Slide 5: Accepted classification

Show `thin -> minor`, `full -> major`, and hotfix only for increasing concrete harm.

### Slide 6: When work may start

Show triage, fixed input, Spec Review, DoR, owners, quality strategy, regression, risks, and rollback.

### Slide 7: When work is complete

Separate implementation complete, DoD, release ready, archive ready, archived, and external Done.

### Slide 8: Tech Lead automation

Show review packs, source-linked reports, scope/risk control, stop/resume, release recommendation, and follow-up visibility.

### Slide 9: Quality and release package

Show QA-owned strategy/regression and reproducible release/transfer handoff.

### Slide 10: Pilot safety and failed runs

Show bounded risk, rollback/hold, AI-disabled path, operational stop conditions, and the rule that retries never erase failures.

### Slide 11: What is deliberately excluded

Show AI-only production, PPRB/project structure, zero-risk claims, and the entire process-effectiveness evaluation layer.

### Slide 12: Delivery path

Phase 2 builds and certifies the reusable deterministic package; Phase 3 configures it and runs one bounded corporate pilot; later accepted changes progressively automate bounded process execution with AI.

## 9. Current Acceptance And Implementation Status

Accepted direction:

- `D-013` records the flat classification and corporate process boundary;
- `D-014` records the two-horizon automation strategy;
- `D-015` pauses Phase 2 implementation until the corrected plan is accepted and selects clean renumbering from `2.3` onward;
- `D-016` records broader testing/traceability as the reliability direction and safe parallel AI work as the speed direction;
- the NIS package is ignored and untracked;
- the NIS OpenSpec change contains 11 capability deltas and 43 tasks after splitting the Phase 2 external-acceptance stop from Phase 3 corporate configuration and pilot execution;
- the transfer OpenSpec change contains 33 tasks after adding safe-parallel and traceable-coverage work;
- Windows, Linux, and macOS plus the risk-oriented Qwen/DeepSeek matrix are accepted;
- the audited `2.3A-2.8` mapping has been replaced by exact work items `2.3-2.14`; implementation waits for explicit human acceptance of the corrected plan;
- failed-run retention remains a requirement and task.

Not implemented yet:

- schema version 2 and classification migration;
- class-aware artifact matrices and gates;
- Tech Lead workflow reports;
- flow-control and release-package schemas;
- failed-run and pilot-safety evidence;
- certification of the expanded process.

The accepted Phase 1 specs and current validator still represent the legacy implementation baseline until the active change is applied, verified, accepted, synchronized, and archived.

## 10. Evidence And Limitations

This report is based on the local ignored NIS v1.6 package, current project decisions, active OpenSpec changes, Phase 2 planning, and the architecture audit.

It does not claim that proposed behavior is implemented. It also does not preserve or endorse the removed evaluation methodology. Current presentation language must distinguish accepted direction from implemented behavior.

The durable presentation message is:

> NIS supplies realistic corporate process behavior for classification, readiness, completion, Tech Lead control, quality, release, and pilot safety. teamSddCli first proves the whole process without AI, then uses AI to automate and parallelize independent work. Broader risk-oriented tests and end-to-end traceability increase reliability; safe parallel execution increases speed. Deterministic verification remains the control plane, human authority stays explicit, and the process-effectiveness evaluation layer remains excluded.
