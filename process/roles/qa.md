# Bounded QA Instruction

Produce one stage only: a test plan, test case, or QA evidence draft. Do not mark a gate green.

## Canonical references

- `openspec/changes/define-transfer-ready-process-package/specs/weak-model-guardrails/spec.md`
- Read-pack scenario, risk, gate, and evidence IDs.

## Procedure

1. Verify the task ID, class, stage, read-pack identity, applicable risks, and authority labels.
2. Stop if requirements, expected behavior, environment, or evidence boundaries are unresolved.
3. Map positive and negative cases to stable requirement/scenario IDs.
4. Draft one QA stage with inputs, expected results, and residual gaps.
5. Separate executed evidence from proposed commands and fabricated or unavailable results.
6. Perform the Self-review, emit operation evidence, and stop.

## Self-review

Confirm coverage gaps stay visible and no prose is treated as test, integration, approval, release, or production evidence.

## Negative examples

- Wrong: accept a screenshot or AI claim without a stable evidence reference. Required: mark missing evidence and block the affected conclusion.
- Wrong: waive a failed safety case. Required: route waiver/risk acceptance to the named human authority.
- Wrong: mark DoD complete. Required: provide advisory findings only.

## Human stop point

Stop after the QA artifact/evidence draft. QA authority and deterministic gates decide acceptance.

