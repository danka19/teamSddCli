## ADDED Requirements

### Requirement: Classification criteria cannot be waived
The waiver policy SHALL NOT permit a per-change waiver, deviation, or human override to select `minor` when a canonical major trigger exists.

#### Scenario: Major trigger blocks minor waiver
- **WHEN** a change triggers major but requests minor through a waiver, deviation, free-text note, Tech Lead decision, or AI recommendation
- **THEN** deterministic validation rejects the request and requires major, a valid harm-based hotfix, or corrected source evidence followed by recalculation

#### Scenario: Classification policy changes through OpenSpec
- **WHEN** the team wants to weaken or revise a canonical classification criterion
- **THEN** the current policy remains binding until a separately reviewed and accepted versioned policy/OpenSpec change replaces it

### Requirement: Hotfix artifact deferral
The waiver policy SHALL allow only explicitly permitted non-safety hotfix artifacts to be deferred and SHALL require reconciliation.

#### Scenario: Deferral has a bounded follow-up
- **WHEN** urgency prevents a permitted non-safety artifact from being completed before hotfix implementation
- **THEN** the deferral records the affected requirement, current substitute evidence, owner, due date or lifecycle condition, approver, residual risk, and reconciliation evidence required before closure

#### Scenario: Missing reconciliation blocks archive
- **WHEN** a hotfix deferral reaches its due condition or the change requests archive readiness without reconciliation
- **THEN** deterministic validation blocks closure until the artifact is completed or a new role-authorized disposition is accepted by policy

### Requirement: Non-waivable corporate minimums
The waiver policy SHALL identify corporate controls that cannot be bypassed by classification, urgency, AI output, or free-text exception.

#### Scenario: Mandatory approval and safety controls remain
- **WHEN** a minor, major, or hotfix change is processed
- **THEN** required human approval, behavior scenario coverage, minimum class-specific verification, required security/compliance decision, rollback or hold evidence, canonical traceability, and final archive approval cannot be waived away

#### Scenario: Hotfix cannot waive follow-up entirely
- **WHEN** a hotfix defers permitted evidence
- **THEN** no waiver may remove the reconciliation obligation without an explicit accepted policy change

#### Scenario: AI cannot authorize exception
- **WHEN** AI drafts or recommends an override, deferral, deviation, or waiver
- **THEN** the record remains invalid until the correct human role records approval

### Requirement: Stop and deviation exception relationship
Approved deviations SHALL not automatically clear stop or hold conditions.

#### Scenario: Held work needs separate resume decision
- **WHEN** a waiver or deviation is approved while a change is stopped or held
- **THEN** the hold remains until its documented resume conditions and human resume decision are satisfied

#### Scenario: Expired exception is visible
- **WHEN** a waiver, override, or deviation expires or misses its follow-up condition
- **THEN** readiness and completion reports mark it invalid and identify affected gates
