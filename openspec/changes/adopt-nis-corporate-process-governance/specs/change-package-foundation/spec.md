## ADDED Requirements

### Requirement: Versioned corporate classification metadata
The change-package foundation SHALL use schema version 2 metadata with canonical `classification`, separate `type`, and lifecycle `status` fields.

#### Scenario: Version 2 metadata is explicit
- **WHEN** a new package is created from the target template
- **THEN** `change.yaml` contains `schema_version: 2`, one of `classification: minor|major|hotfix`, a supported work `type`, and a supported lifecycle `status`

#### Scenario: New writer does not emit legacy mode
- **WHEN** a target-version template, generator, migration, or editor writes metadata
- **THEN** it does not write `mode: thin|full`

### Requirement: Bounded legacy compatibility
The package foundation SHALL support a documented compatibility window for reading legacy `mode: thin|full` packages without preserving legacy values as current authoring options.

#### Scenario: Legacy package receives deprecation result
- **WHEN** a non-archived legacy package is read during the compatibility window
- **THEN** tooling normalizes `thin` to `minor` or `full` to `major` in memory, identifies the legacy source field, emits a deprecation diagnostic, and recommends deterministic migration

#### Scenario: Conflicting metadata is rejected
- **WHEN** a package contains both legacy `mode` and target `classification` with divergent meaning
- **THEN** deterministic validation refuses to choose silently and reports the conflicting values

#### Scenario: Compatibility end is versioned
- **WHEN** legacy read support is changed or removed
- **THEN** the process package records the affected versions, migration prerequisite, reviewed compatibility evidence, and rollback or hold instructions

### Requirement: Deterministic classification migration command
The package foundation SHALL provide separate check and apply behavior for classification migration.

#### Scenario: Check mode is non-mutating
- **WHEN** migration check mode runs
- **THEN** it reports source schema, proposed target schema, field mapping, preserved values, ambiguities, validation result, and affected files without modifying them

#### Scenario: Apply mode preserves unrelated metadata
- **WHEN** an unambiguous migration plan is applied
- **THEN** type, lifecycle, quality, system, review, publication, traceability, waiver, and custom extension data are preserved unless an explicit reviewed schema rule transforms them

#### Scenario: Archived history is excluded
- **WHEN** migration discovery encounters an accepted archive path
- **THEN** the command reports the historical package but does not rewrite it by default

### Requirement: Classification-aware placeholder validation
Template placeholder mode SHALL validate the structure of all three target classification routes without accepting placeholders in real packages.

#### Scenario: Target route examples validate structurally
- **WHEN** package examples for minor, major, and hotfix run in the approved example or placeholder mode
- **THEN** their route-specific metadata and artifact matrices pass structural checks

#### Scenario: Real package rejects undecided classification
- **WHEN** a copied real package still contains a placeholder or unknown classification
- **THEN** normal validation fails and reports the required human classification decision
