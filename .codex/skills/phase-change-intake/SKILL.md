---
name: phase-change-intake
description: Triage new ideas, fixes, scope changes, architecture notes, data contract changes, or verification requests that appear while a roadmap phase is already in progress. Use before switching plans, changing phase scope, creating an OpenSpec change, or deferring user feedback during phase work.
---

# Phase Change Intake

Use this skill when new human feedback appears during an active phase and could alter scope, priorities, architecture, documentation, data contracts, or verification.

## Workflow

1. Restate the new idea in one sentence.
2. Classify it as one or more types: `bug_fix`, `scope_refinement`, `new_feature`, `architecture_change`, `data_contract_change`, `verification_change`, `documentation_change`, or `out_of_scope`.
3. Check impact against the current phase goal, active work item, `openspec/specs/` accepted requirements, active `openspec/changes/<change-id>/` deltas, architecture boundaries, data contracts, verification evidence, privacy, safety, and deployment rules.
4. Choose exactly one routing decision: `adopt_now`, `queue_current_phase`, `create_openspec_change`, `defer`, or `reject`.
5. Interrupt active work only when the idea affects data loss risk, security/privacy, remote deployment, accepted requirements, data contracts, architecture correctness, or the human explicitly says to stop/switch.
6. Persist the decision in the smallest durable place: OpenSpec specs/changes, the relevant phase plan `Change Intake` section, `docs/CURRENT_PROJECT_AUDIT.md`, `docs/CONTEXT.md`, or `docs/AI_STEP_VERIFICATION_CHECKLIST.md`.
7. Continue the previous work item unless the routing decision requires interruption.

## Intake Record Shape

```text
Idea:
Source:
Type:
Decision:
Reason:
Affected specs:
Affected architecture:
Data contract impact:
Verification impact:
Status:
```

## Decision Guidance

- Prefer `queue_current_phase` over interrupting when the idea is relevant but not blocking.
- Prefer `create_openspec_change` when implementation would need new acceptance criteria or data contract changes.
- Prefer `defer` when the idea is valuable but outside the active phase goal.
- Use `adopt_now` only when ignoring the idea would make the current work item wrong or unsafe.
- Never silently discard feedback. Record rejected or deferred items with the reason.
