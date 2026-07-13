## ADDED Requirements

### Requirement: Metrics remain separate from transition gates
The SDD process SHALL distinguish evidence gates that protect correctness from outcome metrics that evaluate whether the process is effective.

#### Scenario: Poor metric does not rewrite required evidence
- **WHEN** a pilot misses a cycle-time or cost target
- **THEN** the miss is recorded for process decision-making but does not waive required safety, approval, readiness, completion, or traceability evidence

#### Scenario: Passing checks are not effectiveness proof
- **WHEN** all deterministic gates pass
- **THEN** the process does not claim improved productivity, quality, or business outcome without the approved comparison evidence

### Requirement: Canonical metric definitions
The pilot contract SHALL define each metric before collection or comparison.

#### Scenario: Metric definition is reproducible
- **WHEN** a metric is approved
- **THEN** its record identifies purpose, unit, numerator and denominator, start and end events, inclusions, exclusions, event sources, owner, missing-data behavior, aggregation, target or decision rule, and privacy classification

#### Scenario: Core outcome set is covered
- **WHEN** the pilot measurement plan is reviewed
- **THEN** it addresses cycle and waiting time, active human effort, machine time and cost, first-pass acceptance, material defects, rework, engineering-package completeness, manual intervention, repeatability, tool/adapter reliability, waivers/bypasses, context switching, and post-pilot delivery stability where applicable

#### Scenario: Context-switch evidence is defined
- **WHEN** portfolio WIP or parallel work is evaluated as a process cost
- **THEN** the metric defines a source event for leaving and resuming governed work, attribution limitations, external interruption handling, aggregation, and privacy boundaries rather than inferring personal productivity from task counts

### Requirement: Event and evidence integrity
Pilot measurement SHALL preserve event provenance, failed runs, and data-quality limitations.

#### Scenario: Automatic source is preferred
- **WHEN** a timestamp or result exists in Git, CI, validator output, tracker history, or an approved integration log
- **THEN** the metric references that source instead of replacing it with unverified self-report

#### Scenario: Manual data is labelled
- **WHEN** a required event cannot be collected automatically
- **THEN** a manual record identifies recorder, time, method, confidence or limitation, and reason automation was unavailable

#### Scenario: Failed runs remain in evidence
- **WHEN** a validation, AI, adapter, or workflow run fails or needs intervention
- **THEN** the failure remains in the measurement dataset and is not discarded merely because a later retry succeeds

#### Scenario: Missing data stays visible
- **WHEN** a required metric input is absent or contaminated
- **THEN** the result is marked incomplete or non-comparable according to the approved rule rather than imputed as success

### Requirement: Privacy, retention, and access boundary
The measurement contract SHALL minimize and govern corporate process data.

#### Scenario: Personal and sensitive data is minimized
- **WHEN** measurement schemas are designed
- **THEN** they avoid prompt content, secrets, personal performance rankings, unrestricted source payloads, and unnecessary personal identifiers unless separately approved

#### Scenario: Data governance is explicit
- **WHEN** a pilot starts
- **THEN** collection purpose, fields, access roles, storage location, retention, redaction, export, deletion, and incident handling are approved and documented

### Requirement: Comparison labels and contamination control
The process SHALL distinguish historical, control, experimental, and production observations.

#### Scenario: Every observation has a context label
- **WHEN** pilot evidence is collected
- **THEN** it records whether the observation is historical baseline, concurrent control, experimental treatment, certification run, or production follow-up plus the relevant process/package version

#### Scenario: Contaminated comparison is disclosed
- **WHEN** staffing, scope, tooling, data quality, external dependencies, or process rules differ materially between compared groups
- **THEN** the analysis records the difference and limits or rejects causal claims

### Requirement: Optional paired experiment integrity
When a paired control experiment is approved, the pilot SHALL preserve comparable input, isolation, independent evidence ownership, and explicit contamination records.

#### Scenario: Paired branches start from the same baseline
- **WHEN** a control and experimental treatment compare the same change
- **THEN** evidence identifies the approved input version, requirements and acceptance set, source commit, environment assumptions, and allowed differences before either branch starts

#### Scenario: Input change triggers comparability review
- **WHEN** requirements, source baseline, acceptance criteria, test data, or environment changes after the paired experiment starts
- **THEN** the change is recorded and the measurement owner decides whether to restart, split, adjust, or mark the pair non-comparable

#### Scenario: Control evidence remains independent
- **WHEN** a control specialist or independent assurance role evaluates the paired result
- **THEN** the role's access, treatment-output visibility, conflict of interest, and review disposition are recorded so an AI checker alone is not treated as independent proof

#### Scenario: Paired implementation is not mandatory for every pilot
- **WHEN** a bounded corporate safety pilot does not justify the cost, data exposure, or delay of duplicate implementation
- **THEN** the approved measurement plan may use historical or other comparison evidence and records the resulting limitation

### Requirement: Pre-registered sample and decision gates
The pilot SHALL define sample-entry, minimum-analysis, decision-ready, and rollout gates before outcome interpretation.

#### Scenario: Thresholds are approved before collection
- **WHEN** a pilot plan becomes active
- **THEN** it records the primary comparator, eligible classes, sample-entry threshold, minimum analyzable sample, decision-ready threshold, rollout rule, stop rule, and decision owners

#### Scenario: Observation window is not a roadmap deadline
- **WHEN** a pilot protocol uses a duration such as a number of weeks
- **THEN** the duration is treated as an experiment parameter and does not silently change roadmap phase deadlines or acceptance criteria

#### Scenario: Decision outcome is explicit
- **WHEN** the decision-ready gate is reached
- **THEN** the authorized process decision records one of scale, bounded rollout, continue collection, revise and repeat, hold, or stop plus evidence, residual risk, limitations, and follow-up

### Requirement: Effectiveness evidence excludes activity proxies
The process SHALL not use artifact counts, prompt counts, AI usage volume, or checklist completion alone as proof of effectiveness.

#### Scenario: Activity metric is contextual only
- **WHEN** an activity measure is reported
- **THEN** it is labelled diagnostic and paired with an approved outcome, quality, effort, reliability, or delivery measure before any effectiveness conclusion is made

#### Scenario: Engineering package completeness is evidence-based
- **WHEN** completeness is scored
- **THEN** the score uses the class-specific required artifact/evidence matrix and substantive validation rather than raw file count

### Requirement: Post-pilot delivery stability
The process SHALL plan post-pilot outcome collection before declaring the process production-ready.

#### Scenario: Stability measures are selected deliberately
- **WHEN** a pilot change can reach a delivery environment
- **THEN** the plan identifies applicable lead-time, deployment-frequency, change-failure, restore-time, escaped-defect, support, rollback, or comparable stability measures and their observation windows

#### Scenario: No production outcome is fabricated
- **WHEN** external deployment or support data is unavailable
- **THEN** the report states that production stability is unverified and does not infer it from archive or test completion

### Requirement: Operability pilot does not prove effectiveness or scale
The process SHALL distinguish the first monitored real-change operability pilot from a later NIS effectiveness or rollout experiment.

#### Scenario: One real change proves bounded operability only
- **WHEN** Phase 3 completes one monitored real minor, major, or hotfix change
- **THEN** the evidence may support compatibility, usability, authority, safety, rollback, and data-collection conclusions but cannot by itself prove productivity improvement, defect reduction, statistical viability, or organization-scale rollout readiness

#### Scenario: Effectiveness decision needs a later approved evidence gate
- **WHEN** a process owner requests a scale, broad rollout, or effectiveness conclusion
- **THEN** a separately approved Phase 4 or later protocol defines the comparator, eligible population, sample gates, control or historical method, contamination rules, production observation, and decision authority before the conclusion is allowed

### Requirement: Pilot safety and isolation
The pilot SHALL use a bounded risk register and stop/rollback controls without claiming zero production risk.

#### Scenario: Pilot risk register covers operational boundaries
- **WHEN** a pilot is approved
- **THEN** risks include data/privacy, secrets, access, accidental delivery, rollback, adapters and MCPs, model/runtime behavior, logs, external dependencies, support ownership, and process bypass

#### Scenario: AI-disabled path is certified
- **WHEN** the process is considered transfer-ready for the pilot
- **THEN** the core classification, readiness, validation, stop, completion, and release evidence path has passed an AI-disabled walkthrough

#### Scenario: AI-only experiment is isolated
- **WHEN** the pilot tests an AI-heavy or no-manual treatment
- **THEN** that treatment is explicitly labelled, bounded, reversible, separately approved, and cannot remove the production fallback or human decision path

#### Scenario: Pilot stop criteria are testable
- **WHEN** branch inputs diverge without approved disposition, treatment output leaks into an independent control, required metric collection fails, isolation or access control fails, safety/security risk exceeds authority, tooling corrupts evidence, rollback becomes unavailable, or comparison integrity is materially lost
- **THEN** the pilot stops or holds according to the approved rule and records escalation and resume conditions
