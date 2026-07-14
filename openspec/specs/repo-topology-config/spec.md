# repo-topology-config Specification

## Roadmap

- Roadmap phase: P1
- Related phases: P0, P2, P3

## Purpose
Define the accepted first supported repository topology, content split, developer/agent workflow, process configuration, package distribution, OpenSpec version pin/upgrade policy, and owner registry contract.
## Requirements
### Requirement: First supported topology
The SDD process SHALL define a first supported repository topology before deterministic tools assume package paths, config paths, OpenSpec version pins, or reviewer assignment sources.

#### Scenario: Central team-specs is the recommended first topology
- **WHEN** the first supported topology is used
- **THEN** the default is a central `team-specs` repository for canonical analytics, change packages, Master Specs, Delta Specs, traceability, shared process assets, owner registry, and publication config, with project repositories referencing change/spec IDs instead of copying requirement text

#### Scenario: Specs-next-to-code remains a future topology
- **WHEN** a team wants project repositories to own local Master Specs and Delta Specs next to code
- **THEN** the process treats that as a future/federated topology that requires cross-repo traceability, generated views, shared process-package distribution, and sync/drift checks before it becomes supported

#### Scenario: Unsupported topology is not silently accepted
- **WHEN** a repository does not match the approved topology or supported future topology contract
- **THEN** validation or setup guidance reports the topology as unsupported and requires an explicit human topology decision before templates or validators rely on it

### Requirement: Repository content split
The SDD process SHALL define which artifact classes are owned by `team-specs` and which are owned by project repositories.

#### Scenario: team-specs owns process and requirement truth
- **WHEN** an SDD change package is authored
- **THEN** `team-specs` owns proposal intent, OpenSpec change deltas, accepted Master Specs after archive, analytics sources, traceability, waivers, process package, config, owner registry, and publication inputs

#### Scenario: Project repos own implementation truth
- **WHEN** implementation work starts for an approved change
- **THEN** project repositories own code, unit/integration tests, AT code when applicable, implementation-local technical docs, runtime config, and PR evidence that references change/spec IDs

#### Scenario: Code PR references canonical specs
- **WHEN** a behavior-changing code PR is opened under the central `team-specs` topology
- **THEN** the PR references the change ID and affected requirement/scenario IDs instead of copying requirement text into project docs or comments

### Requirement: Practical developer and agent workflow
The SDD process SHALL explain how developers and AI agents use canonical specs when those specs live outside the code repository.

#### Scenario: Developer receives a bounded read pack
- **WHEN** a developer or AI agent starts implementation from a project repository
- **THEN** the process provides or identifies a bounded read pack containing the change ID, spec delta paths, affected requirement/scenario IDs, design/tasks when present, and expected traceability evidence

#### Scenario: Agent can work with sibling repositories
- **WHEN** canonical specs live in `team-specs` and implementation lives in a project repository
- **THEN** the process supports a sibling-checkout or configured path pointer so the agent can read canonical specs without copying them into the code repository

#### Scenario: Archive readiness links implementation evidence
- **WHEN** implementation evidence is collected for archive readiness
- **THEN** traceability records link from canonical requirements and scenarios to project-repo PRs, CI/manual verification evidence, and approved waivers where needed

### Requirement: Process configuration files
The SDD process SHALL define a configuration format that deterministic tools and role skills can discover.

#### Scenario: Central config declares supported process assumptions
- **WHEN** the central topology is used
- **THEN** `team-specs` contains a team process config that declares supported topology, process package version, OpenSpec CLI version pin, canonical path roots, validation policy, and config schema version

#### Scenario: Project adapter config points to central process config
- **WHEN** a project repository participates in the central topology
- **THEN** it may contain a small adapter config with project ID, central `team-specs` location or registry reference, consumed process package version, and local path mappings

#### Scenario: Config names are approved defaults
- **WHEN** first-topology config names are documented
- **THEN** names such as `sdd.config.yaml`, `projects.yaml`, `owners.yaml`, and `.sdd-project.yaml` are recommended defaults that became approved first-topology assumptions at gate 1.5

### Requirement: Process package distribution
The SDD process SHALL define shared scripts, templates, schemas, and role skill instructions as a versioned process package instead of independent per-repo forks.

#### Scenario: One versioned folder carries process assets
- **WHEN** another team bootstraps the SDD process
- **THEN** it can consume one versioned process package folder containing workflow schema, templates, validator entry points, role skill instructions, examples, and package version metadata

#### Scenario: Artifact dependencies are shared by skills and validators
- **WHEN** the workflow schema declares artifact dependencies such as `requires`
- **THEN** role skills may use those dependencies for drafting order and deterministic validators may use the same dependencies for missing-artifact checks

#### Scenario: Manual forks are not the default reuse model
- **WHEN** a project repository needs process assets
- **THEN** it consumes a pinned package copy, subtree/submodule, or CI-fetched package version rather than maintaining untracked manual edits

### Requirement: OpenSpec version pin and upgrade policy
The SDD process SHALL define where the OpenSpec CLI version is pinned and how upgrades are approved.

#### Scenario: OpenSpec version is pinned centrally
- **WHEN** the central topology is used
- **THEN** the default pins the verified OpenSpec CLI version `1.4.1` in the central process config

#### Scenario: Version mismatch is reported before gated validation
- **WHEN** deterministic Spec PR or archive validation runs
- **THEN** it reports a mismatch when the running OpenSpec CLI version does not satisfy the pinned policy

#### Scenario: Upgrade requires reviewed evidence
- **WHEN** the team upgrades the OpenSpec CLI version or process package compatibility
- **THEN** the upgrade requires a reviewed change package with compatibility evidence, strict OpenSpec validation, validator/template checks when available, and rollback or hold instructions

### Requirement: Owner registry and reviewer assignment
The SDD process SHALL define a source owner registry and reviewer-assignment contract before generated or validated reviewer rules become binding.

#### Scenario: owners.yaml is the owner source
- **WHEN** the central topology uses reviewer assignment
- **THEN** `owners.yaml` in `team-specs` is the source registry for owner groups, zones, roles, and reviewer assignment rules

#### Scenario: CODEOWNERS is generated or validated from owners registry
- **WHEN** a project repository uses `CODEOWNERS`
- **THEN** the file is generated from or validated against the central owner registry so reviewer rules do not drift silently

#### Scenario: Multi-zone changes require all affected owners
- **WHEN** a change package or project-repo PR touches multiple owner zones
- **THEN** the reviewer-assignment contract requires approval from every affected owner zone or an approved waiver/override recorded in the change evidence

#### Scenario: Unowned paths are visible
- **WHEN** validation finds a touched path or capability without an owner mapping
- **THEN** it reports the missing owner mapping and falls back to default reviewers only as a temporary non-ideal path until the owner registry is fixed

### Requirement: Human decision gate for topology and config
The SDD process SHALL stop for human approval before topology, config, OpenSpec version, process distribution, or owner assignment becomes binding.

#### Scenario: Gate 1.5 presents practical options
- **WHEN** the topology/config/OpenSpec version decision packet is prepared
- **THEN** it presents 2-3 practical options for topology, config format, OpenSpec version upgrade policy, process package distribution, and owner/reviewer assignment, with a recommended default, examples of daily impact, tradeoffs, risks, and unresolved-decision consequences

#### Scenario: Gate 1.5 approved recommended defaults
- **WHEN** work item 1.8 starts after the 2026-07-09 human decision
- **THEN** templates, validators, setup docs, and role skills may use central `team-specs`, central config plus optional project adapter, OpenSpec `1.4.1` central pin, one versioned process package, and `owners.yaml` reviewer source as approved assumptions

#### Scenario: Validator enforcement follows approved implementation scope
- **WHEN** topology, config, OpenSpec version, process distribution, or owner assignment checks are added to deterministic tooling
- **THEN** they are implemented through a reviewed change against the accepted baseline and use the approved gate 1.5 assumptions unless a later accepted decision changes them
