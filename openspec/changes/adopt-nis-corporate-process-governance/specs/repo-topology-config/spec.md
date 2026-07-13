## ADDED Requirements

### Requirement: Corporate governance policy configuration
The central process configuration SHALL declare the versioned policy sources used for classification, readiness, completion, regression, stop/escalation, release handoff, and pilot measurement.

#### Scenario: Config points to canonical policy versions
- **WHEN** deterministic tooling evaluates a change package
- **THEN** it can resolve the process package version, classification policy, artifact matrix, readiness/completion policy, regression matrix version, waiver policy, and workflow-mapping version from validated central configuration

#### Scenario: Project adapter cannot weaken canonical minimums silently
- **WHEN** a project adapter overrides a configurable threshold or mapping
- **THEN** validation identifies the override source and rejects any value that falls below a non-configurable canonical safety or approval minimum

#### Scenario: Missing corporate value is not guessed
- **WHEN** a real Jira state, SLA threshold, approver identity, retention period, environment, integration endpoint, or pilot value is required but absent
- **THEN** setup or validation reports the missing corporate input and does not infer a production value

### Requirement: Tech lead ownership registry
The owner registry SHALL represent tech-lead authority and escalation relationships without making one person the universal owner of all decisions.

#### Scenario: Tech lead mapping is resolvable
- **WHEN** a change affects one or more owner zones
- **THEN** `owners.yaml` or its accepted successor identifies the applicable tech lead, delegate rules, escalation route, and the decision types the role may approve

#### Scenario: Conflicting authority is visible
- **WHEN** affected zones resolve to conflicting tech leads, missing delegates, or incompatible decision authority
- **THEN** readiness reports the conflict and requires a human owner-resolution decision before the affected approval can pass

#### Scenario: Other role authority is preserved
- **WHEN** the tech lead is resolved for a change
- **THEN** product, analyst, QA, AT, security/compliance, release, repository, and archive responsibilities remain separately resolvable according to policy

### Requirement: External workflow mapping
Canonical OpenSpec lifecycle and business gates SHALL map to corporate tracker and release states through validated configuration.

#### Scenario: Mapping distinguishes archive and delivered
- **WHEN** a project config maps OpenSpec status to Jira or another tracker
- **THEN** it represents archive readiness, archived specification state, release readiness, deployment, acceptance, and external Done as distinct concepts when the corporate workflow distinguishes them

#### Scenario: Unmapped external status blocks automation
- **WHEN** an integration encounters an external status or transition not present in the approved mapping
- **THEN** it stops or reports the unknown state for human resolution instead of guessing a canonical transition

### Requirement: Corporate configuration remains external to reusable source
The reusable process package SHALL contain schemas, placeholders, and synthetic fixtures rather than real corporate identifiers, credentials, or sensitive exports.

#### Scenario: Corporate adaptation supplies local values
- **WHEN** the release candidate enters the corporate adaptation step
- **THEN** approved local ignored configuration supplies real project, Jira, owner, model/runtime, integration, retention, and security values

#### Scenario: Reusable correction returns upstream
- **WHEN** the corporate pilot discovers a reusable policy or schema correction
- **THEN** the correction is proposed against the external canonical OpenSpec source and is not maintained as an invisible internal fork
