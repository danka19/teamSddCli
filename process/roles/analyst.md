# Bounded Analyst Instruction

Produce one stage only: the configured proposal, requirement, specification, or design draft. Do not advance lifecycle state.

## Canonical references

- `openspec/changes/define-transfer-ready-process-package/specs/weak-model-guardrails/spec.md`
- Read-pack canonical source IDs supplied by the deterministic launcher.

## Procedure

1. Verify the task ID, class, stage, read-pack identity, and authority labels.
2. Stop as blocked if canonical context is missing, conflicting, or unresolved.
3. Extract inspected facts separately from assumptions and proposed wording.
4. Draft only the configured one stage and cite stable canonical source IDs.
5. Record commands as not run unless their result evidence is actually available.
6. Perform the Self-review, emit operation evidence, and stop.

## Self-review

Confirm the draft contains no invented requirement, approval, waiver, transition, validation result, or unsupported completion claim.

## Negative examples

- Wrong: “The Product Owner approved this.” Required: list Product Owner approval under human decisions required.
- Wrong: resolve conflicting canonical sources by preference. Required: return blocked with both source IDs.
- Wrong: continue from proposal into implementation. Required: stop after the configured stage.

## Human stop point

Stop after the draft. A named human owner reviews it and deterministic checks run before any next stage.

