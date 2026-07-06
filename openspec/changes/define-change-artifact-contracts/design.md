## Context

Current docs and OpenSpec proposals preserve the complete-package direction: proposal, design, tasks, spec deltas, QA plans, test cases, automation plans, and traceability. The accepted strategy narrows the first MVP to a thin change flow and requires deterministic guarantees without depending on AI.

## Proposed Artifact Contract

Thin changes should require only the artifacts needed to understand, review, validate, and later archive the change:

- `proposal.md`
- at least one `specs/<capability>/spec.md` delta
- at least one testable scenario per requirement
- `traceability.yaml` with requirement-to-scenario links
- concise verification evidence in `tasks.md` or a linked evidence section
- `change.yaml` once the final metadata schema is approved

Behavior-changing SDD changes should require an OpenSpec delta by default. A no-spec-change rationale is an approved limited exception, not default behavior. It applies only to docs-only work, refactors with no behavior change, or other no-behavior-change maintenance where a human reviewer approves the classification and the change provides replacement evidence such as existing test coverage, focused manual checks, or review notes showing that behavior did not change.

Full change packages add `design.md`, risk/impact analysis, QA test plan, test case artifacts, automation plan, API/mobile/cross-repo coordination notes, and explicit owner review evidence when their triggers apply.

## Approved Human Decisions From Work Item 1.3

Human approval recorded on 2026-07-06: use the risk-oriented Option A matrix, and keep Jira task automation, Confluence publication, QA/AT proposal generation, and role inboxes outside the first MVP while planning them as later layers. Any validator, template, or CI behavior still changes only in later implementation work items after the related proposal updates are reviewed.

### Decision: Thin Change Minimum

Approved Option A: Require proposal, OpenSpec delta, scenarios, basic traceability, and verification evidence for behavior-changing SDD changes. This keeps small bugfixes and refactors practical while still proving what changed and how it is checked.

Rejected for the default matrix: Require `design.md` for every thin change. This improves review context but adds burden for low-risk work and may encourage empty design files.

Allowed as a limited exception, not the default for behavior-changing SDD work: a no-spec-change rationale for docs-only, refactor, or no-behavior-change maintenance with human reviewer approval and replacement evidence.

Implementation consequence: validator and template expansion may now enforce this matrix in a later work item, but must preserve the limited no-spec-change exception and still reject behavior-changing work without an OpenSpec delta.

### Decision: Full Package Triggers

Approved Option A: Require full package for new features, user-visible behavior changes with broad impact, public API changes, mobile impact, cross-repo changes, data/security risk, or high rollback cost. This matches the architecture while keeping small fixes thin.

Rejected for the default matrix: Use only explicit human labels to choose full package mode. This is flexible but can under-classify risky changes.

Rejected for the default matrix: Require full package for all behavior changes. This maximizes evidence but is too heavy for the first MVP.

Implementation consequence: future gates should infer full-package triggers from risk signals where practical, while allowing explicit human escalation to full package mode.

### Decision: MVP Boundary

Approved Option A: Confirm Jira task automation, Confluence publication, QA/AT proposal generation, and role inboxes remain outside the first MVP. This protects the thin flow and keeps deterministic checks shippable.

Rejected for the first MVP: Add Confluence preview as an MVP artifact. This improves stakeholder visibility but requires the feedback-loop proposal to be accepted first.

Rejected for the first MVP: Add Jira task creation as an MVP artifact. This improves workflow tracking but expands integration and environment risk before the thin flow is proven.

QA/AT proposal generation and role inboxes are intentionally not MVP alternatives in this decision packet because they depend on later scenario, traceability, and task-source contracts. They stay outside the first MVP unless the human owner explicitly re-scopes Phase 1 or the MVP boundary.

Planning consequence: Jira, Confluence, QA/AT proposal generation, and role inboxes stay planned as later layers; their proposals may be drafted, but their absence is not a first-MVP blocker.

## Future Journey, Screen, And Legacy Artifacts

Customer journey and screen artifacts are planned future contracts. A UI-impacting full package may later use `journey.yaml`, `screens.yaml`, and versioned `assets/screens/`, but those artifacts are not required for the first thin MVP. If introduced, specs should reference stable screen IDs instead of embedding large images inside every requirement.

Legacy baseline is planned as a low-bureaucracy mode for already-written behavior. The process should not require full retroactive packages for historical changes. When a legacy function is touched, the change should record observed existing behavior, proposed changed behavior, at least one regression scenario, known gaps, and screenshots when UI behavior is affected.

## AI Assistance Boundary

AI may draft or review artifacts, but the existence, completeness, and acceptance of artifacts must be determined by deterministic checks and human review.
