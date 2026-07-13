## ADDED Requirements

### Requirement: Preliminary initiative triage
The SDD process SHALL provide a preliminary triage record before an initiative is treated as ready for team-level change planning.

#### Scenario: Triage records decision inputs
- **WHEN** a new initiative is assessed
- **THEN** the record captures problem or opportunity, expected value, sponsor or owner, affected contour, urgency, dependencies, known constraints, initial class hypothesis, unanswered questions, and the decision to proceed, hold, split, redirect, or reject

#### Scenario: Triage is not implementation approval
- **WHEN** preliminary triage recommends proceeding
- **THEN** the change must still satisfy formal classification and Definition of Ready before implementation approval

### Requirement: Fixed input and scope-change control
The SDD process SHALL record the approved input baseline and subsequent material scope changes.

#### Scenario: Approved baseline is identifiable
- **WHEN** implementation starts
- **THEN** the package identifies the approved requirements, scenarios, scope, exclusions, dependencies, classification, quality strategy, and decision version that form the working baseline

#### Scenario: Material scope drift triggers reassessment
- **WHEN** work changes business behavior, affected systems, risk, dependencies, acceptance criteria, or expected release outcome beyond the approved baseline
- **THEN** the change records the drift and re-evaluates classification, readiness, owners, estimates, regression, and approval before continuing

### Requirement: Quality strategy before implementation
The process SHALL define and approve a class-aware quality strategy before implementation begins, except for the explicitly accelerated hotfix entry route.

#### Scenario: Quality strategy covers verification contours
- **WHEN** a standard minor or major change reaches Definition of Ready
- **THEN** the strategy identifies required scenario levels, static and deterministic checks, developer tests, QA/manual evidence, automation, data/environment needs, regression scope, negative cases, responsible roles, and allowed waivers

#### Scenario: QA owner confirms quality strategy sufficiency
- **WHEN** quality strategy or regression evidence is required for Definition of Ready
- **THEN** the configured QA/test owner reviews its sufficiency and records the decision; the Tech Lead or AI cannot silently substitute for QA ownership

#### Scenario: Hotfix reconciles deferred planning
- **WHEN** urgency permits only a minimum hotfix quality record before implementation
- **THEN** deferred non-safety planning is listed with an owner and due condition and must be reconciled before final closure

### Requirement: Regression matrix
The SDD process SHALL maintain a deterministic regression matrix linking change impact to required verification.

#### Scenario: Matrix links impact to checks
- **WHEN** a change is classified and affected capabilities are known
- **THEN** the matrix links product or module, requirement and scenario, change class, risk trigger, required check, test data or environment, evidence type, owner, and current result

#### Scenario: Missing applicable regression row is visible
- **WHEN** an affected capability has no matching regression rule or approved not-applicable rationale
- **THEN** readiness or completion reporting identifies the gap rather than assuming no regression is needed

#### Scenario: QA owner dispositions regression results
- **WHEN** required regression checks finish or cannot run
- **THEN** the configured QA/test owner records result sufficiency, material failures, missing evidence, approved role-appropriate waiver where permitted, and whether the affected completion gate may proceed

### Requirement: Stop, hold, escalation, resume, and deviation records
The SDD process SHALL define structured flow-control records for conditions that make continued work unsafe, ambiguous, or outside the approved baseline.

#### Scenario: Stop record is actionable
- **WHEN** a stop condition is raised
- **THEN** the record includes trigger, evidence, severity, affected work, immediate action, owner, escalation path, response expectation, and resume conditions

#### Scenario: Canonical production stop triggers cannot be disabled silently
- **WHEN** required canonical context is missing or contradictory, material scope drift lacks reassessment, required verification cannot run, a critical defect is unresolved, security/compliance/access policy is violated, unauthorized data/output leakage or accidental delivery is possible, mandatory evidence collection fails, owner authority conflicts, rollback or hold becomes unavailable, an integration corrupts canonical evidence, or continued work exceeds approved safety authority
- **THEN** the affected work stops or holds and requires the configured escalation and resume evidence; project configuration may add triggers but cannot remove these minimums without an accepted policy change

#### Scenario: Resume is auditable
- **WHEN** work resumes after a stop or hold
- **THEN** the record links corrective evidence, residual risk, required approvals, decision owner, date, and any follow-up

#### Scenario: Approved deviation remains traceable
- **WHEN** the team intentionally departs from the standard sequence or artifact matrix
- **THEN** an approved deviation or waiver identifies the affected obligations, reason, substitute controls, expiry or follow-up, and role-authorized decision

### Requirement: Release-package handoff
The SDD process SHALL define a versioned release or transfer package for deliverables that leave the implementation team.

#### Scenario: Handoff is reproducible
- **WHEN** a release or transfer package is prepared
- **THEN** it identifies artifact/version, included changes, canonical requirements and scenarios, verification evidence, known limitations, configuration assumptions, installation or transfer steps, rollback or hold instructions, operations/support contacts, and unresolved follow-ups

#### Scenario: Consumer acceptance is recorded separately
- **WHEN** another team or corporate contour accepts the package
- **THEN** acceptance evidence records the package version, receiver, compatibility result, deviations, and decision without changing external canonical files invisibly

### Requirement: Human decision and AI execution evidence
The process SHALL distinguish accountable human decisions from AI execution or certification evidence.

#### Scenario: Human decision log is explicit
- **WHEN** a classification confirmation or source correction, approval, waiver, stop/resume, release, or archive decision occurs
- **THEN** the log identifies decision type, source evidence, decision, accountable role and person, date, and follow-up

#### Scenario: AI run evidence is reproducible
- **WHEN** AI contributes an artifact, review, or certification run
- **THEN** evidence records model/runtime identity when available, prompt or skill version, input scope, tool/config version, output location, reviewer disposition, and failures or manual interventions without storing secrets

### Requirement: Role-understanding verification
The transfer-ready process SHALL verify that each role understands actions, evidence, authority, escalation, and AI boundaries.

#### Scenario: Role walkthrough tests real decisions
- **WHEN** analyst, developer, QA, tech lead, or another governed role is certified
- **THEN** the walkthrough includes positive and negative cases for required inputs, outputs, approvals, forbidden actions, stop/escalation behavior, and AI-disabled execution

#### Scenario: Checklist completion alone is insufficient
- **WHEN** a participant marks a role checklist complete without scenario evidence or reviewer disposition
- **THEN** role certification remains incomplete

### Requirement: Portable corporate role map
The process SHALL preserve the portable responsibilities from the NIS role model without copying a team-specific organization chart.

#### Scenario: Governed roles are mapped explicitly
- **WHEN** a project configures the corporate process
- **THEN** it maps business or product owner, Tech Lead, analyst, developer, QA/test owner, release or deployment/support owner, and architecture and security roles when applicable to real people or approved groups

#### Scenario: Missing role is not assigned to AI
- **WHEN** a required responsibility has no configured human owner or delegate
- **THEN** readiness or pilot entry reports a blocker and does not assign the decision to an AI assistant, generic team label, or unrelated role

#### Scenario: Team-specific hierarchy is excluded
- **WHEN** NIS source material names PPRB clusters, directions, temporary groups, or organization-specific reporting lines
- **THEN** the reusable role map retains only portable responsibilities and requires a separate approved local mapping for real organization structure

### Requirement: Corporate system-of-record links
The process SHALL preserve traceable separation between business workflow, canonical specifications, implementation, verification, build artifacts, and release handoff.

#### Scenario: Evidence chain crosses systems by identifier
- **WHEN** a governed change reaches release or transfer readiness
- **THEN** traceability can link tracker item, canonical Git/OpenSpec change and requirements, implementation commit or PR, CI/test evidence, immutable artifact-repository coordinate when applicable, release package, and external delivery evidence without copying each system's full content

#### Scenario: Missing artifact repository is explicit
- **WHEN** a major or hotfix release expects Nexus or another artifact repository but the corporate integration is unavailable or unverified
- **THEN** release readiness records the missing integration or approved substitute evidence and does not fabricate an artifact coordinate

### Requirement: Portfolio WIP and pilot-selection controls
The process SHALL record enough portfolio context to select a representative pilot and expose excessive parallel work.

#### Scenario: Pilot selection is justified
- **WHEN** a real pilot candidate is chosen
- **THEN** the record includes representativeness, class, systems, dependencies, data/security constraints, team readiness, rollback feasibility, and exclusion risks

#### Scenario: Excessive WIP is visible
- **WHEN** concurrent governed changes exceed an approved team or pilot limit
- **THEN** the process reports the WIP condition and requires an explicit prioritization, hold, or exception decision rather than silently starting more work

### Requirement: Failed-run evidence retention
The process SHALL preserve failed validation, AI, adapter, integration, and workflow attempts as source-linked execution evidence.

#### Scenario: Successful retry does not erase failure
- **WHEN** a failed attempt is followed by a successful retry
- **THEN** both attempts remain identifiable with outcome, source, time, relevant version or configuration, and reviewer or owner disposition where required

#### Scenario: Failed run can trigger operational control
- **WHEN** a failed attempt indicates corrupted evidence, unsafe continuation, unavailable rollback, or an unresolved mandatory check
- **THEN** the applicable stop, hold, escalation, or remediation rule is evaluated without converting the failure into an effectiveness score

### Requirement: Monitored-pilot safety boundary
The monitored corporate pilot SHALL use a bounded risk register and operational stop/rollback controls without claiming zero production risk.

#### Scenario: Pilot risk register covers operational boundaries
- **WHEN** pilot entry is reviewed
- **THEN** the record covers data/privacy, secrets, access, accidental delivery, rollback or hold, adapters and MCPs, model/runtime behavior, logs, external dependencies, support ownership, evidence corruption, and process bypass

#### Scenario: AI-disabled path is certified
- **WHEN** the process is considered transfer-ready for the pilot
- **THEN** the core classification, readiness, validation, stop, completion, release, and failed-run-evidence path has passed an AI-disabled walkthrough

#### Scenario: Operational pilot stop is testable
- **WHEN** access or isolation fails, unauthorized output delivery is possible, safety or security risk exceeds authority, tooling corrupts canonical evidence, rollback becomes unavailable, or a mandatory failed-run disposition is unresolved
- **THEN** the pilot stops or holds according to the canonical rule and records escalation and resume conditions
