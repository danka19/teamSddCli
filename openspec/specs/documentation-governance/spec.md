# documentation-governance Specification

## Roadmap

- Roadmap phase: P1
- Related phases: P0, P2, P3, P4

## Purpose
Define the accepted documentation governance rules for durable updates, AI verification evidence, scenario-first verification, human feedback memory, canonical language, docs/OpenSpec responsibility, and source ownership.
## Requirements
### Requirement: Documentation update discipline
The SDD process SHALL define when project documentation must be updated for workflow, contract, setup, security, roadmap, or user-visible behavior changes.

#### Scenario: Behavior change updates durable docs
- **WHEN** work changes SDD workflow behavior, CLI behavior, artifact contracts, integration boundaries, setup, operations, security, roadmap status, or user-visible command text
- **THEN** the worker updates the narrowest relevant durable documentation or records why no documentation update is needed

#### Scenario: Proposed behavior stays in proposed changes
- **WHEN** behavior is still under proposal and not yet accepted
- **THEN** the behavior is documented under `openspec/changes/` and is not written to accepted `openspec/specs/`

#### Scenario: Accepted specs require human archive approval
- **WHEN** a proposed OpenSpec change is ready to become accepted behavior
- **THEN** the worker stops for explicit human archive or acceptance approval before updating `openspec/specs/`

### Requirement: AI verification checklist evidence
The SDD process SHALL require completion reports to include AI verification checklist evidence for relevant work.

#### Scenario: Completion report includes verification evidence
- **WHEN** an AI worker reports completion of a roadmap step, OpenSpec change, artifact contract, documentation update, or deterministic behavior change
- **THEN** the report includes commands run, results, blockers if any, manual checks performed, documentation updates or no-doc rationale, residual manual-verification risk, skills used, and subagents used with role names and token counts when available

#### Scenario: Checklist does not replace deterministic validation
- **WHEN** the AI verification checklist is completed
- **THEN** deterministic checks, tests, or manual verification still provide the actual evidence for behavior claims

### Requirement: TDD-style verification discipline
The SDD process SHALL use scenario-first verification planning for deterministic behavior and artifact contract changes.

#### Scenario: Scenarios identified before implementation
- **WHEN** work changes deterministic validation, templates, artifact contracts, lifecycle gates, traceability rules, waiver rules, or future CLI behavior
- **THEN** affected OpenSpec scenarios or acceptance examples are identified before implementation changes are made

#### Scenario: Negative cases are covered
- **WHEN** a change defines a gate that rejects invalid metadata, missing artifacts, missing traceability, invalid waivers, placeholder production values, or unsupported modes
- **THEN** tests or manual verification include negative cases for the rejection behavior

#### Scenario: Manual verification is explicit when automation is absent
- **WHEN** automated tests do not exist for an affected behavior
- **THEN** the worker records manual verification steps, expected evidence, and residual risk before reporting completion

### Requirement: Human feedback memory
The SDD process SHALL preserve durable human feedback that changes product behavior, acceptance criteria, verification habits, or rejected behavior.

#### Scenario: Feedback affects proposed behavior
- **WHEN** the human adds or corrects an acceptance criterion for proposed SDD behavior
- **THEN** the relevant `openspec/changes/` artifact and phase plan are updated before completion is reported

#### Scenario: Feedback affects accepted behavior
- **WHEN** the human changes already accepted behavior
- **THEN** the worker records the change through the accepted-spec workflow and does not silently edit accepted specs without the required approval gate

### Requirement: Canonical language and localized generated views
The SDD process SHALL keep Russian as the canonical language for newly created
project documentation and OpenSpec requirement/scenario prose, while preserving
technical tokens required for stable references and tooling.

#### Scenario: New documentation and specs use Russian prose
- **WHEN** an analyst or another project participant creates a new requirement,
  scenario, proposal, design, task list, runbook, audit, or project document
- **THEN** its human-readable prose is written in Russian; stable IDs, file
  paths, CLI/API tokens, and structural OpenSpec keywords (`Requirement`,
  `Scenario`, `SHALL`, `WHEN`, `THEN`) remain English where tooling or a stable
  cross-reference requires them

#### Scenario: Historical evidence is preserved without bulk translation
- **WHEN** a historical accepted artifact, immutable release candidate, raw
  evidence, or checksum-bound document is encountered
- **THEN** it is preserved as historical evidence and is not translated in bulk;
  a later substantive change follows the normal OpenSpec/change workflow

#### Scenario: Generated view follows the canonical Russian source
- **WHEN** a Confluence or other generated view is created for readers
- **THEN** it uses the Russian canonical Git/OpenSpec source and links back to
  that source rather than creating a separate translated requirement authority

#### Scenario: Feedback changes the Russian canonical source
- **WHEN** feedback on documentation or a generated view changes accepted or
  proposed behavior
- **THEN** the change is recorded in the canonical Russian Git/OpenSpec source
  through the applicable approval workflow rather than as an untracked manual
  translation

### Requirement: Docs versus OpenSpec responsibility
The SDD process SHALL keep product behavior contracts separate from project operating documentation.

#### Scenario: Product behavior belongs in OpenSpec
- **WHEN** documentation describes accepted or proposed product behavior, SDD workflow behavior, artifact contracts, traceability, waiver behavior, or acceptance criteria
- **THEN** the behavior is recorded in accepted or proposed OpenSpec artifacts according to its approval state

#### Scenario: Project organization belongs in docs
- **WHEN** documentation describes project overview, repository map, setup, runbook, contribution workflow, glossary, integration map, operations, release/rollback notes, legacy baseline notes, AI/agent guide, or decision rationale
- **THEN** it is recorded in `docs/` or another explicitly mapped project documentation location

### Requirement: Source ownership and deduplication
The SDD process SHALL prevent OpenSpec, docs, role guides, generated views, and project memory from carrying divergent maintained copies of the same behavior or process rule.

#### Scenario: Behavior text is referenced rather than duplicated
- **WHEN** docs, role guides, generated views, project memory, or read packs describe accepted or proposed behavior, artifact contracts, lifecycle rules, traceability rules, waiver rules, scenarios, or acceptance criteria
- **THEN** they reference the canonical OpenSpec requirement, scenario, change ID, or source path instead of maintaining a separate normative copy

#### Scenario: Derived view includes source metadata
- **WHEN** a generated view, role guide, memory note, or read pack summarizes canonical behavior or process rules
- **THEN** it includes enough source metadata for review, such as source file, stable ID, change ID, source commit, generated timestamp, or source warning according to the artifact type

#### Scenario: Conflict is resolved from the canonical owner
- **WHEN** a derived surface conflicts with its canonical source
- **THEN** the worker treats the canonical source as authoritative and fixes or regenerates the derived surface instead of editing multiple maintained copies by hand

#### Scenario: Weak-model read pack identifies authority
- **WHEN** a task read pack is generated for a local AI model
- **THEN** it labels each referenced artifact as canonical, supporting context, generated/advisory, or evidence so weaker models know which source to trust

#### Scenario: Documentation drift checks are planned
- **WHEN** documentation governance checks are implemented
- **THEN** they include checks for normative language outside canonical files, duplicate requirement IDs with divergent text, missing source links, hand-edited generated blocks, stale memory entries, and orphan maintained documents where practical
