## ADDED Requirements

### Requirement: Transfer-ready release candidate contents
The SDD process SHALL define a versioned external release candidate that contains every reusable artifact needed to install, configure, migrate, validate, operate, update, and roll back the first minor/major/hotfix workflow.

#### Scenario: Release candidate contains the reusable core
- **WHEN** a release candidate is prepared for transfer
- **THEN** it contains or identifies the versioned process package, configuration schemas, templates, deterministic validators, workflow entry points, role instructions, synthetic examples, compatibility metadata, transfer runbook, and release manifest

#### Scenario: Release candidate does not contain corporate values
- **WHEN** release assets are inspected before transfer
- **THEN** they contain no corporate credentials, private specifications, production URLs, internal repository exports, or inferred real owner and project values

### Requirement: Reproducible bootstrap and maintenance
The SDD process SHALL provide deterministic bootstrap, compatibility validation, upgrade, and rollback behavior for the versioned process package.

#### Scenario: Clean environment can bootstrap the reference setup
- **WHEN** a supported clean environment consumes the release candidate
- **THEN** documented non-interactive steps create or validate the reference `team-specs` setup without requiring an AI assistant

#### Scenario: Incompatible runtime is reported before gated work
- **WHEN** the installed runtime, OpenSpec version, package version, configuration schema, or required dependency is incompatible
- **THEN** deterministic validation reports the mismatch and blocks release or pilot readiness instead of allowing a weak model to infer a workaround

#### Scenario: Upgrade can be rolled back
- **WHEN** a package or configuration upgrade fails its verification gate
- **THEN** the runbook restores the previously pinned package and configuration version without rewriting canonical change or living-spec history

#### Scenario: Supported desktop hosts produce equivalent governed behavior
- **WHEN** the release candidate is bootstrapped on clean supported Windows, Linux, and macOS hosts with the documented Python, Node.js/OpenSpec, Git, MCP, shell, and package dependencies provisioned
- **THEN** the same canonical fixtures, deterministic gates, evidence contracts, update path, and rollback behavior pass without platform-specific weakening or manual source edits

### Requirement: External release acceptance gate
The SDD process SHALL require reproducible external evidence before a release candidate is accepted for corporate transfer.

#### Scenario: External gate proves the reference class-aware flow
- **WHEN** external release acceptance is evaluated
- **THEN** evidence covers clean bootstrap, configuration validation, legacy migration, minor/major/hotfix classification, change creation, Spec PR, DoR, human-owned approval, implementation controls, DoD, release or transfer readiness when applicable, archive support, traceability, and package update or rollback on a synthetic reference project

#### Scenario: External gate proves AI-disabled operation
- **WHEN** the AI assistant is disabled
- **THEN** every gated action in the reference class-aware flow remains executable and verifiable through deterministic scripts, standard tools, and human decisions

#### Scenario: External gate includes weak-model certification
- **WHEN** the release candidate includes role instructions for Qwen/DeepSeek-class assistants
- **THEN** release acceptance includes actual weak-model run evidence and the negative safety scenarios defined by the weak-model-guardrails capability

#### Scenario: Missing evidence blocks transfer readiness
- **WHEN** any mandatory release-manifest evidence is missing, failed, stale, or refers only to an AI assertion
- **THEN** the candidate is not marked transfer-ready

#### Scenario: Human owner makes the final external acceptance decision
- **WHEN** the external release-candidate evidence packet is complete
- **THEN** the human owner accepts or rejects transfer readiness using recorded Tech Lead and QA evidence plus security evidence when the applicable class, data, integration, or risk contract requires it

### Requirement: Corporate adaptation boundary
The SDD process SHALL limit corporate-environment work to verified environment inventory, real configuration, approved integration wiring, thin tool adapters, and pilot evidence.

#### Scenario: Corporate setup supplies real configuration
- **WHEN** the accepted release candidate is installed in the corporate environment
- **THEN** authorized maintainers populate real project paths, project registry, owner registry, policy overrides, approved secret references, supported standard-tool integrations, and the available AI adapter without modifying reusable process rules

#### Scenario: Unknown environment facts remain explicit
- **WHEN** runtime versions, network policy, artifact distribution, MCP availability, or integration capabilities are not yet verified
- **THEN** the adaptation checklist records them as unresolved inputs and does not infer values from external examples

#### Scenario: Corporate environment is not the primary development surface
- **WHEN** setup identifies a missing reusable schema, validator, workflow rule, role instruction, or release capability
- **THEN** the gap is routed to the external canonical source as a controlled change rather than implemented as an untracked internal fork

### Requirement: Corporate pilot entry and acceptance
The SDD process SHALL require an externally accepted release candidate and a green corporate adaptation check before a real governed-change pilot starts.

#### Scenario: Pilot entry checks the real environment
- **WHEN** maintainers request pilot entry
- **THEN** deterministic evidence confirms the installed package version, OpenSpec compatibility, configuration validity, owner and project mappings, secret handling, available integration adapters, rollback path, and AI-disabled gate execution

#### Scenario: Pilot executes one selected real governed change
- **WHEN** pilot entry is accepted
- **THEN** the team selects and executes one bounded real minor, major, or hotfix change through triage, classification, Spec Review, DoR and human approval, implementation controls, DoD, applicable release or transfer readiness, traceability, and archive readiness while recording compatibility, usability, intervention, quality, flow, and follow-up evidence

#### Scenario: Pilot failure preserves the accepted baseline
- **WHEN** the real pilot exposes an integration, adapter, or workflow failure
- **THEN** the team records the failure, rolls back or holds the affected transition, and leaves accepted specs and previously archived change history intact

### Requirement: Release evidence and auditability
The SDD process SHALL make the release candidate and corporate pilot traceable to exact versions and evidence.

#### Scenario: Release manifest identifies what was certified
- **WHEN** a release candidate is accepted
- **THEN** its manifest records the process-package version, config-schema version, OpenSpec pin, included artifact versions, compatibility assumptions, verification commands or normalized evidence paths, raw-artifact references and checksums, weak-model certification references, known limitations, and rollback reference

#### Scenario: Pilot evidence identifies installed state
- **WHEN** pilot results are recorded
- **THEN** the evidence identifies the installed release, real non-secret configuration revision, adapter versions, change ID, relevant PR and test evidence, human decisions, deviations, and follow-up changes

#### Scenario: Verification coverage is traceable and gaps remain visible
- **WHEN** release-candidate verification is reviewed
- **THEN** every applicable requirement and positive or negative scenario links to an automated test or recorded manual evidence, while any permitted gap records risk, owner, reason, compensating evidence, and follow-up instead of being hidden by an aggregate pass result

### Requirement: First transfer boundary preserves later-layer exclusions
The transfer-ready release candidate SHALL prove the accepted minor/major/hotfix core flow without requiring later automation layers.

#### Scenario: Later integrations do not block transfer readiness
- **WHEN** Jira task automation, Confluence publication, QA/AT proposal generation, role inboxes, deploy, Zephyr integration, or graph-backed project memory are absent
- **THEN** their absence does not block release-candidate or governed-pilot readiness

#### Scenario: Standard integration wiring may be configured
- **WHEN** a standard corporate tool feature is required for the real governed pilot
- **THEN** the adaptation layer may configure that feature without adding a custom integration client or expanding the release-candidate capability contract
