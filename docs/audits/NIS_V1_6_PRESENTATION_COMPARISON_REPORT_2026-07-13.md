# NIS v1.6 Presentation Comparison Report

Date: 2026-07-13
Status: updated after the human decision to exclude process-effectiveness evaluation; presentation-ready current comparison.
Normative owner: `D-013` and `openspec/changes/adopt-nis-corporate-process-governance/`.

## 1. Executive Summary

NIS does not replace the teamSddCli architecture. Git/OpenSpec remains canonical, Confluence remains a generated publication surface, Jira remains workflow/status, Bitbucket PR remains review/audit, Jenkins remains deterministic verification, and AI remains advisory.

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

## 3. What Was Already The Same

| Area | Existing teamSddCli direction | NIS alignment |
|---|---|---|
| Canonical source | Git/OpenSpec owns behavior | Git-centered process and reconstructable evidence |
| Human authority | Humans approve, merge, waive, release, and archive | Named role ownership and decision records |
| AI boundary | AI drafts and checks but cannot own gates | AI execution is separated from accountable decisions |
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

### Slide 2: What was already the same

Git/OpenSpec source ownership, human authority, deterministic gates, traceability, and AI as assistant.

### Slide 3: Accepted classification

Show `thin -> minor`, `full -> major`, and hotfix only for increasing concrete harm.

### Slide 4: When work may start

Show triage, fixed input, Spec Review, DoR, owners, quality strategy, regression, risks, and rollback.

### Slide 5: When work is complete

Separate implementation complete, DoD, release ready, archive ready, archived, and external Done.

### Slide 6: Tech Lead automation

Show review packs, source-linked reports, scope/risk control, stop/resume, release recommendation, and follow-up visibility.

### Slide 7: Quality and release package

Show QA-owned strategy/regression and reproducible release/transfer handoff.

### Slide 8: Pilot safety and failed runs

Show bounded risk, rollback/hold, AI-disabled path, operational stop conditions, and the rule that retries never erase failures.

### Slide 9: What is deliberately excluded

Show AI-only production, PPRB/project structure, zero-risk claims, and the entire process-effectiveness evaluation layer.

### Slide 10: Delivery path

Phase 2 builds and certifies the reusable package; Phase 3 configures it and runs one bounded corporate pilot; later expansion requires new accepted changes.

## 9. Current Acceptance And Implementation Status

Accepted direction:

- `D-013` records the flat classification and corporate process boundary;
- the NIS package is ignored and untracked;
- the active OpenSpec change contains 11 capability deltas and 42 tasks after removing the evaluation capability;
- Phase 2 work item 2.3A owns implementation;
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

> NIS supplies realistic corporate process behavior for classification, readiness, completion, Tech Lead control, quality, release, and pilot safety. teamSddCli keeps its architecture, human authority, deterministic gates, and transfer boundary. The evaluation layer is excluded; only failed-run retention remains.
