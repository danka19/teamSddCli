## ADDED Requirements

### Requirement: Proposed thin change artifact contract
The SDD process SHALL define a proposed thin change artifact contract before deterministic tools enforce missing-artifact failures.

#### Scenario: Thin change has minimum reviewable evidence
- **WHEN** a change is classified as a thin change
- **THEN** the proposed contract requires proposal intent, at least one OpenSpec delta for behavior-changing SDD work, at least one testable scenario per requirement, basic traceability, and verification evidence

#### Scenario: Thin change avoids full package burden by default
- **WHEN** a thin change has no feature, public API, mobile, cross-repo, data/security, or high-risk impact
- **THEN** the proposed contract does not require QA/AT plans, Confluence publication evidence, Jira task creation, or role inbox evidence by default

#### Scenario: Behavior-changing work requires OpenSpec delta by default
- **WHEN** a change modifies SDD workflow behavior, artifact/process contracts, user-visible behavior, validation behavior, or future CLI behavior
- **THEN** the proposed contract requires an OpenSpec delta and does not accept a no-spec-change rationale as the default path

### Requirement: Proposed full package artifact contract
The SDD process SHALL define a proposed full change package contract for broader or riskier changes.

#### Scenario: Full package trigger expands required evidence
- **WHEN** a change is feature, public API, mobile, cross-repo, data/security, or high-risk
- **THEN** the proposed contract requires expanded design, impact analysis, QA strategy, test case or waiver evidence, automation plan or waiver evidence, and complete traceability before archive readiness

#### Scenario: Empty artifacts are not accepted as evidence
- **WHEN** a required artifact exists but contains only placeholders or non-substantive text
- **THEN** deterministic validation or review treats the artifact as incomplete

### Requirement: Artifact waiver eligibility
The artifact contract SHALL distinguish required artifacts that may be waived from artifacts that are always required.

#### Scenario: Core source artifacts cannot be waived
- **WHEN** a change package is prepared for review
- **THEN** proposal intent, required OpenSpec delta, scenario evidence, and basic traceability cannot be replaced by an unapproved free-text note

#### Scenario: No-spec-change rationale is limited
- **WHEN** a change uses a no-spec-change rationale
- **THEN** it is acceptable only for docs-only, refactor, or no-behavior-change maintenance with human reviewer approval and replacement evidence proving that no behavior contract changed

#### Scenario: No-spec-change rationale cannot hide behavior change
- **WHEN** a change modifies behavior but provides only a no-spec-change rationale instead of an OpenSpec delta
- **THEN** deterministic validation or review rejects the package as not archive-ready

#### Scenario: QA or automation artifact can be waived with approved evidence
- **WHEN** a full package does not need a new test case or automation artifact
- **THEN** the missing artifact is acceptable only when an approved waiver records reason, evidence, and approver

### Requirement: Artifact matrix approval gate
The artifact matrix SHALL remain proposed until the Phase 1 human decision gate approves it.

#### Scenario: Proposal does not change deterministic behavior immediately
- **WHEN** this proposed change is drafted
- **THEN** templates, validators, tests, and pre-commit behavior remain unchanged until a later approved implementation work item
