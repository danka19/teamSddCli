## MODIFIED Requirements

### Requirement: Unresolved feedback and publication blockers
The SDD process SHALL define how unresolved Confluence comments affect future publication and archive gates.

#### Scenario: Feedback SLA is configurable
- **WHEN** a Confluence-enabled workflow defines feedback triage rules
- **THEN** blocker and non-blocker triage SLA values are read from editable team/process configuration and may be disabled explicitly when corporate workflow tooling owns timing control

#### Scenario: Default triage SLA is used when enabled
- **WHEN** feedback SLA is enabled and no stricter team override exists
- **THEN** blocker comments are triaged within 1 working day and non-blocker comments are triaged within 3 working days

#### Scenario: Blocker comment prevents final publication
- **WHEN** a Confluence-enabled flow has an unresolved blocker comment
- **THEN** final publication or archive readiness is blocked until the comment has an accepted, rejected, deferred, duplicate, or approved-waiver disposition

#### Scenario: Non-blocking comment still needs disposition
- **WHEN** a Confluence-enabled flow has a non-blocking comment
- **THEN** the flow may continue only when the comment has an explicit disposition and any accepted/deferred follow-up is recorded

#### Scenario: Core class routes do not require fabricated Confluence evidence
- **WHEN** a minor, major, or hotfix package is evaluated before Confluence publication exists in the supported implementation
- **THEN** missing publication, preview, or feedback evidence is handled according to the approved implementation boundary and is not fabricated as a satisfied gate or treated as a blocker

#### Scenario: Applicable publication becomes class-aware later
- **WHEN** generated Confluence publication is implemented and required by the artifact matrix
- **THEN** publication and feedback evidence is selected by class, impact, project configuration, and lifecycle gate while Git/OpenSpec remains canonical

#### Scenario: Existing Confluence corpus is read-only archive
- **WHEN** an existing Confluence analytics page is used as input for new SDD work
- **THEN** the page is treated as read-only reference material and any accepted requirement or analytics content is rewritten or linked through a Git/OpenSpec change instead of editing the legacy page as canonical source

#### Scenario: Generated views are selected in corporate environment
- **WHEN** the first Confluence-enabled workflow is planned
- **THEN** the required generated view set is decided inside the corporate environment using real corporate templates, approval practices, and tool constraints rather than being finalized in the external planning repository
