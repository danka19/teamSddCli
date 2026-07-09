## Why

The project uses Git/OpenSpec/Markdown as the canonical source for requirements and process contracts. Confluence is still valuable for reading, discussion, agreement, analytics, and navigation, but it must not become a second source of truth.

Phase 1 needs a proposed Confluence feedback and publication contract before any publication automation, preview generation, comment processing, or final Confluence page behavior is implemented. The human owner reaffirmed on 2026-07-06 that Confluence publication stays outside the first MVP and is planned as a later layer.

## What Changes

- Define Confluence as a generated read/publication model, not a requirement source.
- Define generated page metadata: source commit, source PR/change ID, generated timestamp, source warning, and links back to canonical Git/OpenSpec files.
- Define generated view types: change page, capability page, customer journey page, release/change summary, technical appendix, and optional screens/gallery page.
- Define a feedback loop where comments are triaged and recorded as accepted, rejected, deferred, or duplicate.
- Define unresolved-comment behavior and publication/archive blockers for future Confluence-enabled flows.
- Define that testing and approval status is displayed only when backed by evidence links or approved waivers.
- Keep Confluence publication outside the first MVP until a later accepted implementation plan.

## Capabilities

### New Capabilities

- `confluence-feedback-loop`: Proposed generated publication, feedback disposition, unresolved-comment, and source-of-truth rules for Confluence.

### Modified Capabilities

- None.

## Impact

- Adds proposed OpenSpec requirements only.
- Does not modify templates, scripts, tests, pre-commit behavior, accepted specs, or Confluence/Jira integrations.
- Adds a later human decision gate for feedback owner, SLA/service expectation, and unresolved-comment behavior.
