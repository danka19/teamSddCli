## MODIFIED Requirements

### Requirement: OpenSpec version pin and upgrade policy
The SDD process SHALL define where the OpenSpec CLI version is pinned and SHALL deterministically require reviewed evidence before a process-package or OpenSpec compatibility upgrade is accepted.

#### Scenario: OpenSpec version is pinned centrally
- **WHEN** the central topology is used
- **THEN** the default pins the verified OpenSpec CLI version `1.4.1` in the central process config

#### Scenario: Version mismatch is reported before gated validation
- **WHEN** deterministic Spec PR or archive validation runs
- **THEN** it reports a mismatch when the running OpenSpec CLI version does not satisfy the pinned policy

#### Scenario: Upgrade requires reviewed evidence
- **WHEN** compatibility is checked or an update is requested for the OpenSpec CLI version or process package
- **THEN** deterministic validation requires a schema-valid reviewed change-package record bound to the from/to identities, compatibility evidence, passing strict OpenSpec validation, applicable validator/template checks or explicit non-applicability, and rollback or hold instructions before the update can be accepted or mutate the installation
