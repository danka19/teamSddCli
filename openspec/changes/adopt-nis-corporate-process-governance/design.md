## Context

The accepted Phase 1 baseline defines `thin` and `full` change modes, six internal lifecycle states, deterministic validation, traceability, waivers, central ownership, and human approval boundaries. The active transfer-readiness change packages that baseline for external certification and a later corporate pilot, but its role kit and reference flow still use the internal `thin-change` vocabulary and cover analyst, developer, and QA roles only.

The local, git-ignored `NIS_Clean_v1.6_Approved_Package` documents real corporate process expectations: `minor`, `major`, and `hotfix` classification; preliminary initiative triage; tech-lead control; readiness and completion expectations; regression planning; stop/escalation rules; release-package handoff; audit and role-understanding records; pilot safety; and failed-run retention. The architecture audit recorded strong alignment as well as internal NIS inconsistencies and unsafe AI-only production assumptions. The human owner subsequently decided that the NIS corporate process model is authoritative input for this project's target workflow, explicitly chose the flat NIS classification over an alternative two-axis model, and excluded the package's process-effectiveness measurement layer.

The design must therefore promote the useful corporate process into canonical OpenSpec behavior while preserving existing non-negotiable architecture: deterministic and AI-disabled gates, human-owned decisions, Git/OpenSpec source ownership, generated Confluence, no inferred corporate values, no internal package fork, and the external-release-before-corporate-pilot boundary.

Stakeholders are product/business owners, analysts, developers, QA/AT owners, tech leads, architects, security/compliance owners, release/support roles, process owners, CI/repository owners, and teams consuming the process package.

## Goals / Non-Goals

**Goals:**

- Use `minor`, `major`, and `hotfix` as the only target user-facing change classes.
- Define deterministic, auditable classification, readiness, completion, stop, escalation, and release-handoff behavior.
- Make the tech lead a first-class role with bounded authority and deterministic decision support.
- Preserve the accepted six-state OpenSpec lifecycle while attaching explicit business gates to its transitions.
- Distinguish archive completion from tracker delivery completion.
- Adopt the useful NIS business processes, role checks, evidence records, regression/release controls, pilot safety, and failed-run retention.
- Normalize NIS inconsistencies into single canonical contracts and generated/derived role views.
- Migrate current templates, validators, tests, role instructions, and read packs without rewriting accepted archive history.
- Complete and externally certify the reusable behavior before the real corporate pilot.

**Non-Goals:**

- Reproducing PPRB-specific staffing, cluster/direction reporting, or repository layout as universal architecture.
- Requiring AI to create every artifact, prohibiting human-authored artifacts, or prohibiting manual QA evidence.
- Making AI output an approval, waiver, lifecycle, release, or correctness authority.
- Adding deploy automation, Zephyr integration, custom Jira/Confluence clients, or real corporate credentials/configuration.
- Defining one universal Jira workflow; tracker mapping remains configuration over the canonical OpenSpec lifecycle and gates.
- Adding process-effectiveness metrics, comparison methodology, sample rules, or decision thresholds to the target workflow.

## Decisions

### 1. Adopt the flat NIS classification exactly as the target vocabulary

The canonical target enum is:

```yaml
classification: minor | major | hotfix
```

The alternative `impact: minor|major` plus `delivery: standard|hotfix` model is rejected because the human owner explicitly chose the NIS model as the best reflection of real corporate work. `thin` and `full` remain only as migration inputs and historical words; new templates, reports, prompts, docs, and user-facing diagnostics must not present them as current options.

`type` remains separate and answers what kind of work is occurring (`new_feature`, `behavior_change`, `bugfix`, `refactor`, `docs_only`, `config_ops`). `classification` selects the governed process route. `status` records lifecycle state. Quality/risk fields record why the route and evidence matrix apply.

### 2. Make classification deterministic and conservative

Minor is allowed only when every minor condition is satisfied: the change is local and small, rollback is simple, and there is no user-scenario, SLA, security/compliance, external-integration, data-model, component-interaction, public-API, cross-repository, reliability, performance, operations, governed-test, or governed-documentation impact and no architecture decision requirement.

Major is required when any major trigger is present: new feature; changed business logic, user scenario, component interaction, required test behavior, or governed user/operational documentation; public API/integration/data/security/compliance/SLA impact; external dependency; cross-repository work; significant reliability/performance/operations impact; regression risk; high rollback cost; or required architecture decision.

Hotfix is used only when delay increases production or pre-production harm and the work needs an accelerated route. Hotfix is not a low-evidence route. It has a mandatory minimum safety, regression, rollback/hold, decision, and traceability set. Risk-triggered major artifacts remain required unless a specifically permitted non-safety artifact is deferred by a valid waiver with follow-up/expiry. Security/compliance review, human approval, minimum test evidence, rollback/hold evidence, and post-hotfix reconciliation cannot be waived by classification alone.

The classifier emits the selected class, triggered rules, source fields, blockers, and required human approvals. A major trigger cannot be overridden to minor per change. If source evidence is wrong, an authorized human corrects it with an audit record and the classifier runs again; uncertainty may select a stricter route. Weakening a canonical trigger requires a separately reviewed and accepted versioned policy/OpenSpec change. AI may recommend but cannot select or approve the final class.

### 3. Use schema version 2 and a bounded compatibility migration

Target metadata begins with:

```yaml
schema_version: 2
classification: minor
type: behavior_change
status: draft
```

The migration maps `mode: thin` to `classification: minor` and `mode: full` to `classification: major`. Existing `type`, status, quality, systems, review, publication, traceability, and waiver data are preserved. No legacy value maps to hotfix automatically.

For one explicitly documented compatibility window, readers may normalize legacy packages in memory and emit a deprecation diagnostic. Writers produce only schema version 2. A deterministic check/apply migration command produces a machine-readable plan before mutation, is idempotent, and refuses ambiguous or already divergent metadata. Archived accepted history is not rewritten. Rollback restores the previous process-package/config pin; it does not reverse canonical history already accepted under a later version.

### 4. Preserve the six lifecycle states and attach named business gates

The lifecycle remains:

```text
draft -> spec_review -> approved -> in_implementation -> ready_to_archive -> archived
```

Named gates provide corporate meaning without duplicating status ownership:

- `draft -> spec_review`: review-ready gate;
- `spec_review -> approved`: Definition of Ready / ready-for-implementation gate;
- `approved -> in_implementation`: recorded implementation start;
- `in_implementation -> ready_to_archive`: Definition of Done plus required release/transfer evidence;
- `ready_to_archive -> archived`: final deterministic checks and explicit human archive approval.

A tracker may expose additional business states, but mappings are derived configuration. `archived` means canonical change/spec reconciliation, not necessarily deployed to production, accepted by a customer, or closed in Jira.

### 5. Define one common DoR plus class-specific evidence

Common Definition of Ready requires business goal/value, owner, scope/out-of-scope, type/class/rationale, affected systems and owners, dependencies, requirements, scenarios, acceptance criteria, quality strategy, verification approach, security/data/operations assessment, rollback/hold approach, initial traceability, resolved blocker questions, valid waivers, and required human approvals.

Minor uses the minimum reviewable evidence already proven by the project. Major adds expanded design, impact/risk analysis, architecture decision or explicit not-required evidence, QA/test/automation planning or valid waivers, owner-zone approvals, dependency/migration/rollback evidence, and release-package expectations. Hotfix uses a mandatory accelerated-entry record, harm/urgency rationale, bounded scope, minimum safety/regression set, immediate rollback/hold, named decision owner, known gaps, and mandatory reconciliation follow-up.

### 6. Separate implementation complete, Definition of Done, release readiness, archive, and delivered

The process must not use one ambiguous “done” flag.

- Implementation complete: code/config and required tests exist, required checks ran, and implementation evidence is linked.
- Definition of Done: acceptance evidence, defects, docs, traceability, review dispositions, waivers, and class-specific obligations are complete.
- Release/transfer ready: when applicable, release notes, artifact/tag, deployment/support instructions, rollback, operational checks, limitations, and responsible roles are complete.
- Archive ready: all canonical evidence is resolved and final archive approval can be requested.
- Archived: Delta Spec/history is reconciled into Master Spec under human approval.
- Delivered/production done: external tracker/deployment state mapped from real corporate workflow; not inferred from archive alone.

### 7. Make tech-lead governance human-owned and automation-supported

The tech lead confirms classification, prevents under-classification, owns technical readiness, makes or coordinates architecture decisions, verifies owner/reviewer coverage, controls technical stop/resume, approves design/risk exceptions within role authority, confirms engineering completion, and prepares a release-readiness recommendation.

Deterministic support produces:

- classification report and triggered rules;
- readiness report with blocking/non-blocking gaps;
- bounded tech-lead review pack;
- affected owner/repository/dependency map;
- scope-drift and missing-context findings;
- stop/hold/escalation recommendation;
- completion and release-readiness report;
- follow-up/expiry view for hotfix and waivers;
- role inbox/read model after task/status sources are available.

AI may draft questions, risk analysis, architecture options, and summaries. It cannot confirm class, mark DoR/DoD green, approve waivers, resume a held change, accept release readiness, or mutate canonical state without the required deterministic and human evidence.

### 8. Adopt NIS corporate flow controls as structured records

The process adds or plans typed records/views for:

- preliminary initiative triage and readiness for team discussion;
- fixed input/baseline and recorded scope changes;
- quality strategy approved before implementation;
- regression matrix linking product/module/scenario/class to checks, data, and environment;
- human decision log and AI execution/certification evidence;
- stop, hold, escalation, resume, and deviation records;
- release-package handoff;
- role-understanding checks and role walkthrough evidence;
- portfolio WIP and pilot/project-selection evidence;
- pilot safety, rollback/hold, and failed-run evidence.

Exact storage paths are implemented inside the versioned process package after schema design. Derived Markdown guides and Confluence views reference or render these canonical records; they do not maintain separate rules.

### 9. Preserve failed-run evidence without creating a measurement layer

Failed validation, AI, adapter, integration, and workflow attempts remain in source-linked execution evidence even when a later retry succeeds. Retention protects traceability and incident diagnosis; it is not a productivity or effectiveness metric.

The target process does not define effectiveness metrics, comparison cohorts, comparison-integrity or contamination records, missing-measurement-data treatment, sample gates, or outcome thresholds. Operational correctness remains governed by DoR, DoD, required verification, stop/hold, release, rollback, reconciliation, and human decisions.

### 10. Preserve safe AI and corporate-transfer boundaries

The NIS prohibition on manual artifacts/testing is rejected. Production workflow always has templates, deterministic commands, human-authored artifacts, and manual verification/waiver paths where allowed. QA ownership remains part of the governed quality strategy; the target process does not create a separate comparison-assurance role.

No package may claim zero production risk. Pilot evidence includes data/privacy, secret, access, accidental-delivery, rollback, adapter, runtime, and logging risks. Real corporate values remain configuration supplied during adaptation. Reusable findings return to the external canonical source rather than an internal fork.

### 11. Place the change before the real pilot without invalidating the package foundation

Phase 2 work item 2.1 remains ready because the versioned package/config/schema foundation is required by both active changes. This governance change becomes a sequential dependency for classification-aware thin-flow replacement, expanded role certification, release-candidate acceptance, and Phase 3 pilot entry.

The existing transfer-readiness change may continue through foundation work that does not encode `thin/full` as permanent behavior. Before the packaged reference flow, role kit, certification, manifest, and release acceptance are finalized, they must consume the accepted outcome of this change or explicitly remain blocked.

## Risks / Trade-offs

- [Flat hotfix classification can hide impact severity] -> Require major-trigger evaluation inside the hotfix route, mandatory minimum safety/rollback/release-reconciliation evidence, restricted deferrals, and explicit residual-risk approval.
- [Breaking vocabulary change disrupts current validators and tests] -> Use schema version 2, deterministic check/apply migration, compatibility diagnostics, idempotency tests, and no archive rewriting.
- [The change is broad and can delay the transfer-ready release] -> Keep package/config foundation independent, split implementation into reviewable work items, and block only the reference flow/role/certification gates that depend on new behavior.
- [DoR/DoD becomes bureaucratic] -> Use class-specific matrices; minor remains small, major expands by risk, and hotfix accelerates sequence while preserving minimum evidence.
- [Role guides duplicate rules] -> Generate or validate from canonical specs and include source metadata/IDs.
- [AI-generated classification or review appears authoritative] -> Deterministic reports label proposals and require named human decisions before state mutation.
- [Corporate processes vary by project] -> Keep canonical minimums in OpenSpec and configurable mappings in validated process config; do not infer real values externally.
- [NIS source documents disagree] -> Treat this change as the normalized canonical contract; future NIS-derived views are generated from it rather than copied.
- [Hotfix follow-up is forgotten] -> Block final archive/closure when mandatory reconciliation evidence or follow-up disposition remains pending.

## Migration Plan

1. Accept this proposal and its delta specs before changing accepted behavior.
2. Complete the Phase 2 package/config/schema foundation that provides versioned homes for the new contracts.
3. Add schema version 2 and deterministic legacy classification discovery.
4. Add migration check/apply behavior with `thin -> minor`, `full -> major`, no automatic hotfix mapping, idempotency, JSON evidence, and rollback/hold instructions.
5. Replace templates, validator matrices, diagnostics, tests, examples, role guides, read packs, and certification fixtures with `minor|major|hotfix` behavior.
6. Add readiness/completion, tech-lead, flow-control, release-package, pilot-safety, and failed-run-evidence schemas plus deterministic validators.
7. Extend AI-disabled and Qwen/DeepSeek certification to minor, major, hotfix, and tech-lead negative/authority cases.
8. Rehearse migration and rollback on synthetic legacy/current packages without rewriting archived specs.
9. Update release manifest, transfer runbook, corporate adaptation checklist, and pilot template.
10. Stop for external release-candidate human acceptance before Phase 3.
11. In Phase 3, map real Jira statuses, owners, systems, and integration evidence through validated corporate configuration and run one monitored real change.
12. Route reusable pilot findings through new external OpenSpec changes; never maintain an internal behavior fork.

## Open Questions

No product-architecture question blocks proposal readiness. Exact real Jira state names, corporate SLA values, selected pilot project, model/runtime identifiers, Nexus/integration availability, evidence-retention periods, and security approvers are mandatory corporate adaptation inputs and must remain configurable rather than guessed externally.
