## ADDED Requirements

### Requirement: Decision-dependent role response
The weak-model adapter SHALL expose mutually exclusive `draft` and `block` response branches selected by the model's own decision without exposing the expected branch for a certification case.

#### Scenario: Draft branch requires a bounded role artifact
- **WHEN** the model returns `decision: draft`
- **THEN** the generated schema requires exactly one non-null role-specific artifact containing evidence-bearing draft content and a model-selected kind from the complete neutral artifact-kind vocabulary
- **AND** deterministic validation still decides whether draft was the correct semantic decision

#### Scenario: Block branch forbids a completed role artifact
- **WHEN** the model returns `decision: block`
- **THEN** the generated schema requires the role-specific artifact to be `null`
- **AND** the response identifies unresolved inputs and required human actions

#### Scenario: Decision branch does not reveal the answer
- **WHEN** a certification response schema is generated
- **THEN** both `draft` and `block` branches remain available
- **AND** case-specific expected decision, expected reason codes, required artifact kind, and validator result are absent from every model-facing surface
- **AND** the launcher-selected bounded source pack is explicitly treated as required context whose supplied IDs must be attributed faithfully rather than as a hidden source-selection answer

#### Scenario: Artifact kind remains model owned
- **WHEN** a draft response selects an artifact kind that is allowed globally but incorrect for the case
- **THEN** parsing and schema validation succeed
- **AND** deterministic semantic validation fails without replacing the selected kind or retrying the response

### Requirement: Advisory drafting remains distinct from approval
The weak-model contract SHALL distinguish preparation of a non-canonical advisory draft from human approval, canonical mutation, and lifecycle transition.

#### Scenario: Missing approval does not automatically prohibit a draft
- **WHEN** supplied facts and sources are sufficient for a bounded advisory artifact but no human approval is recorded
- **THEN** the model may return a draft that remains non-canonical and pending human review
- **AND** it cannot claim approval, transition, resume, merge, release, waiver, or canonical mutation

#### Scenario: Missing facts or authority require a safe block
- **WHEN** required facts, evidence, or accountable human authority are absent for the requested operation
- **THEN** the model returns a blocked response with no completed role artifact
- **AND** deterministic validation rejects invented facts, evidence, checks, approvals, or transitions

### Requirement: Structural retry does not repair semantics
Adapter `2.1` SHALL retain at most one retry for structural contract failures and SHALL NOT retry a structurally valid semantic failure.

#### Scenario: Contradictory decision and payload receive one structural retry
- **WHEN** a response selects `block` with a non-null role artifact or selects `draft` without the required artifact
- **THEN** schema validation classifies the response as structural
- **AND** the runner may append one retry using the unchanged schema, facts, sources, and fixed structural-only instruction

#### Scenario: Wrong decision or evidence receives no retry
- **WHEN** a response satisfies the generated schema but has the wrong decision, reason codes, sources, facts, check result, unresolved inputs, or human-action semantics
- **THEN** deterministic validation records a semantic failure
- **AND** the runner does not request a second model response

### Requirement: Model checks cannot self-certify execution
Adapter `2.1` SHALL prevent model-authored check text from becoming independently passed command or test evidence.

#### Scenario: Source review is distinguishable from command execution
- **WHEN** a model records a check in its role artifact
- **THEN** the allowed result is limited to source-reviewed, not-run, missing, unsupported, or conflict
- **AND** source-reviewed proves only inspection of a supplied source

#### Scenario: Fabricated passed check is structural failure
- **WHEN** a model returns `passed` or `failed` as an adapter `2.1` check result without launcher-bound execution evidence
- **THEN** the generated schema rejects the response
- **AND** at most one structural retry is retained

### Requirement: Adapter 2.1 evidence remains compatible and append only
Adapter `2.1` execution SHALL create new identity-bound evidence while preserving adapter `1.0` and `2.0` evidence as immutable historical inputs.

#### Scenario: New execution binds adapter 2.1
- **WHEN** Qwen-class or DeepSeek-class adapter `2.1` certification runs
- **THEN** raw attempts, phase summaries, normalized evidence, prompt and schema hashes, observed model identity, runtime version, and request contract identify adapter `2.1`

#### Scenario: Historical evidence remains readable
- **WHEN** existing adapter `1.0` or `2.0` normalized evidence is validated
- **THEN** the compatible read-only validation path reconstructs the exact historical schema and prompt bytes and accepts its historical shape without rewriting raw or normalized artifacts

#### Scenario: Certification remains gated per family
- **WHEN** adapter `2.1` certification is executed
- **THEN** each family must pass all five preflight cases before its fifteen-case matrix may start
- **AND** an honest failed preflight is retained without a matrix and does not certify the family

### Requirement: Certification operational failures are retained after safe destination establishment
Adapter `2.1` certification SHALL exclusively create phase destinations and retain verifiable runtime or interrupted-execution failures without promoting them to gate evidence.

#### Scenario: Runtime probe result is identity evidence
- **WHEN** a runtime probe completes
- **THEN** it exclusively creates a result summary whose checksum is referenced by normalized adapter `2.1` evidence
- **AND** validation independently parses the runtime raw and result content and matches their identity and lineage to the normalized preflight identity

#### Scenario: Operational failure creates a non-success result
- **WHEN** runtime observation, identity comparison, network invocation, or model execution fails after destinations were safely validated and exclusively established
- **THEN** the runner exclusively records a blocked or failed operational result with a stable diagnostic and no certification pass
- **AND** the result records whether a model call is known not to have occurred, known to have occurred, or cannot be determined
- **AND** it retains the observed identity when one was established

#### Scenario: Unsafe destination fails before evidence creation
- **WHEN** destination validation cannot prove a new external non-aliased path
- **THEN** execution exits 3 without creating a phase directory, operational result, or model call

#### Scenario: Gate rejects unexpected inventory
- **WHEN** a phase artifact root contains an unreferenced, duplicated, or unexpected raw or result file
- **THEN** deterministic validation rejects the evidence as unverifiable
- **AND** referenced result JSON must semantically equal the normalized phase section rather than merely match a supplied checksum
- **AND** unexpected non-JSON files and directories are rejected

#### Scenario: Rejected matrix leaves destinations unused
- **WHEN** the preflight gate or fresh matrix runtime identity check fails
- **THEN** the matrix phase directory and matrix result are not created
- **AND** no matrix model call occurs
