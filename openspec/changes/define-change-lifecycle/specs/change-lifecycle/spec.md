## ADDED Requirements

### Requirement: Proposed lifecycle states
The SDD process SHALL define proposed lifecycle states for change packages before deterministic tools enforce state transitions.

#### Scenario: Thin change remains lightweight
- **WHEN** a change is classified as a thin change
- **THEN** the proposed lifecycle requires draft, review, approval, implementation evidence, and archive readiness without requiring full QA/AT/package artifacts by default

#### Scenario: Full package uses expanded evidence
- **WHEN** a change is feature, API, mobile, cross-repo, high-risk, or otherwise classified as a full change package
- **THEN** the proposed lifecycle requires expanded design, QA, AT, risk, and traceability evidence before archive readiness

### Requirement: Deterministic transition gates
The SDD process SHALL define deterministic checks for lifecycle transitions where the transition can be validated without human judgment.

#### Scenario: Allowed transitions are explicit
- **WHEN** deterministic tooling or review evaluates a lifecycle status change
- **THEN** only these transitions are proposed as valid: `draft` -> `spec_review`, `spec_review` -> `draft`, `spec_review` -> `approved`, `approved` -> `in_implementation`, `in_implementation` -> `ready_to_archive`, `ready_to_archive` -> `in_implementation`, and `ready_to_archive` -> `archived`

#### Scenario: Spec PR transition checks structure
- **WHEN** a change moves from `draft` to `spec_review`
- **THEN** deterministic validation checks required files, metadata shape, at least one OpenSpec delta, and scenario presence

#### Scenario: Archive transition checks completion evidence
- **WHEN** a change moves to `ready_to_archive`
- **THEN** deterministic validation checks traceability completion, required verification evidence, and approved waivers before archive is requested

#### Scenario: Draft cannot skip to approved
- **WHEN** a change attempts to move directly from `draft` to `approved`
- **THEN** deterministic validation or review rejects the transition because Spec PR review and human approval evidence are missing

#### Scenario: Draft cannot skip to archive readiness
- **WHEN** a change attempts to move directly from `draft` to `ready_to_archive`
- **THEN** deterministic validation or review rejects the transition because review, approval, implementation, and verification evidence are missing

#### Scenario: Archive requires explicit human approval
- **WHEN** any change attempts to move to `archived`
- **THEN** deterministic validation or review rejects the transition unless the current state is `ready_to_archive`, final archive checks pass, and explicit human archive approval is recorded

### Requirement: Human approval ownership
The SDD process SHALL preserve human ownership for approval, merge, correctness, and final archive decisions.

#### Scenario: AI cannot approve lifecycle transitions
- **WHEN** an AI assistant drafts text, reviews a package, or proposes a state change
- **THEN** the proposal remains advisory until a human records the decision through Git, PR review, or an approved process artifact

#### Scenario: CI blocks but does not approve
- **WHEN** deterministic checks pass for a lifecycle transition
- **THEN** the checks allow the transition to proceed but do not replace human approval where approval is required

### Requirement: MVP boundary for lifecycle automation
The first lifecycle implementation SHALL stay focused on the thin change flow unless the human owner explicitly re-scopes the MVP.

#### Scenario: Deferred integrations are not lifecycle blockers
- **WHEN** a thin MVP change has no Jira task automation, Confluence publication, QA/AT proposal generation, or role inbox evidence
- **THEN** the lifecycle proposal does not treat those deferred integrations as required blockers for the first MVP
