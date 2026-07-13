## ADDED Requirements

### Requirement: Common Definition of Ready
The SDD process SHALL define a common Definition of Ready before a change can receive human approval for implementation.

#### Scenario: Common readiness evidence is complete
- **WHEN** a change requests the `spec_review` to `approved` transition
- **THEN** it provides business goal and value, owner, scope and exclusions, type and classification rationale, affected systems and owners, dependencies, requirements and scenarios, acceptance criteria, quality and verification strategy, security/data/operations assessment, rollback or hold approach, initial traceability, resolved blocking questions, valid waivers, and required human approvals

#### Scenario: Readiness report separates blockers
- **WHEN** Definition of Ready is evaluated
- **THEN** deterministic output identifies satisfied checks, blocking gaps, advisory gaps, responsible roles, and source evidence without treating advisory items as automatic blockers

#### Scenario: Green checks do not approve implementation
- **WHEN** every deterministic readiness check passes
- **THEN** the change remains unapproved until the required human decision is recorded

### Requirement: Class-specific Definition of Ready
Definition of Ready SHALL add obligations according to the confirmed `minor`, `major`, or `hotfix` route.

#### Scenario: Minor uses minimum reviewable evidence
- **WHEN** a confirmed minor change requests approval
- **THEN** it requires the common readiness set and enough bounded impact, regression, implementation, verification, and rollback evidence to justify the minor route without major-only artifacts

#### Scenario: Major expands readiness evidence
- **WHEN** a confirmed major change requests approval
- **THEN** it additionally requires expanded design and impact analysis, architecture-decision evidence or an explicit not-required result, QA/test/automation planning or valid waivers, owner-zone approvals, dependency and migration evidence, broad regression strategy, and release-package expectations

#### Scenario: Hotfix uses accelerated entry evidence
- **WHEN** a confirmed hotfix requests accelerated implementation approval
- **THEN** it requires the harm and urgency rationale, bounded scope, named decision owner, known gaps, minimum safety and regression set, immediate rollback or hold instructions, required risk review, and a mandatory reconciliation follow-up with owner and due condition

### Requirement: Implementation-complete evidence
The process SHALL distinguish implementation completion from Definition of Done and final delivery.

#### Scenario: Implementation can be complete before final closure
- **WHEN** code or configuration, required tests, required deterministic checks, and linked implementation evidence are complete
- **THEN** the package may record implementation complete while unresolved acceptance, release, traceability, waiver, or follow-up obligations remain visible

#### Scenario: AI statement is not implementation evidence
- **WHEN** an AI assistant states that implementation is complete without source-linked code, test, or verification evidence
- **THEN** the implementation-complete check remains unsatisfied

### Requirement: Class-aware Definition of Done
The SDD process SHALL require class-aware Definition of Done evidence before `ready_to_archive` can be requested.

#### Scenario: Done includes outcome and evidence
- **WHEN** a change requests `ready_to_archive`
- **THEN** requirements and scenarios have acceptance evidence, defects and review comments are dispositioned, documentation and traceability are current, required checks are complete, waivers are valid, and all class-specific obligations are satisfied or validly deferred

#### Scenario: Hotfix reconciliation blocks closure
- **WHEN** a hotfix has unresolved mandatory reconciliation, post-change verification, or follow-up disposition
- **THEN** Definition of Done and final closure remain blocked even if the urgent implementation was applied

#### Scenario: Placeholder artifact does not satisfy done
- **WHEN** a required completion artifact exists but is empty, stale, or contains only placeholders
- **THEN** deterministic validation treats the obligation as incomplete

### Requirement: Release and transfer readiness
The process SHALL evaluate release or transfer readiness separately when the change affects a deliverable or operational handoff.

#### Scenario: Release package is complete
- **WHEN** release or transfer readiness applies
- **THEN** the evidence includes version or tag, release notes, included change and requirement IDs, verification summary, known limitations, deployment or transfer instructions, rollback or hold instructions, operational/support checks, responsible roles, and unresolved follow-ups

#### Scenario: Non-release change records not-applicable rationale
- **WHEN** a change has no releasable or transferable outcome
- **THEN** the release-readiness field records an approved not-applicable rationale rather than fabricating release evidence

#### Scenario: Major and hotfix default to release-package evidence
- **WHEN** a major or hotfix change produces a releasable or transferable outcome
- **THEN** release/transfer readiness and its complete evidence package are mandatory before final closure

### Requirement: Archive readiness and archive approval
Archive readiness SHALL mean that canonical change evidence can be reconciled into accepted specs, not that external delivery has necessarily completed.

#### Scenario: Archive readiness checks canonical completion
- **WHEN** `ready_to_archive` is requested
- **THEN** deterministic checks evaluate Definition of Done, required release or transfer evidence, traceability, waivers, follow-ups, and current policy compatibility

#### Scenario: Archive remains human-approved
- **WHEN** final archive checks pass
- **THEN** `archived` still requires explicit human archive approval and the accepted OpenSpec archive action

### Requirement: External delivered or done state remains distinct
The SDD process SHALL not infer tracker delivery, deployment, customer acceptance, or production completion from OpenSpec archive state.

#### Scenario: Archive does not close Jira automatically
- **WHEN** a change becomes `archived`
- **THEN** tracker status changes only through the configured corporate mapping and required human or integration evidence

#### Scenario: Tracker Done has configured evidence
- **WHEN** a corporate project maps an external status such as `Done`
- **THEN** the mapping identifies the required deployment, acceptance, release, support, or closure evidence and the role authorized to record it
