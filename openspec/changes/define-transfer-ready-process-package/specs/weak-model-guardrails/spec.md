## ADDED Requirements

### Requirement: Deterministic workflow launch
The SDD process SHALL select the applicable weak-model workflow, role instruction, read pack, output contract, and stop point outside the AI model.

#### Scenario: User starts a bounded role operation
- **WHEN** a user starts an analyst, developer, or QA thin-change operation
- **THEN** a deterministic launcher or explicit non-AI procedure supplies the exact instruction, canonical inputs, required output, evidence fields, and stage boundary

#### Scenario: Model does not select its own authority
- **WHEN** a Qwen/DeepSeek-class assistant receives a task
- **THEN** it is not asked to decide which lifecycle, skill, source hierarchy, approval power, or mutation permission applies

### Requirement: Bounded authority-labelled read packs
The SDD process SHALL provide weak models with bounded task-specific context that labels every source by authority.

#### Scenario: Read pack identifies source authority
- **WHEN** a read pack is created for a weak-model task
- **THEN** each referenced artifact is labelled as canonical, supporting context, generated or advisory, or evidence and includes a stable path or identifier

#### Scenario: Read pack stays task specific
- **WHEN** a role operation needs only a subset of project context
- **THEN** the read pack includes the smallest sufficient files, sections, IDs, known traps, and unresolved inputs instead of requiring the model to synthesize the whole repository

#### Scenario: Missing canonical context is visible
- **WHEN** a required canonical source, stable ID, project mapping, or evidence input is unavailable
- **THEN** the read pack and model output record the missing input and block the affected draft or transition instead of inventing it

### Requirement: Role instructions and explicit stop points
The SDD process SHALL provide tool-agnostic role instructions with numbered steps, concrete examples, negative cases, output structure, self-review, and explicit human stop points.

#### Scenario: One operation produces one bounded artifact stage
- **WHEN** a weak model completes proposal, spec, design, task, implementation-prep, QA-evidence, or archive-prep work
- **THEN** it stops at the configured stage and requests the required deterministic check or human review before the next stage begins

#### Scenario: Negative examples prevent common overreach
- **WHEN** an instruction covers uncertain requirements, approvals, waivers, lifecycle transitions, evidence, or source conflicts
- **THEN** it includes concrete prohibited behavior and the required blocked, escalation, or correction response

### Requirement: AI remains advisory and non-authoritative
Qwen/DeepSeek-class assistants SHALL remain draft and review aids and SHALL NOT own gates, approvals, waivers, merges, archive decisions, or canonical state transitions.

#### Scenario: Model attempts a forbidden approval
- **WHEN** model output claims to approve a waiver, accept a spec, authorize a merge, mark a gate green, or archive a change
- **THEN** deterministic validation or human review rejects the claim as non-evidence and leaves lifecycle state unchanged

#### Scenario: Model draft becomes evidence only after review
- **WHEN** a model proposes requirements, traceability rows, QA evidence, configuration, or a compatibility finding
- **THEN** the proposal becomes canonical evidence only after the required deterministic checks and human review are recorded and committed

### Requirement: Evidence-backed weak-model output
The SDD process SHALL require weak-model outputs to distinguish inspected facts, generated proposals, commands or evidence, unresolved inputs, and prohibited actions.

#### Scenario: Completion output includes evidence boundaries
- **WHEN** a weak model reports completion of a bounded operation
- **THEN** its output identifies sources read, artifacts drafted, deterministic commands run or not run, results, human decisions still required, unresolved inputs, and residual limitations

#### Scenario: Unsupported claim fails certification
- **WHEN** model output claims validation, approval, file state, integration state, or test success without corresponding evidence
- **THEN** the certification check records the claim as a failure and does not promote the output to release evidence

### Requirement: Deterministic fallback
Every weak-model-assisted operation SHALL have a documented path that completes its gated checks without an AI assistant.

#### Scenario: AI is unavailable or unusable
- **WHEN** the configured model is unavailable, exceeds context limits, repeatedly ignores instructions, or produces invalid output
- **THEN** the user can continue with templates, deterministic commands, checklists, and human-authored artifacts without weakening any gate

#### Scenario: Model adapter failure does not alter canonical data
- **WHEN** a Qwen/DeepSeek or GigaCode adapter fails during an operation
- **THEN** the process preserves existing canonical files and reports partial generated output as non-canonical scratch data or removes it through the documented recovery path

### Requirement: Actual weak-model certification
The release candidate SHALL be evaluated with actual Qwen/DeepSeek-class assistants against repeatable role workflows and safety cases before transfer readiness is accepted.

#### Scenario: Certification records the evaluated runtime
- **WHEN** a weak-model certification run is executed
- **THEN** evidence records the model and runtime identifier, adapter version, process-package version, read-pack identity, operation, input fixture, output artifact, deterministic validation result, human intervention, and known limitations

#### Scenario: Certification covers first pilot roles
- **WHEN** release-candidate weak-model certification is complete
- **THEN** it includes analyst, developer, and QA thin-change walkthroughs plus negative cases for missing context, conflicting sources, fabricated evidence, forbidden approval, skipped stop point, and invalid lifecycle transition

#### Scenario: Fluency does not substitute for compliance
- **WHEN** a model produces readable output that fails deterministic validation, violates a stop point, hides uncertainty, or claims forbidden authority
- **THEN** the run fails certification regardless of prose quality

#### Scenario: Model limitation is routed explicitly
- **WHEN** a model cannot reliably perform a role operation after bounded instruction and one documented remediation attempt
- **THEN** the release evidence identifies the limitation and routes the operation to a deterministic command, simpler instruction, mandatory human execution, or a strategy-trigger review

### Requirement: Weak-model artifacts preserve source ownership
Role instructions, read packs, examples, and certification fixtures SHALL reference canonical requirements and SHALL NOT become a second maintained behavior source.

#### Scenario: Derived instruction references canonical contracts
- **WHEN** a role instruction or read pack summarizes lifecycle, artifact, traceability, waiver, topology, or documentation rules
- **THEN** it references the accepted OpenSpec source or stable identifier rather than maintaining a divergent normative copy

#### Scenario: Derived artifact conflict is corrected from source
- **WHEN** a weak-model artifact conflicts with its referenced canonical contract
- **THEN** the derived artifact is fixed or regenerated from the canonical source and is not used to edit multiple copies of the rule
