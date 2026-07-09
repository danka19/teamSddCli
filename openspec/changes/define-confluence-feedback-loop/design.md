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

Approved gate 1.7 default on 2026-07-09:

- owner: analyst/change owner;
- feedback SLA is a triage SLA, not an implementation SLA;
- default SLA: blocker comments are triaged within 1 working day; non-blocker comments are triaged within 3 working days;
- SLA settings must be editable and may be disabled by explicit team/process config for environments where timing is handled by corporate workflow tools;
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

## Existing Confluence Corpus And Assets

Human decision on 2026-07-09:

- existing Confluence analytics content is a read-only archive for the first pilot;
- no bulk migration is required before the first thin flow;
- reused legacy analytics content becomes new Git/OpenSpec source through a reviewed change instead of being edited in Confluence as canonical source;
- accepted diagrams, journey schemes, and screen assets use Git-managed source or source+export with stable IDs and generated Confluence embeds.

If an analyst draws a diagram directly in Confluence, treat it as a discussion draft or feedback artifact. Before it becomes accepted/published source, export or recreate it into the Git-managed asset flow. Visio is acceptable when it is the team's practical source format, but it is not mandatory; diagram-as-code, draw.io/diagrams.net source, Figma exports, or another agreed source+export pair are also acceptable if they preserve version history, stable IDs, and generated-view traceability.

Generated-view selection for the first corporate Confluence-enabled workflow is intentionally deferred to the corporate environment. The external planning repository records the contract boundaries, but the actual view set must be chosen against real corporate templates, approval practices, and tool constraints.

## Risks / Trade-offs

- Publishing raw OpenSpec 1:1 would be cheap but hard for business readers to use.
- Generating audience-specific pages improves readability but requires a publication model and drift/source-warning discipline.
- Treating comments as direct edits would create a second source of truth, so accepted feedback must become Git/OpenSpec changes or PR updates.
- Blocking every unresolved comment can stall delivery; the proposed default distinguishes blocker comments from non-blocking comments with explicit disposition.
- Diagrams drawn only inside Confluence are easy for analysts during discussion but are hard to diff, validate, reuse, or regenerate. Treating them as drafts preserves convenience while keeping accepted artifacts versioned in Git.
