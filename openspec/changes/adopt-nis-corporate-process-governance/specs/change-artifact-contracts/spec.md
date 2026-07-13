## ADDED Requirements

### Requirement: Minor change artifact contract
The SDD process SHALL define a compact minor artifact contract for bounded low-impact work that has passed deterministic classification.

#### Scenario: Minor change has minimum reviewable evidence
- **WHEN** a confirmed minor change is prepared for review and implementation
- **THEN** it includes proposal intent, required OpenSpec delta for behavior change, testable scenarios, classification rationale, bounded impact and risk evidence, quality and regression approach, basic traceability, implementation plan, verification evidence, rollback or hold approach, and required human decisions

#### Scenario: Minor avoids major-only burden
- **WHEN** no major trigger applies and release, journey/screen, broad QA/AT, migration, or cross-team evidence is not applicable
- **THEN** those major-only artifacts are not required when the minor package records enough evidence or an approved not-applicable result for deterministic validation

### Requirement: Major change artifact contract
The SDD process SHALL define an expanded major artifact contract for changes with any material impact trigger.

#### Scenario: Major change expands required evidence
- **WHEN** a confirmed major change reaches Definition of Ready or Definition of Done
- **THEN** it includes expanded design and impact analysis, architecture decision or not-required evidence, owner/dependency map, quality strategy, QA/test and automation plans or valid waivers, broad regression matrix, migration and rollback evidence where applicable, a release/transfer package or approved not-applicable result when no releasable outcome exists, complete traceability, and class-appropriate approvals

#### Scenario: Empty major artifact is not evidence
- **WHEN** a required major artifact contains only placeholders, stale content, or non-substantive text
- **THEN** deterministic validation or review treats the obligation as incomplete

### Requirement: Hotfix change artifact contract
The SDD process SHALL define an accelerated hotfix artifact contract with mandatory pre-change minimums and post-change reconciliation.

#### Scenario: Hotfix entry package is bounded
- **WHEN** a hotfix is approved for implementation
- **THEN** it contains harm and urgency rationale, bounded scope, affected contour, named decision owner, known gaps, testable scenario, minimum safety and regression evidence, rollback or hold instructions, required risk decisions, traceability, and a reconciliation plan

#### Scenario: Deferred artifact has follow-up
- **WHEN** policy permits a non-safety artifact to be deferred because of hotfix urgency
- **THEN** a structured deferral identifies substitute evidence, owner, approver, residual risk, due condition, and completion evidence required before closure

#### Scenario: Hotfix release package is reconciled
- **WHEN** an urgent hotfix creates or changes a releasable outcome
- **THEN** a complete release/transfer package is required before final closure even if permitted parts were deferred until after the urgent implementation

#### Scenario: Hotfix does not bypass major-impact evidence silently
- **WHEN** a hotfix triggers one or more major-impact rules
- **THEN** its artifact matrix shows the major obligations and their completed, deferred, waived, not-applicable, or blocking status


## MODIFIED Requirements

### Requirement: Artifact waiver eligibility
The artifact contract SHALL distinguish required artifacts that may be waived or deferred from artifacts that are always required.

#### Scenario: Core source artifacts cannot be waived
- **WHEN** a change package is prepared for review
- **THEN** proposal intent, required OpenSpec delta, scenario evidence, classification evidence, and basic traceability cannot be replaced by an unapproved free-text note

#### Scenario: No-spec-change rationale is limited
- **WHEN** a change uses a no-spec-change rationale
- **THEN** it is acceptable only for docs-only, refactor, or no-behavior-change maintenance with human reviewer approval and replacement evidence proving that no behavior contract changed

#### Scenario: No-spec-change rationale cannot hide behavior change
- **WHEN** a change modifies behavior but provides only a no-spec-change rationale instead of an OpenSpec delta
- **THEN** deterministic validation or review rejects the package as not archive-ready

#### Scenario: QA or automation artifact can be waived with approved evidence
- **WHEN** a major package does not need a new test case or automation artifact
- **THEN** the missing artifact is acceptable only when an approved waiver records reason, substitute evidence, approver, residual risk, and follow-up or expiry where applicable

#### Scenario: Hotfix deferral follows restricted policy
- **WHEN** a hotfix cannot complete a permitted non-safety artifact before urgent implementation
- **THEN** the artifact is deferred only through the structured hotfix deferral policy and remains a closure obligation

### Requirement: Artifact matrix baseline status
The Phase 1 artifact matrix SHALL remain historical accepted evidence while the target matrix is versioned and replaced with minor, major, and hotfix routes through this change.

#### Scenario: Existing implementation evidence remains recorded
- **WHEN** legacy template or validator behavior is audited
- **THEN** Phase 1 work items 1.8 and 1.9 remain valid evidence for the legacy subset without being presented as the target classification contract

#### Scenario: Target matrix is versioned
- **WHEN** target templates or validators select required evidence
- **THEN** they use the accepted minor, major, and hotfix matrix version resolved from the process configuration

#### Scenario: Deferred integrations are explicit
- **WHEN** a minor first release has no Jira task automation, Confluence publication, generated QA/AT proposal, or role inbox evidence
- **THEN** the artifact matrix treats those later-layer artifacts according to the approved implementation boundary and does not invent evidence

#### Scenario: Future corrections use accepted-spec workflow
- **WHEN** the target artifact matrix is corrected or expanded after acceptance
- **THEN** the correction is proposed as a new OpenSpec change against the accepted baseline

### Requirement: Future journey and screen artifacts
The artifact contract SHALL plan journey and screen artifacts as conditional evidence without making them universal requirements for minor work.

#### Scenario: UI major package may require screen catalog
- **WHEN** a major UI-impacting package changes journeys or screens
- **THEN** policy may require versioned screen assets and a catalog linking screen IDs to capability, journey, journey step, state, source, requirements, and scenarios

#### Scenario: Non-UI minor does not require screen catalog
- **WHEN** a minor change has no journey or screen impact
- **THEN** absence of `journey.yaml`, `screens.yaml`, or `assets/screens/` does not block the package

#### Scenario: Hotfix records deferred UI evidence
- **WHEN** an urgent UI hotfix cannot complete otherwise applicable screen evidence before implementation
- **THEN** the missing evidence follows the restricted deferral and reconciliation policy

### Requirement: Legacy baseline artifact mode
The artifact contract SHALL allow gradual documentation of already-written behavior without requiring complete retroactive packages for historical changes.

#### Scenario: Legacy change records observed behavior
- **WHEN** a change touches legacy behavior that is not fully covered by living specs
- **THEN** the package records observed existing behavior, proposed changed behavior, regression scenario, known gaps, and screenshots when UI behavior is affected

#### Scenario: Historical changes do not require retroactive target package
- **WHEN** behavior already exists before SDD coverage
- **THEN** the process does not require a complete retroactive minor, major, or hotfix package unless a later human decision explicitly scopes a baseline or discovery effort


## REMOVED Requirements

### Requirement: Thin change artifact contract
**Reason**: The human owner selected the real corporate NIS classification, so `thin` is no longer target process vocabulary.

**Migration**: Map supported non-archived `mode: thin` packages to `classification: minor`, then re-run deterministic classification because the target minor route is conditional rather than a blind permanent alias.

### Requirement: Full package artifact contract
**Reason**: The human owner selected the real corporate NIS classification, so `full` is no longer target process vocabulary.

**Migration**: Map supported non-archived `mode: full` packages to `classification: major`; preserve existing evidence and validate it against the target major matrix.
