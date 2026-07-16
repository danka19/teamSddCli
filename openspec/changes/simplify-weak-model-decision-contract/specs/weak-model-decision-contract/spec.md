## ADDED Requirements

### Requirement: Decision-dependent role response
The weak-model adapter SHALL expose mutually exclusive `draft` and `block` response branches selected by the model's own decision without exposing the expected branch for a certification case.

#### Scenario: Draft branch requires a bounded role artifact
- **WHEN** the model returns `decision: draft`
- **THEN** the generated schema requires exactly one non-null role-specific artifact containing evidence-bearing draft content
- **AND** deterministic validation still decides whether draft was the correct semantic decision

#### Scenario: Block branch forbids a completed role artifact
- **WHEN** the model returns `decision: block`
- **THEN** the generated schema requires the role-specific artifact to be `null`
- **AND** the response identifies unresolved inputs and required human actions

#### Scenario: Decision branch does not reveal the answer
- **WHEN** a certification response schema is generated
- **THEN** both `draft` and `block` branches remain available
- **AND** case-specific expected decision, expected reason codes, required source IDs, required artifact kind, and validator result are absent from every model-facing surface

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

### Requirement: Adapter 2.1 evidence remains compatible and append only
Adapter `2.1` execution SHALL create new identity-bound evidence while preserving adapter `1.0` and `2.0` evidence as immutable historical inputs.

#### Scenario: New execution binds adapter 2.1
- **WHEN** Qwen-class or DeepSeek-class adapter `2.1` certification runs
- **THEN** raw attempts, phase summaries, normalized evidence, prompt and schema hashes, observed model identity, runtime version, and request contract identify adapter `2.1`

#### Scenario: Historical evidence remains readable
- **WHEN** existing adapter `1.0` or `2.0` normalized evidence is validated
- **THEN** the compatible read-only validation path accepts its historical shape without rewriting raw or normalized artifacts

#### Scenario: Certification remains gated per family
- **WHEN** adapter `2.1` certification is executed
- **THEN** each family must pass all five preflight cases before its fifteen-case matrix may start
- **AND** an honest failed preflight is retained without a matrix and does not certify the family
