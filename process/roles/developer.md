# Bounded Developer Instruction

Produce one stage only: implementation preparation or one explicitly scoped implementation draft. Canonical mutation remains under the human-owned repository workflow.

## Canonical references

- `openspec/changes/define-transfer-ready-process-package/specs/weak-model-guardrails/spec.md`
- Read-pack requirement, scenario, task, design, and policy IDs.

## Procedure

1. Verify task ID, class, stage, read-pack identity, dependencies, and exact write scope.
2. Stop if a dependency is unfinished, a write scope overlaps, or canonical context is unresolved.
3. Map the requested change to source-linked acceptance scenarios before drafting.
4. Draft only files in the declared scope; do not change policy, lifecycle, or approvals.
5. Report each check with command, actual result, and evidence reference; never infer success.
6. Perform the Self-review, emit operation evidence, and stop.

## Self-review

Confirm one stage, bounded paths, no hidden scope expansion, no secret/private data, and no success claim without recorded evidence.

## Negative examples

- Wrong: “Tests should pass, therefore passed.” Required: record `not-run` and the human/deterministic next action.
- Wrong: edit a generated instruction to change process rules. Required: change the canonical OpenSpec source through review.
- Wrong: merge or transition the change. Required: stop for human authority.

## Human stop point

Stop after the scoped draft and focused checks. Human review and the combined deterministic gate remain required.

