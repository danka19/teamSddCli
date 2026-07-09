## Why

Traceability is one of the core architecture guarantees, but the first MVP must avoid manual bureaucracy. Phase 1 needs a proposed traceability contract that deterministic tools can validate in layers.

Work item 1.1 commit `6fbde43` already introduced basic requirement-to-scenario validation in the local validator. This proposal defines the broader target contract for later work.

## What Changes

- Define minimum traceability for draft/spec review.
- Define completion traceability for archive readiness.
- Define waiver behavior for missing task, test, or automation links.
- Distinguish deterministic link checks from AI-generated traceability suggestions.
- Avoid requiring Jira, QA/AT repositories, or role inbox automation for the first thin MVP.

## Capabilities

### New Capabilities

- `traceability-contract`: Proposed traceability links, completion checks, and waiver scenarios for SDD changes.

### Modified Capabilities

- None.

## Impact

- Adds proposed OpenSpec requirements only.
- Does not update `traceability.yaml`, validator logic, tests, or accepted specs.
- Provides acceptance scenarios for later validator and CI expansion.
