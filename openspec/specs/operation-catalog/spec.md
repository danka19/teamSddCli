## Purpose

Единый versioned реестр локальных process operations P3.

## Roadmap

- Roadmap phase: P3
- Related phases: P4, P5

## Requirements

### Requirement: Canonical operation catalog

Process package SHALL contain one versioned catalog defining each local script operation by stable ID, entrypoint, visibility, roles, situations, inputs/outputs, mutation/risk level, human boundary, evidence, fallback, runbook, tests and lifecycle.

#### Scenario: Every local script is covered
- **WHEN** package validation runs
- **THEN** every `scripts/*.py` file has exactly one catalog record with an existing entrypoint; missing or duplicate coverage is blocking

#### Scenario: Internal service operations remain governed
- **WHEN** a weak-model or certification entrypoint is cataloged
- **THEN** it remains `internal`, included in package/validator coverage, and is not offered by a normal guided route

#### Scenario: Analytics preview is public and read-only
- **WHEN** `preview_analytics.py` is cataloged
- **THEN** it is `public`, `read_only`, and declares a local result without an external call

### Requirement: Catalog policy is fail-closed

The loader SHALL allow only supported visibility, mutation, risk and automation values and reject inconsistent combinations.

#### Scenario: Mutation has a human boundary
- **WHEN** a record is `mutate_local`, `mutate_release`, or `mutate_external`
- **THEN** it has a human decision and confirmation requirement and cannot be `ai_auto`

#### Scenario: External mutation is forbidden in P3
- **WHEN** the validator encounters `mutate_external`
- **THEN** it rejects the package as outside P3 scope

### Requirement: Derived operation views cannot drift

Guided routes, release allowlist, AI read packs and the README operation table SHALL be deterministically derived or validated against the catalog.

#### Scenario: Divergent derived view blocks release
- **WHEN** a route, allowlist, read pack, or README table differs from the catalog
- **THEN** validation fails before release and identifies the divergent artifact
