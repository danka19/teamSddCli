## Why

The accepted SDD baseline uses internal `thin` / `full` terminology and does not yet encode several real corporate delivery controls documented by the approved NIS v1.6 reference package: `minor` / `major` / `hotfix` classification, readiness and completion gates, tech-lead governance, stop/escalation rules, regression and release-package expectations, and outcome-based process measurement. The human owner has decided that these corporate processes must become first-class project behavior before the real corporate pilot rather than remain research input.

## What Changes

- **BREAKING** Replace the target `thin` / `full` change-mode vocabulary with the NIS-aligned flat classification `minor` / `major` / `hotfix`; provide a reviewed compatibility migration from legacy `thin -> minor` and `full -> major` rather than maintaining two permanent user-facing vocabularies.
- Define deterministic classification criteria, mandatory triggers, classification evidence, under-classification rejection, human confirmation, source-evidence correction, and stricter-route selection; forbid per-change lower-class overrides.
- Define business-process gates for intake, Spec Review, Definition of Ready, implementation, verification, Definition of Done, release/transfer readiness, and archive/closure without conflating OpenSpec archive state with Jira delivery state.
- Define `minor`, `major`, and accelerated `hotfix` artifact/evidence matrices. Hotfix shortens sequence and waiting, but cannot bypass human ownership, minimum safety evidence, rollback/hold behavior, or mandatory follow-up for deferred artifacts.
- Add tech lead as a first-class governed role with deterministic classification, readiness, risk/design, stop/resume, completion, and release-readiness support. AI may prepare evidence and options but cannot approve on the tech lead's behalf.
- Adopt NIS-derived preliminary initiative triage, scope-change control, automatic regression-matrix planning, stop/escalation criteria, release-package handoff, role-understanding checks, human decision logs, AI execution evidence, controlled/external wait-time separation, and portfolio/pilot measurement boundaries.
- Define outcome metrics and a controlled-pilot evidence contract separately from transition gates: cycle time, human effort, cost, first-pass acceptance, defects, engineering-package completeness, manual intervention, repeatability, waiting/hand-off time, and post-pilot delivery stability.
- Correct NIS package ambiguities before adoption: one canonical rule source, normalized thresholds and sample gates, explicit control definition, privacy/retention boundaries, no absolute “zero production risk” claim, and no AI-only or no-manual-testing production dependency.
- Require all role guides, checklists, dashboards, scorecards, and generated views to reference canonical OpenSpec requirements instead of becoming duplicate normative sources.
- Place this change after the transfer-package/configuration foundation and before the real Phase 3 pilot acceptance path; do not infer corporate values or implement production integrations externally.

## Capabilities

### New Capabilities

- `corporate-change-classification`: Defines the canonical `minor`, `major`, and `hotfix` classes, classification evidence, escalation triggers, under-classification rejection, human confirmation/correction, and the prohibition on per-change lower-class overrides.
- `readiness-completion-gates`: Defines Definition of Ready, implementation-complete, Definition of Done, release/transfer readiness, archive readiness, and the distinction from tracker-level delivered/done state.
- `tech-lead-workflow`: Defines tech-lead responsibilities, authority limits, deterministic decision-support outputs, stop/resume behavior, review inputs, and AI advisory boundaries.
- `corporate-flow-controls`: Defines preliminary initiative triage, input/scope control, regression matrix, stop and escalation rules, release-package handoff, role-understanding checks, and external-contour timing boundaries.
- `process-measurement-pilot`: Defines process/outcome metric ownership, event and evidence boundaries, controlled-pilot records, data quality, privacy, comparison integrity, and post-pilot measurement.

### Modified Capabilities

- `change-package-foundation`: Replace the target `mode: thin|full` metadata contract with versioned `minor|major|hotfix` classification and explicit compatibility behavior.
- `change-artifact-contracts`: Replace thin/full artifact rules with minor/major/hotfix evidence matrices and NIS-derived conditional corporate artifacts.
- `change-lifecycle`: Add explicit readiness/completion transition gates and prevent archive state from being treated as tracker delivery completion.
- `traceability-contract`: Extend archive evidence to classification, readiness, completion, release-package, decision, and follow-up links.
- `waiver-policy`: Forbid classification-criterion waivers and define restricted hotfix deferrals without allowing safety, approval, scenario, release-package reconciliation, or follow-up bypasses.
- `repo-topology-config`: Extend owner/config contracts for tech-lead authority, classification policy, readiness/completion policy, regression ownership, and corporate workflow mapping.
- `confluence-feedback-loop`: Replace the legacy thin-MVP reference with class-aware generated-publication boundaries while keeping Confluence non-canonical and non-blocking until implemented.

## Impact

- Affects accepted OpenSpec behavior and therefore requires human acceptance before promotion into `openspec/specs/`.
- Affects `change.yaml`, process-package schemas, validator behavior, templates, compatibility/migration checks, role instructions, read-pack/evidence contracts, certification fixtures, pilot templates, and tests.
- Adds the tech-lead role to the transfer-ready operating kit and certification scope after the foundational package paths and schemas exist.
- Requires roadmap and Phase 2 planning updates so the new corporate-governance change is completed and externally certified before the Phase 3 real pilot.
- Preserves deterministic and AI-disabled gates, human approvals, OpenSpec/Git source ownership, generated Confluence boundaries, and the no-internal-fork transfer rule.
- Does not add custom Jira/Confluence clients, deploy automation, Zephyr integration, or real corporate configuration to the external repository.
