# Weak-Model Adapter Remediation Design

Date: 2026-07-16
Status: approved in conversation; awaiting written-spec review before implementation planning
Primary phase: Phase 2
Active work item: 2.11, AI-Disabled And Weak-Model Certification

## Context

The first frozen non-leading certification established a trustworthy failure baseline rather than weak-model reliability:

- `qwen3.5:9b` passed 0/5 preflight cases and 1/15 matrix cases;
- `deepseek-r1:8b` passed 0/5 preflight cases and 0/15 matrix cases;
- the AI-disabled baseline passed 11/11;
- deterministic validation rejected invalid model output without granting approval, resume, lifecycle-transition, release, or canonical-write authority.

Most model failures occurred before semantic validation because the assistants did not return the exact compact JSON contract. DeepSeek also consumed output capacity in a reasoning envelope and sometimes produced no usable final response. The deterministic control plane behaved correctly and must not be weakened.

The remediation goal is to make the internal AI layer effective enough to produce valid bounded drafts and safe-stop decisions while preserving all existing human-authority, evidence, source-ownership, lifecycle, and safety boundaries.

## Phase Change Intake

```text
Idea: Remediate the weak-model adapter so Qwen- and DeepSeek-family assistants can reliably produce bounded role output without weakening deterministic authority or safety checks.
Source: Human rejection of fallback-only acceptance after Phase 2 work item 2.11 certification results, confirmed on 2026-07-16.
Type: scope_refinement, architecture_change, data_contract_change, verification_change, documentation_change
Decision: adopt_now
Reason: Accepting the current fallback dispositions would leave the internal AI layer ineffective and would make the intended work item 2.11 outcome incorrect for the human's stated product goal.
Affected specs: Existing define-transfer-ready-process-package weak-model-guardrails delta and its certification tasks; no independent capability is introduced.
Affected architecture: Add a thin model-family generation adapter, role-specific constrained response contracts, reasoning/final separation, and mechanical normalization ahead of the unchanged deterministic validator.
Data contract impact: Replace the model-facing all-role compact envelope with a generated common decision envelope plus one role-specific payload; preserve the existing normalized operation-evidence contract downstream.
Verification impact: Require adapter-focused TDD, negative authority/evidence/source tests, append-only retry evidence, 5/5 preflight for each model family before its matrix, and 15/15 matrix completion for both families.
Status: adopted for design; implementation remains blocked until the written design and implementation plan are reviewed.
```

The change belongs in the already active `define-transfer-ready-process-package` change because that change owns the weak-model operating kit, adapters, certification contract, and work item 2.11. The implementation plan must preserve the completed first-run evidence and add explicit remediation tasks instead of rewriting completed history.

## Goals

1. Make both frozen local proxy models return structurally valid bounded decisions reliably.
2. Reduce model-facing contract complexity through role-specific schemas.
3. Keep reasoning bytes separate from the authoritative final-response boundary.
4. Keep normalization mechanical and incapable of repairing model semantics.
5. Preserve deterministic validation, human authority, canonical-source ownership, and append-only failed-run evidence.
6. Gate expensive matrix execution behind a strict per-family 5/5 preflight.

## Non-Goals

- Granting AI approval, waiver, merge, release, resume, archive, lifecycle-transition, or canonical-write authority.
- Relaxing expected decisions, required reason codes, required sources, evidence sufficiency, or negative safety cases.
- Encoding expected case answers in prompts or generated schemas.
- Automatically inventing missing facts, claims, checks, source references, role artifacts, or human decisions.
- Hiding, overwriting, or reclassifying the original Qwen and DeepSeek certification failures.
- Establishing equivalence between the local proxy models and a future corporate runtime.
- Starting work item 2.12 before remediation acceptance.

## Considered Approaches

### Prompt-only remediation

This is the smallest change, but the 0/5 preflight results show that prompt instructions alone do not reliably enforce the current JSON boundary. It also leaves the model responsible for repetitive technical fields that do not require model judgment.

### Runtime schema constraint only

Passing a JSON Schema to the runtime should improve syntactic compliance, but it leaves the same cross-role semantic surface and does not by itself address reasoning/final separation or the oversized common envelope.

### Thin family adapter with role-specific constrained generation

This is the selected approach. It combines runtime schema-constrained generation, explicit reasoning/final separation, a smaller role-specific model contract, mechanical normalization, and the unchanged deterministic validator. It targets the observed failure boundary without moving policy or authority into the adapter.

## Architecture

The remediation adds a bounded generation boundary between deterministic task launch and existing semantic validation:

```text
case + role + read pack
        |
deterministic launcher
        |
model-family adapter + generated role schema
        |
raw reasoning envelope + raw final response
        |
strict role-response parser
        |
mechanical normalizer
        |
existing operation-evidence validator
        |
append-only certification evidence
```

The launcher remains the owner of workflow selection, role, stage, available sources, authority limits, and mandatory human stop. The family adapter owns only runtime request formation and response-envelope handling. The model supplies bounded semantic choices. The normalizer translates those explicit choices into the existing operation-evidence shape. The validator remains the final control plane.

## Components

### Deterministic contract builder

The certification orchestrator may retain the selected validator case for downstream semantic validation, but it must first ask the deterministic launcher to bind an optional closed `model_response_contract` into the task launch. That launcher-owned projection contains exactly:

- `case_id`;
- `operation`;
- `role_payload_key`;
- `required_artifact_kind`;
- the global allowed reason-code vocabulary.

The task-launch identity covers the projection. Verified source IDs are not copied from the validator case into the projection; the builder derives them only from the launch's verified source manifest. Existing non-certification launches remain valid without the optional projection.

The builder receives only the verified launch. It creates a JSON Schema that contains:

- the shared bounded-decision fields;
- only the selected role payload;
- enumerated source IDs from the supplied read pack and synthetic case facts;
- the globally allowed reason-code vocabulary;
- closed objects with no additional properties.

The projection is not serialized wholesale into the model prompt, generated schema, or runtime request. The builder may expose only its safe model-facing fields: `case_id`, `operation`, `role_payload_key`, and the global reason-code vocabulary. `required_artifact_kind` remains internal launcher metadata used only by mechanical normalization and downstream semantic validation. The schema and prompts must not contain the expected decision, required case-specific reason codes, required source subset, risk/contract classification, expected role output, or any other validator-only answer.

### Model-family adapters

The Qwen and DeepSeek adapters remain thin. They may set only runtime-level generation options supported by the pinned local runtime, including the generated schema, reasoning mode, and bounded output budget. They must not contain process rules, expected case answers, lifecycle policy, or human-authority decisions.

Family-specific behavior is limited to differences demonstrated by runtime evidence. Unsupported runtime capabilities must fail explicitly instead of silently degrading to an unconstrained contract.

### Reasoning/final separator

Raw reasoning and raw final output are retained as distinct evidence fields. Only the final-response channel may enter the strict parser. Reasoning is never promoted to a final answer, normalized evidence, authority, or a passing result.

Forbidden authority or fabricated-evidence language found in the retained model response remains available to negative validation and audit. Separation is an envelope operation, not semantic sanitization.

### Role-response parser

The parser accepts exactly one schema-conforming JSON object. It rejects Markdown fences, prose wrappers, unknown keys, unknown sources, unsupported reason codes, and a payload for any role other than the selected role.

### Mechanical normalizer

The normalizer receives the parsed response, verified launch, and read pack, never the full validator case. It maps only explicit model fields into the existing operation-evidence contract. It may add deterministic launch metadata and contract-owned invariant fields, including the internal `required_artifact_kind`, but it must not:

- change `draft` to `block` or `block` to `draft`;
- add or remove reason codes or sources;
- invent a role summary, observation, claim, check, unresolved input, or human decision;
- reinterpret unsupported or conflicting evidence as sufficient;
- remove prohibited statements to make an answer pass.

Any transformation that would require domain judgment is a validation failure, not normalization.

### Existing deterministic validator

The downstream validator continues to enforce expected safe decisions, required reason codes, required source coverage, source hashes, evidence sufficiency, role output kind, human stop, pending review, forbidden authority, and forbidden lifecycle behavior. Remediation must not delete or relax an existing diagnostic to make a model pass.

## Model-Facing Contracts

Every role response includes:

- `case_id`;
- `decision` as `draft` or `block`;
- `reason_codes`;
- `source_ids`;
- `unresolved_inputs`;
- `human_decisions_required`;
- one role-specific payload or `null`.

Role payloads are:

- analyst: `requirements_note`;
- developer: `implementation_prep_note`;
- QA: `qa_review_note`;
- Tech Lead: `advisory_review_note`.

A non-null role payload contains a concise summary, source-linked observations, source-linked claims, and source-linked checks. A blocked decision requires a null role payload plus concrete unresolved inputs and required human decisions.

Approval, transition, resume, human-stop, review-pending, canonical-write, and similar authority fields are not model choices. They are fixed by the deterministic launch contract and rechecked downstream. Free-text content remains subject to forbidden-authority and unsupported-evidence validation.

## Data Flow

1. The certification orchestrator retains the full case for downstream semantic validation and asks the deterministic launcher to bind the closed `model_response_contract`; the launch identity covers it.
2. The contract builder consumes only that verified launch, derives source IDs from its verified manifest, and generates the role-specific closed JSON Schema without validator-only expected answers.
3. The family adapter adds only the pinned runtime options for Qwen or DeepSeek.
4. The runtime returns raw reasoning and raw final-response bytes.
5. The separator preserves both channels and passes only final-response bytes to the parser.
6. The parser validates exact structure and permitted identifiers.
7. The normalizer consumes only the response, verified launch, and read pack and expands the explicit response into the existing operation-evidence shape.
8. The unchanged deterministic validator receives the retained full case and evaluates expected decisions, case-specific reason codes, artifact-kind semantics, evidence, authority, and stop rules.
9. The runner records the attempt, raw checksum, diagnostics, intervention, and fallback without overwriting earlier attempts.

## Retry And Failure Handling

One transparent technical retry is permitted only when the final response is empty or is not valid schema-conforming JSON. The retry:

- uses the same case facts, sources, role, authority boundary, and generated schema;
- does not reveal the expected decision, required reason codes, or expected output;
- may restate only the structural response requirement;
- is recorded as a new append-only raw attempt;
- never replaces or suppresses the first failure.

There is no automatic retry for a syntactically valid but semantically incorrect answer. Such an answer is a genuine certification failure. Exhausted technical retries route to the existing named human or deterministic fallback and keep work item 2.11 open.

## Safety Properties

- AI remains advisory and cannot mutate canonical state.
- The adapter cannot select workflow, authority, lifecycle, approval, or safety policy.
- Schema constraints limit form but do not encode expected answers.
- Normalization cannot repair semantics.
- The existing semantic validator remains mandatory and fail-closed.
- Every raw attempt and retry is checksum-bound and append-only.
- Original failed certification evidence remains immutable historical baseline.
- No private paths, corporate identifiers, secrets, or real corporate source material enter Git evidence.

## Verification Strategy

Implementation follows scenario-first TDD. Focused tests must cover:

1. role-specific closed-schema generation;
2. absence of every validator-only field name and unique sentinel value from generated schemas, initial prompts/requests, and structural-retry prompts/requests, while the internal artifact-kind sentinel is available only to normalization;
3. Qwen and DeepSeek request formation;
4. reasoning/final separation, including empty final output;
5. successful mechanical normalization for each role;
6. rejection of semantic repair attempts;
7. unknown source IDs and unsupported reason codes;
8. prohibited authority language and fabricated evidence;
9. wrong-role payloads and invalid JSON wrappers;
10. one-retry limit and append-only preservation of both attempts;
11. unchanged downstream validator behavior;
12. normalized evidence and raw-artifact checksum consistency.

After focused and regression tests pass, certification runs in this order for each model family:

1. execute the five-case preflight;
2. require 5/5 passing results;
3. only then execute the fifteen-case matrix;
4. require 15/15 passing results.

Qwen and DeepSeek are gated independently, but remediation succeeds only when both families pass both gates.

## Acceptance Criteria

The remediation is accepted only when all of the following hold:

- `qwen3.5:9b`: preflight 5/5 and matrix 15/15;
- `deepseek-r1:8b`: preflight 5/5 and matrix 15/15;
- analyst, developer, QA, and Tech Lead role contracts all produce valid structured output;
- minor, major, and hotfix classes remain covered;
- critical authority, missing-context, fabricated-evidence, unsafe-resume, failed-run-retention, QA-evidence, reconciliation, stop-point, approval, and lifecycle cases pass unchanged semantic expectations;
- no expected answer is exposed in a prompt, schema, retry, or adapter;
- no existing authority, source, evidence, stop, or lifecycle check is weakened;
- both the original baseline and all remediation attempts remain retained and checksum-bound;
- AI-disabled certification remains passing;
- focused tests, relevant regression tests, OpenSpec strict validation, roadmap/OpenSpec validation, privacy checks, and Git diff checks pass.

If either model family fails its preflight after the single permitted technical retry, its matrix is not run. Work item 2.11 remains open, work item 2.12 remains blocked, and the exact residual incompatibility is recorded for a new human disposition.

## Documentation And Status Effects

Implementation planning must update the active weak-model OpenSpec delta and tasks before product code changes. The plan must also update the Phase 2 change-intake record and work item 2.11 status from `pending_acceptance` back to `in_progress` without unchecking or rewriting the already completed first certification execution task. New remediation and recertification tasks must preserve exact roadmap/OpenSpec ownership and historical evidence.

The original recommendation to accept fallback-only dispositions is superseded by the human decision to attempt remediation now. That supersession must be reflected in the Phase 2 plan, current audit, and new dated remediation evidence; the original dated certification audits remain unchanged historical records.
