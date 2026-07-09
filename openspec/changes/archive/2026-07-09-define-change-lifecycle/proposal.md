## Why

The architecture describes a change lifecycle from draft through archive, but Phase 1 needs a testable proposal before templates, validators, CI, or future CLI commands can enforce state transitions.

Work item 1.1 delivered the first deterministic evidence in commit `6fbde43`: a copyable change package template, validator, pre-commit entrypoint, and OpenSpec change. This proposal builds on that evidence by defining what lifecycle states and gates those deterministic tools will eventually protect.

## What Changes

- Define proposed lifecycle states for thin and full SDD changes.
- Define the allowed transition points for draft, Spec PR review, approval, implementation, verification, and archive.
- Separate deterministic gates from AI advisory support.
- Preserve human ownership for approval, merge, correctness, and final archive decisions.
- Keep Jira task automation, Confluence publication, QA/AT generation, and role inboxes outside the first MVP unless a later human decision re-scopes the pilot.

## Capabilities

### New Capabilities

- `change-lifecycle`: Proposed lifecycle states, transition gates, and ownership rules for SDD change packages.

### Modified Capabilities

- None.

## Impact

- Adds a proposed OpenSpec capability only.
- Does not create accepted specs.
- Does not implement new validator behavior, templates, scripts, or CLI commands.
- Provides acceptance scenarios for later deterministic validation and CI checks.
