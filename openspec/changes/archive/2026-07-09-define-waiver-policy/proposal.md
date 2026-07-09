## Why

The SDD process needs exceptions that are transparent and reviewable. A waiver should prevent unnecessary bureaucracy for valid cases, but it must not become a free-text escape hatch from tests, traceability, documentation, or human approval.

Work item 1.1 commit `6fbde43` created the first deterministic validator but intentionally left final waiver behavior for later Phase 1 decisions. This proposal drafts that contract.

## What Changes

- Define proposed waiver fields: ID, type, scope, reason, evidence, approver, expiry or review point, and affected requirements/scenarios.
- Define when a waiver can satisfy a missing artifact or verification expectation.
- Define negative cases where waivers are insufficient.
- Keep waiver approval human-owned and audit-ready.
- Record the 2026-07-06 human decision approving role-appropriate approvers and minimum evidence.

## Capabilities

### New Capabilities

- `waiver-policy`: Proposed waiver requirements, approval rules, and negative scenarios.

### Modified Capabilities

- None.

## Impact

- Adds proposed OpenSpec requirements only.
- Does not modify validator behavior, templates, tests, or accepted specs.
- Records the approved Phase 1 work item 1.3 waiver decision.
- Leaves deterministic waiver enforcement to later approved implementation work.
