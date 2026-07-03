## Context

The architecture describes traceability as requirement -> scenario -> dev task -> test case -> automated test. The accepted strategy keeps the initial proof small, with basic `traceability.yaml` in the first MVP and richer integration later.

## Proposed Design

Traceability is staged:

- Review minimum: each proposed requirement has at least one testable scenario, and `traceability.yaml` links requirement IDs to scenario IDs or headings.
- Implementation evidence: tasks, commits, PRs, or verification notes link back to the relevant requirement/scenario where available.
- Archive readiness: required task, test, automation, and waiver links are complete according to the approved artifact and waiver policies.

When Jira, QA/AT, and automation repositories are not yet in MVP scope, equivalent manual evidence may be recorded as stable IDs, file paths, PR links, or explicit pending/waived status. Pending traceability is allowed only before archive readiness. At archive readiness every required downstream link must resolve to concrete evidence or an approved waiver; otherwise the change returns to implementation or review.

## Deterministic Gates Versus AI Assistance

Deterministic validation can check existence, parseable IDs, missing links, and unsupported statuses. AI may suggest missing links or summarize coverage gaps, but AI output is not traceability evidence until reviewed and committed.

## Risks / Trade-offs

- Requiring full downstream traceability too early would block thin changes before task and QA automation exist.
- Allowing free-form evidence forever would weaken archive confidence.
- The proposal therefore stages checks by lifecycle point and mode.
