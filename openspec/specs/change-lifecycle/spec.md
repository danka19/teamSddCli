# change-lifecycle Specification

## Roadmap

- Roadmap phase: P1
- Related phases: P2, P3

## Purpose
Define the accepted SDD change lifecycle states, transition gates, human approval boundaries, MVP automation boundary, generated status display rules, and archive history convention.
## Requirements
### Requirement: Lifecycle states
The SDD process SHALL define lifecycle states for change packages before deterministic tools enforce state transitions.

#### Scenario: Thin change remains lightweight
- **WHEN** a change is classified as a thin change
- **THEN** the lifecycle requires draft, review, approval, implementation evidence, and archive readiness without requiring full QA/AT/package artifacts by default

#### Scenario: Full package uses expanded evidence
- **WHEN** a change is feature, API, mobile, cross-repo, high-risk, or otherwise classified as a full change package
- **THEN** the lifecycle requires expanded design, QA, AT, risk, and traceability evidence before archive readiness

### Requirement: Deterministic transition gates
The SDD process SHALL define deterministic checks for lifecycle transitions where the transition can be validated without human judgment.

#### Scenario: Allowed transitions are explicit
- **WHEN** deterministic tooling or review evaluates a lifecycle status change
- **THEN** only these transitions are valid: `draft` -> `spec_review`, `spec_review` -> `draft`, `spec_review` -> `approved`, `approved` -> `in_implementation`, `in_implementation` -> `ready_to_archive`, `ready_to_archive` -> `in_implementation`, and `ready_to_archive` -> `archived`

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
- **THEN** the lifecycle does not treat those deferred integrations as required blockers for the first MVP

### Requirement: Derived approval and verification display
The SDD process SHALL distinguish lifecycle source-of-truth state from generated displays of that state.

#### Scenario: Confluence displays but does not own approval state
- **WHEN** a generated Confluence view displays lifecycle, approval, or verification status
- **THEN** the displayed state is derived from source artifacts such as the change package, PR/review surface, CI evidence, tracker state after tasks exist, or approved waiver records

#### Scenario: Generated view cannot approve transition
- **WHEN** a generated Confluence page shows that all displayed status rows are green
- **THEN** the page does not replace human approval, merge approval, final archive approval, or deterministic checks required by the lifecycle

#### Scenario: Public lifecycle can be simpler than internal readiness
- **WHEN** the process is explained to business or stakeholder readers
- **THEN** it may use the simplified lifecycle `draft -> spec_review -> approved -> implemented -> archived` while internal validation may separately track implementation and archive-readiness evidence

### Requirement: Archive history convention
The SDD process SHALL define an archive history convention for changes archived into accepted specs.

#### Scenario: Archive uses dated history path
- **WHEN** a change package is archived after explicit human approval
- **THEN** the convention moves it under a dated archive path such as `openspec/changes/archive/YYYY-MM-DD-<change-id>` or the closest OpenSpec CLI-compatible equivalent

#### Scenario: Archive commit is greppable
- **WHEN** archive movement is committed
- **THEN** the commit message follows a stable grammar such as `spec: archive <change-id>` so archive history can be searched and audited

#### Scenario: Archive convention does not replace approval
- **WHEN** the archive path and commit grammar are satisfied
- **THEN** they still do not replace final deterministic checks or explicit human archive approval
