## Why

Adapter `2.0` proved that both frozen proxy models can return schema-valid role responses, but all ten preflight responses failed semantic validation. The dominant failure was contract ambiguity: nine responses combined `decision: block` with a completed role artifact, while other responses confused advisory drafting with approval, omitted required evidence boundaries, or invented a successful check.

Adapter `2.1` is needed now because work item 2.11 cannot complete until the model-facing contract makes `draft` and `block` mutually exclusive without revealing validator-only expected answers or weakening deterministic and human authority gates.

## What Changes

- Add a decision-discriminated response contract:
  - `draft` requires exactly one bounded role artifact with a model-selected kind from one neutral global artifact vocabulary and evidence-bearing content.
  - `block` requires the role artifact to be `null` and requires unresolved inputs plus human actions.
- Replace prose-dependent interpretation of the decision branch with JSON Schema `oneOf`/`const` constraints selected by the model's own `decision`.
- Keep reason-code and artifact-kind choice model-owned and validate them semantically after parsing; do not expose case-specific expected decisions, expected reason codes, or required artifact kind.
- Treat the bounded source pack as launcher-selected required context. The model is checked on faithful attribution to supplied source IDs, not on guessing a hidden required-source subset.
- Clarify the universal process distinction between preparing a non-canonical advisory draft and approving or advancing work.
- Retain one retry only for structural contract failures; structurally valid semantic failures remain non-retryable and are retained.
- Preserve exact adapter `1.0` and `2.0` schema, prompt, diagnostics, and evidence reconstruction as immutable historical inputs while generating new adapter `2.1` append-only evidence.
- Remove model-authored `passed`/`failed` check results from adapter `2.1`; only source review or explicit missing/not-run/conflict states can be promoted mechanically.
- Exclusively create phase directories, retain operational failure summaries, and bind runtime-probe summary checksums into normalized evidence.
- Re-run exact-identity Qwen and DeepSeek certification in new external artifact roots, gating each fifteen-case matrix behind its own five-of-five preflight.

## Capabilities

### New Capabilities

- `weak-model-decision-contract`: Decision-dependent weak-model response schemas, non-leading role semantics, structural retry classification, compatibility, and adapter `2.1` certification acceptance.

### Modified Capabilities

None. The existing accepted specs do not yet contain this proposed adapter behavior; the related `weak-model-guardrails` delta remains owned by the active transfer-readiness change and is referenced rather than duplicated.

## Impact

- Code: `process/model_adapter.py`, `process/actual_certification.py`, adapter profiles, certification schema/catalog support, runner/gate/normalization paths.
- Tests: model adapter, actual certification, package schema, compatibility, leakage, retry, and external-evidence validation.
- Evidence: new append-only Qwen, DeepSeek, and AI-disabled raw artifact roots outside Git plus normalized Git evidence.
- Documentation: weak-model operating kit, certification runbook, Phase 2 audit/status, file structure, and current project audit.
- Safety: no change to human authority, deterministic gates, canonical-write prohibition, semantic-repair prohibition, or exact-identity/runtime/destination controls.

## Roadmap

Execution phase: P2

Related phases: P3

Lifecycle status: in_progress
