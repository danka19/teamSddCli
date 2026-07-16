# Weak-Model Adapter 2.1 Design

## Accepted Direction

The human owner accepted option 1 on 2026-07-16 and explicitly authorized design recording, planning, implementation, and a new certification run without another design-approval pause.

Adapter `2.1` uses a decision-dependent response schema:

- `draft` requires one bounded non-canonical role artifact;
- `block` requires the role artifact to be `null` and requires unresolved inputs plus human actions;
- both branches remain visible to the model, so the schema does not reveal the correct answer;
- case-specific expected decisions, reason codes, sources, artifact kind, and validator outcomes remain outside all model-facing surfaces.

The normative behavior and architecture are owned by:

- `openspec/changes/simplify-weak-model-decision-contract/specs/weak-model-decision-contract/spec.md`
- `openspec/changes/simplify-weak-model-decision-contract/design.md`

## Observed Adapter 2.0 Failure Classification

The ten retained Qwen/DeepSeek preflight responses were structurally valid but semantically invalid:

| Category | Count | Adapter 2.1 response |
|---|---:|---|
| Blocked decision with completed role artifact | 9/10 | Make the combination structurally impossible. |
| Wrong draft/block decision | 5/10 | Add neutral draft-vs-approval guidance; keep semantic validation. |
| Wrong/incomplete reason codes | 7/10 | Keep the global vocabulary visible but do not reveal case-specific required codes. |
| Missing required role sources | 2/10 | Keep source selection model-owned and deterministic validation strict. |
| Fabricated passed check | 1/10 | Preserve evidence/source semantic validation and no semantic retry. |
| Missing unresolved input | 1/10 | Require non-empty unresolved inputs and human actions on the block branch. |

## Safety Boundaries

Adapter `2.1` does not select the answer, repair semantics, inspect or publish hidden reasoning, approve work, transition lifecycle state, mutate canonical files, or weaken any deterministic gate. One retry remains available only when the response is empty, invalid JSON, or violates the generated schema.

Runtime certification retains exact observed full digest/runtime binding, immediate pre-call identity checks, external non-aliased append-only destinations, prompt/schema/request hashes, failed-run retention, and AI-disabled fallback.

## Certification Acceptance

Each exact model family must independently pass:

```text
preflight: 5/5
matrix:   15/15
```

A failed family receives no matrix. Its evidence is retained and work item 2.11 remains open. Phase 2.12 cannot start until the required model evidence is complete and explicitly accepted by the human owner.
