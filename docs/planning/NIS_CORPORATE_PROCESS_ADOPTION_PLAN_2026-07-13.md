# NIS Corporate Process Adoption Plan

Date: 2026-07-13
Status: accepted planning direction under `D-013`; proposed behavior remains unimplemented until the active OpenSpec change is applied and accepted.

## 1. Executive Decision

The project uses the approved NIS v1.6 package as primary input for real corporate business-process behavior. The target flat classification is:

```text
minor | major | hotfix
```

Legacy migration is deterministic:

```text
thin -> minor
full -> major
```

Hotfix is never inferred from legacy metadata.

The project adopts NIS-derived business gates, Tech Lead governance, quality and regression ownership, scope and stop controls, release-package handoff, role-understanding evidence, pilot safety, and failed-run retention.

The project does not adopt a process-effectiveness evaluation program. No canonical project contract is created for effectiveness metrics, comparison groups, independent comparison assurance, comparison-contamination accounting, missing-measurement-data rules, sample sizing, outcome thresholds, or scale decisions. The only retained rule from that material is that a failed run remains visible after a successful retry.

## 2. Source Ownership

Git and OpenSpec remain canonical. The local NIS package is research input only and remains git-ignored. It is never imported as a second normative source.

Target behavior is owned by:

- accepted requirements in `openspec/specs/`;
- proposed deltas in `openspec/changes/adopt-nis-corporate-process-governance/` until implementation and promotion;
- versioned process policy/configuration after implementation;
- `docs/DECISIONS.md` for the human decision record.

Role guides, checklists, reports, and future Confluence views must reference canonical requirement IDs or policy versions. They must not restate classification, readiness, approval, or stop rules as independent authority.

## 3. Adoption Matrix

| NIS concept | Decision | Project treatment |
|---|---|---|
| `minor`, `major`, `hotfix` | Adopt | One flat target enum |
| Legacy thin/full terminology | Migrate | `thin -> minor`, `full -> major`; historical records are not rewritten |
| Preliminary initiative triage | Adopt | Proceed, hold, split, redirect, or reject before formal readiness |
| Definition of Ready | Adopt | Separate class-aware gate before implementation approval |
| Implementation complete | Adopt | Engineering-work checkpoint, not final completion |
| Definition of Done | Adopt | Verification and role acceptance checkpoint |
| Release/transfer readiness | Adopt | Separate evidence package for deliverables leaving the team |
| Archive readiness and external Done | Adopt with separation | Neither state is inferred from the other |
| Tech Lead role | Adopt | First-class human owner with bounded authority and deterministic decision support |
| Quality strategy and regression matrix | Adopt | QA/test owner keeps sufficiency and result disposition |
| Fixed input and scope-drift control | Adopt | Material drift triggers reassessment before continuation |
| Stop, hold, escalation, resume | Adopt | Structured records and non-disableable safety minimums |
| Release package | Adopt | Versioned, source-linked handoff evidence |
| Role-understanding walkthrough | Adopt | Scenario-based certification, including negative and AI-disabled cases |
| Human decision and AI execution evidence | Adopt | Human authority is distinct from AI execution |
| Portfolio WIP and pilot selection | Adopt | Operational prioritization and bounded pilot entry |
| Pilot risk register and rollback/hold | Adopt | Honest residual risk; no zero-risk claim |
| Failed-run retention | Adopt | Failed attempts remain source-linked after retry |
| Effectiveness or productivity metrics | Exclude | No project metric dictionary, scorecard, or outcome-evaluation contract |
| Historical/control/experimental comparison design | Exclude | No comparison cohorts or causal-evaluation workflow |
| Independent comparison assurance | Exclude | QA ownership remains; no extra comparison-control role |
| Comparison contamination accounting | Exclude | No comparison-integrity data model |
| Missing measurement data rules | Exclude | No measurement data model to impute or qualify |
| Sample, analysis, rollout, or outcome thresholds | Exclude | No effectiveness decision gates |
| AI-only production constitution | Reject | Deterministic and human/manual fallback remains mandatory |
| “Zero production risk” | Reject | Pilot safety uses explicit risk, stop, rollback, and owner decisions |
| PPRB organization chart | Reject | Only portable responsibilities are retained |
| NIS repository/project structure | Reject | Existing project topology remains authoritative |

## 4. Classification Contract

### Minor

Minor is allowed only when every eligibility condition is satisfied. The change must remain local and small, have a simple rollback, and avoid impact on user scenarios, SLA, security/compliance, external integrations, data models, component interaction, public APIs, cross-repository behavior, reliability, performance, operations, governed tests, governed documentation, and architecture decisions.

Unknown impact is not minor.

### Major

Major is required when any major trigger exists, including feature or business-logic change, user-scenario impact, component interaction, governed test/documentation obligations, public API or integration change, data/security/compliance/SLA impact, external dependency, cross-repository behavior, reliability/performance/operations impact, material regression risk, difficult rollback, or architecture decision.

A major trigger cannot be waived down to minor. The valid paths are audited source correction followed by recalculation, a stricter route, or a separate accepted policy change.

### Hotfix

Hotfix is allowed only when delay increases concrete harm. Convenience, deadline pressure, or incomplete planning is not enough.

Hotfix retains:

- a named human owner;
- minimum scenario, regression, safety, security, and compliance evidence;
- rollback or hold instructions;
- traceability;
- a release package for a releasable result;
- mandatory reconciliation before closure.

## 5. Business Gates

The target business sequence is:

```text
preliminary triage
  -> change package and initial classification
  -> approved input baseline
  -> Spec Review
  -> Definition of Ready and human approval
  -> implementation with scope-drift and stop controls
  -> implementation complete
  -> Definition of Done
  -> release/transfer readiness when applicable
  +-> archive readiness and human archive approval
  \-> configured external delivery/Done evidence
```

Archive and external delivery are independently recorded. Corporate mapping decides their practical order.

## 6. Tech Lead Governance And Automation

The Tech Lead is a first-class human role responsible for bounded technical decisions:

- classification review and source correction;
- readiness and missing-context review;
- architecture/risk review;
- owner, repository, dependency, and affected-zone review;
- stop/hold/escalation/resume decisions inside granted authority;
- engineering-completion review;
- release-readiness recommendation;
- waiver-expiry and hotfix-follow-up visibility.

Automation may prepare source-linked reports, packs, gap lists, and follow-up views. It may not approve, waive, resume, release, merge, archive, or impersonate QA, product, security, or release ownership.

Operational checkpoints may be scheduled or event-driven. Their content and authority boundaries are canonical; cadence remains configuration.

## 7. Corporate Flow Records

The versioned process package will define structured records for:

- initiative triage;
- classification confirmation and audited source correction;
- approved input baseline and material scope change;
- class-aware quality strategy;
- regression matrix and QA/test-owner disposition;
- stop, hold, escalation, resume, deviation, waiver, and hotfix deferral;
- release/transfer package and receiver acceptance;
- human decisions and AI execution evidence;
- role-understanding walkthroughs;
- portfolio WIP and pilot selection;
- pilot safety and risk;
- failed validation, AI, adapter, integration, and workflow attempts.

Exact paths are implementation details owned by the package schema.

## 8. Failed-Run Integrity

Failed-run retention is the only retained rule from the removed evaluation material.

When a validation, AI, adapter, integration, or workflow attempt fails:

- the failure receives source-linked evidence;
- a later successful retry does not overwrite or hide it;
- both attempts remain identifiable with outcome and relevant version/configuration;
- the required human or role disposition remains visible;
- unsafe failures still invoke normal stop, hold, escalation, rollback, or remediation rules.

This evidence is used for traceability, diagnosis, and safety. It is not converted into an effectiveness score.

## 9. Pilot Safety

The monitored corporate pilot remains bounded and reversible. Entry requires an accepted Phase 2 release candidate and a risk record covering privacy, secrets, access, accidental delivery, rollback/hold, integrations, model/runtime behavior, logs, dependencies, support ownership, evidence corruption, and process bypass.

The pilot stops or holds when safety/security authority is exceeded, access or isolation fails, unauthorized delivery is possible, canonical evidence is corrupted, rollback becomes unavailable, or a mandatory failed-run disposition remains unresolved.

Core gates and failed-run handling must work with AI disabled.

## 10. Implementation Sequence

### Stage A: Package and policy foundation

Create the versioned process package, configuration discovery, schema version 2, and canonical policy homes.

### Stage B: Classification and migration

Implement conservative classification, human confirmation/source correction, lower-class rejection, and check/apply migration without rewriting archive history.

### Stage C: Gates and corporate flow

Implement artifact matrices, DoR/DoD, release/archive separation, Tech Lead support, quality/regression, scope/stop controls, decision logs, release packages, and traceability.

### Stage D: Pilot safety and failed-run integrity

Implement failed-attempt evidence, retry preservation, pilot safety templates, risk/rollback/hold controls, and AI-disabled verification.

### Stage E: Certification and external release

Certify minor, major, hotfix, Tech Lead, QA, migration, stop/resume, release, pilot-safety, and failed-run scenarios with deterministic checks, AI disabled, and actual Qwen-class and DeepSeek-class assistants. Stop for human release-candidate acceptance.

### Stage F: Corporate adaptation

Configure real paths, owners, Jira mappings, approved integrations, secret references, evidence retention, model/runtime identifiers, and one bounded pilot. Reusable fixes return to external OpenSpec rather than creating an internal fork.

## 11. Required Corporate Inputs

The reusable design must not guess:

- real Jira/tracker states and transitions;
- project, repository, system, and path mappings;
- owner registry, Tech Lead delegates, and escalation routes;
- class-policy values beyond canonical minimums;
- SLA and response expectations;
- security/compliance approvers;
- approved model/runtime identities and tool availability;
- MCP, integration, and artifact-repository availability;
- evidence-retention, redaction, access, export, and deletion rules;
- pilot candidate and operational owners;
- deployment, support, release, and rollback evidence sources.

Real values belong in approved ignored configuration.

## 12. NIS Source-Coverage Appendix

Every source in the approved local package receives a disposition without importing the package into Git.

| NIS source | Disposition |
|---|---|
| `README.md` | Inventory/audit orientation only |
| `NIS_Clean_v1.6_Standard.md` | Adopt classification, gates, roles, regression, release, safety, and failed-run rule; reject AI-only production and evaluation methodology |
| `NIS_Clean_v1.6_Portfolio_Team_Model.md` | Adopt portable triage, WIP, regression, release, and responsibility semantics; reject organization chart |
| `NIS_Clean_v1.6_Team_Lead_Guide.md` | Adopt bounded Tech Lead responsibilities and configurable checkpoints |
| `NIS_Clean_v1.6_Role_Understanding_Check.md` | Adopt scenario-based portable role verification; exclude comparison-decision roles |
| `NIS_Clean_v1.6_Metrics_Guide.md` | Exclude evaluation content; retain only failed-run integrity where applicable |
| `NIS_Clean_v1.6_Metrics.csv` | Exclude; no target metric schema or thresholds |
| `NIS_Clean_v1.6_Methodological_Basis.md` | Exclude evaluation methodology |
| `NIS_Clean_v1.6_Experiment_Protocol.md` | Adopt only fixed input, operational safety, QA ownership, stop/rollback, and failed-run integrity; exclude comparison design |
| `NIS_Clean_v1.6_Implementation_Plan.md` | Adapt external-release-first sequencing, bounded pilot safety, rollback, and no-fork feedback; exclude evaluation stages |
| `NIS_Clean_v1.6_CTO_Decision_Memo.md` | Retain only human decision ownership and honest risk limitations; exclude score-based conclusions |
| `NIS_Clean_v1.6_Project_Selection.csv` | Retain qualitative pilot-entry considerations; exclude formulas and weights |
| `templates/experiment-card.md` | Retain only bounded pilot scope, owner, risk, rollback, and failed-run evidence |
| `templates/experiment-task.md` | Retain only fixed input, acceptance, owner, result, intervention, and failure evidence |
| `templates/control-branch-protocol.md` | Exclude |
| `templates/ai-execution-log.md` | Adopt source-linked AI execution and failure evidence with privacy/secret limits |
| `templates/cto-decision.md` | Retain accountable human decision structure without evaluation scoring |
| `templates/cto-scorecard.csv` | Exclude |
| `templates/project-selection-checklist.md` | Adapt for class, risk, rollback, privacy, readiness, and exclusions |
| `NIS_CTO_Executive_Deck_v1.6.pptx` | Audit/cross-check only; not normative |
| `NIS_CTO_Executive_Deck_v1.6.pdf` | Audit/cross-check only; not normative |
| Verified deck montage | Audit/cross-check only; not normative |

## 13. Acceptance And Verification

This planning update is consistent only when:

- `D-013`, roadmap, Phase 2, context, audit, OpenSpec, and agent guidance describe the same boundary;
- the `process-measurement-pilot` capability is absent;
- no target document defines effectiveness metrics, comparison groups, independent comparison assurance, contamination handling, missing-measurement-data behavior, sample rules, or decision thresholds;
- failed-run retention remains an explicit requirement and implementation task;
- ordinary QA ownership, DoR/DoD, verification, operational stop/hold, rollback, and pilot-safety controls remain intact;
- PPRB organization and NIS project structure remain excluded;
- `openspec validate --all --strict` passes;
- documentation-wide search and diff checks pass;
- intentional changes are committed.

Implementation acceptance later requires all remaining active-change scenarios and tasks, AI-disabled verification, actual Qwen/DeepSeek certification, migration rehearsal, external release-candidate acceptance, and a bounded monitored corporate pilot.
