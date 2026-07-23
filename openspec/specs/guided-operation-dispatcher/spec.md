## Purpose

Локальный situation-first `sdd` dispatcher P3 поверх canonical operation catalog.

## Roadmap

- Roadmap phase: P3
- Related phases: P4, P5

## Requirements

### Requirement: Situation-first discovery

`sdd` SHALL provide `guide`, `next`, `op list`, and `op show` from the canonical catalog without moving domain logic out of existing scripts.

#### Scenario: Missing context blocks route
- **WHEN** situation or required fact is missing or invalid
- **THEN** dispatcher returns a structured block and does not guess a command or human decision

### Requirement: Safe dispatch classes

`check` SHALL run only `read_only`, `prepare` only `prepare`, and `request` only prepare a non-authoritative review request with canonical input digest and stable JSON/exit classes.

#### Scenario: Wrong class is blocked before entrypoint
- **WHEN** a caller uses an operation with an incompatible command class
- **THEN** dispatcher blocks before spawning the entrypoint

### Requirement: Mutations remain fail-closed

`sdd run` SHALL validate a supplied operation-confirmation artifact when present, but SHALL not execute a P3 mutation; `mutate_external` is always forbidden.

#### Scenario: Valid confirmation still does not execute
- **WHEN** a valid artifact is supplied to `sdd run`
- **THEN** it returns `confirmation-contract-pending` without spawning an entrypoint

#### Scenario: Invalid confirmation has no side effect
- **WHEN** the artifact is missing, expired, or mismatched on role, operation, input, or revision
- **THEN** it returns a structured block without mutating package, evidence, lifecycle, release, or external state

### Requirement: Direct script compatibility

Adding `sdd` SHALL NOT remove or change supported direct Python script contracts.

#### Scenario: Existing entrypoint remains usable
- **WHEN** a direct-script compatibility smoke runs
- **THEN** it preserves its documented JSON and exit-code behavior
