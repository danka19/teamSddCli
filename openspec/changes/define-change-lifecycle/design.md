## Context

The accepted implementation strategy says the first process must work without a custom `sdd` CLI. Lifecycle enforcement therefore starts as documented OpenSpec behavior and later becomes deterministic script, pre-commit, and CI behavior where practical.

## Proposed Design

The lifecycle is modeled as a small set of named states:

- `draft`: author is preparing the change package.
- `spec_review`: the Spec PR is open and deterministic checks are expected to run.
- `approved`: humans approved and merged the Spec PR; later automation may create tasks from this state.
- `in_implementation`: implementation and verification work is active.
- `ready_to_archive`: required evidence is complete and archive can be requested.
- `archived`: the change has been applied to living specs after explicit human approval.

## Allowed Transition Table

| Current state | Allowed next state | Required gate / owner |
|---|---|---|
| `draft` | `spec_review` | Deterministic review-minimum validation passes; author opens the Spec PR or equivalent review surface. |
| `spec_review` | `draft` | Human reviewer requests rework or the author withdraws review. |
| `spec_review` | `approved` | Required human reviewers approve and the Spec PR or equivalent review is merged/accepted. |
| `approved` | `in_implementation` | Implementation work starts from approved scope; later automation may create tasks only after approval. |
| `in_implementation` | `ready_to_archive` | Required implementation, verification, traceability, documentation, and waiver evidence is complete. |
| `ready_to_archive` | `in_implementation` | Archive readiness review finds missing or stale evidence and sends the change back for rework. |
| `ready_to_archive` | `archived` | Explicit human archive approval is recorded and final archive checks pass. |
| `archived` | none | Archived changes are immutable process history; follow-up behavior changes require a new change. |

Skipped states are not valid transitions. In particular, `draft` cannot move directly to `approved`, `ready_to_archive`, or `archived`. No state can move to `archived` without first reaching `ready_to_archive`, passing final deterministic checks, and recording explicit human archive approval.

Thin changes may skip heavy artifacts, but they do not skip proposal/spec/scenario/traceability evidence. Full packages add design, QA, AT, and risk evidence when feature/API/mobile/cross-repo/high-risk conditions apply.

## Deterministic Gates Versus AI Assistance

Deterministic gates validate structure, required artifacts, OpenSpec deltas, traceability links, waiver shape, and later CI evidence. AI may draft proposals, reviews, context packs, or skeletons, but AI output is advisory until a human accepts it in Git, PR review, or a documented decision.

## Human Ownership

Humans own approval, merge, correctness, accepted scope, and final archive. CI or future scripts may block invalid transitions, but they must not approve requirements, decide business correctness, or silently resolve unresolved decisions.

Generated Confluence views may display lifecycle, approval, and verification status in later publication flows, but Confluence is not the status owner. Displayed status must be derived from source artifacts such as the change package, PR/review surface, CI evidence, tracker state after tasks exist, or approved waiver records.

The human-facing MVP lifecycle may be presented as `draft -> spec_review -> approved -> implemented -> archived`, while internal validation may use the more explicit `in_implementation` and `ready_to_archive` states to separate active work from archive readiness. The final naming should be reviewed during Phase 1 acceptance readiness before accepted specs are promoted.

## Risks / Trade-offs

- A single lifecycle for every change can become heavy for small fixes, so the proposal keeps thin changes lightweight.
- Too many lifecycle states can create busywork, so task creation, publication, and role inbox states stay outside the first MVP.
- Archive is intentionally gated by a later human decision because it writes accepted living specs.
- Some docs and generated-view examples mention richer approval/testing gates; those are later layers unless a human explicitly re-scopes the first MVP.
