## ADDED Requirements

### Requirement: Confluence is generated publication
The SDD process SHALL treat Confluence as a generated read/publication model, not the canonical requirement source.

#### Scenario: Generated page links back to source
- **WHEN** a Confluence page is generated from OpenSpec or Markdown source
- **THEN** the page shows source commit, source PR or change ID, generated timestamp, a warning that generated content must be edited in Git/OpenSpec, and links back to canonical files

#### Scenario: Generated content is not edited as source
- **WHEN** a stakeholder wants to change requirement content displayed on a generated Confluence page
- **THEN** the process routes the change back to a Git/OpenSpec change or PR update instead of accepting the manual Confluence edit as canonical

#### Scenario: Raw OpenSpec is not published as the main business view
- **WHEN** publication targets business, product, or analyst readers
- **THEN** the generated Confluence page groups content by audience meaning, such as change, capability, journey, release, technical appendix, or screen gallery, instead of mirroring raw file structure 1:1

### Requirement: Feedback loop disposition
The SDD process SHALL require explicit disposition for Confluence comments before those comments affect requirements or publication readiness.

#### Scenario: Accepted comment becomes source change
- **WHEN** a Confluence comment is accepted as requirement feedback
- **THEN** the owner records the disposition and updates the Git/OpenSpec change, opens a follow-up change, or updates the relevant PR before generated publication is refreshed

#### Scenario: Rejected comment records reason
- **WHEN** a Confluence comment is rejected
- **THEN** the owner records the rejection reason so the comment does not remain ambiguous feedback

#### Scenario: Deferred comment records follow-up
- **WHEN** a Confluence comment is deferred
- **THEN** the owner records the follow-up task, change, or review point that will handle it later

#### Scenario: Duplicate comment links to source disposition
- **WHEN** a Confluence comment duplicates existing feedback
- **THEN** the owner records the duplicate disposition and links or refers to the original disposition where practical

### Requirement: Unresolved feedback and publication blockers
The SDD process SHALL define how unresolved Confluence comments affect future publication and archive gates.

#### Scenario: Blocker comment prevents final publication
- **WHEN** a Confluence-enabled flow has an unresolved blocker comment
- **THEN** final publication or archive readiness is blocked until the comment has an accepted, rejected, deferred, duplicate, or approved-waiver disposition

#### Scenario: Non-blocking comment still needs disposition
- **WHEN** a Confluence-enabled flow has a non-blocking comment
- **THEN** the flow may continue only when the comment has an explicit disposition and any accepted/deferred follow-up is recorded

#### Scenario: Thin MVP does not require Confluence evidence
- **WHEN** a first-MVP thin change has no Confluence publication, preview, or feedback evidence
- **THEN** the absence of Confluence evidence does not block review or archive readiness because Confluence publication is outside the first MVP

#### Scenario: Existing Confluence corpus is read-only archive
- **WHEN** an existing Confluence analytics page is used as input for new SDD work
- **THEN** the page is treated as read-only reference material and any accepted requirement or analytics content is rewritten or linked through a Git/OpenSpec change instead of editing the legacy page as canonical source

### Requirement: Generated publication assets
The SDD process SHALL keep accepted diagrams, journey schemes, and screen assets in a versioned source or source+export flow that generated Confluence pages can embed with stable traceability.

#### Scenario: Accepted diagram has versioned source
- **WHEN** a diagram, journey scheme, or screen asset becomes accepted source for a generated view
- **THEN** it has a stable ID and Git-managed source or source+export artifact that can be linked from OpenSpec, traceability, or generated Confluence output

#### Scenario: Confluence drawing is draft-only
- **WHEN** an analyst draws a diagram directly in Confluence during discussion
- **THEN** the drawing may be used as feedback or draft input, but it must be exported or recreated into the Git-managed asset flow before it becomes accepted/published source

### Requirement: Evidence-backed status display
The SDD process SHALL display approval and testing state in generated Confluence pages only when backed by source evidence.

#### Scenario: Status display has evidence link or waiver
- **WHEN** a generated change page displays QA, AT, CI, manual test, approval, or traceability status
- **THEN** each displayed status links to evidence or an approved waiver

#### Scenario: Confluence does not own status
- **WHEN** Confluence displays approval, testing, or lifecycle state
- **THEN** the source of truth remains the corresponding Git/OpenSpec artifact, PR/review surface, CI result, tracker state, or approved waiver
