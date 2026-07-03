## ADDED Requirements

### Requirement: Proposed documentation update discipline
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
