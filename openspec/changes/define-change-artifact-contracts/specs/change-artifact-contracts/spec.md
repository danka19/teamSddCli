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

### Requirement: Artifact matrix acceptance status
The artifact matrix approved in Phase 1 work item 1.3 SHALL remain proposed OpenSpec behavior until the final archive/accepted-spec gate promotes it.

#### Scenario: Approved matrix does not change deterministic behavior immediately
- **WHEN** this proposed change is drafted
- **THEN** templates, validators, tests, and pre-commit behavior remain unchanged until a later approved implementation work item

#### Scenario: Accepted specs still require final archive approval
- **WHEN** the Phase 1 artifact matrix has human decision approval
- **THEN** it is still not written to accepted `openspec/specs/` until the final human archive or acceptance gate approves promotion

#### Scenario: First MVP excludes later workflow artifacts
- **WHEN** a thin first-MVP change has no Jira task, Confluence publication, QA/AT proposal, or role inbox evidence
- **THEN** the artifact contract does not treat those missing later-layer artifacts as review or archive blockers

### Requirement: Future journey and screen artifacts
The artifact contract SHALL plan journey and screen artifacts as later contracts without making them mandatory for the first thin MVP.

#### Scenario: UI full package may reference screen catalog
- **WHEN** a future UI-impacting full package includes screen evidence
- **THEN** the package may store versioned screen assets and a screen catalog linking screen IDs to capability, journey, journey step, state, source, requirements, and scenarios

#### Scenario: Thin MVP does not require screen catalog
- **WHEN** a first-MVP thin change has no journey or screen catalog
- **THEN** the absence of `journey.yaml`, `screens.yaml`, or `assets/screens/` does not block the package

### Requirement: Legacy baseline artifact mode
The artifact contract SHALL allow gradual documentation of already-written behavior without requiring full retroactive packages for historical changes.

#### Scenario: Legacy change records observed behavior
- **WHEN** a change touches legacy behavior that is not fully covered by living specs
- **THEN** the package records observed existing behavior, proposed changed behavior, regression scenario, known gaps, and screenshots when UI behavior is affected

#### Scenario: Historical changes do not require retroactive full package
- **WHEN** behavior already exists before SDD coverage
- **THEN** the process does not require a full historical change package unless a later human decision explicitly scopes a baseline/discovery effort
