## ADDED Requirements

### Requirement: Situation-based guided operation
The process package SHALL provide one versioned, discoverable guided-operation interface that maps a declared user situation and known facts to permitted next commands, expected inputs, expected evidence, blockers, deterministic fallbacks, and human decision boundaries.

#### Scenario: User starts from a business requirement
- **WHEN** a human or AI assistant declares a new synthetic business requirement
- **THEN** the guided interface identifies the draft-change and Delta Spec preparation route, explains the required human classification confirmation, and does not require prior knowledge of repository-internal script names

#### Scenario: Existing change has a known state
- **WHEN** a user provides a valid change identity and its known lifecycle/evidence state
- **THEN** the guided interface returns only the catalog-declared next permitted operations and their required evidence

#### Scenario: Unknown or incomplete situation blocks safely
- **WHEN** the situation, required facts, or canonical context is unknown or incomplete
- **THEN** the guided interface returns a structured block, the missing inputs, and the accountable human route instead of guessing a command or decision

### Requirement: Shared human and AI operating instructions
The package SHALL provide a concise onboarding guide usable by humans and AI assistants that is generated from or deterministically validated against the versioned guided-operation contract.

#### Scenario: Guide begins with a business situation
- **WHEN** a new colleague opens the onboarding guide
- **THEN** the guide starts with supported business situations and leads to the relevant command, evidence, and human decision rather than requiring prior knowledge of repository topology

#### Scenario: Guide and catalog cannot drift
- **WHEN** a catalog route, command, or authority boundary changes
- **THEN** deterministic validation detects a divergent guide before package release

### Requirement: Human authority remains explicit
The guided interface and any AI assistant SHALL NOT confirm classification, approve DoR or DoD, approve a waiver or residual risk, resume work, approve release or archive, merge, deploy, or mutate external state.

#### Scenario: Guided route reaches a human gate
- **WHEN** a route reaches classification confirmation, DoR, DoD, waiver, resume, release, archive, or risk acceptance
- **THEN** it names the required accountable human decision, its evidence prerequisites, and the consequence of withholding it

#### Scenario: AI is unavailable
- **WHEN** an AI runtime or configured integration is unavailable
- **THEN** the guided interface reports the unavailable surface and supplies the documented deterministic/manual fallback without weakening any gate

### Requirement: Pre-corporate self-service verification
The reusable package SHALL be verified in a synthetic environment through its guided interface before corporate adaptation begins.

#### Scenario: All supported routes have reproducible evidence
- **WHEN** the package is proposed for corporate adaptation
- **THEN** synthetic evidence covers the supported business situations, all target change classes, required negative branches, and AI-disabled fallback
