## ADDED Requirements

### Requirement: Tech lead governance responsibilities
The SDD process SHALL define the tech lead as a first-class human role for technical classification, readiness, risk, execution control, completion, and release recommendation.

#### Scenario: Tech lead review covers required decisions
- **WHEN** a change requires tech-lead review
- **THEN** the review covers classification, technical scope, architecture impact, affected owners and dependencies, quality/regression strategy, implementation readiness, stop conditions, completion evidence, and release or transfer readiness

#### Scenario: Business ownership remains separate
- **WHEN** the tech lead confirms technical readiness
- **THEN** that decision does not replace product/business acceptance, QA ownership, security/compliance approval, merge approval, or final archive approval assigned to other roles

### Requirement: Tech lead classification control
The tech lead workflow SHALL prevent unsupported under-classification while preserving deterministic evidence.

#### Scenario: Tech lead receives classification evidence
- **WHEN** classification confirmation is requested
- **THEN** the tech lead receives the classifier result, all triggered rules, unknown inputs, affected systems, owner mappings, and proposed artifact matrix

#### Scenario: Tech lead cannot approve a lower class
- **WHEN** a major trigger is present but minor is requested
- **THEN** the tech lead rejects the route, corrects erroneous source evidence for deterministic recalculation, or escalates a proposed versioned policy change without approving a per-change lower-class exception

### Requirement: Tech lead readiness and architecture control
The tech lead workflow SHALL provide deterministic support for technical Definition of Ready and architecture decisions.

#### Scenario: Readiness pack is bounded and source-linked
- **WHEN** a tech lead opens a change for readiness review
- **THEN** the pack identifies relevant requirements, scenarios, design decisions, affected repositories and owner zones, dependencies, risks, regression obligations, blockers, waivers, and source paths without copying a second normative specification

#### Scenario: Architecture decision is explicit
- **WHEN** classification or impact criteria indicate an architecture decision may be required
- **THEN** the readiness report links an accepted or proposed ADR/design decision or records an approved evidence-based not-required result

### Requirement: Tech lead stop, hold, escalation, and resume control
The tech lead workflow SHALL support explicit control of technically unsafe or insufficiently specified work.

#### Scenario: Stop condition creates a hold record
- **WHEN** a defined technical stop condition occurs
- **THEN** the change records the trigger, observed evidence, affected work, immediate safety action, owner, escalation route, and conditions required for resume

#### Scenario: Resume requires resolved evidence
- **WHEN** held work requests resume
- **THEN** deterministic checks confirm required corrective evidence exists and an authorized human records the resume decision

#### Scenario: AI cannot resume held work
- **WHEN** an AI assistant proposes that a stop condition is resolved
- **THEN** the proposal remains advisory and cannot change the hold state

### Requirement: Tech lead completion and release recommendation
The tech lead workflow SHALL produce a source-linked completion and release-readiness recommendation without replacing other approvals.

#### Scenario: Completion report exposes unresolved obligations
- **WHEN** implementation completion or Definition of Done is reviewed
- **THEN** the report shows scenario evidence, checks, defects, architecture dispositions, risk decisions, waivers, follow-ups, release obligations, and blocking gaps

#### Scenario: Recommendation is not final approval
- **WHEN** the tech lead records a positive release or transfer recommendation
- **THEN** required QA, product, security, release, merge, archive, or tracker decisions remain independently required

### Requirement: Deterministic tech lead decision support
The process package SHALL provide deterministic tech-lead views before an AI-enhanced role inbox is treated as reliable workflow support.

#### Scenario: Required deterministic views are available
- **WHEN** the tech lead evaluates a change
- **THEN** available outputs include classification, readiness, owner/dependency, scope-drift, stop/escalation, completion, release-readiness, waiver-expiry, and hotfix-follow-up reports

#### Scenario: Role inbox waits for authoritative sources
- **WHEN** task or tracker synchronization is not yet authoritative
- **THEN** a tech-lead inbox is labelled partial or deferred and does not invent status, ownership, or due dates

#### Scenario: Configured control checkpoint exposes flow risks
- **WHEN** a scheduled or event-driven Tech Lead checkpoint runs
- **THEN** the report identifies untriaged or unclassified work, missing fixed input, class/gate blockers, scope drift, missing owners, stopped or externally waiting work, failed evidence collection, invalid waivers, overdue hotfix reconciliation, process bypass, and release-package gaps from authoritative sources

#### Scenario: Cadence is configuration rather than universal policy
- **WHEN** a project needs daily, weekly, release-based, or event-driven Tech Lead review
- **THEN** the approved project configuration selects the cadence and owners while the canonical report content and authority boundaries remain unchanged

### Requirement: AI advisory boundary for tech lead automation
AI support SHALL not impersonate or replace the tech lead's accountable decisions.

#### Scenario: AI may draft analysis
- **WHEN** AI support is enabled
- **THEN** it may draft questions, summaries, risk hypotheses, architecture options, missing-context findings, and proposed review comments with source references

#### Scenario: AI may not approve
- **WHEN** an action would confirm classification, mark DoR or DoD green, approve a waiver, accept residual risk, resume a hold, or accept release readiness
- **THEN** the action requires deterministic evidence and the authorized human decision even if AI output recommends it
