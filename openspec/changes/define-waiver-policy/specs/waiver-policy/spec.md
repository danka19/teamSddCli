## ADDED Requirements

### Requirement: Proposed waiver record
The SDD process SHALL define a structured waiver record before missing required evidence can be accepted.

#### Scenario: Waiver has required audit fields
- **WHEN** a change package uses a waiver
- **THEN** the waiver records ID, type, affected requirements or scenarios, reason, evidence, approver, date, and follow-up or expiry when risk remains

#### Scenario: Free-text exception is rejected
- **WHEN** a required artifact or verification step is missing and the change only contains an unapproved free-text note
- **THEN** deterministic validation or review treats the requirement as unmet

### Requirement: Proposed waiver approval ownership
The SDD process SHALL keep waiver approval human-owned and role-appropriate.

#### Scenario: AI cannot approve a waiver
- **WHEN** an AI assistant drafts waiver text or recommends accepting an exception
- **THEN** the waiver remains invalid until a human approver records approval in the change package or review surface

#### Scenario: Approver matches waived obligation
- **WHEN** a waiver covers missing test, automation, design, or documentation evidence
- **THEN** the approver role matches the obligation being waived according to the approved policy

### Requirement: Waiver negative cases
The SDD process SHALL define cases where a waiver is not sufficient.

#### Scenario: Waiver cannot replace human approval
- **WHEN** a change requires human approval, merge approval, or final archive approval
- **THEN** a waiver cannot substitute for that approval

#### Scenario: Waiver cannot hide behavior scenario coverage
- **WHEN** a behavior requirement has no scenario or acceptance-example coverage
- **THEN** a waiver cannot make the change archive-ready

#### Scenario: Non-behavior work is reclassified instead of waived
- **WHEN** work has no behavior-changing requirement and therefore has no behavior scenario coverage
- **THEN** the package is reclassified or handled through the limited no-spec-change rationale with human reviewer approval and replacement evidence instead of using a waiver to bypass behavior scenario coverage

#### Scenario: Waiver cannot bypass mandatory risk review
- **WHEN** a change triggers security, compliance, data, public API, mobile release, or cross-repo risk review
- **THEN** a waiver cannot bypass the review unless the approved policy explicitly names the permitted exception and approver

### Requirement: Waiver policy approval gate
The waiver policy SHALL remain proposed until the Phase 1 human decision gate approves approvers and minimum evidence.

#### Scenario: Proposal does not change validator behavior immediately
- **WHEN** this proposed change is drafted
- **THEN** existing templates, validators, tests, and pre-commit behavior remain unchanged until a later approved implementation work item
