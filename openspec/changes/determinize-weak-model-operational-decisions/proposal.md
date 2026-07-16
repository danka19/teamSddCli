## Why

Adapter `2.1` proved that Qwen- and DeepSeek-class models can satisfy the
structural JSON contract, but the supported workflow still asks them to infer
policy decisions, exact reason codes, required source inventory, and artifact
kind from dense prose. The retained preflight evidence shows that some failures
come from hidden or ambiguous validator expectations, including rejection of
safe references to required human decisions, so another prompt-only revision
would not reliably reduce operational error.

## What Changes

- Move draft-versus-block eligibility, policy reason codes, required source
  inventory, artifact kind, and accountable human action codes into a
  deterministic operation plan created before the model call.
- Give the model one explicit bounded action: populate a non-canonical draft or
  explain a deterministic block without choosing policy state.
- Bind source inventory and human handoff mechanically; require model citations
  only for claims it actually authors.
- Replace natural-language authority rejection on human-handoff text with
  structured authority fields and scope-aware checks.
- Make every model-visible semantic obligation explicit and give each failure a
  local stable diagnostic; retain one structural-only retry and prohibit
  semantic repair or self-critique loops.
- Certify the supported operational path against the existing frozen Qwen and
  DeepSeek proxies while retaining adapter `2.1` as immutable diagnostic
  baseline evidence.

## Capabilities

### New Capabilities

- `weak-model-operational-decision-plan`: Deterministic operation planning,
  model task-card projection, structured human handoff, and operational
  certification criteria for weak-model assistance.

### Modified Capabilities

None. The blocked `weak-model-decision-contract` change remains immutable
adapter `2.1` history; the active transfer-readiness change continues to own the
broader weak-model and certification objective.

## Impact

- Code: weak-model launcher, response normalization, authority validation,
  certification catalog/runner, and stable diagnostics.
- Contracts: a deterministic operation-plan document and a smaller model-facing
  content contract.
- Tests: ambiguity fixtures, policy-projection tests, authority false-positive
  tests, source binding, Qwen/DeepSeek preflight and matrix gates, and
  AI-disabled regression.
- Documentation: the Phase 2.11 audit and plan reference this change; role
  documents remain canonical supporting sources and are not duplicated into a
  new documentation hierarchy.

## Roadmap

- Execution phase: P2
- Related phases: P3
- Lifecycle status: planned
