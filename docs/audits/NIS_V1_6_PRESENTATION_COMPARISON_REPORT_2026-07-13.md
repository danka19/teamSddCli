# NIS v1.6 Presentation Comparison And Adoption Report

Date: 2026-07-13.

Status: presentation-ready read model of accepted decision `D-013`. It summarizes evidence and accepted direction; it is not a second normative process source and does not mean the proposed behavior has been implemented.

Canonical sources:

- human decision: `docs/DECISIONS.md`, `D-013`;
- evidence audit: `docs/audits/NIS_V1_6_ARCHITECTURE_COMPATIBILITY_AUDIT_2026-07-13.md`;
- complete adoption and source-coverage plan: `docs/planning/NIS_CORPORATE_PROCESS_ADOPTION_PLAN_2026-07-13.md`;
- proposed normative behavior: `openspec/changes/adopt-nis-corporate-process-governance/specs/`;
- architecture rationale: `openspec/changes/adopt-nis-corporate-process-governance/design.md`;
- implementation backlog: `openspec/changes/adopt-nis-corporate-process-governance/tasks.md`.

## 1. Executive Summary For Presentation

The project does not copy NIS verbatim. It adopts the corporate delivery process that matches real work, keeps the parts that already align with the project architecture, repairs inconsistent or unsafe rules, and rejects team-specific organization and project structure.

The central accepted decision is:

```text
Target classification: minor | major | hotfix
Legacy migration: thin -> minor, full -> major
No legacy value maps to hotfix automatically
```

The project also accepts NIS-derived business gates, Tech Lead governance, quality and regression controls, release-package handoff, stop/escalation behavior, role-understanding evidence, measurement, and controlled-pilot practices.

What remains unchanged from the project architecture:

- Git/OpenSpec is canonical;
- Confluence is generated publication;
- Jira/tracker owns workflow status, not requirements;
- CI and deterministic checks own validation evidence;
- humans own approval, risk, merge, release, archive, and correctness decisions;
- AI is an assistant, not a process authority;
- reusable behavior is developed and certified externally before corporate adaptation;
- PPRB organization and NIS repository structure are not adopted.

Implementation status:

- accepted as documentation and architecture direction;
- fully specified in an apply-ready OpenSpec change;
- 47 implementation tasks are planned;
- current accepted specs and validator still represent the legacy Phase 1 thin/full implementation baseline until the change is implemented, verified, accepted, and promoted.

## 2. Short Answer: Metrics And Control Ideas Recorded

Yes. The documentation records both outcome metrics and experiment/control ideas.

### 2.1 Outcome and process metrics

| Metric family | What is recorded |
|---|---|
| End-to-end cycle time | Time from accepted input to the defined result, with explicit start and end events |
| Active human effort | Time spent on clarification, decisions, review, verification, approval, and recovery |
| Machine/runtime time and cost | Model/tool execution, retries, adapter failures, and approved cost source |
| Waiting and handoff time | Internal queue, review wait, external dependency wait, and team handoff intervals |
| Context switching and WIP | Leave/resume events, concurrent work, attribution limitations, and privacy boundary |
| First-pass acceptance | Share of changes accepted at the defined first review or verification point |
| Material defects | Critical/material defect rules, escaped defects, rollback, and support evidence |
| Rework | Repeated implementation, spec correction, review cycles, and post-verification repair |
| Engineering-package completeness | Substantive class-specific evidence, not simple file counts |
| Manual intervention | Human corrections, fallbacks, overrides of AI proposals, and recovery actions |
| Repeatability | Stability of results across comparable runs, models, projects, or process versions |
| Tool and adapter reliability | Failed runs, retries, MCP/adapter/runtime availability, and evidence corruption |
| Waivers, deferrals, and bypasses | Denominator, approver, expiry, residual risk, and unresolved follow-up |
| Delivery stability | Applicable lead time, deployment frequency, change failure, restore time, escaped defects, support, and rollback after the operability pilot |

### 2.2 Control and comparison ideas

The documentation records:

- historical baseline;
- concurrent control when separately justified;
- experimental treatment;
- certification runs;
- production follow-up;
- fixed identical input and source baseline for a paired comparison;
- predefined acceptance set and allowed differences;
- isolation between treatment and control;
- independent assurance ownership;
- input-change and contamination records;
- automatic event collection where possible;
- labelled manual data where automation is unavailable;
- failed-run retention;
- missing-data and non-comparability rules;
- sample-entry, minimum-analysis, decision-ready, rollout, and stop gates;
- explicit decisions: scale, bounded rollout, continue collection, revise and repeat, hold, or stop.

The control branch is optional, not mandatory for every pilot. A paired implementation can improve comparison quality, but it may also double cost, delay delivery, or increase data exposure. A bounded Phase 3 operability pilot may use approved historical evidence instead.

### 2.3 What is not accepted as proof

The following may be diagnostic data but cannot prove effectiveness by themselves:

- number of generated files;
- number of prompts;
- volume of AI usage;
- checklist completion;
- fluent AI output;
- one successful real change;
- green deterministic checks without outcome comparison;
- archive completion without production evidence.

## 3. What Is The Same In NIS And The Project

These ideas were already aligned before the NIS adoption decision.

| Area | Shared position | Project interpretation |
|---|---|---|
| Engineering source of truth | Git-centered engineering artifacts | Git/OpenSpec is canonical; generated views cannot own behavior |
| Workflow tracker | Tracker records intake and status | Jira or equivalent does not own requirements |
| Generated publication | Business readers need readable views | Confluence is generated from canonical source and links back to it |
| Human accountability | People remain responsible for decisions | AI and CI cannot approve, merge, accept risk, or archive |
| AI execution vs responsibility | AI can perform or prepare work | Every AI result remains proposed evidence until deterministic/human review |
| Traceability | Work must connect input to output | Requirement -> scenario -> implementation -> test -> release evidence |
| Quality before release | Verification must be planned and evidenced | Quality strategy, regression matrix, QA ownership, and completion gates |
| Stop and escalation | Unsafe or invalid work must stop | Structured stop/hold/escalation/resume records and non-disableable minimum triggers |
| Release handoff | A release candidate needs a complete package | Version, contents, tests, limits, instructions, rollback, support, and owners |
| Outcome measurement | Process value must be measured, not assumed | Cycle, effort, cost, quality, completeness, intervention, and stability evidence |
| Failed-run visibility | Failures must not disappear after retry | Failed AI, adapter, validation, and workflow runs remain in evidence |
| Controlled rollout | Expansion requires evidence and a decision | External release gate, corporate operability pilot, then a separate scale gate |

Presentation message:

> NIS does not replace the architecture. It gives the architecture a stronger corporate operating process and measurement layer.

## 4. What Is Borrowed From NIS

### 4.1 Flat change classification

The project adopts the NIS classification as the only target process-route vocabulary:

- `minor`;
- `major`;
- `hotfix`.

No hidden second classification axis is introduced. Work `type`, lifecycle `status`, and risk evidence are separate metadata, not competing process routes.

#### Minor

Minor is allowed only when all low-impact conditions are known and satisfied:

- local and small change;
- simple rollback;
- no user-scenario impact;
- no SLA impact;
- no security/compliance impact;
- no external-integration impact;
- no data-model impact;
- no component-interaction impact;
- no public-API or cross-repository impact;
- no material reliability, performance, operations, governed-test, or governed-documentation impact;
- no architecture decision requirement.

Unknown impact does not count as low impact.

#### Major

Major is mandatory when any major trigger exists:

- new feature;
- changed business logic or user scenario;
- changed component interaction;
- changed required test behavior;
- changed governed user or operational documentation;
- public API, integration, data, security, compliance, or SLA impact;
- external dependency;
- cross-repository work;
- reliability, performance, or operations impact;
- regression risk;
- high rollback cost;
- architecture decision.

A major trigger cannot be reduced to minor by a waiver, Tech Lead decision, or AI recommendation. Incorrect input evidence may be corrected and classification recalculated. A stricter route may always be selected. Weakening a canonical criterion requires a new accepted policy/OpenSpec change.

#### Hotfix

Hotfix is used when delay increases concrete production or pre-production harm. It is not a shortcut for deadlines or reduced documentation.

Hotfix retains:

- named human decision owner;
- urgency and harm rationale;
- bounded scope;
- minimum test and regression evidence;
- security/compliance decisions when triggered;
- rollback or hold instructions;
- traceability;
- release-package evidence for a releasable result;
- mandatory reconciliation of permitted deferred artifacts before closure.

### 4.2 Business-process gates

The project adopts NIS readiness and completion thinking but makes each state explicit.

| Gate or state | Meaning |
|---|---|
| Preliminary triage | Decide proceed, hold, split, redirect, or reject before team planning |
| Review ready | Package has enough structure and evidence for Spec Review |
| Definition of Ready | Common and class-specific evidence is sufficient for human implementation approval |
| Implementation complete | Code/config, required tests, checks, and source-linked implementation evidence exist |
| Definition of Done | Acceptance, defects, reviews, docs, traceability, waivers, and class obligations are complete |
| Release/transfer ready | Reproducible artifact/handoff package, limitations, instructions, rollback, operations, and owners are complete |
| Archive ready | Canonical evidence can be reconciled into accepted Master Specs |
| Archived | Human-approved OpenSpec reconciliation is complete |
| Delivered / production Done | Real tracker, deployment, customer, or operational state is satisfied according to corporate mapping |

Archive and Delivered are independent. One is not inferred from the other.

### 4.3 Tech Lead governance and automation

The project adopts Tech Lead as a first-class governed role.

Human responsibilities:

- confirm or challenge classification;
- prevent under-classification;
- own technical readiness;
- coordinate architecture and technical risk decisions;
- verify repository, system, owner, and dependency coverage;
- control technical stop/resume;
- confirm engineering completion;
- issue release-readiness recommendation.

Automation to be built:

- classification report and all triggered rules;
- DoR blocker/advisory report;
- bounded Tech Lead review pack;
- repository/system/owner/dependency map;
- architecture-decision required/not-required evidence;
- scope-drift and missing-context report;
- quality/regression gaps;
- stop/hold/escalation and resume-condition report;
- implementation-complete, DoD, and release-readiness reports;
- waiver/deferral/expiry view;
- hotfix reconciliation view;
- configurable scheduled or event-driven control report;
- later role inbox only after tracker/task sources are authoritative.

AI may draft analysis but cannot confirm classification, approve DoR/DoD, accept residual risk, approve a waiver, resume held work, approve release readiness, or mutate canonical state.

### 4.4 Corporate flow controls

Borrowed controls include:

- preliminary initiative triage;
- fixed approved input baseline;
- material scope-change record and reassessment;
- class-aware quality strategy before implementation;
- source-linked regression matrix;
- QA/test-owner approval of strategy, matrix sufficiency, and run results;
- stop, hold, escalation, resume, and deviation records;
- release-package handoff;
- human decision log;
- AI execution/certification log;
- role-understanding walkthroughs;
- controlled versus external time;
- WIP and context-switch evidence;
- pilot/project selection;
- tracker/Git/OpenSpec/PR/CI/artifact repository/release traceability.

Canonical production stop/hold triggers include:

- missing or contradictory canonical context;
- unapproved material scope drift;
- unavailable required verification;
- unresolved critical defect;
- security, compliance, access, leakage, or accidental-delivery risk;
- failed mandatory evidence collection;
- owner-authority conflict;
- unavailable rollback or hold path;
- integration corruption of canonical evidence;
- continued work beyond approved safety authority.

Local configuration may add stop triggers but cannot remove these minimums without an accepted policy change.

### 4.5 Portable role model

The project borrows responsibilities, not the PPRB organization chart.

| Responsibility | Portable target role |
|---|---|
| Business value, scope, product acceptance | Business/product owner |
| Technical class, readiness, architecture/risk, stop/resume | Tech Lead, architect/security when triggered |
| Requirements, scenarios, baseline, feedback, traceability | Analyst/change owner |
| Implementation evidence | Developer/implementation owner |
| Quality strategy, regression, tests, defect disposition | QA/test owner and AT owner where separately governed |
| Release package, operations, rollback, support handoff | Release/deployment/support owner |
| Independent comparison evidence | Control/assurance role when a controlled experiment is used |
| Scale, continue, revise, hold, or stop decision | Configured process owner or sponsor, never AI |

Missing human ownership is a blocker. AI cannot fill an absent accountable role.

## 5. What Is Adapted Rather Than Copied

| NIS idea | Why it needs adaptation | Accepted project form |
|---|---|---|
| AI creates every artifact | Useful as an experiment but unsafe as production dependency | Optional isolated treatment; production has deterministic, human-authored, manual fallback |
| No manual testing | May hide exploratory, accessibility, security, operational, and incident risks | QA-owned strategy with automated and manual evidence as applicable |
| Independent AI checker | Agent separation alone does not make evidence independent | AI may propose adversarial checks; deterministic evidence and human QA ownership remain required |
| Paired manual control branch | Improves comparability but doubles cost and exposure | Optional when justified; approved historical comparator is allowed for bounded operability pilot |
| Daily/weekly Tech Lead checks | Cadence varies by project | Configurable scheduled, release-based, or event-driven checkpoints with canonical report content |
| Nexus linkage | Real artifact repository may differ or be unavailable | Generic immutable artifact coordinate; Nexus is one corporate configuration option |
| Project-selection score | NIS files contain different formulas and weights | One approved local schema; representativeness, risk, rollback, privacy, comparator, and exclusions are explicit |
| Viability thresholds | Memo, deck, standard, guide, and CSV disagree | One versioned metric/decision schema approved before collection |
| Minimum sample | Package uses conflicting values | Separate entry, minimum-analysis, decision-ready, and rollout gates |
| Experiment duration | A protocol needs an observation window | Stored as experiment configuration, never a roadmap deadline |
| Control definition | NIS alternates between production team, manual specialist, and history | Primary comparator and secondary evidence are named before collection |
| Whole-project rollout | May precede production stability and cross-project evidence | Phase 3 proves operability; Phase 4 or later owns effectiveness and scale evidence |

## 6. What Does Not Match And Is Rejected

### 6.1 Architecture conflicts

| Rejected default | Why it conflicts |
|---|---|
| AI owns production artifact creation | Makes process guarantees depend on model behavior and availability |
| Zero manual authoring | Removes safe human fallback and can turn correction into a methodology failure |
| No manual testing | Conflicts with human QA ownership and risk-based verification |
| AI checker is sufficient independent evidence | Evidence independence requires external ownership and deterministic verification |
| LLM/MCP availability at every stage | Core gates must work with AI disabled and integrations unavailable |
| Confluence or duplicated documents become normative | Git/OpenSpec remains the single canonical behavior source |
| NIS repository/project structure | The project already has an accepted topology and transfer boundary |
| PPRB cluster/direction/team structure | It belongs to another team and was explicitly excluded by the human owner |

### 6.2 Safety and rollout conflicts

| Rejected default | Why it conflicts |
|---|---|
| “No production risk” | Branch isolation reduces some risk but does not cover secrets, privacy, logs, access, accidental delivery, adapters, or rollback failure |
| Busiest/highest-load project first | Improves representativeness but maximizes blast radius, dependencies, and data exposure |
| Broad project switch after initial decision | May happen before production stability and cross-project evidence exist |
| One successful change proves effectiveness | It proves bounded operability only |
| Failed retries may disappear behind final success | Hides model/tool/process reliability and manual intervention cost |

### 6.3 Documentation and measurement conflicts

The NIS package contains verified internal disagreements:

- document approval status;
- viability thresholds;
- allowed amount of manual execution;
- minimum sample;
- project-selection formula;
- primary control definition;
- rollout timing.

Therefore, the package cannot be copied as one deterministic standard. The project uses one canonical OpenSpec/policy source and generates role guides, scorecards, dashboards, templates, and presentation views from it.

## 7. Presentation-Ready Comparison Matrix

| Topic | Same as our architecture | Borrow from NIS | Adapt or reject |
|---|---|---|---|
| Source of truth | Git/OpenSpec canonical | End-to-end Git-centered evidence | Reject duplicated normative copies |
| Change routes | Existing risk-aware process intent | Flat `minor|major|hotfix` and exact criteria | Replace legacy thin/full through migration |
| Readiness | Human approval and deterministic evidence | Explicit DoR and class-specific gates | Do not equate ticket existence with readiness |
| Completion | Human-owned validation/archive | DoD and complete release package | Split implementation, DoD, release, archive, Delivered |
| Tech Lead | Existing waiver/design responsibility | Full classification/readiness/stop/release role | AI supports but never impersonates approval |
| QA | Scenario and evidence orientation | Quality strategy and regression matrix ownership | Reject AI-only independent quality proof |
| Release | Transfer/rollback already required | Full major/hotfix release package and external handoff | Artifact repository is configured, not assumed |
| Metrics | Strategy already wanted outcome evidence | Cycle, effort, cost, acceptance, defects, completeness, intervention, repeatability | Normalize conflicting thresholds and data rules |
| Control | AI-disabled and negative certification | Historical/control/experimental comparison discipline | Paired control is optional, not universal |
| Pilot | External release before corporate work | Fixed input, stop rules, decision log, evidence collection | First real change proves operability, not scale |
| Organization | Human roles and owner registry | Portable responsibility map | Reject PPRB structure and NIS team ratios |
| Integrations | Jira/Confluence/MCP boundaries already defined | Artifact/release traceability | No custom clients or guessed corporate values |

## 8. Suggested Future Presentation Structure

### Slide 1: Why NIS matters

- It describes real corporate delivery rather than an abstract SDD workflow.
- It fills gaps in classification, readiness, completion, Tech Lead operations, release handoff, and measurement.

### Slide 2: What was already the same

- Git/OpenSpec truth;
- human accountability;
- deterministic gates;
- generated Confluence;
- tracker status;
- traceability and audit.

### Slide 3: The accepted classification

- `minor | major | hotfix`;
- `thin -> minor`, `full -> major`;
- any major factor means major;
- hotfix is accelerated but not simplified.

### Slide 4: When work may start

- preliminary triage;
- fixed scope/input;
- classification;
- requirements and scenarios;
- quality/regression strategy;
- risk, rollback, owners;
- human DoR approval.

### Slide 5: When work is really complete

- implementation complete;
- DoD;
- release/transfer ready;
- archive ready;
- archived;
- external Delivered/Done.

### Slide 6: Tech Lead automation

- reports, review pack, dependencies, gaps, scope drift;
- stop/resume and follow-up control;
- release recommendation;
- clear AI authority boundary.

### Slide 7: Quality and release package

- QA-owned quality strategy;
- regression matrix and result disposition;
- mandatory release package for releasable major/hotfix;
- artifact, CI, tests, limitations, rollback, support.

### Slide 8: Metrics and controls

- cycle, effort, cost, acceptance, defects, completeness;
- intervention, repeatability, waiting, context switching;
- historical/control/experimental/production labels;
- failed runs, missing data, privacy, contamination.

### Slide 9: What was corrected or rejected

- no AI-only production constitution;
- no zero-risk claim;
- no conflicting thresholds;
- no busiest-project-first requirement;
- no PPRB structure or NIS repository topology;
- no effectiveness claim from one pilot.

### Slide 10: Delivery path

- Phase 2: implement and externally certify the class-aware process;
- Phase 3: configure the real environment and run one operability pilot;
- Phase 4: only if approved, run a scale/effectiveness evidence protocol;
- reusable findings return to the external canonical OpenSpec source.

## 9. Current Documentation Acceptance

Accepted in project documentation:

- decision `D-013`;
- flat classification and migration direction;
- exact class criteria and no lower-class override;
- business gates and completion-state separation;
- Tech Lead governance/automation boundary;
- QA ownership, regression, production stop triggers, release handoff;
- metrics, control ideas, privacy, failed-run and comparison rules;
- Phase 3 operability limitation and later scale gate;
- PPRB/project-structure exclusions;
- complete source coverage of the 22 NIS package files/categories.

Not yet implemented or promoted into accepted specs:

- schema version 2;
- classifier and migration command;
- minor/major/hotfix templates and validators;
- DoR/DoD reports;
- Tech Lead automation;
- flow-control and release-package schemas;
- metric/pilot evidence collection;
- Qwen/DeepSeek and AI-disabled certification for the new process.

The active OpenSpec change contains 47 unchecked implementation tasks. The next implementation sequence remains Phase 2 work items 2.1, 2.2, and then task-sized slices of 2.3A.

## 10. Evidence And Limitations

Verified evidence:

- every NIS package file/category is mapped in the adoption source-coverage appendix;
- the local NIS package is git-ignored and untracked;
- the active NIS governance change is structurally complete and strict-valid;
- the previous independent critic returned `PASS`;
- the previous reviewer-approver returned `APPROVE WITH NON-BLOCKING NOTES`;
- accepted/current thin/full behavior is explicitly distinguished from proposed target behavior.

Limitations:

- no actual NIS experiment dataset or result was supplied;
- no real corporate Jira, repository, owner, model, MCP, Nexus, privacy, retention, deployment, or support configuration was verified;
- the report does not prove NIS effectiveness;
- exact pilot thresholds remain future approved corporate configuration;
- current automated tests prove the legacy implementation baseline, not the proposed 47-task implementation.

Presentation safety rule:

> Present the adopted process and implementation plan as accepted direction. Do not present it as already deployed, statistically proven, or accepted into current Master Specs until implementation, verification, human acceptance, and OpenSpec promotion are complete.
