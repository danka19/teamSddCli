# traceability-contract Specification

## Purpose
Define the accepted traceability contract for review readiness, archive readiness, waived links, AI advisory suggestions, future journey/screen traceability, and legacy baseline gaps.
## Requirements
### Requirement: Review-minimum traceability
The SDD process SHALL define minimum traceability required before a change is reviewable.

#### Scenario: Requirement links to scenario
- **WHEN** a change package enters Spec PR review
- **THEN** each proposed requirement has at least one testable scenario and a traceability row linking the requirement to that scenario

#### Scenario: Missing scenario blocks review readiness
- **WHEN** a requirement has no testable scenario
- **THEN** deterministic validation or review reports the missing scenario before the change is considered ready for review

### Requirement: Archive-readiness traceability
The SDD process SHALL define completion traceability required before a change can be archived.

#### Scenario: Full package archive checks downstream evidence
- **WHEN** a full change package requests archive readiness
- **THEN** traceability links requirements and scenarios to required dev evidence, QA evidence, automation evidence, or approved waivers

#### Scenario: Thin change archive accepts practical evidence
- **WHEN** a thin change requests archive readiness before Jira or QA/AT automation exists in the MVP
- **THEN** traceability may use committed verification notes, PR links, test command evidence, or approved waivers instead of generated task/test IDs

#### Scenario: Verification evidence remains source-linked
- **WHEN** traceability records verification evidence
- **THEN** the evidence points to a committed note, PR, CI or local test output, manual QA record, automation result, or approved waiver rather than a generated display alone

#### Scenario: Pending traceability is allowed before archive readiness
- **WHEN** a change is in review or implementation before archive readiness
- **THEN** required downstream task, test, automation, or evidence links may be marked pending when the missing evidence is expected later in the lifecycle

#### Scenario: Pending downstream link blocks archive readiness
- **WHEN** a change requests archive readiness and a required downstream link is still marked pending
- **THEN** deterministic validation or review rejects archive readiness unless the link is replaced by concrete evidence or an approved waiver

### Requirement: Waived traceability links
The SDD process SHALL require approved waiver evidence before missing required traceability links are accepted.

#### Scenario: Missing automation link requires waiver
- **WHEN** automation is required by the approved artifact policy but no automation evidence exists
- **THEN** archive readiness fails unless an approved waiver links to the affected requirement and scenario

#### Scenario: Waiver does not hide requirement coverage
- **WHEN** a waiver covers missing task, test, or automation evidence
- **THEN** the requirement and scenario remain visible in traceability with a waived status and waiver reference

### Requirement: AI traceability suggestions are advisory
AI-generated traceability suggestions SHALL remain advisory until reviewed and committed.

#### Scenario: AI proposes missing links
- **WHEN** an AI assistant suggests traceability rows or coverage gaps
- **THEN** the rows become evidence only after a human reviews and commits them to the change package

### Requirement: Future journey and screen traceability
The SDD process SHALL plan journey and screen traceability as later contracts without making them first-MVP blockers.

#### Scenario: Journey view links product path to evidence
- **WHEN** a future customer journey view is generated
- **THEN** it links journey steps to screens, requirements, scenarios, and test or verification evidence

#### Scenario: Screen catalog preserves requirement links
- **WHEN** a future screen catalog is used for a UI-impacting full package
- **THEN** each screen entry links a stable screen ID to file path, capability, journey, journey step, state, source, requirement refs, and scenario refs

#### Scenario: First MVP does not require journey or screen traceability
- **WHEN** a first-MVP thin change has no journey or screen metadata
- **THEN** the missing journey/screen links do not block review or archive readiness

### Requirement: Legacy baseline traceability
The SDD process SHALL make legacy coverage gaps visible without requiring full retroactive traceability for historical behavior.

#### Scenario: Legacy baseline records known gaps
- **WHEN** already-written behavior is documented through a legacy baseline
- **THEN** traceability records what is known, what is observed, known gaps, risks, and regression scenarios where available

#### Scenario: Legacy gaps are not hidden in generated views
- **WHEN** legacy behavior lacks full requirement, scenario, or test coverage
- **THEN** traceability and generated views show the gap instead of marking the area fully covered
