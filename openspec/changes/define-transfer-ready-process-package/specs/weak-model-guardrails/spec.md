## ADDED Requirements

### Requirement: Deterministic workflow launch
The SDD process SHALL select the applicable weak-model workflow, role instruction, read pack, output contract, and stop point outside the AI model.

#### Scenario: User starts a bounded role operation
- **WHEN** a user starts an analyst, developer, QA, or Tech Lead operation for a minor, major, or hotfix change
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
- **THEN** a fresh runtime probe records the exact observed model tag and full digest plus Ollama runtime version, and evidence binds that observed identity with the adapter version, process-package version, read-pack identity, operation, input fixture, output artifact, deterministic validation result, human intervention, and known limitations

#### Scenario: Matrix execution rejects runtime identity drift
- **WHEN** a family passed preflight and the matrix runner is about to invoke any model case
- **THEN** it freshly observes the current tag digest and runtime version and requires exact equality to the immutable runtime-identity catalog and the preflight observed identity
- **AND** an unavailable, malformed, repointed, or changed identity exits 3 before the model call and before creating matrix raw or result output

#### Scenario: Actual certification destinations are external and non-aliased
- **WHEN** any AI-disabled, runtime-probe, preflight, or matrix phase is requested
- **THEN** raw and result destinations are resolved before directory creation or model execution, are new paths outside the repository and canonical process sources, contain no symlink, junction, or reparse component, do not overlap, and keep result output inside the selected external artifact root
- **AND** an unsafe or unverifiable destination exits 3 without model calls or output creation

#### Scenario: Model-facing contract is role specific and schema constrained
- **WHEN** the deterministic launcher prepares a Qwen-class or DeepSeek-class role operation
- **THEN** it supplies a closed role-specific JSON Schema containing only supplied source IDs and the global reason-code vocabulary, without exposing validator-only expected answers

#### Scenario: Normalization cannot repair model semantics
- **WHEN** the adapter parses a structurally valid model response
- **THEN** normalization may add launch-owned identity and invariant authority fields but does not change the model decision, reasons, sources, evidence observations, unresolved inputs, or required human decisions

#### Scenario: Technical retry is bounded and retained
- **WHEN** final model output is empty, invalid JSON, or fails the generated response schema
- **THEN** the runner may make one structurally prompted retry with identical facts and sources, retaining both attempts separately, and does not retry a structurally valid semantic failure

#### Scenario: Preflight gates matrix execution
- **WHEN** actual weak-model remediation certification is executed
- **THEN** each family must pass all five frozen preflight cases with the same adapter version before its fifteen-case matrix may start

#### Scenario: Failed preflight evidence is retained without a matrix
- **WHEN** all five preflight cases completed and deterministic revalidation proves an honest semantic failure
- **THEN** normalization exclusively creates a new document with top-level `status: failed`, retains the exact append-only attempts, diagnostics, and same-family immutable adapter 1.0 baseline reference, records `matrix_not_run: preflight-gate-failed`, and does not require or accept matrix evidence
- **AND** a passed preflight still requires a complete passing fifteen-case matrix
- **AND** malformed, mismatched, private, forged, cross-family, or otherwise unverifiable preflight or baseline evidence exits 3 without creating output or modifying baseline or raw evidence
- **AND** an existing output is never overwritten

#### Scenario: Certification covers first pilot roles
- **WHEN** release-candidate weak-model certification is complete
- **THEN** it includes analyst, developer, QA, and Tech Lead class-aware walkthroughs plus negative cases for missing context, conflicting sources, under-classification, pseudo-hotfix, fabricated evidence, forbidden approval, unsafe resume, unresolved reconciliation, skipped stop point, and invalid lifecycle transition

#### Scenario: Certification uses the accepted risk-oriented matrix
- **WHEN** Qwen-class and DeepSeek-class release-candidate certification is planned and executed
- **THEN** each model family performs analyst, developer, QA, and Tech Lead work once, minor/major/hotfix are each exercised by both families, and critical authority, fabricated-evidence, unsafe-resume, and hotfix-reconciliation negative cases run on both families

#### Scenario: Fluency does not substitute for compliance
- **WHEN** a model produces readable output that fails deterministic validation, violates a stop point, hides uncertainty, or claims forbidden authority
- **THEN** the run fails certification regardless of prose quality

#### Scenario: Model limitation is routed explicitly
- **WHEN** a model cannot reliably perform a role operation after bounded instruction and one documented remediation attempt
- **THEN** the release evidence identifies the limitation and routes the operation to a deterministic command, simpler instruction, mandatory human execution, or a strategy-trigger review

#### Scenario: Certification evidence is stored without private raw data in Git
- **WHEN** AI-disabled or weak-model certification evidence is finalized for a release candidate
- **THEN** Git contains normalized synthetic evidence, the evidence manifest, content hashes, and stable references, while raw model/runtime outputs are stored in the versioned release artifact and linked by manifest and checksum

### Requirement: Weak-model artifacts preserve source ownership
Role instructions, read packs, examples, and certification fixtures SHALL reference canonical requirements and SHALL NOT become a second maintained behavior source.

#### Scenario: Derived instruction references canonical contracts
- **WHEN** a role instruction or read pack summarizes lifecycle, artifact, traceability, waiver, topology, or documentation rules
- **THEN** it references the accepted OpenSpec source or stable identifier rather than maintaining a divergent normative copy

#### Scenario: Derived artifact conflict is corrected from source
- **WHEN** a weak-model artifact conflicts with its referenced canonical contract
- **THEN** the derived artifact is fixed or regenerated from the canonical source and is not used to edit multiple copies of the rule

### Requirement: Safe parallel AI execution
The SDD process SHALL allow AI-assisted work to execute in parallel only when task independence, ownership, write scope, dependencies, and integration responsibility are explicit.

#### Scenario: Independent tasks run concurrently
- **WHEN** two or more AI-assisted tasks have no unresolved dependency and do not mutate the same owned artifact or state boundary
- **THEN** the launcher may assign them concurrently with separate task IDs, read packs, write scopes, evidence records, owners, and stop conditions

#### Scenario: Shared mutation prevents unsafe parallelism
- **WHEN** proposed concurrent tasks would edit the same canonical artifact, depend on an unfinished output, or make conflicting lifecycle or policy decisions
- **THEN** the process serializes them, splits the shared boundary, or blocks execution until a human-approved dependency and ownership plan exists

#### Scenario: Parallel outputs pass an integration gate
- **WHEN** concurrent task outputs are complete
- **THEN** each output passes its focused checks and the combined result passes deterministic integration, traceability, review, and conflict checks before it can become canonical evidence
