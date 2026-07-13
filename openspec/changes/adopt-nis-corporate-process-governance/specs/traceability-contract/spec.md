## ADDED Requirements

### Requirement: Corporate governance traceability
Traceability SHALL connect classification, readiness, flow-control, completion, release, and follow-up evidence to the requirements and scenarios they govern.

#### Scenario: Classification decision is source-linked
- **WHEN** a class is confirmed or classifier source evidence is corrected
- **THEN** traceability links the classification report, triggering rules, human decision, affected requirements or systems, corrected source evidence, recalculation result, and any follow-up record

#### Scenario: Gate result links evidence and owner
- **WHEN** Definition of Ready, Definition of Done, release readiness, or archive readiness is evaluated
- **THEN** each blocking or satisfied obligation links its source evidence, responsible role, result, policy version, and waiver or deferral where applicable

#### Scenario: Stop and resume history remains visible
- **WHEN** a change is stopped, held, escalated, resumed, or deviates from the baseline
- **THEN** traceability preserves the linked trigger, decision, corrective evidence, residual risk, and affected scenarios

#### Scenario: Release package links canonical scope
- **WHEN** a release or transfer package is prepared
- **THEN** it links included change, requirement, scenario, artifact, verification, limitation, rollback, and follow-up identifiers

#### Scenario: Failed attempts remain traceable after retry
- **WHEN** a validation, AI, adapter, integration, or workflow attempt fails and a later attempt succeeds
- **THEN** traceability preserves both attempt identifiers, outcomes, source evidence, and the required disposition instead of replacing the failure with the successful result


## MODIFIED Requirements

### Requirement: Archive-readiness traceability
The SDD process SHALL define class-aware completion traceability required before a change can be archived.

#### Scenario: Major package archive checks expanded evidence
- **WHEN** a major change requests archive readiness
- **THEN** traceability links requirements and scenarios to required implementation, QA, automation, architecture, regression, release, and approval evidence or permitted approved waivers

#### Scenario: Minor package accepts practical evidence
- **WHEN** a minor change requests archive readiness before deferred Jira or QA/AT automation exists
- **THEN** traceability may use committed verification notes, PR links, test command evidence, manual QA records, deterministic reports, or approved waivers according to the minor matrix

#### Scenario: Hotfix package links reconciliation
- **WHEN** a hotfix requests archive readiness
- **THEN** traceability links urgent-entry evidence, minimum verification, rollback or hold evidence, applied implementation, post-change checks, deferred artifacts, and completed reconciliation or approved disposition

#### Scenario: Verification evidence remains source-linked
- **WHEN** traceability records verification evidence
- **THEN** the evidence points to a committed note, PR, CI or local test output, manual QA record, automation result, deterministic report, human decision, or approved waiver rather than a generated display alone

#### Scenario: Pending traceability is allowed before archive readiness
- **WHEN** a change is in review or implementation before archive readiness
- **THEN** required downstream task, test, automation, release, or evidence links may be marked pending when the missing evidence is expected later in the lifecycle

#### Scenario: Pending downstream link blocks archive readiness
- **WHEN** a change requests archive readiness and a required downstream link or hotfix reconciliation remains pending
- **THEN** deterministic validation or review rejects archive readiness unless the link is replaced by concrete evidence or a policy-permitted approved disposition

### Requirement: Future journey and screen traceability
The SDD process SHALL use journey and screen traceability when the class and impact matrix require it without making it a universal minor blocker.

#### Scenario: Journey view links product path to evidence
- **WHEN** a customer journey view is generated for an applicable change
- **THEN** it links journey steps to screens, requirements, scenarios, and test or verification evidence

#### Scenario: Screen catalog preserves requirement links
- **WHEN** a screen catalog is required for a UI-impacting major or hotfix change
- **THEN** each screen entry links a stable screen ID to file path, capability, journey, journey step, state, source, requirement refs, and scenario refs

#### Scenario: Non-UI minor does not require journey traceability
- **WHEN** a minor change has no journey or screen impact
- **THEN** missing journey or screen links do not block review or archive readiness

#### Scenario: Deferred hotfix screen evidence remains pending
- **WHEN** an applicable hotfix screen artifact is validly deferred
- **THEN** traceability keeps the gap, deferral, owner, and due condition visible until reconciliation
