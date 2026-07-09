# change-package-foundation Specification

## Purpose
TBD - created by archiving change add-change-template-validation. Update Purpose after archive.
## Requirements
### Requirement: Change package template
The project SHALL provide a copyable `templates/change/` skeleton for SDD change packages.

#### Scenario: Template contains required artifacts
- **WHEN** the template is inspected
- **THEN** it contains `change.yaml`, `proposal.md`, `design.md`, `tasks.md`, at least one OpenSpec delta under `specs/`, `qa/test-plan.md`, `qa/automation-plan.md`, and `traceability.yaml`

### Requirement: Local change package validation
The project SHALL provide a deterministic local validator for SDD change packages.

#### Scenario: Valid package passes validation
- **WHEN** a copied change package contains required artifacts, valid metadata, at least one requirement scenario, and requirement-to-scenario traceability
- **THEN** the validator exits successfully

#### Scenario: Missing artifact fails validation
- **WHEN** a change package is missing a required artifact
- **THEN** the validator exits unsuccessfully and reports the missing artifact path

#### Scenario: Missing traceability fails validation
- **WHEN** a change package has a requirement scenario without a matching traceability row
- **THEN** the validator exits unsuccessfully and reports the missing traceability link

### Requirement: Pre-commit validation entrypoint
The project SHALL provide a pre-commit configuration that runs the local validator against SDD change packages.

#### Scenario: Plain OpenSpec project change is ignored
- **WHEN** staged files belong to an OpenSpec change folder that does not contain `change.yaml`
- **THEN** the pre-commit validation discovery ignores that folder

#### Scenario: SDD package is validated
- **WHEN** staged files belong to a folder that contains `change.yaml`
- **THEN** the pre-commit validation discovery passes that folder to the validator

### Requirement: Template placeholder validation mode
The project SHALL allow the template skeleton to be structurally validated without accepting placeholder values as production metadata.

#### Scenario: Template validates in placeholder mode
- **WHEN** the validator runs with `--allow-placeholders` against `templates/change`
- **THEN** structural checks pass even though placeholder metadata remains

#### Scenario: Real package rejects placeholders
- **WHEN** the validator runs without `--allow-placeholders` against a copied package containing placeholder metadata
- **THEN** validation fails and reports placeholder fields
