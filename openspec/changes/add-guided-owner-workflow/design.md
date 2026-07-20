## Context

The package currently exposes bounded scripts such as bootstrap, create, classify, gate evaluation, Tech Lead review, archive preparation, and fallback planning. The scripts are safe but are not a self-service workflow interface. Existing role instructions are AI-facing and assume that the caller already selected the role, stage, and command.

## Goals

- Let a new colleague start with a business situation instead of internal filenames or script names.
- Give humans and AI assistants the same current, versioned route map.
- Keep command selection deterministic and evidence-backed.
- Preserve human ownership of classification confirmation, DoR, DoD, waiver, resume, release, archive, and risk acceptance.
- Make absence of AI or an integration explicit and route the user to the deterministic fallback.

## Non-Goals

- Autonomous lifecycle transitions, approval, archive, release, merge, deployment, or external-system mutation.
- Corporate configuration, credentials, integration wiring, or pilot execution.
- A second source of workflow policy outside the package and OpenSpec contracts.

## Architecture

1. A versioned machine-readable guided-workflow catalog owns route definitions. Each route declares its situation identifier, prerequisites, applicable lifecycle/class constraints, command sequence, expected inputs and evidence, human decision boundary, and deterministic fallback.
2. One guided CLI entry point consumes that catalog. It accepts an explicit situation and supplied known facts, validates them, and returns the next permitted action or a structured block. It is read-only unless it delegates to an already explicit, separately invoked mutating command.
3. A human/AI onboarding guide is generated from or deterministically checked against the catalog. It must never carry divergent command or authority rules.
4. AI receives a bounded route excerpt and may explain, draft, or identify missing context. It cannot select an undocumented route, infer authority, or assert that a gate is approved.

## Primary Routes

- New business requirement: capture problem and outcome, create a draft change, select or correct proposed classification, and prepare Delta Spec work.
- Existing change: inspect current state, choose the next allowed review, implementation, QA, gate, release, or archive-preparation operation.
- Urgent incident: evaluate hotfix eligibility, preserve minimum safety/traceability/reconciliation obligations, and stop for human confirmation.
- Blocked or failed operation: retain the failed evidence, show hold/escalation/resume prerequisites, and never silently retry or clear the control.
- Unavailable AI or integration: make the unavailable surface explicit and return the AI-disabled/manual route.

## Trade-offs

- A catalog plus guided CLI introduces a small maintained interface, but prevents fragile knowledge from being distributed across runbooks and prompts.
- The guide must be narrow and route-focused; it must reference, not duplicate, detailed policy thresholds.
- The entry point may recommend a command but must not make a human decision. This keeps the requested usability improvement compatible with the existing governance model.

## Verification Strategy

- Unit and CLI tests prove every published situation maps only to declared commands and authority boundaries.
- Synthetic end-to-end tests start from a business requirement and cover minor, major, hotfix, unknown context, unavailable AI/integration, failed-run retention, and forbidden approval paths.
- A contract check proves the human/AI guide and machine catalog are synchronized.
- Bootstrap/install documentation is rehearsed in a clean synthetic workspace; no corporate service or credential is used.
- A successor package is versioned and verified by the applicable deterministic, AI-disabled, privacy, update/rollback, and release-integrity gates before Phase 4 starts.
