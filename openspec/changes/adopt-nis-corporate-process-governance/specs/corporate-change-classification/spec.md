## ADDED Requirements

### Requirement: Canonical corporate change classification
The SDD process SHALL use the flat `minor`, `major`, and `hotfix` classification as the only target user-facing process-route vocabulary.

#### Scenario: New package uses canonical classification
- **WHEN** a new change package is created
- **THEN** `change.yaml` records exactly one of `minor`, `major`, or `hotfix` in `classification` and does not offer `thin` or `full` as current choices

#### Scenario: Work type remains separate
- **WHEN** a change is classified
- **THEN** its work `type`, lifecycle `status`, and risk evidence remain separate fields and do not create another user-facing process classification axis

#### Scenario: Unknown class is rejected
- **WHEN** metadata contains an unrecognized classification
- **THEN** deterministic validation fails with the allowed values and the source field that must be corrected

### Requirement: Deterministic minor eligibility
The SDD process SHALL allow `minor` only when every approved low-impact condition is satisfied.

#### Scenario: Bounded low-impact change qualifies as minor
- **WHEN** a change is local and small, rollback is simple, and it has no user-scenario, SLA, security/compliance, external-integration, data-model, component-interaction, public-API, cross-repository, reliability, performance, operations, governed-test, or governed-documentation impact and needs no architecture decision
- **THEN** the classifier may report `minor` with the satisfied conditions and required minor evidence

#### Scenario: Missing minor evidence blocks minor route
- **WHEN** one or more required minor conditions is unknown or unsupported
- **THEN** deterministic classification reports the uncertainty as a blocker and does not silently treat the change as minor

### Requirement: Conservative major triggers
The SDD process SHALL require `major` whenever any approved major trigger applies and the work is not being handled through the accelerated hotfix route.

#### Scenario: Any material trigger requires major
- **WHEN** a change adds a feature, changes business logic, a user scenario, component interaction, required test behavior, or governed user/operational documentation, changes a public API, integration, data, security, compliance, or SLA contract, adds an external dependency, spans repositories, materially affects reliability, performance, or operations, creates regression risk or high rollback cost, or requires an architecture decision
- **THEN** deterministic classification reports `major`, the triggering rules, and the expanded evidence obligations

#### Scenario: Multiple triggers remain visible
- **WHEN** more than one major trigger applies
- **THEN** the classification report lists every triggered rule instead of recording only the first match

### Requirement: Accelerated hotfix route
The SDD process SHALL use `hotfix` only when delay increases concrete production or pre-production harm and an accelerated route is justified.

#### Scenario: Urgent harmful delay qualifies for hotfix assessment
- **WHEN** an incident, material defect, security exposure, failed release, or comparable condition will cause greater harm if correction waits for the standard sequence
- **THEN** the classifier may propose `hotfix` and records the harm, urgency, affected contour, bounded scope, decision owner, and known gaps

#### Scenario: Convenience does not qualify as hotfix
- **WHEN** a team requests `hotfix` only to meet a preferred date, avoid normal review, or reduce artifact work without evidence of increasing harm
- **THEN** deterministic validation or review rejects the hotfix rationale

#### Scenario: Hotfix preserves minimum safety evidence
- **WHEN** a hotfix proceeds through the accelerated route
- **THEN** human ownership, minimum scenario and regression evidence, rollback or hold instructions, traceability, required security or compliance review, and mandatory reconciliation follow-up remain required

#### Scenario: Major-impact hotfix keeps risk obligations visible
- **WHEN** a hotfix also triggers major-impact criteria
- **THEN** the report records those triggers and retains the corresponding risk obligations unless a specifically permitted non-safety artifact has an approved time-bounded deferral

### Requirement: Explainable classification report
Deterministic tooling SHALL produce an auditable classification report before a class-dependent gate is evaluated.

#### Scenario: Report explains the result
- **WHEN** classification is evaluated
- **THEN** the report contains the proposed or confirmed class, source metadata, satisfied conditions, triggered rules, unknown inputs, blockers, required artifacts, required reviewers, and tool/policy version

#### Scenario: Machine-readable result is stable
- **WHEN** the same normalized input and policy version are evaluated repeatedly
- **THEN** the machine-readable classification result is semantically identical

### Requirement: Human-owned classification confirmation and correction
Final classification SHALL remain human-confirmed, SHALL allow correction of erroneous source evidence, and SHALL NOT allow a waiver or per-change decision to weaken canonical class criteria.

#### Scenario: AI recommendation is advisory
- **WHEN** an AI assistant recommends a class or drafts rationale
- **THEN** the recommendation cannot mutate canonical classification or satisfy an approval field until an authorized human records the decision

#### Scenario: Under-classification is rejected
- **WHEN** metadata declares `minor` but a major trigger is present
- **THEN** deterministic validation blocks the route until the class is corrected to major or, when urgency and harm satisfy the canonical rule, hotfix

#### Scenario: Erroneous source input is corrected and recalculated
- **WHEN** an authorized human proves that a classifier input or triggered fact is wrong
- **THEN** the source evidence is corrected with author, reason, date, and reference and the deterministic classifier runs again instead of recording a lower-class exception

#### Scenario: Stricter route may be selected
- **WHEN** uncertainty or local policy requires more evidence than the minimum classifier result
- **THEN** an authorized human may select a stricter route and records the reason without weakening any canonical obligation

#### Scenario: Class criteria change only through policy change
- **WHEN** the team believes a canonical major trigger should permit minor treatment
- **THEN** the current change remains blocked or major and the criterion may change only through a separately reviewed and accepted versioned policy/OpenSpec change

### Requirement: Legacy classification migration
The process SHALL provide a bounded deterministic migration from the legacy `thin` and `full` vocabulary.

#### Scenario: Legacy values map conservatively
- **WHEN** a current non-archived package uses `mode: thin` or `mode: full`
- **THEN** migration proposes `classification: minor` or `classification: major` respectively and never assigns `hotfix` automatically

#### Scenario: Migration preview precedes mutation
- **WHEN** a migration is requested
- **THEN** a check mode emits a machine-readable plan, ambiguities, preserved fields, and affected paths before apply mode is allowed

#### Scenario: Migration is idempotent
- **WHEN** apply mode runs twice against a successfully migrated package
- **THEN** the second run makes no semantic change and reports that the target schema is already satisfied

#### Scenario: Accepted archive history is preserved
- **WHEN** legacy words exist in accepted or archived historical artifacts
- **THEN** migration leaves those artifacts unchanged and treats the words as historical evidence rather than current options
