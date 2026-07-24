## ADDED Requirements

### Requirement: Canonical schema-v2 continuation source

`sdd next` SHALL read the existing change lifecycle from the required
top-level `status` field of `change.yaml`, SHALL pass that value into the
validated existing-change guided route, and SHALL NOT use a top-level
`lifecycle_state` field as a storage fallback. The operation SHALL remain
read-only and SHALL NOT infer, change or approve lifecycle state.

#### Scenario: Real created change continues

- **WHEN** a supported role invokes `sdd next` for a change created by the
  schema-v2 `create_change` writer with a supported `status`
- **THEN** the dispatcher returns the role-appropriate guided continuation
  without lifecycle or external mutation

#### Scenario: Noncanonical field does not become a fallback

- **WHEN** `change.yaml` omits `status` and contains only `lifecycle_state`
- **THEN** the dispatcher returns a structured missing-status block and no next
  command

#### Scenario: Unsupported canonical status is blocked

- **WHEN** `change.yaml` contains a nonempty `status` outside the guided
  lifecycle values
- **THEN** the dispatcher returns a structured invalid-context block and does
  not guess a route or mutate state
