## Context

The source architecture shows a complete package with proposal, design, tasks, spec deltas, QA plans, test cases, automation plans, and traceability. The accepted strategy narrows the first MVP to a thin change flow and requires deterministic guarantees without depending on AI.

## Proposed Artifact Contract

Thin changes should require only the artifacts needed to understand, review, validate, and later archive the change:

- `proposal.md`
- at least one `specs/<capability>/spec.md` delta
- at least one testable scenario per requirement
- `traceability.yaml` with requirement-to-scenario links
- concise verification evidence in `tasks.md` or a linked evidence section
- `change.yaml` once the final metadata schema is approved

Behavior-changing SDD changes should require an OpenSpec delta by default. A no-spec-change rationale is a pending and limited human decision, not default behavior. If approved, it applies only to docs-only work, refactors with no behavior change, or other no-behavior-change maintenance where a human reviewer approves the classification and the change provides replacement evidence such as existing test coverage, focused manual checks, or review notes showing that behavior did not change.

Full change packages add `design.md`, risk/impact analysis, QA test plan, test case artifacts, automation plan, API/mobile/cross-repo coordination notes, and explicit owner review evidence when their triggers apply.

## Decision Notes For Work Item 1.3

Pending human approval: the final artifact matrix must be approved before any validator, template, or CI gate treats this proposal as binding.

### Decision: Thin Change Minimum

Option A, recommended: Require proposal, OpenSpec delta, scenarios, basic traceability, and verification evidence for behavior-changing SDD changes. This keeps small bugfixes and refactors practical while still proving what changed and how it is checked.

Option B: Require `design.md` for every thin change. This improves review context but adds burden for low-risk work and may encourage empty design files.

Option C: Allow a limited no-spec-change rationale for docs-only, refactor, or no-behavior-change maintenance with human reviewer approval and replacement evidence. This is fastest for true non-behavior work, but it is a pending human decision and must not become the default for behavior-changing SDD changes.

Consequence if unresolved: validator and template expansion must wait because the project cannot safely decide which missing artifacts are errors.

### Decision: Full Package Triggers

Option A, recommended: Require full package for new features, user-visible behavior changes with broad impact, public API changes, mobile impact, cross-repo changes, data/security risk, or high rollback cost. This matches the architecture while keeping small fixes thin.

Option B: Use only explicit human labels to choose full package mode. This is flexible but can under-classify risky changes.

Option C: Require full package for all behavior changes. This maximizes evidence but is too heavy for the first MVP.

Consequence if unresolved: future gates may either block too much work or allow high-risk changes with thin evidence.

### Decision: MVP Boundary

Option A, recommended: Confirm Jira task automation, Confluence publication, QA/AT proposal generation, and role inboxes remain outside the first MVP. This protects the thin flow and keeps deterministic checks shippable.

Option B: Add Confluence preview as an MVP artifact. This improves stakeholder visibility but requires the feedback-loop proposal to be accepted first.

Option C: Add Jira task creation as an MVP artifact. This improves workflow tracking but expands integration and environment risk before the thin flow is proven.

QA/AT proposal generation and role inboxes are intentionally not MVP alternatives in this decision packet because they depend on later scenario, traceability, and task-source contracts. They stay outside the first MVP unless the human owner explicitly re-scopes Phase 1 or the MVP boundary.

Consequence if unresolved: Phase 1 cannot clearly separate artifact contracts for the thin MVP from later full workflow automation.

## AI Assistance Boundary

AI may draft or review artifacts, but the existence, completeness, and acceptance of artifacts must be determined by deterministic checks and human review.
