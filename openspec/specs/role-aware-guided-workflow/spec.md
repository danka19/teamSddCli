## Purpose

Определить детерминированный role-aware guided workflow P3, который сохраняет человеческую власть над решениями и подготовкой операций.

## Roadmap

- Roadmap phase: P3
- Related phases: P4

## Requirements

### Requirement: Fail-closed role-aware guidance

P3 guided workflow SHALL require an explicit supported `human_role` before it returns a role-sensitive route or CTA.

#### Scenario: Unknown role is blocked

- **WHEN** a caller omits `human_role` or supplies an unsupported value
- **THEN** the read-only payload SHALL be `blocked` with `unknown-role` or `invalid-role` and no commands or CTA

#### Scenario: Analyst cannot receive implementation CTA

- **WHEN** an `Analyst` requests guidance for an approved change
- **THEN** the payload SHALL not contain `begin-approved-implementation` and SHALL name an authorized human handoff

### Requirement: Trusted revision-bound human acceptance

P3 implementation guidance SHALL require a schema-valid acceptance event from a trusted human role, a literal message, a trusted event reference, and a digest matching the shown Delta Spec revision.

#### Scenario: UI confirmation is rejected

- **WHEN** acceptance evidence contains only `Да` or another non-literal UI confirmation
- **THEN** the validator SHALL reject it as `guided-process.acceptance-message-invalid`

#### Scenario: Accepted revision differs from current spec

- **WHEN** acceptance evidence names a digest different from the referenced Delta Spec bytes or summary digest
- **THEN** the validator SHALL reject implementation guidance as revision-mismatched

### Requirement: Readiness preserves DoR

P3 trusted acceptance SHALL not bypass Definition of Ready.

#### Scenario: Incomplete package remains blocked

- **WHEN** required documents, scenario traceability, `DoR: passed`, or blocker/placeholder-free content are absent
- **THEN** the validator SHALL return invalid even when a trusted-looking acceptance record exists

### Requirement: MCP-free P3 guidance

P3 guided catalog, runbook, and read-pack SHALL contain no MCP invocation, setup, credential, dependency, or fallback.

#### Scenario: Existing-change route has no MCP fallback

- **WHEN** the local existing-change route is rendered
- **THEN** its fallback list SHALL not include MCP and it SHALL not request any external integration action

### Requirement: Human-confirmed decision card

P3 guided workflow SHALL represent a natural-language human decision as a non-authoritative `decision_draft` card bound to one change and revision before it can become a recorded decision.

#### Scenario: Natural-language decision prepares but does not record

- **WHEN** an Analyst writes a natural-language decision such as `Принимаю спецификацию` for a shown revision
- **THEN** the workflow SHALL show one `DEC-…` card with the quoted message, revision digest and one stated consequence, and SHALL not create acceptance, DoR or implementation authority

#### Scenario: Card confirmation records only the active decision

- **WHEN** the next human message is `Подтверждаю DEC-…` or normalized `Подтверждаю` for the active unexpired card
- **THEN** the workflow SHALL record the decision with both verbatim human messages and the bound revision digest

#### Scenario: Ambiguous chat text cannot record a decision

- **WHEN** the human writes `что дальше?`, `да`, `продолжай`, an unrelated message, or a confirmation after another message/card
- **THEN** the workflow SHALL keep the decision unconfirmed and SHALL not mutate acceptance, DoR or lifecycle authority

### Requirement: Proactive discovery completeness

In `обычно` mode P3 guided workflow SHALL proactively surface material unresolved decision areas before declaring intake sufficient or preparing a spec draft.

#### Scenario: Material unknowns receive an explicit choice

- **WHEN** a requirement leaves a material area unresolved that changes behavior, scope, UX, runtime, risk or verification
- **THEN** the workflow SHALL describe the impact and offer `углубиться`, `принять defaults`, or `подготовить draft с открытыми решениями`

#### Scenario: Silence is not default acceptance

- **WHEN** the human does not explicitly choose a proposed default or deferral
- **THEN** the workflow SHALL retain the area as unresolved and SHALL not report intake or spec readiness as sufficient

### Requirement: Non-authoritative operation confirmation binding

P3 SHALL bind a typed operation-confirmation request and event to a trusted human role, catalog `operation_id`, canonical `input_digest`, card `revision_digest`, trusted event chain, and expiry. A local `sdd request` intent without actual trusted event metadata SHALL be separate from the typed request, SHALL report that trusted metadata is required, and SHALL NOT fabricate the event chain. Neither record nor intent SHALL grant authority for lifecycle, DoR, acceptance, release, or execution.

#### Scenario: Missing, mismatched, future, expired, or extra operation evidence is blocked

- **WHEN** an operation-confirmation event omits a binding field, has an unknown field, an unauthorized role or operation, altered input/card digest, a future issued/confirmed timestamp, or is expired at validation
- **THEN** validation SHALL reject it before an entrypoint starts

#### Scenario: Local request does not invent trusted ingress

- **WHEN** `sdd request` is invoked without actual trusted human/assistant/human event metadata
- **THEN** it SHALL return only non-authoritative intent with `trusted_event_metadata_required: true` and SHALL NOT return an operation-confirmation record or fabricated event references

#### Scenario: Operation confirmation never enables P3 execution

- **WHEN** a valid operation-confirmation event is supplied to `sdd run`
- **THEN** the dispatcher SHALL return `confirmation-contract-pending` without spawning an entrypoint

#### Scenario: External mutation remains forbidden

- **WHEN** a caller requests or runs an operation classified as `mutate_external`
- **THEN** P3 SHALL reject it irrespective of any confirmation artifact
