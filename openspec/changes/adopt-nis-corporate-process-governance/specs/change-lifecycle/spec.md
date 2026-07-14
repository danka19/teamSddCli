## ADDED Requirements

### Requirement: Named corporate business gates
The lifecycle SHALL attach explicit business gates to canonical state transitions without introducing duplicate status ownership.

#### Scenario: Review-ready gate precedes Spec Review
- **WHEN** a change requests `draft` to `spec_review`
- **THEN** required review inputs, classification evidence, scenarios, and source structure pass deterministic review-ready checks

#### Scenario: Definition of Ready precedes approval
- **WHEN** a change requests `spec_review` to `approved`
- **THEN** common and class-specific Definition of Ready evidence passes deterministic checks and the required humans record approval

#### Scenario: Definition of Done precedes archive readiness
- **WHEN** a change requests `in_implementation` to `ready_to_archive`
- **THEN** common and class-specific Definition of Done plus applicable release or transfer evidence pass deterministic checks

### Requirement: Delivered state is external to archive state
The lifecycle SHALL treat external delivery, deployment, customer acceptance, and tracker Done as configured states or evidence rather than synonyms for `archived`.

#### Scenario: Archived spec may precede or follow delivery
- **WHEN** the canonical change is archived
- **THEN** external delivery state is reported from its configured source and is not inferred from the archive transition

#### Scenario: Tracker transition uses mapping
- **WHEN** automation proposes a corporate tracker transition
- **THEN** it uses the validated workflow mapping, required evidence, and authorized human or integration action for that project


## MODIFIED Requirements

### Requirement: Lifecycle states
The SDD process SHALL use the six accepted lifecycle states for minor, major, and hotfix packages while class-specific gates determine the required evidence.

#### Scenario: Minor route remains compact
- **WHEN** a change is confirmed as minor
- **THEN** the lifecycle requires draft, review, approval, implementation evidence, Definition of Done, and archive readiness without imposing inapplicable major-only artifacts

#### Scenario: Major route uses expanded gates
- **WHEN** a change is confirmed as major
- **THEN** the same lifecycle states require expanded design, owner, quality, regression, risk, traceability, and release evidence at the applicable gates

#### Scenario: Hotfix accelerates sequence but not accountability
- **WHEN** a change is confirmed as hotfix
- **THEN** the process may shorten waiting and combine explicitly permitted review steps while preserving named states, recorded human decisions, minimum safety evidence, rollback or hold capability, and mandatory reconciliation before closure

### Requirement: Deterministic transition gates
The SDD process SHALL define deterministic checks for lifecycle transitions and attach the approved readiness and completion policies where judgment and human approval remain explicit.

#### Scenario: Allowed transitions are explicit
- **WHEN** deterministic tooling or review evaluates a lifecycle status change
- **THEN** only these transitions are valid: `draft` -> `spec_review`, `spec_review` -> `draft`, `spec_review` -> `approved`, `approved` -> `in_implementation`, `in_implementation` -> `ready_to_archive`, `ready_to_archive` -> `in_implementation`, and `ready_to_archive` -> `archived`

#### Scenario: Spec PR transition checks structure
- **WHEN** a change moves from `draft` to `spec_review`
- **THEN** deterministic validation checks required files, schema-versioned metadata, classification evidence, at least one required OpenSpec delta, scenario presence, and review-minimum traceability

#### Scenario: Approval transition checks Definition of Ready
- **WHEN** a change moves from `spec_review` to `approved`
- **THEN** deterministic validation checks common and class-specific readiness evidence, valid waivers or deferrals, required owner coverage, and recorded human approvals

#### Scenario: Archive-readiness transition checks Definition of Done
- **WHEN** a change moves from `in_implementation` to `ready_to_archive`
- **THEN** deterministic validation checks class-specific completion, traceability, verification, defect and review disposition, required release or transfer evidence, valid waivers, and hotfix reconciliation

#### Scenario: Draft cannot skip to approved
- **WHEN** a change attempts to move directly from `draft` to `approved`
- **THEN** deterministic validation or review rejects the transition because Spec PR review, Definition of Ready, and human approval evidence are missing

#### Scenario: Draft cannot skip to archive readiness
- **WHEN** a change attempts to move directly from `draft` to `ready_to_archive`
- **THEN** deterministic validation or review rejects the transition because review, approval, implementation, Definition of Done, and verification evidence are missing

#### Scenario: Archive requires explicit human approval
- **WHEN** any change attempts to move to `archived`
- **THEN** deterministic validation or review rejects the transition unless the current state is `ready_to_archive`, final archive checks pass, and explicit human archive approval is recorded

#### Scenario: Lifecycle expiry remains due after rework
- **WHEN** a waiver or deferral became due at a reached lifecycle state and the change later follows an allowed rework transition to a lower state
- **THEN** versioned source-linked human-recorded reached-state evidence keeps the expiry due, while missing or inconsistent history fails closed when the current state alone cannot determine prior reach

### Requirement: MVP boundary for lifecycle automation
The next lifecycle implementation SHALL support the deterministic minor, major, and hotfix foundation before deferred corporate integrations become mandatory.

#### Scenario: Core process is AI-disabled and integration-independent
- **WHEN** Jira automation, Confluence publication, generated QA/AT proposals, or role inboxes are unavailable
- **THEN** classification, readiness, lifecycle, stop, completion, traceability, waiver, and release evidence can still be executed with canonical files, deterministic checks, and human decisions

#### Scenario: Deferred integration is not fabricated
- **WHEN** an applicable later integration has not been implemented or configured
- **THEN** the lifecycle reports it as deferred, unavailable, or manually evidenced according to policy rather than marking it complete
