## ADDED Requirements

### Requirement: Fail-closed role-aware guidance
P3 guided workflow SHALL require an explicit supported `human_role` before it returns a role-sensitive route or CTA.

#### Scenario: Unknown role is blocked
- **WHEN** a caller omits `human_role` or supplies an unsupported value
- **THEN** the read-only payload SHALL be `blocked` with `unknown-role` or `invalid-role` and no commands or CTA

#### Scenario: Analyst cannot receive implementation CTA
- **WHEN** an `Analyst` requests guidance for an approved change
- **THEN** the payload SHALL not contain `begin-approved-implementation` and SHALL name an authorized human handoff

### Requirement: Trusted revision-bound human acceptance
P3 implementation guidance SHALL require a schema-valid acceptance event from a trusted human role, a literal message, a trusted event reference, and a digest matching the shown Delta Spec revision.

#### Scenario: UI confirmation is rejected
- **WHEN** acceptance evidence contains only `Да` or another non-literal UI confirmation
- **THEN** the validator SHALL reject it as `guided-process.acceptance-message-invalid`

#### Scenario: Accepted revision differs from current spec
- **WHEN** acceptance evidence names a digest different from the referenced Delta Spec bytes or summary digest
- **THEN** the validator SHALL reject implementation guidance as revision-mismatched

### Requirement: Readiness preserves DoR
P3 trusted acceptance SHALL not bypass Definition of Ready.

#### Scenario: Incomplete package remains blocked
- **WHEN** required documents, scenario traceability, `DoR: passed`, or blocker/placeholder-free content are absent
- **THEN** the validator SHALL return invalid even when a trusted-looking acceptance record exists

### Requirement: MCP-free P3 guidance
P3 guided catalog, runbook, and read-pack SHALL contain no MCP invocation, setup, credential, dependency, or fallback.

#### Scenario: Existing-change route has no MCP fallback
- **WHEN** the local existing-change route is rendered
- **THEN** its fallback list SHALL not include MCP and it SHALL not request any external integration action
