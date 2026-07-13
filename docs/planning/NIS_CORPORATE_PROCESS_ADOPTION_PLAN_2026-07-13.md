# NIS Corporate Process Adoption Plan

Status: accepted planning direction; normative behavior is proposed in `openspec/changes/adopt-nis-corporate-process-governance/` and remains unimplemented until that change is applied and accepted.

Decision owner: human project owner.

Decision date: 2026-07-13.

Evidence base: the local git-ignored `docs/NIS_Clean_v1.6_Approved_Package/`, the compatibility audit in `docs/audits/NIS_V1_6_ARCHITECTURE_COMPATIBILITY_AUDIT_2026-07-13.md`, accepted project specs, the active transfer-readiness change, and the human clarification that the NIS package reflects the target corporate processes.

## 1. Executive Decision

The project will adopt the NIS corporate process model as a primary business-process input rather than treating it only as experimental research. The target process classification is the flat NIS model:

```text
minor | major | hotfix
```

This explicitly supersedes the target `thin | full` vocabulary. Existing non-archived data migrates conservatively as `thin -> minor` and `full -> major`; no legacy value becomes `hotfix` automatically. Historical accepted and archived artifacts are not rewritten.

The project will also adopt and normalize the real-work controls documented across NIS: preliminary triage, readiness for implementation, completion and release readiness, Tech Lead governance, quality strategy, regression planning, fixed-input/scope-change control, stop/hold/escalation/resume behavior, release-package handoff, role-understanding verification, decision and AI-run evidence, flow-time separation, portfolio/pilot controls, and outcome measurement.

The adoption is not a verbatim import. NIS contains inconsistent thresholds, duplicated normative rules, experiment-only restrictions, organizational assumptions, and absolute safety claims that cannot become deterministic production guarantees. Those elements are corrected through one canonical OpenSpec contract while the useful corporate process is preserved.

## 2. Source-Ownership Rule

This document explains the adoption and implementation sequence. It does not duplicate the final normative wording.

- Canonical proposed behavior: `openspec/changes/adopt-nis-corporate-process-governance/specs/`.
- Architecture and migration rationale: `openspec/changes/adopt-nis-corporate-process-governance/design.md`.
- Executable implementation backlog: `openspec/changes/adopt-nis-corporate-process-governance/tasks.md`.
- Evidence-backed source comparison and unresolved source inconsistencies: `docs/audits/NIS_V1_6_ARCHITECTURE_COMPATIBILITY_AUDIT_2026-07-13.md`.
- Accepted current behavior until promotion: `openspec/specs/`.
- Human decision: `D-013` in `docs/DECISIONS.md`.

Role guides, checklists, dashboards, scorecards, Confluence views, and prompts must reference canonical requirement IDs or policy versions. They must not become independent places where classification criteria, gates, thresholds, or approval rules drift.

## 3. Complete Adoption Matrix

| NIS-derived process element | Project decision | Normalization or correction | Canonical target |
|---|---|---|---|
| `minor`, `major`, `hotfix` classification | Adopt as the target flat model | Replace `thin/full`; keep work type, lifecycle status, and risk evidence separate | `corporate-change-classification` |
| Minor criteria | Adopt | Minor is allowed only when every low-impact condition is known and satisfied | `corporate-change-classification` |
| Major criteria | Adopt | Any material trigger requires major unless urgent work uses hotfix while retaining impact obligations | `corporate-change-classification` |
| Hotfix route | Adopt | Acceleration shortens sequence and waiting, not safety, ownership, traceability, rollback, or reconciliation | `corporate-change-classification`, `waiver-policy` |
| Preliminary initiative triage | Adopt | Triage is a proceed/hold/split/redirect/reject input, not implementation approval | `corporate-flow-controls` |
| Criteria for ready-to-implement | Adopt as Definition of Ready | Use one common gate plus class-specific evidence and explicit human approval | `readiness-completion-gates` |
| Criteria for completed work | Adopt and split | Separate implementation complete, Definition of Done, release/transfer ready, archive ready, archived, and externally delivered/Done | `readiness-completion-gates`, `change-lifecycle` |
| Tech Lead process ownership | Adopt as first-class role | Bound authority; do not let Tech Lead replace product, QA, security, release, merge, or archive owners | `tech-lead-workflow`, `repo-topology-config` |
| Tech Lead automation | Adopt | Automate evidence collection, reports, review packs, gaps, follow-ups, and recommendations; never automate accountable approval through AI | `tech-lead-workflow` |
| Fixed input and scope-change control | Adopt | Record baseline and re-run class/readiness/owner/regression decisions on material drift | `corporate-flow-controls` |
| Quality strategy before implementation | Adopt | Class-aware; hotfix may defer only permitted non-safety planning and must reconcile it | `corporate-flow-controls`, `readiness-completion-gates` |
| Regression matrix | Adopt | Make it a typed source-linked matrix, not a free-text checklist | `corporate-flow-controls`, `change-artifact-contracts` |
| Stop/hold/escalation/resume | Adopt | Use structured triggers, evidence, owners, immediate action, response route, and resume conditions | `corporate-flow-controls`, `tech-lead-workflow` |
| Deviation and exception handling | Adopt | Integrate with waivers, expiry, residual risk, and separate resume decisions | `waiver-policy`, `corporate-flow-controls` |
| Release-package handoff | Adopt | Versioned reproducible handoff with canonical scope, verification, limitations, operations, rollback, and receiver evidence | `corporate-flow-controls`, `readiness-completion-gates` |
| Human decision log | Adopt | Keep accountable decisions distinct from AI output and generated status | `corporate-flow-controls`, `traceability-contract` |
| AI execution/certification evidence | Adopt | Record runtime/tool/input/output/reviewer/failure evidence without secrets; AI remains advisory | `corporate-flow-controls`, `process-measurement-pilot` |
| Role-understanding checks | Adopt | Require scenario walkthroughs and negative/authority cases; checklist-only completion is insufficient | `corporate-flow-controls`, `tech-lead-workflow` |
| Controlled versus external time | Adopt | Preserve total cycle and separately attribute active, automated, queue, review, external wait, and handoff intervals | `corporate-flow-controls`, `process-measurement-pilot` |
| Portfolio WIP/context switching | Adopt as a planned control | Require explicit limit/config and prioritization/hold decision; do not guess a universal threshold | `corporate-flow-controls` |
| Pilot/project selection | Adopt | Require representativeness, risk, rollback, comparator, and exclusions; avoid PPRB structure assumptions | `corporate-flow-controls`, `process-measurement-pilot` |
| Cycle time, human effort, cost, acceptance, defects, completeness, intervention, repeatability | Adopt | Define exact events, denominators, provenance, missing data, privacy, and decision thresholds before collection | `process-measurement-pilot` |
| Post-pilot delivery stability | Adopt | Select applicable DORA-like or equivalent measures only when real deployment/support data exists | `process-measurement-pilot` |
| AI-heavy/no-manual experiment | Retain only as an optional isolated treatment | Never make it the production constitution or remove the manual/AI-disabled fallback | `process-measurement-pilot` |
| “Zero production risk” | Reject as a guarantee | Use a bounded risk register, stop/rollback controls, residual-risk acceptance, and honest limitations | `process-measurement-pilot` |
| Repeated NIS thresholds and formulas | Normalize before use | One versioned metric/policy source; thresholds are configured and approved before a pilot | `process-measurement-pilot`, `repo-topology-config` |
| PPRB-specific team, cluster, direction, or reporting model | Exclude | The user identified PPRB as another team; retain only portable process semantics | All target capabilities |
| NIS repository/project structure | Exclude as an architecture source | The project already has an accepted topology and transfer boundary | `repo-topology-config` remains authoritative |

### 3.1 Portable role mapping

NIS describes responsibilities that are useful even though its concrete organization is not ours. The reusable process will therefore require a local mapping for these responsibility groups:

| Portable responsibility | Target ownership |
|---|---|
| Business goal, value, scope, and product acceptance | Business/product owner or approved equivalent |
| Technical class, readiness, architecture/risk coordination, stop/resume, engineering completion, release recommendation | Tech Lead, with architect/security participation when triggered |
| Requirements, scenarios, scope baseline, feedback disposition, and traceability | Analyst/change owner |
| Implementation and developer evidence | Developer/implementation owner |
| Quality strategy, regression matrix, test evidence, and defect disposition | QA/test owner; AT owner where automation is separately governed |
| Release package, transfer/deployment instructions, operational checks, rollback, and support handoff | Release/deployment/support owner |
| Independent comparison or assurance evidence when a controlled experiment is used | Control/assurance role with access and independence recorded |
| Scale, continue, revise/repeat, hold, or stop decision for the process/pilot | Configured process decision owner, such as CTO/process sponsor, never AI |

Missing human ownership is a blocker, not an invitation to assign the decision to AI. PPRB clusters, directions, temporary-group membership, and reporting lines are not portable defaults.

### 3.2 System-of-record mapping

The NIS end-to-end evidence chain usefully reinforces the accepted architecture without replacing its topology:

```text
tracker item/status
  -> Git/OpenSpec change, requirements, scenarios, and decisions
  -> implementation commit/PR
  -> CI and test evidence
  -> immutable artifact-repository coordinate when applicable
  -> release/transfer package and rollback/support instructions
  -> configured external delivery/Done evidence
```

Nexus is treated as one possible corporate artifact repository, not a mandatory external-development product choice. If the real repository or integration is unavailable, the gap and approved substitute evidence remain explicit. Full corporate payloads are referenced by stable identifiers rather than copied into every system.

### 3.3 Controlled experiment subset

The target production process does not require duplicate implementation of every change. When a paired NIS-style experiment is separately approved, it adopts the useful integrity rules: same fixed input and source baseline, predefined acceptance set and allowed differences, isolation between treatment and control, independent assurance ownership, explicit input-change/comparability decisions, automatic event collection where possible, and contamination disclosure. A bounded safety pilot may instead use historical or another approved comparator when duplicate implementation would add excessive cost, delay, or data exposure.

Pilot stop/hold conditions include unapproved branch-input divergence, treatment leakage into control, failed metric collection, isolation/access failure, safety/security risk outside current authority, corrupted evidence, unavailable rollback, or materially lost comparability. Decision outcomes are explicit: scale, bounded rollout, continue collection, revise and repeat, hold, or stop.

## 4. Target Classification

### 4.1 Minor

Minor is a governed low-impact route, not merely a small estimate. It is allowed only when all required conditions are positively known: the change is local and small; rollback is simple; and there is no user-scenario, SLA, security/compliance, external-integration, data-model, component-interaction, public-API, cross-repository, reliability, performance, operations, governed-test, or governed user/operational-documentation impact and no architecture decision requirement.

Unknown information is not interpreted as low risk. If a required condition is unknown, the package is not ready for a minor decision.

### 4.2 Major

Major is required when any material trigger applies: new feature; changed business logic, user scenario, component interaction, required test behavior, or governed user/operational documentation; public contract/integration/data/security/compliance/SLA impact; external dependency; cross-repository change; significant reliability/performance/operations impact; regression risk; high rollback cost; or an architecture decision.

This is conservative by design. The classifier reports all triggers, not just the first one, so reviewers see the real obligation set.

### 4.3 Hotfix

Hotfix is a third flat class because that is the selected NIS process model. It applies when waiting creates increasing concrete harm and the change needs an accelerated path. It is not a synonym for minor, urgent business preference, or reduced documentation.

The hotfix route must preserve:

- named human decision ownership;
- harm and urgency rationale;
- bounded scope and affected contour;
- at least one testable scenario and minimum regression evidence;
- mandatory security/compliance decisions when triggered;
- rollback or hold instructions;
- traceability and source-linked implementation evidence;
- major-impact obligations made visible when the hotfix also has major impact;
- a mandatory reconciliation/follow-up record for permitted deferred artifacts;
- closure blocking while required reconciliation is unresolved.

### 4.4 Confirmation, correction, and stricter routing

AI may propose a class and deterministic tooling calculates the governed result, but an authorized human confirms the canonical value. A major trigger cannot be waived or overridden to minor for one change. If the source fact is wrong, the human corrects the evidence with reason and provenance and runs classification again. Uncertainty or local policy may select a stricter route. Changing a canonical criterion requires a separate reviewed and accepted versioned policy/OpenSpec change. Urgency uses hotfix only when its harm rule is satisfied; it is not a lower-class override.

## 5. Ready for Implementation: Definition of Ready

The point at which a task is ready for implementation is the `spec_review -> approved` gate, not the existence of a ticket or an AI-generated design.

The common Definition of Ready includes:

- business goal and expected value;
- accountable owner;
- scope and explicit exclusions;
- work type, class, rationale, and classifier evidence;
- affected systems, repositories, owner zones, and dependencies;
- requirements, testable scenarios, and acceptance criteria;
- quality and verification strategy;
- security, data, compliance, operations, reliability, and performance assessment as applicable;
- regression approach and required environments/data;
- rollback or hold approach;
- initial traceability;
- resolved blocking questions;
- valid waivers or deferrals where policy permits them;
- all required human approvals.

Minor adds bounded impact/regression/rollback evidence. Major adds expanded design, architecture decision or explicit not-required evidence, owner-zone decisions, QA/test/automation planning, broad regression, dependency/migration, and release expectations. Hotfix uses the accelerated entry set described above and creates mandatory reconciliation obligations.

Deterministic checks report whether evidence exists and whether it is structurally valid. Passing those checks does not itself approve implementation.

## 6. When Work Is Complete

The project will not use one ambiguous “done” state.

| Completion concept | Meaning |
|---|---|
| Implementation complete | Code/config and required tests exist; required checks ran; source-linked implementation evidence exists. |
| Definition of Done | Acceptance evidence, defects, review dispositions, documentation, traceability, waivers, class-specific obligations, and applicable post-hotfix reconciliation are complete. |
| Release/transfer ready | Version/tag, release notes, package contents, verification, limitations, transfer/deployment/support instructions, rollback, operational checks, roles, and follow-ups are complete. |
| Archive ready | Canonical change evidence can be reconciled into accepted specs and final archive approval can be requested. |
| Archived | The accepted OpenSpec change has been reconciled into living specs under explicit human approval. |
| Delivered / production Done | The real external tracker/deployment/customer state is satisfied according to configured corporate workflow evidence. It is not inferred from archive. |

This separation prevents a common corporate failure: closing Jira because code exists, archiving a spec as if production delivery occurred, or calling a package “done” while release/support/rollback evidence is missing.

## 7. Tech Lead Automation Plan

### 7.1 Human responsibilities

The Tech Lead confirms or challenges classification, prevents under-classification, owns technical readiness, makes or coordinates architecture decisions, verifies owners and reviewers, evaluates technical risk and regression strategy, controls technical stop/resume, confirms engineering completion, and issues a release-readiness recommendation.

The role does not absorb product/business acceptance, QA sign-off, security/compliance approval, repository merge approval, release authorization, or final archive approval unless the real owner registry explicitly grants a particular decision.

### 7.2 Deterministic automation

The process will provide:

- classification report with every triggered rule and unknown input;
- DoR report with blockers, advisories, owners, and evidence paths;
- bounded Tech Lead review pack;
- affected repository/system/owner/dependency map;
- architecture-decision required/not-required evidence;
- scope-drift and missing-context report;
- quality-strategy and regression-matrix gaps;
- stop/hold/escalation recommendation and resume-condition report;
- implementation-complete, DoD, and release-readiness reports;
- waiver, override, deviation, and expiry/follow-up view;
- hotfix reconciliation view;
- configured scheduled or event-driven control report for untriaged/unclassified work, missing fixed input, blockers, scope drift, missing owners, holds/external waits, evidence-collection failures, bypasses, expiry/follow-up, and release-package gaps;
- later role inbox only after task/tracker status sources are authoritative.

The NIS daily/weekly Tech Lead checks are adopted as configurable operational checkpoints rather than hard-coded universal calendar rules. A project may choose daily, weekly, release-based, or event-driven cadence; the evidence content and authority boundaries remain canonical.

### 7.3 AI assistance

AI may draft questions, summaries, risk hypotheses, architecture alternatives, missing-context findings, and review comments. It may not confirm class, mark DoR/DoD green, accept residual risk, approve a waiver, resume held work, approve release readiness, or mutate canonical state without deterministic evidence and the authorized human decision.

## 8. Corporate Flow and Evidence Records

The target process sequence is:

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
  +-> archive readiness and human archive approval -> archived Master Spec
  \-> configured external delivery/Done evidence (independent external state)
```

Archive and external delivery are linked by evidence but are not ordered universally. Corporate configuration decides whether delivery precedes or follows archive; neither state is inferred from the other.

The versioned process package will define structured records for:

- initiative triage;
- classification confirmation, source correction, and recalculation;
- input baseline and scope change;
- quality strategy;
- regression matrix;
- decision log;
- AI run/certification evidence;
- stop/hold/escalation/resume;
- deviations, waivers, and hotfix deferrals;
- release/transfer package and receiver acceptance;
- role-understanding walkthroughs;
- controlled/external time events;
- portfolio WIP and pilot selection;
- metric definitions and pilot observations.

Exact file paths are implementation details owned by the versioned package schema. They must not be guessed before the package/config foundation exists.

## 9. Metrics Versus Gates

The earlier word “metrics” could be misunderstood as readiness/completion criteria. This plan distinguishes them:

- Gates answer: “May the change move to the next governed state?”
- Metrics answer: “Did this process improve delivery outcomes and at what cost/risk?”

DoR, DoD, release readiness, archive readiness, stop conditions, and required approvals are gates. Cycle time, human effort, cost, first-pass acceptance, defects, rework, completeness, intervention, repeatability, tool reliability, waiting, and delivery stability are metrics.

Every metric needs purpose, unit, numerator/denominator, start/end events, source, exclusions, missing-data behavior, owner, aggregation, privacy class, and pre-approved decision rule. Failed runs and manual interventions remain in the evidence. Historical, control, experimental, certification, and production observations are labelled; contaminated comparisons cannot support strong causal conclusions.

Artifact count, prompt count, AI usage, or checklist completion may be diagnostics but are not proof of effectiveness.

## 10. Safe Adoption Corrections

The following NIS ideas are intentionally repaired before adoption:

1. **One canonical policy source.** Conflicting thresholds or repeated rules are replaced by versioned OpenSpec/policy configuration.
2. **No AI-only production dependency.** AI-heavy/no-manual execution may be an isolated experiment, while production retains deterministic and human-authored/manual fallback paths.
3. **No absolute zero-risk claim.** Pilot safety uses an explicit risk register, access/privacy controls, stop conditions, rollback, residual-risk decisions, and honest limitations.
4. **Independent quality evidence.** A second model may challenge work, but independence requires external evidence ownership and human/role disposition.
5. **Pre-registered measurement.** Comparator, eligible sample, minimum analysis, decision-ready, rollout, and stop rules are approved before interpretation.
6. **Privacy and retention.** Process measurement cannot become hidden personal surveillance or a repository of prompts, secrets, unrestricted source payloads, or personal rankings.
7. **Failed-run integrity.** Retries do not erase failed AI, adapter, validation, or workflow attempts.
8. **No PPRB inheritance.** PPRB team structure, roles, reporting hierarchy, and project layout are not copied.
9. **No NIS repository topology inheritance.** Existing project topology and the external-release/corporate-adaptation boundary remain authoritative.

## 11. Implementation Sequence

### Stage A: Canonical contracts

Accept and implement the OpenSpec change, schema version 2, policy schemas, and synthetic class fixtures. Phase 2 package/config foundation remains the first prerequisite because it provides versioned homes and deterministic discovery.

### Stage B: Classification and migration

Implement the conservative classifier, reports, human confirmation/source-correction/recalculation path, lower-class override rejection, and check/apply migration. Replace target templates, tests, diagnostics, examples, and guides. Preserve archive history and add compatibility diagnostics.

### Stage C: Gates and corporate flow

Implement artifact matrices, DoR/DoD, release/archive distinction, Tech Lead support, scope/regression/stop controls, decision logs, release packages, and traceability.

### Stage D: Measurement and certification

Implement metric/pilot schemas, privacy rules, comparison integrity, role-understanding walkthroughs, and certification for minor, major, hotfix, Tech Lead, and negative authority cases. Prove all core behavior with AI disabled and with actual Qwen-class and DeepSeek-class assistants.

### Stage E: External release gate

Rehearse bootstrap, compatibility, migration, update/rollback, release manifest, and transfer. Stop for explicit human acceptance of the external release candidate.

### Stage F: Corporate adaptation and monitored pilot

Only after external acceptance, supply real ignored corporate configuration: Jira mappings, owners, thresholds, project/repository paths, model/runtime identifiers, integration availability, retention, security approvers, and one approved representative pilot. Run one monitored real change. Reusable corrections return to the external OpenSpec source rather than forming an internal fork.

## 12. Phase and Scope Impact

Phase 2 work item 2.1 remains ready because process-package/config/schema foundations are prerequisites for this adoption. The new governance workstream must complete before the transfer candidate finalizes the packaged reference flow, Tech Lead role kit, certification matrix, release manifest, or acceptance evidence.

The old phrase “thin flow” remains only as historical/current-implementation context until migration. Target Phase 2 and Phase 3 behavior is a class-aware flow. Phase 3 is not limited to a “thin-change pilot”; it will select one representative `minor`, `major`, or `hotfix` candidate through the approved pilot-selection rules. The default recommendation for the first real pilot is a bounded minor change unless representativeness requires another class, but the actual project and class remain a later human corporate-adaptation decision.

The single Phase 3 change is an operability and transfer pilot. It may prove that configuration, roles, gates, evidence collection, rollback/hold, and the selected real flow work in the corporate environment. It cannot by itself prove NIS effectiveness, statistical viability, defect reduction, productivity improvement, or readiness for organization-scale rollout. Any such conclusion belongs to a separately approved Phase 4 or later scale-evidence protocol with a predefined population, comparator, sample gates, contamination rules, production-stability observation, and decision owner.

This adoption does not pull deferred Jira task automation, Confluence publication, Zephyr, deploy automation, generated QA/AT proposals, or broad role inboxes into the immediate foundation. It defines the process contracts those later layers must obey.

## 13. Required Corporate Inputs Still Unknown

The architecture is not blocked by these values, but production adaptation is:

- real Jira/tracker status and transition names;
- project/repository/system identifiers and path mappings;
- owner registry, Tech Lead delegates, and escalation routes;
- class thresholds or configurable local policy values beyond canonical minimums;
- SLA and response expectations;
- security/compliance approvers;
- approved model/runtime identifiers and tool availability;
- MCP/integration/Nexus availability and constraints;
- retention, redaction, access, export, and deletion rules;
- pilot project, comparator, sample and decision thresholds;
- deployment, support, release, and rollback evidence sources.

These values must be supplied in approved local ignored configuration. They must not be inferred or committed to the reusable repository.

## 14. NIS Source-Coverage Appendix

This appendix makes the “nothing omitted” claim reviewable. It maps every file in the approved local package to canonical proposed behavior, an explicit adaptation/rejection, or audit-only evidence. Requirement and scenario names below refer to `openspec/changes/adopt-nis-corporate-process-governance/specs/`; implementation is tracked in its `tasks.md`.

| NIS source and sections | Disposition | Target requirement/scenario or durable record |
|---|---|---|
| `README.md` package inventory and status | Audit/orientation only | NIS compatibility audit evidence; the ignored package is never a canonical project source |
| `NIS_Clean_v1.6_Standard.md` §§1-3 purpose, principle, target production process | Adopt with AI-safety correction | Design goals; `corporate-flow-controls` preliminary triage/input/quality/release flow; AI-disabled fallback in `process-measurement-pilot` |
| Standard §§4-5 responsibility split and team model | Adopt portable responsibilities; reject organization chart | `corporate-flow-controls` portable corporate role map, human decision/AI evidence, role-understanding verification; `tech-lead-workflow` authority limits |
| Standard §6 portfolio teams, triage, regression, external contour | Adopt process semantics | `corporate-flow-controls` preliminary triage, regression matrix, controlled/external time, system-of-record links, release handoff, portfolio WIP |
| Standard §§7-8 system separation and Git as master | Align with accepted architecture | `corporate-flow-controls` system-of-record links; `traceability-contract` governance/release traceability; existing Git/OpenSpec canonical boundary |
| Standard §9 minor/major/hotfix | Adopt as selected flat classification | `corporate-change-classification`: canonical enum, exact minor all-conditions, major any-trigger, harm-based hotfix, no lower-class waiver |
| Standard §§10-11 no-manual experimental execution and quality model | Experiment-only adaptation | `process-measurement-pilot` AI-only treatment isolation and AI-disabled path; `corporate-flow-controls` QA-owned quality strategy/regression; production manual fallback retained |
| Standard §12 release package | Adopt; mandatory for releasable major/hotfix | `change-artifact-contracts` major/hotfix contracts; `readiness-completion-gates` release/transfer readiness; `corporate-flow-controls` release-package handoff/system links |
| Standard §§13-16 experiment, comparison contours, integrity, rollout sequence | Adopt controlled subset; reject automatic broad rollout | `process-measurement-pilot` comparison labels, paired experiment integrity, sample/decision gates, pilot safety; Phase 3 operability non-claim and Phase 4 scale gate |
| Standard §§17-19 metrics, viability thresholds, production measures | Adopt metric families; normalize conflicting thresholds | `process-measurement-pilot` canonical definitions, event integrity, privacy, comparison, pre-registered gates, activity-proxy rejection, post-pilot stability |
| Standard §§20-21 temporary NIS group and summary formula | Reject group structure; retain process summary | Portable role map and explicit PPRB/organization exclusion; design and adoption plan executive decision |
| `NIS_Clean_v1.6_Portfolio_Team_Model.md` §§1-5 | Adopt portable portfolio controls | `corporate-flow-controls` role map, triage, regression matrix, external time, artifact-repository/release links, WIP and pilot selection |
| `NIS_Clean_v1.6_Team_Lead_Guide.md` §§1-3 role/task control/stop | Adopt | `tech-lead-workflow` responsibilities, classification/readiness/architecture, stop/hold/escalation/resume, completion/release recommendation |
| Team Lead Guide §§4-7 daily/weekly checks, project selection, team communication | Adapt cadence; adopt evidence content | Configured Tech Lead checkpoint scenarios; `corporate-flow-controls` pilot selection and role understanding; no universal calendar cadence |
| `NIS_Clean_v1.6_Role_Understanding_Check.md` §§1-8 | Adopt portable role responsibilities | `corporate-flow-controls` portable role map and scenario-based role-understanding verification; process decision outcomes in `process-measurement-pilot` |
| `NIS_Clean_v1.6_Metrics_Guide.md` §§1-6 | Adopt | `process-measurement-pilot` metrics-vs-gates, canonical metrics, provenance, context switching, quality constraints |
| Metrics Guide §§7-11 thresholds, data quality, dashboard, invalid evidence, production measures | Adopt after normalization | `process-measurement-pilot` pre-registered decision gates, failed/missing data, privacy, activity-proxy rejection, post-pilot stability and scale non-claim |
| `NIS_Clean_v1.6_Metrics.csv` | Treat as source examples, not canonical thresholds | Metric-family coverage in `process-measurement-pilot`; exact conflicting values remain documented in the NIS audit and require approved pilot config |
| `NIS_Clean_v1.6_Methodological_Basis.md` §§1-7 | Adopt measurement principles with claim limits | Paired comparison, multi-metric evidence, delivery flow, repeatability, comparison-integrity and one-change non-claim requirements |
| `NIS_Clean_v1.6_Experiment_Protocol.md` §§1-3 preparation and independent quality | Adopt controlled subset | Fixed input/scope, quality strategy, regression/QA ownership, paired experiment integrity and independent assurance |
| Experiment Protocol §§4-10 branches, history, sample, collection, stop, audit | Adopt when experiment is approved | Comparison labels, event provenance, sample gates, pilot stop criteria, human/AI evidence and end-to-end traceability; duplicate control is optional, not universal |
| `NIS_Clean_v1.6_Implementation_Plan.md` §§1-3 decision, selection, risk | Adapt | Pilot selection, risk register, external release gate, one-change operability pilot; busiest-project-first and zero-risk claims rejected |
| Implementation Plan §§4-8 sequence, duration, results, risks, CTO output | Adapt and split across phases | Phase 2 external certification, Phase 3 operability, Phase 4 scale/effectiveness gate; observation duration is protocol config, not roadmap deadline |
| `NIS_Clean_v1.6_CTO_Decision_Memo.md` §§1-6 | Adopt decision inputs/outcomes; reject absolute safety claim | Process metrics/decision gates and scale/continue/revise/hold/stop outcomes; pilot risk register and explicit residual limitations |
| `NIS_Clean_v1.6_Project_Selection.csv` | Adopt criteria categories; reject fixed formula as universal | `corporate-flow-controls` pilot-selection record; thresholds/weights require approved local configuration |
| `templates/experiment-card.md`, `experiment-task.md`, `control-branch-protocol.md` | Convert into typed/versioned pilot evidence | Fixed input, class, acceptance, branch/comparator, isolation, result, intervention, stop, and comparability records in flow/measurement specs |
| `templates/ai-execution-log.md` | Adopt with privacy/secret limits | `corporate-flow-controls` AI execution evidence; `process-measurement-pilot` failed-run retention and data governance |
| `templates/cto-decision.md`, `cto-scorecard.csv` | Generate from canonical measurement evidence | Pre-registered decision outcome and metric definitions; dashboard is a derived view, never a normative threshold source |
| `templates/project-selection-checklist.md` | Adapt | Pilot-selection record with representativeness, class, rollback, privacy, comparator, and exclusion risks |
| `NIS_CTO_Executive_Deck_v1.6.pptx`, `.pdf`, and verified montage | Audit/cross-check only | Used by the compatibility audit to compare claims; not imported as a separate normative source |

Implementation task trace for the target requirements:

| Target requirement family | OpenSpec task groups |
|---|---|
| Classification, schema, and thin/full migration | 1-2 |
| Artifact matrices, DoR/DoD, release/archive/delivered gates | 3 |
| Tech Lead automation, authority, checkpoints, and certification guide | 4 |
| Triage, scope, quality/regression, stop/escalation, role/system/release records | 5 |
| Metrics, context switching, comparison, privacy, pilot and Phase 4 scale evidence | 6 |
| Traceability, generated views, workflow mapping, AI-disabled integration boundary | 7 |
| Full deterministic, Qwen/DeepSeek, migration, privacy, release, and reviewer certification | 8 |

Coverage rule: future NIS file or section additions must enter this appendix and receive an adopt/adapt/defer/reject disposition before they change scope. The exact-name/full-block delta check found necessary during reviewer approval is retained as a future archive verification step.

## 15. Acceptance and Verification

The adoption is documentation-complete only when:

- the human decision is recorded consistently in decisions, context, roadmap, Phase 2, audit, project map, and agent verification guidance;
- the OpenSpec proposal, design, delta specs, and tasks pass `openspec validate --all --strict`;
- no target documentation still presents `thin/full` as the future choice without a migration/historical qualifier;
- Tech Lead authority and AI limitations are explicit;
- DoR, implementation complete, DoD, release ready, archive ready, archived, and delivered remain distinct;
- hotfix cannot bypass mandatory safety, approval, rollback, traceability, or reconciliation;
- NIS inconsistencies and excluded PPRB/project-structure assumptions remain visible;
- critic and reviewer-approver reviews have no unresolved blocking findings;
- the final documentation diff is clean and committed.

Implementation acceptance later requires all scenarios and tasks in the OpenSpec change, AI-disabled certification, actual weak-model certification, migration rehearsal, external release-candidate acceptance, and a monitored corporate pilot under real approved configuration.
