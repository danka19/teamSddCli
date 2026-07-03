## Why

The architecture lists a rich change package shape, while the accepted implementation strategy requires a practical thin MVP first. Phase 1 needs a proposed artifact contract that avoids over-heavy defaults but still protects requirement, scenario, and traceability quality.

Work item 1.1 commit `6fbde43` proves a baseline template and validator can check package structure. This proposal defines the next artifact matrix those deterministic checks can later enforce after human approval.

## What Changes

- Define proposed artifact groups for thin changes and full change packages.
- Mark which artifacts are required, optional, deferred, or waiver-eligible.
- Reserve full package defaults for feature, API, mobile, cross-repo, high-risk, or broad behavior changes.
- Record decision notes for work item 1.3 before the matrix becomes binding.
- Keep AI assistance as drafting/review support only.

## Capabilities

### New Capabilities

- `change-artifact-contracts`: Proposed artifact matrix and scenarios for thin changes and full change packages.

### Modified Capabilities

- None.

## Impact

- Adds proposed OpenSpec requirements only.
- Does not change `templates/change/`, `scripts/validate_change.py`, tests, or pre-commit behavior.
- Creates a decision packet for Phase 1 work item 1.3.
