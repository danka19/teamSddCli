## ADDED Requirements

### Requirement: Installed self-service entrypoint
The process package SHALL provide an installed `sdd` command as the documented operator entrypoint. It SHALL delegate to the package version selected by the supported configuration and SHALL NOT require the operator to know a `scripts/*.py` path.

#### Scenario: Operator discovers the installed command
- **WHEN** an operator invokes `sdd --help` in a supported workspace
- **THEN** the command lists `setup`, `start`, and `next` and identifies the installed package version

#### Scenario: Direct compatibility is preserved
- **WHEN** an existing documented `scripts/*.py` entrypoint is invoked directly
- **THEN** it preserves its documented JSON and exit-code contract

### Requirement: Controlled workspace setup
`sdd setup` SHALL preflight the destination, process package and non-secret configuration before it creates or changes a local `team-specs` workspace. It SHALL require explicit human confirmation for a local mutation and SHALL report the resulting workspace, configuration and next command.

#### Scenario: Valid confirmed bootstrap
- **WHEN** a human confirms a valid empty destination and supported package
- **THEN** `sdd setup` creates the local `team-specs` workspace and returns a structured next action

#### Scenario: Unsafe setup is blocked
- **WHEN** the destination is non-empty, configuration is incompatible, or confirmation is absent
- **THEN** `sdd setup` returns a structured block and does not change the destination

### Requirement: Situation-first start and continuation
`sdd start` SHALL route a new operator from a declared situation, and `sdd next --change <id>` SHALL return exactly one next permitted action for an existing change. Both SHALL identify missing facts, the responsible role, human decision boundary, deterministic fallback and the exact next `sdd` command.

#### Scenario: New requirement route
- **WHEN** an Analyst starts a new requirement with sufficient declared facts
- **THEN** the result identifies the classification and change-creation preparation route without creating a change implicitly

#### Scenario: Existing change continuation
- **WHEN** a Developer requests `sdd next` for an existing approved change
- **THEN** the result identifies the implementation preparation action and its required evidence

#### Scenario: Missing information is not guessed
- **WHEN** a route lacks a required fact or a permitted role
- **THEN** the result blocks with the missing fact and does not invent a decision or command

### Requirement: AI-compatible deterministic guidance
Every public self-service command SHALL support non-interactive structured input and output so an AI assistant can invoke it or explain its result. The output SHALL distinguish advice, prepared action, local mutation, blocked action and forbidden external mutation.

#### Scenario: AI receives an authority boundary
- **WHEN** an AI invokes a public `sdd` command using structured output
- **THEN** the result states whether human confirmation is required and whether execution is unavailable

#### Scenario: Unavailable automation has a fallback
- **WHEN** an AI or integration is unavailable
- **THEN** the command returns a deterministic manual fallback without changing lifecycle or external state

### Requirement: P3 mutation boundary remains fail-closed
The self-service entrypoint SHALL NOT execute release operations or external mutations in P3. It SHALL preserve the existing `sdd run` fail-closed behavior until a later accepted change explicitly enables a bounded operation.

#### Scenario: External operation is forbidden
- **WHEN** an operator or AI requests an external mutation through `sdd`
- **THEN** the command blocks the request before any external call and identifies the required future authorization path

#### Scenario: Release operation is not implicitly executed
- **WHEN** an operator reaches a release-related step through `sdd next`
- **THEN** the result prepares or explains the required human-owned evidence and does not execute a release
