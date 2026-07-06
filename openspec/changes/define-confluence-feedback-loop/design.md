## Context

The accepted implementation strategy keeps deterministic process guarantees in templates, scripts, OpenSpec, CI, and standard tool features. Confluence is a generated publication layer and must not be used as the editable source of requirements.

The first MVP remains the thin change flow. This proposal plans later Confluence behavior without adding Confluence publication as an MVP artifact.

## Proposed Publication Model

Raw OpenSpec artifacts should not be published 1:1 for business readers. Publication should use an intermediate model:

```text
OpenSpec/change packages/living specs
  -> publication model
  -> audience-oriented Markdown pages
  -> generated Confluence pages
```

The generated views should include, as useful for the audience:

- change page;
- capability page;
- customer journey page;
- release/change summary;
- technical appendix;
- screens/gallery page.

Every generated page must show source commit, source PR or change ID, generated timestamp, a warning that generated content must be edited in Git/OpenSpec, and links back to canonical files.

## Feedback Loop

Recommended default for the later human gate:

- owner: analyst/change owner;
- blocker comments block final approval/publication for Confluence-enabled flows;
- non-blocking comments may continue only when every comment has an explicit disposition;
- rejected comments require a reason;
- deferred comments require a follow-up task or change.

Proposed flow:

```text
Confluence comment
  -> triage by owner
  -> accepted / rejected / deferred / duplicate
  -> accepted feedback becomes OpenSpec change or PR update
  -> generated Confluence preview republishes
```

## Approval And Verification Display

Confluence may display approval and testing state, but it is not the approval or validation source. Sources of truth are:

- `change.yaml`: change intent and status before approval, once the schema is accepted;
- Bitbucket PR or equivalent review surface: review and approval evidence;
- Jenkins/CI or equivalent deterministic check: validation and testing evidence;
- Jira/tracker: execution workflow after tasks exist;
- OpenSpec/living specs: accepted product truth;
- Confluence: generated read model.

Testing status must be displayed only when there is an evidence link or approved waiver. Future change pages should include an `Approval & Verification Status` block with spec status, source PR, source commit, approvals by role, OpenSpec validation, change package validation, traceability check, CI pipeline, relevant QA/AT/manual statuses, Confluence feedback state, and blockers.

## MVP Boundary

Confluence publication, preview, final publication, comment sync, feedback automation, and generated gallery pages are not required for the first MVP. They are planned later contracts. For the first thin MVP, absence of Confluence evidence is not an archive blocker.

When Confluence publication is enabled for a later flow, final publication/archive must be blocked by unresolved blocker comments or missing required evidence links unless an approved waiver or disposition permits continuation.

## Risks / Trade-offs

- Publishing raw OpenSpec 1:1 would be cheap but hard for business readers to use.
- Generating audience-specific pages improves readability but requires a publication model and drift/source-warning discipline.
- Treating comments as direct edits would create a second source of truth, so accepted feedback must become Git/OpenSpec changes or PR updates.
- Blocking every unresolved comment can stall delivery; the proposed default distinguishes blocker comments from non-blocking comments with explicit disposition.
