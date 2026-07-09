# Phase 1. Discovery And Requirements

Status: in progress.

## Goal

Turn the architecture and accepted delivery strategy into executable requirements for the first thin SDD flow: proposed OpenSpec specs, decision gates, artifact contracts, validation scenarios, and deterministic template/script updates that do not depend on the AI layer.

## Inputs To Read

- `AGENTS.md`
- `docs/README.md`
- `docs/00_FILE_STRUCTURE.md`
- `docs/ROADMAP.md`
- `docs/IMPLEMENTATION_STRATEGY.md`
- `docs/CURRENT_PROJECT_AUDIT.md`
- `docs/AI_STEP_VERIFICATION_CHECKLIST.md`
- `openspec/` when `sdd CLI` behavior, workflow requirements, proposed changes, artifact contracts, or acceptance criteria are involved
- `docs/CONTEXT.md`

## OpenSpec And Acceptance Mapping

- Affected accepted requirements:
  - None yet; Phase 1 drafts the first proposed requirement set and must stop before promoting changes into accepted specs.
- Active proposed changes:
  - `add-change-template-validation` remains active and unarchived.
  - Planned Phase 1 proposal set:
    - `define-change-lifecycle`
    - `define-change-artifact-contracts`
    - `define-traceability-contract`
    - `define-waiver-policy`
    - `define-documentation-governance`
    - `define-repo-topology-config` (also covers the OpenSpec version pin/upgrade policy per the 2026-07-06 merge decision)
    - `define-confluence-feedback-loop`
- Acceptance scenarios:
  - A completed/current work item 1.1 has a copyable change package template, local validator, pre-commit entrypoint, focused tests, OpenSpec change evidence, and commit evidence.
  - Proposed change lifecycle requirements define status ownership, allowed transitions, Spec PR/archive gates, and the boundary between deterministic checks, human approval, and AI assistance.
  - Proposed artifact contract requirements define thin and full change package artifacts, required/optional/waived fields, and the exact point where the final artifact matrix becomes binding.
  - Proposed traceability requirements define requirement -> scenario -> task/test/change evidence links, validator expectations, and waiver behavior.
  - Proposed waiver requirements define approvers, evidence, audit trail, and negative cases where waivers are not enough.
  - Proposed documentation governance requirements define source-of-truth rules, phase-plan update rules, and acceptance evidence before docs/specs are promoted.
  - Proposed repo topology/config requirements define the first supported topology, configuration format, OpenSpec version pin/upgrade policy, process package reuse, and owner/reviewer assignment before scripts or templates assume concrete paths.
  - Proposed Confluence feedback requirements define owner, service expectation, unresolved comment handling, and accepted/rejected comment outcomes before publication automation exists.
  - Template and validator behavior is expanded only after the relevant human decision gate is approved.
  - The final Phase 1 gate stops before archiving OpenSpec changes into accepted specs.
- Verification evidence expected before completion:
  - `git show --no-patch --oneline 6fbde43` for completed work item 1.1 evidence.
  - Focused `python -m pytest tests/test_validate_change.py -v` when validator behavior changes.
  - Manual `python scripts/validate_change.py --allow-placeholders templates/change` when templates change.
  - Negative validator runs for missing artifacts, invalid artifact matrix, missing traceability, placeholder production values, and invalid/unsupported waiver data when those contracts are implemented.
  - `openspec list`, `openspec list --specs`, and `openspec validate --all --strict`.
  - `git diff --check`.
  - Worker, reviewer, architecture-checker, and verification-checker evidence recorded for each work item before moving to the next item when subagent tooling is available; if unavailable, record the local fallback and limitation.
  - Human decision records for blocking gates before work proceeds past each gate.

## Change Intake

Record new ideas, fixes, scope changes, architecture notes, artifact contract changes, integration changes, or verification requests that appear during the phase.

```text
Idea:
Source:
Type:
Decision:
Reason:
Affected specs:
Affected architecture:
Data contract impact:
Verification impact:
Status:
```

```text
Idea: Delete the stale historical architecture draft and make `docs/` plus `openspec/` the only current architecture sources.
Source: Human instruction on 2026-07-06.
Type: architecture_change, documentation_change
Decision: adopt_now
Reason: The old draft is no longer current and keeping it as a required source creates conflicting guidance; the project already stores accepted decisions and proposed contracts in durable docs and OpenSpec artifacts.
Affected specs: None directly; existing OpenSpec proposals remain the current proposed behavior contracts.
Affected architecture: Replaces the parallel historical architecture file with `docs/`, `openspec/`, and accepted human decisions as source-of-truth surfaces.
Data contract impact: None to current artifact schemas; future data contracts must be derived from accepted OpenSpec requirements.
Verification impact: Requires link/reference cleanup, strict OpenSpec validation, and repository status checks.
Status: Adopted; `sdd_final_architecture.md` removed and references updated.
```

```text
Idea: Run the remainder of Phase 1 with clean worker, reviewer, architecture-checker, and verification-checker gates; stop only for the listed human decisions before changing scope, implementing gated contracts, or archiving OpenSpec changes.
Source: Human instruction on 2026-07-03 for the clean Phase 1 planning worker.
Type: scope_refinement, verification_change, documentation_change
Decision: adopt_now
Reason: The instruction changes the active Phase 1 execution model and must be built into this plan before the main agent can safely continue; the resulting gated work items are queued in the current phase below.
Affected specs: Active change `add-change-template-validation`; planned changes `define-change-lifecycle`, `define-change-artifact-contracts`, `define-traceability-contract`, `define-waiver-policy`, `define-documentation-governance`, merged `define-repo-topology-config`, and `define-confluence-feedback-loop`.
Affected architecture: Preserves OpenSpec/Markdown-first, deterministic-gates-first, no-custom-CLI-upfront, and human-owned approval boundaries.
Data contract impact: Requires explicit human gates before finalizing artifact matrix, repo topology/config, waiver contract, Confluence feedback handling, OpenSpec version policy, and accepted specs.
Verification impact: Requires worker/reviewer/architecture/verification evidence per work item and OpenSpec validation before completion; final archive/acceptance requires a human stop.
Status: Adopted into this plan; downstream work remains queued for Phase 1 execution.
```

```text
Idea: Apply reviewer and architecture-checker fixes for Phase 1 work item 1.2: explicit lifecycle transition table, limited no-spec-change rationale, waiver/scenario coverage consistency, archive-readiness traceability, completion evidence reporting, and MVP-boundary clarification.
Source: Human instruction on 2026-07-03 for the clean fix worker after reviewer/architecture feedback.
Type: bug_fix, scope_refinement, data_contract_change, verification_change, documentation_change
Decision: adopt_now
Reason: The feedback closes contradictions and loopholes in the active proposed deltas before human decision gate 1.3; ignoring it would leave the proposal set ambiguous and hard to validate.
Affected specs: Proposed changes `define-change-lifecycle`, `define-change-artifact-contracts`, `define-traceability-contract`, `define-waiver-policy`, and `define-documentation-governance`.
Affected architecture: Preserves OpenSpec/Markdown-first, deterministic-gates-first, human-owned approval/archive, and no-custom-CLI-upfront boundaries.
Data contract impact: Clarifies allowed lifecycle transitions, archive approval, no-spec-change limits, waiver eligibility, traceability pending status, and completion evidence fields.
Verification impact: Requires `openspec validate --all --strict`, `git diff --check`, and manual checks that accepted specs and prohibited paths were not changed.
Status: Adopted for work item 1.2 reviewer fix pass; no accepted specs are created and no deterministic validator/template behavior changes are made.
```

```text
Idea: Human decision-gate questions must be rewritten in normal human-readable language with examples of impact and arguments, then recorded as a durable rule.
Source: Human instruction on 2026-07-03 after the first item 1.3 question packet.
Type: documentation_change, verification_change
Decision: adopt_now
Reason: The Phase 1 process requires human decisions; if questions are written as terse internal labels, the owner cannot safely approve tradeoffs or understand what each choice changes.
Affected specs: Proposed documentation-governance behavior; active phase decision gates.
Affected architecture: Preserves human-owned decisions by making decision packets understandable and reviewable.
Data contract impact: None to artifact schemas; affects decision-record format and acceptance evidence.
Verification impact: Future human gates must be checked for clear Russian question text, 2-3 options, recommended default, practical impact examples, tradeoffs/risks, and unresolved-decision consequences.
Status: Adopted into `AGENTS.md`, `docs/AI_STEP_VERIFICATION_CHECKLIST.md`, and this phase plan.
```

```text
Idea: Record the human's 2026-07-06 decisions approving Option A for the thin/full artifact matrix, Option A for waiver ownership/evidence, and Option A for keeping Jira, Confluence publication, QA/AT proposal generation, and role inboxes outside the first MVP while planning them as later layers.
Source: Human reply on 2026-07-06 to the Phase 1 work item 1.3 decision packet.
Type: scope_refinement, data_contract_change, documentation_change, acceptance_criterion
Decision: adopt_now
Reason: These answers close the work item 1.3 human decision gate and unblock proposal synchronization while preserving the accepted thin-MVP boundary.
Affected specs: Proposed changes `define-change-artifact-contracts`, `define-waiver-policy`, `define-change-lifecycle`, `define-traceability-contract`, `define-documentation-governance`, and planned `define-confluence-feedback-loop`.
Affected architecture: Preserves Git/OpenSpec canonical source, no-custom-CLI-upfront delivery, deterministic-gates-first, and human-owned approval boundaries; confirms Confluence/Jira/QA/AT/role inbox remain planned later layers, not first-MVP dependencies.
Data contract impact: Approves the risk-oriented thin/full artifact matrix and role-appropriate waiver fields/approvers; plans future journey/screen, publication, localization, and legacy-baseline contracts without making them first-MVP blockers.
Verification impact: OpenSpec proposal scenarios and tasks must be updated; scripts/templates/validator tests are not changed until later implementation work items.
Status: Adopted into project docs, active OpenSpec proposals, audit, and this phase plan; deterministic enforcement remains queued.
```

```text
Idea: Add generated Confluence publication/read-model, feedback disposition, canonical-language/localized-view, journey/screen, legacy-baseline, and docs-vs-OpenSpec responsibility rules from the attached summary.
Source: Human attachment on 2026-07-06.
Type: architecture_change, data_contract_change, documentation_change, workflow_behavior_rule, acceptance_criterion
Decision: queue_current_phase
Reason: The ideas are important for Phase 1 proposals and future publication/traceability/artifact contracts, but they must not expand the first MVP or require immediate validator/template changes.
Affected specs: Proposed changes `define-confluence-feedback-loop`, `define-documentation-governance`, `define-change-artifact-contracts`, `define-traceability-contract`, and `define-change-lifecycle`.
Affected architecture: Reinforces Git/OpenSpec/Markdown as canonical source, Confluence as generated publication/read model, no bidirectional sync, and no custom Jira/Confluence REST clients from the AI layer.
Data contract impact: Plans source metadata, feedback dispositions, generated view types, journey/screen metadata, legacy baseline evidence, canonical language, and docs-vs-specs routing; schemas remain future work.
Verification impact: Requires OpenSpec strict validation and docs diff checks now; no Confluence/Jira/QA/AT/template/validator tests are required until implementation work changes deterministic artifacts.
Status: Queued into current Phase 1 proposals and later work items; not implemented as first-MVP behavior.
```

```text
Idea: Adopt five orientation and scope improvements from the comparison with a similar product: project memory triad, existing-code onboarding, deterministic sync/upgrade maintenance, PDLC narrative, and explicit exclusion of deploy/Zephyr/Jira/Confluence from the first MVP.
Source: Human instruction on 2026-07-06 after reviewing the comparison with the external presentation.
Type: architecture_change, scope_refinement, documentation_change, workflow_behavior_rule
Decision: adopt_now
Reason: The five points clarify future project memory, legacy onboarding, maintenance, and stakeholder explanation without expanding the first thin MVP or requiring immediate validator/template behavior changes.
Affected specs: Proposed changes `define-documentation-governance`, `define-change-artifact-contracts`, `define-traceability-contract`, merged `define-repo-topology-config`, and future memory/onboarding contracts.
Affected architecture: Adds the project memory triad as the future orientation model; defines existing-code onboarding as `scan -> baseline -> map -> validate`; treats `sync` and `upgrade` as deterministic maintenance; frames the process as PDLC-wide shared context; preserves the first-MVP boundary.
Data contract impact: Future schemas may be needed for project map, legacy baseline, memory sync reports, and template/spec-package version metadata; no schema changes are made now.
Verification impact: Requires docs diff checks and OpenSpec strict validation now; deterministic sync/upgrade and onboarding checks remain future implementation work after the merged topology/config/version policy is approved.
Status: Adopted into project docs, audit, roadmap, context, and this phase plan; no first-MVP implementation scope added.
```

```text
Idea: Design project memory and documentation controls for weaker corporate AI models, including graph/navigation aids, concise useful docs, repeated-error memory, mandatory spec-questioning workflow, skill-use safeguards, and analyst/QA onboarding.
Source: Human questions on 2026-07-06 about graphify-like skills, documentation sufficiency, weak Qwen/DeepSeek-class models, repeated mistakes, skill forgetting, spec grilling, and role usability.
Type: architecture_change, verification_change, documentation_change, new_feature
Decision: queue_current_phase
Reason: These concerns are central to whether the process works with weaker local models and non-developer roles, but the exact solution needs a separate proposal/decision gate so it does not become unreviewed tool or documentation sprawl.
Affected specs: Proposed documentation-governance behavior, future repo topology/config, future memory/onboarding capability, and possible future skill/process contracts.
Affected architecture: Points toward deterministic navigation/indexing, concise evidence-backed memory, generated or validated project maps, reusable failure-pattern records, and a spec-questioning workflow before implementation planning.
Data contract impact: Possible future contracts for memory index, known failure records, role guides, documentation lint rules, and spec-question prompts; no data contract is accepted yet.
Verification impact: Future work should define checks for stale docs, orphaned docs, unreferenced memory entries, repeated failure recurrence, and role walkthrough evidence for QA/analyst usability.
Status: Queued for Phase 1 exploration/proposal; detailed planning input captured in `docs/planning/PROJECT_MEMORY_AND_WEAK_MODEL_GUARDRAILS.md`; not accepted as implementation scope yet.
```

```text
Idea: Add source ownership and deduplication rules so OpenSpec, docs, role guides, generated views, read packs, and project memory do not carry divergent copies of the same behavior.
Source: Human question on 2026-07-06 about preventing specs and documentation from duplicating or containing different versions of the same information.
Type: documentation_change, verification_change, architecture_change, data_contract_change
Decision: adopt_now
Reason: The process relies on Git/OpenSpec as canonical behavior truth, but weak local models and human onboarding surfaces need summaries; without explicit source ownership, those summaries can become conflicting second sources of truth.
Affected specs: Proposed change `define-documentation-governance`; future project-memory, generated-view, role-guide, and read-pack contracts.
Affected architecture: Reinforces OpenSpec as behavior/acceptance owner, `docs/` as rationale/context owner, `AGENTS.md` as agent operating-rule owner, and memory/generated views as read models.
Data contract impact: Future schemas should support source IDs, source paths, source commit or generated timestamp, canonical/supporting/advisory/evidence labels, and stale-review metadata; no deterministic schema is accepted now.
Verification impact: Requires OpenSpec strict validation and docs diff checks now; future checks should cover normative-language linting, duplicate requirement IDs, source links, generated-block edits, stale memory, and orphan docs.
Status: Adopted into documentation-governance proposal, context, planning docs, checklist, audit, and this phase plan; deterministic enforcement remains future work.
```

```text
Idea: Record the 2026-07-06 Fable 5 audit decision batch: canonical six-state lifecycle naming, error-level enforcement in work item 1.8, a canonical decision log at acceptance readiness, and merging the OpenSpec version policy into the repo topology/config proposal.
Source: Human reply on 2026-07-06 to the Fable 5 documentation/architecture review decision packet (`docs/audits/FABLE5_DOCUMENTATION_ARCHITECTURE_REVIEW_2026-07-06.md`, section 5).
Type: scope_refinement, documentation_change, acceptance_criterion
Decision: adopt_now
Reason: The answers unblock validator status-vocabulary reconciliation planning for work item 1.8, reduce the Phase 1 proposal set by one change and one human gate, and schedule decision-record consolidation at a phase boundary instead of mid-phase.
Affected specs: `define-change-lifecycle` (naming decision closes its tasks item 2.2); `define-change-artifact-contracts` and `define-waiver-policy` (error-level enforcement consequence for 1.8); planned merged `define-repo-topology-config`.
Affected architecture: No boundary changes; preserves deterministic-gates-first, human-owned approvals, and the thin-MVP boundary.
Data contract impact: Validator status vocabulary must be reconciled to the six canonical states in work item 1.8; the OpenSpec version pin location is decided inside the merged topology/config proposal.
Verification impact: Work item 1.8 negative tests must cover rejected historical statuses and error-level matrix enforcement; this documentation pass requires `openspec validate --all --strict` and `git diff --check`.
Status: Adopted into README, audit, roadmap, the lifecycle proposal, and this phase plan; `docs/DECISIONS.md` creation is deferred to work item 1.10.
```

```text
Idea: Record the 2026-07-06 adoption-readiness feedback batch: adopt Master Spec / Delta Spec team-facing terminology; make other-team reusability a topology design constraint; open the canonical-analytics-language revision question (Russian prose); require the topology proposal to define the project-repo versus team-specs content split and shared script/skill distribution; plan analytics diagram/journey/screen storage and gradual on-touch migration of existing Confluence analytics.
Source: Human reply on 2026-07-06 after the Fable 5 audit decision batch.
Type: scope_refinement, documentation_change, architecture_change, open_decision
Decision: adopt_now for terminology and the reusability constraint; queue_current_phase for the language revision, repo-split contract, diagram/asset conventions, and migration approach (they land in work items 1.4-1.7 proposals and gates).
Reason: The team-facing naming and reuse constraint clarify adoption without changing behavior contracts; the language, storage-split, diagram, and migration questions are prerequisites for real analyst adoption and must be decided at the existing gates instead of silently expanding the MVP.
Affected specs: planned merged `define-repo-topology-config`; `define-documentation-governance` (canonical-language requirement may need revision if the language decision changes); `define-change-artifact-contracts` and `define-traceability-contract` (future diagram/journey/screen storage conventions); `define-confluence-feedback-loop` (approval-readiness input the human owner is gathering).
Affected architecture: No boundary changes; Git/OpenSpec stays canonical; Confluence stays generated; the first MVP is not expanded.
Data contract impact: Future topology/config contract must cover repo content split, shared script/skill consumption, and other-team bootstrap; glossary gains Master Spec / Delta Spec terms; a strict-mode probe confirmed OpenSpec accepts Russian prose with English keywords.
Verification impact: `openspec validate --all --strict` and `git diff --check` for this documentation pass; future work items keep their existing verification lists.
Status: Terminology and reuse constraint adopted into context, README, audit, roadmap, and this plan; language/migration/diagram/split questions recorded as open decisions below and AUDIT-018.
```

```text
Idea: Record the 2026-07-06 analytics-adoption batch: Russian-prose canonical language for team product analytics specs (English keywords and stable IDs; process specs stay English), and the full structural analysis of the corporate analytics approval template with a migration plan mapping its sections to SDD artifacts as typed YAML records instead of nested tables.
Source: Human decision and template photos provided on 2026-07-06; photos reviewed in full from the git-ignored local folder `arch-screenshots/analytic-template/` (moved from the earlier local `analytic-template/` location).
Type: data_contract_change, documentation_change, scope_refinement, open_decision
Decision: adopt_now for the language decision; queue_current_phase for the typed-artifact contracts (status model, channel support, platform services, data model), which land through work items 1.4/1.9 without expanding the thin MVP.
Reason: Analysts must be able to read and approve canonical sources directly without an AI layer, and the corporate template's nested tables must become deterministic, weak-model-safe form artifacts before a pilot can convert real analytics.
Affected specs: `define-documentation-governance` (canonical-language requirement revised); planned `define-repo-topology-config` (analytics source/asset placement); `define-change-artifact-contracts` (future conditional typed artifacts); `define-confluence-feedback-loop` (approval-view requirements use the 2026-07-09 minimal validator-backed default until a later full-package contract).
Affected architecture: Git/OpenSpec stays canonical; generated Confluence renders typed records back into the approver-familiar nested layout; no MVP expansion.
Data contract impact: Future YAML schemas for status-model, channel-support, platform-services, and data-model records; red mandatory-callout rules from the template become validator/checklist candidates.
Verification impact: A strict-mode OpenSpec probe confirmed Russian prose validates; `openspec validate --all --strict` and `git diff --check` for this documentation pass; future schemas require their own validator tests in 1.8/1.9.
Status: Language decision recorded across docs and the governance proposal; template analysis recorded in `docs/planning/ANALYTIC_TEMPLATE_STRUCTURE_AND_MIGRATION_PLAN_2026-07-06.md`; `arch-screenshots/` and `outputs/` are git-ignored so local corporate photos/screenshots are not committed.
```

```text
Idea: Use local screenshots of an internal OpenSpec customization / repository-topology approach as input to work item 1.4, and record that corporate screenshot material now lives under `arch-screenshots/`.
Source: Human instruction on 2026-07-09; local folders `arch-screenshots/analytic-template/` and `arch-screenshots/openspec-de/`.
Type: architecture_change, documentation_change, scope_refinement
Decision: queue_current_phase
Reason: The screenshots can inform the merged repo-topology/config/OpenSpec-version proposal, but they must be evaluated before any structure is accepted or copied into the product design.
Affected specs: Planned `define-repo-topology-config`; later impact possible for `define-change-artifact-contracts`, `define-traceability-contract`, and `define-confluence-feedback-loop`.
Affected architecture: Must be compared against the current product goal: deterministic OpenSpec/Markdown-first SDD process, thin first MVP, analytics stored with OpenSpec sources, Confluence as generated publication, and no process guarantees depending on AI.
Data contract impact: No schema change yet; possible future impact on repo split, config format, shared scripts/templates/skills distribution, owner registry, generated analytics views, and asset placement.
Verification impact: Screenshot readability must be reported explicitly; if text or structure is unclear, the human owner must clarify or provide new photos before recommendations are treated as evidence.
Status: Screenshot analysis completed on 2026-07-09 (25 photos; key process, template, topology, and master-spec content legible; some tail sections not fully visible). Findings, criteria assessment, and borrow/differ recommendations are recorded in `docs/planning/OPENSPEC_DE_INTERNAL_SOLUTION_ANALYSIS_2026-07-09.md` and `docs/planning/REPO_TOPOLOGY_EVALUATION_CRITERIA_2026-07-09.md`; reviewer and architecture-checker gates agree that central `team-specs` remains the recommended first topology and specs-next-to-code is a later/federated option. Proposal drafting is now routed to `openspec/changes/define-repo-topology-config/`.
```

```text
Idea: Apply the OpenSpec-DE analysis recommendations and produce a consistent work item 1.4 documentation state without duplicate normative rules.
Source: Human instruction on 2026-07-09 after reviewing the recommendation list.
Type: data_contract_change, documentation_change, scope_refinement, verification_change
Decision: adopt_now
Reason: Work item 1.4 must now turn the analysis into a proposed OpenSpec contract and route borrowed patterns to their canonical owners before later validators/templates assume topology, config, version, or owner behavior.
Affected specs: `define-repo-topology-config`, `define-change-artifact-contracts`, `define-change-lifecycle`; planning impact for weak-model guardrails and future role skills.
Affected architecture: Preserves central `team-specs` as the recommended first topology, specs-next-to-code as a later/federated option, deterministic guarantees over AI self-review, and no first-MVP expansion.
Data contract impact: Adds proposed contracts for topology/config/version/process package/owners, Delta Spec operation vocabulary, artifact-height/task checkbox expectations, and archive history convention.
Verification impact: Requires read-only reviewer/architecture/verification gates, strict OpenSpec validation, docs diff checks, and explicit gate 1.5 human approval before enforcement.
Status: Adopted into the work item 1.4 proposal and related docs; gate 1.5 was approved on 2026-07-09.
```

```text
Idea: Close the Phase 1 gate 1.5 topology/config/OpenSpec-version decision batch using the recommended defaults.
Source: Human reply on 2026-07-09 to the gate 1.5 interview packet.
Type: architecture_change, data_contract_change, documentation_change, scope_refinement
Decision: adopt_now
Reason: Work item 1.8 must not reconcile templates and validators until the first supported topology, config shape, OpenSpec pin policy, process package reuse, and reviewer assignment source are approved.
Affected specs: Proposed change `define-repo-topology-config`.
Affected architecture: Approves central `team-specs` as the first supported topology; central team config plus optional project adapter; central OpenSpec `1.4.1` pin upgraded only through a reviewed change package; one versioned process package; and `owners.yaml` as the source for generated or validated `CODEOWNERS`.
Data contract impact: Future templates, validators, setup docs, CI checks, and role skills may assume the approved topology/config/version/owner defaults after they are encoded in the proposed contracts; no accepted specs are created in this intake step.
Verification impact: Requires OpenSpec strict validation, task checklist update for `define-repo-topology-config`, and documentation updates before work item 1.8 starts.
Status: Adopted into the Phase 1 plan, repo topology/config proposal, roadmap, audit, and task checklist; work item 1.8 is no longer blocked by gate 1.5.
```

```text
Idea: Close the Phase 1 Confluence, analytics-source, diagram/asset, weak-model, role-guide, and validator-readiness decision batch using the recommended defaults, with the existing Confluence corpus treated as read-only.
Source: Human reply on 2026-07-09 to the open-decision interview packet.
Type: architecture_change, data_contract_change, documentation_change, verification_change, scope_refinement
Decision: adopt_now
Reason: These answers remove Phase 1 ambiguity without expanding the first thin MVP; Confluence publication, project memory tooling, role guides, and asset handling remain planned contracts or later layers unless the thin flow explicitly needs them.
Affected specs: Proposed changes `define-confluence-feedback-loop`, `define-documentation-governance`, `define-repo-topology-config`, and future project-memory/asset contracts.
Affected architecture: Confluence stays generated/read-only for requirements; the existing analytics corpus is a read-only archive, not a bulk-migration source; diagrams/screens use Git-managed source or source+export with stable IDs; analyst/change owner triages Confluence feedback; blocker comments block later Confluence-enabled flows while non-blockers require explicit disposition; project memory lives with the future `team-specs` topology; first graph/navigation implementation is a deterministic lightweight index; mandatory weak-model guardrails are read packs, role skills, and evidence checklists; pilot role guides start with analyst, developer, and QA thin-change walkthroughs.
Data contract impact: Future schemas/checks may be needed for asset metadata, publication model references, feedback dispositions, memory index, read packs, and role guides; no first-MVP validator behavior is expanded by this decision except where work item 1.8 already covers approved thin/full and waiver enforcement.
Verification impact: Requires OpenSpec strict validation and documentation/audit updates now; future implementation must add validator or manual checks for generated asset source metadata, Confluence dispositions, memory index evidence, and role-guide walkthroughs when those features enter scope.
Status: Adopted into the Phase 1 plan, Confluence proposal, planning docs, audit, and roadmap; final OpenSpec archive approval remains open.
```

```text
Idea: Confirm the Confluence feedback SLA default and make the SLA editable and disableable; confirm read-only Confluence corpus handling and defer generated-view selection to the corporate environment.
Source: Human replies on 2026-07-09 after the SLA explanation.
Type: data_contract_change, documentation_change, scope_refinement
Decision: adopt_now
Reason: The feedback SLA affects later Confluence-enabled publication/archive readiness and must be configurable because real corporate workflow tooling may already own timing control; generated-view selection depends on corporate templates and approval practice that are not available in the external planning repository.
Affected specs: Proposed change `define-confluence-feedback-loop`.
Affected architecture: Preserves Confluence as generated/read-only view and keeps corporate-environment-specific publication shape out of the first thin MVP.
Data contract impact: Future team/process config needs an editable feedback SLA section with an explicit disabled state; proposed defaults are 1 working day for blocker triage and 3 working days for non-blocker triage.
Verification impact: Requires OpenSpec strict validation and documentation updates now; future implementation must test enabled, overridden, and disabled SLA behavior when Confluence tooling enters scope.
Status: Adopted into the Confluence feedback proposal, Phase 1 plan, and audit; no first-MVP implementation scope is added.
```

## Work Items

Gate rule:

- For every work item below, the listed worker/reviewer/architecture-checker/verification-checker roles are required decision gates when subagent tooling is available, even when the section label says "Recommended subagents".
- A work item is not complete until gate findings are resolved or explicitly recorded as non-blocking with rationale.
- Each human decision packet must be written in plain human-readable Russian, not as terse internal protocol labels, and must include 2-3 practical options, a recommended default, concrete examples of day-to-day impact, tradeoffs, risks, and the consequence of leaving the decision unresolved.

### 1.1 Change Package Template And Local Validation Gate

Status: completed/current evidence; do not archive or accept the active OpenSpec change yet.

Objective:

- Create the first deterministic Phase 1 artifact: `templates/change/`, `scripts/validate_change.py`, and `.pre-commit-config.yaml`.
- Preserve the current evidence that commit `6fbde43 Add phase 1 change template validation gate` exists on branch `phase-1/change-template-validation`.

Expected files/modules:

- `openspec/changes/add-change-template-validation/`
- `templates/change/`
- `scripts/validate_change.py`
- `tests/test_validate_change.py`
- `.pre-commit-config.yaml`
- `docs/00_FILE_STRUCTURE.md`
- `docs/ROADMAP.md`
- `docs/CURRENT_PROJECT_AUDIT.md`

Verification:

- `git show --no-patch --oneline 6fbde43`
- `python -m pytest tests/test_validate_change.py -v`
- `python scripts/validate_change.py --allow-placeholders templates/change`
- `openspec list`
- `openspec list --specs`
- `openspec validate --all --strict`
- `git diff --check`

Documentation updates:

- Update the repository map for new OpenSpec, templates, scripts, tests, and pre-commit paths.
- Update the roadmap to record Phase 1 as started.
- Update the audit to record OpenSpec initialization and the deterministic validation gate.
- Keep the active OpenSpec change listed as active; do not mark it archived or accepted in this work item.

Recommended subagents:

- worker: implement the bounded template and validator change.
- reviewer: inspect validation gaps, false positives, and missing tests.
- architecture-checker: verify the deterministic layer stays independent from AI.
- verification-checker: verify command evidence and final report completeness.

Exit criteria:

- The template is copyable and structurally valid in placeholder mode.
- The validator rejects incomplete real change packages.
- The pre-commit hook points to the same validator without validating plain project OpenSpec changes as SDD packages.
- The OpenSpec change validates strictly.
- Commit `6fbde43` is available as work item 1.1 evidence.
- The OpenSpec change remains active until a later human archive gate.

OpenSpec and acceptance evidence:

- `add-change-template-validation` / `change-package-foundation`.
- Commit evidence: `6fbde43 Add phase 1 change template validation gate`.

### 1.2 Draft Core OpenSpec Proposal Set For Lifecycle, Artifacts, Traceability, Waivers, And Documentation Governance

Status: drafted in this branch; reviewer, architecture-checker, and verification-checker gates passed after fix review; human decision gate 1.3 completed on 2026-07-06.

Objective:

- Draft proposed OpenSpec changes for the core Phase 1 behavior contract before adding more deterministic enforcement.
- Cover change lifecycle, artifact contracts, traceability, waiver behavior, and documentation governance as separate capabilities or clearly separated spec sections.

Expected files/modules:

- `openspec/changes/define-change-lifecycle/`
- `openspec/changes/define-change-artifact-contracts/`
- `openspec/changes/define-traceability-contract/`
- `openspec/changes/define-waiver-policy/`
- `openspec/changes/define-documentation-governance/`
- `docs/phases/PHASE_1_DISCOVERY_AND_REQUIREMENTS.md`
- `docs/00_FILE_STRUCTURE.md`
- `docs/CURRENT_PROJECT_AUDIT.md` if new risks are discovered
- `docs/CONTEXT.md` only if glossary terms change

Verification:

- `openspec list`
- `openspec list --specs`
- `openspec validate --all --strict`
- `git diff --check`
- Manual review that no proposed requirement is promoted into `openspec/specs/`.

Documentation updates:

- Update this phase plan with proposal status and any new decision blockers.
- Update the repository map when new OpenSpec change folders are added.
- Update audit only when a risk is fixed, invalidated, or newly discovered.
- Update context only for new canonical terms or boundary rules.

Recommended subagents:

- worker: draft the proposal, design, tasks, and spec deltas.
- reviewer: check whether requirements are testable and avoid over-heavy full-package defaults.
- architecture-checker: verify deterministic layer, human approval, and no-custom-CLI-upfront boundaries.
- verification-checker: verify OpenSpec validation and final evidence.

Exit criteria:

- Each proposed change has a proposal, design where needed, tasks, and spec delta scenarios.
- Proposed requirements distinguish deterministic gates from AI assistance.
- Documentation governance scenarios explicitly cover documentation update discipline, AI verification checklist evidence, and TDD-style verification rules.
- Worker, reviewer, architecture-checker, and verification-checker gate evidence for this work item is recorded before moving to work item 1.3.
- The proposals explicitly reference work item 1.1 as implementation evidence where relevant.
- The active change `add-change-template-validation` is not archived or accepted.

OpenSpec and acceptance evidence:

- Draft scenarios cover lifecycle transitions, artifact matrix behavior, traceability links, waiver approvals/evidence, and documentation governance checks.
- Documentation-governance draft covers the rule that documentation governance and TDD-style verification rules belong in the accepted documentation-governance spec once approved.
- Acceptance remains proposed until the final human archive gate.
- Draft proposal folders created:
  - `define-change-lifecycle`
  - `define-change-artifact-contracts`
  - `define-traceability-contract`
  - `define-waiver-policy`
  - `define-documentation-governance`
- Work item 1.1 implementation evidence referenced where relevant: commit `6fbde43 Add phase 1 change template validation gate`.
- Decision blockers carried into work item 1.3 and completed on 2026-07-06:
  - final thin vs full artifact matrix: approved Option A risk-oriented matrix;
  - waiver approver model and minimum evidence: approved Option A role-appropriate approvers and evidence;
  - MVP boundary: approved Option A keeping Jira task automation, Confluence publication, QA/AT proposal generation, and role inboxes outside the first MVP while planning them as later layers.
- Gate evidence: worker draft, reviewer, architecture-checker, verification-checker, fix worker, and re-review gates completed in the current Codex run before committing item 1.2.

### 1.3 Human Decision Gate: Artifact Matrix, Waivers, And MVP Boundary

Status: completed; human approved the recommended defaults on 2026-07-06.

Objective:

- Stop for human approval before making the artifact matrix, waiver rules, or MVP exclusion boundary binding.

Expected files/modules:

- `docs/phases/PHASE_1_DISCOVERY_AND_REQUIREMENTS.md`
- OpenSpec proposal files from work item 1.2
- Optional decision notes inside relevant `design.md` files

Verification:

- Manual check that the decision packet includes the final thin vs full artifact matrix.
- Manual check that the decision packet includes waiver policy approvers and evidence.
- Manual check that the decision packet asks the human to confirm Jira and Confluence remain outside MVP.
- Manual check that the decision packet explicitly states QA/AT proposal generation and role inboxes are not 1.3 MVP alternatives because they depend on later scenario, traceability, and task-source contracts unless the human explicitly re-scopes.
- Manual check that every blocking question includes 2-3 options, a recommended default, tradeoffs, risks, and the consequence of leaving it unresolved.
- `openspec validate --all --strict`
- `git diff --check`

Documentation updates:

- Record the human decision in this phase plan and in the relevant proposal/design files.
- Update `docs/CURRENT_PROJECT_AUDIT.md` only if the decision closes or creates a risk.

Recommended subagents:

- worker: prepare the decision packet and recommended defaults.
- reviewer: identify ambiguity, missing negative cases, and process-burden risks.
- architecture-checker: verify the decision keeps Phase 1 aligned with the accepted implementation strategy.
- verification-checker: confirm no implementation work proceeds before the gate is approved.

Exit criteria:

- Human explicitly approves or revises:
  - final thin vs full artifact matrix;
  - waiver policy approvers/evidence;
  - confirming Jira/Confluence/QA/AT/role inbox remain outside MVP.
- If the human does not approve, downstream implementation work waits or the plan is revised through change intake.

Human decision record:

- Artifact matrix: approved Option A, the risk-oriented matrix. Thin behavior-changing SDD changes require intent/proposal, OpenSpec delta, scenario coverage, basic traceability, and verification evidence. Full packages are required for new features, public API, mobile, cross-repo, data/security, high-risk, high-rollback-cost, or broad behavior changes. A limited no-spec-change rationale is allowed only for docs-only, refactor, or no-behavior-change maintenance with human reviewer approval and replacement evidence.
- Waiver policy: approved Option A, role-appropriate approvers and evidence. QA owners approve test evidence gaps, AT owners approve automation gaps, tech leads approve design/risk exceptions, and analyst/product owners approve scope or documentation exceptions. Required evidence includes reason, affected requirement/scenario, approver, substitute evidence, and follow-up/expiry when residual risk remains.
- MVP boundary: approved Option A. Jira task automation, Confluence publication, QA/AT proposal generation, and role inboxes remain outside the first MVP and are planned as later layers.

OpenSpec and acceptance evidence:

- Approved decision text is reflected in proposed OpenSpec deltas before validator/template implementation begins.
- If rejected or revised, the rejection/revision is recorded as durable phase evidence.

### 1.4 Draft Repo Topology, Config Format, And OpenSpec Version Policy Proposals

Status: drafted in this branch as `openspec/changes/define-repo-topology-config/`; docs synchronized; reviewer gate completed; architecture and verification gates remain part of final work-item evidence.

Objective:

- Draft requirements for the first supported repository topology/config format and the OpenSpec version pin/upgrade policy as one merged platform-assumptions proposal (2026-07-06 merge decision).

Expected files/modules:

- `openspec/changes/define-repo-topology-config/` (single merged proposal; a separate `define-openspec-version-policy` change is no longer planned)
- `docs/planning/OPENSPEC_DE_INTERNAL_SOLUTION_ANALYSIS_2026-07-09.md` as screenshot-review input
- `docs/planning/REPO_TOPOLOGY_EVALUATION_CRITERIA_2026-07-09.md` as topology-comparison criteria
- `docs/IMPLEMENTATION_STRATEGY.md` only if the accepted strategy needs clarification
- `docs/CURRENT_PROJECT_AUDIT.md` if a new environment or compatibility risk is found
- `docs/phases/PHASE_1_DISCOVERY_AND_REQUIREMENTS.md`

Verification:

- `openspec list`
- `openspec list --specs`
- `openspec validate --all --strict`
- `git diff --check`
- Manual check that examples do not treat placeholder corporate repositories, owners, Jira projects, Confluence spaces, or Jenkins jobs as real configuration.

Documentation updates:

- Update this phase plan with proposal status and decision gate status.
- Update audit if OpenSpec version, config location, or topology assumptions change known risks.
- Do not create or depend on a parallel architecture source outside `docs/` and `openspec/`.

Recommended subagents:

- worker: draft repo topology/config and OpenSpec version proposals.
- reviewer: check configuration ergonomics and upgrade failure modes.
- architecture-checker: verify the proposed topology matches OpenSpec/Markdown-first and no-custom-CLI-upfront strategy.
- verification-checker: verify OpenSpec and docs checks.

Exit criteria:

- `define-repo-topology-config` contains proposal, design, tasks, and spec delta for first supported topology, config format, OpenSpec version pin/upgrade, process package reuse, project-repo split, and owners/reviewer assignment.
- The gate 1.5 decision packet includes 2-3 practical options with a recommended default, impact examples, tradeoffs, risks, and unresolved-decision consequences.
- Placeholder corporate examples remain clearly non-authoritative.
- Screenshot-analysis input is used as evidence only; proposal text distinguishes observed screenshot facts, architecture inference, and the human-approved gate 1.5 defaults for this product.

Current analysis input and routing:

- The internal solution shows staged topology variants: one repo for a small pilot, separate requirements/code/tests repos for a team pilot, and a later scaling model with central business/solution requirements plus per-system specs near code.
- Recommended draft default remains central `team-specs` for the first supported topology, with project repos keeping code/tests and references to change/spec IDs; the canonical proposed contract is `define-repo-topology-config`.
- Borrowed artifact-height, Delta Spec vocabulary, task checkbox, and archive-history patterns are routed to `define-change-artifact-contracts` and `define-change-lifecycle`.
- Weak-model instruction patterns are routed to `docs/planning/PROJECT_MEMORY_AND_WEAK_MODEL_GUARDRAILS.md` and future role skills.
- Do not borrow AI-only gates, copied tooling in every repo, non-blocking critical verification, a mandatory rich master-spec tree for thin changes, or specs-next-to-code as the first canonical topology.

OpenSpec and acceptance evidence:

- Proposed scenarios cover supported topology discovery, unsupported topology rejection, project-repo developer/agent workflow, config discovery, version pin discovery, upgrade review evidence, process package reuse, and owners/CODEOWNERS drift.

### 1.5 Human Decision Gate: Topology, Config, And OpenSpec Version

Status: completed on 2026-07-09; the human owner approved the recommended defaults.

Objective:

- Stop for human approval before any template, validator, or future setup script assumes a repository topology, config format, or OpenSpec version policy.

Expected files/modules:

- `docs/phases/PHASE_1_DISCOVERY_AND_REQUIREMENTS.md`
- `openspec/changes/define-repo-topology-config/` (merged proposal covering topology, config format, and OpenSpec version policy)
- `docs/CURRENT_PROJECT_AUDIT.md` if risks are updated

Verification:

- Manual check that the human decision explicitly covers:
  - first supported repo topology/config format;
  - OpenSpec version pin/upgrade policy.
- Manual check that each question includes 2-3 options, a recommended default, tradeoffs, risks, and the consequence of leaving it unresolved.
- `openspec validate --all --strict`
- `git diff --check`

Documentation updates:

- Record the human decision in the relevant proposal/design files and this phase plan.
- Update audit when the decision changes environment or compatibility risk.

Recommended subagents:

- worker: prepare the decision packet and recommended defaults.
- reviewer: check operational gaps and unclear config ownership.
- architecture-checker: verify topology/config choices preserve Git/OpenSpec as canonical source.
- verification-checker: confirm the gate is approved before downstream implementation.

Exit criteria:

- Human explicitly approves or revises the first supported repo topology/config format.
- Human explicitly approves or revises the OpenSpec version pin/upgrade policy.
- Downstream work item 1.8 is unblocked by this gate.

OpenSpec and acceptance evidence:

- Approved decisions are incorporated into the proposed OpenSpec deltas.
- If these decisions are later revised, work item 1.8 must reconcile the validator/template assumptions with the revised decision before implementation continues.

### 1.6 Draft Confluence Feedback Loop Proposal

Status: drafted in this branch as part of the 2026-07-06 docs/proposal synchronization pass; human decision gate 1.7 completed on 2026-07-09 for owner/disposition/unresolved-comment behavior.

Objective:

- Draft the proposed Confluence feedback loop contract before any publication, preview, or comment-handling automation is implemented.

Expected files/modules:

- `openspec/changes/define-confluence-feedback-loop/`
- `docs/phases/PHASE_1_DISCOVERY_AND_REQUIREMENTS.md`
- `docs/CONTEXT.md` only if generated-page or feedback terms change
- `docs/CURRENT_PROJECT_AUDIT.md` if unresolved feedback creates a new process risk

Verification:

- `openspec list`
- `openspec list --specs`
- `openspec validate --all --strict`
- `git diff --check`
- Manual check that the proposal does not implement Confluence publication or custom REST integration.

Documentation updates:

- Update this phase plan with proposal status.
- Update context only for new canonical terms.
- Update audit if an unresolved-feedback risk is newly identified or resolved.

Recommended subagents:

- worker: draft feedback-loop proposal, design, tasks, and scenarios.
- reviewer: check unresolved-comment and accepted/rejected-comment edge cases.
- architecture-checker: verify one-way Git -> Confluence source-of-truth boundaries and MCP-only AI access.
- verification-checker: verify OpenSpec and documentation checks.

Exit criteria:

- Draft proposal defines generated-page ownership, feedback intake, accepted/rejected comment outcomes, unresolved comment behavior, and publication blockers.
- Draft proposal includes the approved feedback-owner/SLA/unresolved-comment defaults, including editable/disableable triage SLA values.
- Draft explicitly keeps Confluence as generated view, not source of truth.
- No publication automation is added in this work item.

Current draft notes:

- `define-confluence-feedback-loop` covers Confluence as generated read/publication model, generated page source metadata, source warnings, accepted/rejected/deferred/duplicate comment dispositions, editable/disableable triage SLA defaults, unresolved blocker behavior, and evidence-backed approval/testing status display.
- The proposal intentionally includes generated publication model basics rather than creating a separate accepted MasterSpec source.
- The existing Confluence analytics corpus is a read-only archive for the first pilot; accepted diagrams, journey schemes, and screen assets use Git-managed source or source+export with stable IDs, while Confluence drawings are draft/feedback artifacts until exported or recreated into that flow.
- Publication automation, preview publishing, comment synchronization, and generated gallery implementation remain outside the first MVP.

OpenSpec and acceptance evidence:

- Proposed scenarios cover comment accepted into Git/OpenSpec, comment rejected with reason, unresolved comment blocking/non-blocking behavior, and generated-page source warnings.

### 1.7 Human Decision Gate: Confluence Feedback Owner, SLA, And Unresolved Comments

Status: completed on 2026-07-09; the human owner approved the recommended defaults.

Objective:

- Stop for human approval before Confluence feedback handling becomes a binding contract or implementation target.

Expected files/modules:

- `docs/phases/PHASE_1_DISCOVERY_AND_REQUIREMENTS.md`
- `openspec/changes/define-confluence-feedback-loop/`
- `docs/CURRENT_PROJECT_AUDIT.md` if risks are updated

Verification:

- Manual check that the human decision explicitly covers Confluence feedback loop owner/SLA/unresolved comments.
- Manual check that accepted/rejected comment outcomes are recorded in the proposal.
- Manual check that each question includes 2-3 options, a recommended default, tradeoffs, risks, and the consequence of leaving it unresolved.
- `openspec validate --all --strict`
- `git diff --check`

Documentation updates:

- Record the human decision in the feedback-loop proposal/design and this phase plan.
- Update audit if unresolved-feedback handling changes a known risk.

Recommended subagents:

- worker: prepare decision packet and recommended defaults.
- reviewer: check business/analyst workflow ambiguity and stale-comment risks.
- architecture-checker: verify no bidirectional synchronization is introduced.
- verification-checker: confirm no implementation proceeds before approval.

Exit criteria:

- Human explicitly approves or revises the owner, SLA/service expectation, unresolved-comment handling, and accepted/rejected comment outcomes.
- If these decisions are later revised, Confluence-related implementation must reconcile the generated publication and feedback contracts before implementation continues.

OpenSpec and acceptance evidence:

- Approved decisions are reflected in the proposed Confluence feedback scenarios.
- Rejected alternatives are recorded as proposal rationale or phase-plan notes.

### 1.8 Expand Templates And Validator After Approved Decision Gates

Status: completed on 2026-07-09 in a separate implementation step; validator, tests, and template were reconciled to the approved Phase 1 contracts while all OpenSpec changes remained proposed.

Objective:

- Expand `templates/change/` and `scripts/validate_change.py` only after the relevant human decision gates approve the artifact matrix, waiver behavior, topology/config assumptions, and OpenSpec version policy.

Expected files/modules:

- `templates/change/`
- `scripts/validate_change.py`
- `tests/test_validate_change.py`
- `.pre-commit-config.yaml` only if hook invocation needs to change
- Relevant OpenSpec proposal files from work items 1.2, 1.4, and 1.6
- `docs/00_FILE_STRUCTURE.md` if files or folders are added, removed, or repurposed
- `docs/CURRENT_PROJECT_AUDIT.md` if verification evidence or risks change
- `docs/phases/PHASE_1_DISCOVERY_AND_REQUIREMENTS.md`

Verification:

- `python -m pytest tests/test_validate_change.py -v`
- `python scripts/validate_change.py --allow-placeholders templates/change`
- Negative validator checks for missing/invalid artifacts, missing traceability, placeholder production values, unsupported modes, and invalid waiver data covered by tests or manual commands.
- `openspec list`
- `openspec list --specs`
- `openspec validate --all --strict`
- `git diff --check`

Documentation updates:

- Update repository map for any new deterministic artifact paths.
- Update audit with fresh validator/test evidence.
- Update this phase plan with completed evidence and remaining gates.
- Do not archive proposed OpenSpec changes.

Recommended subagents:

- worker: implement bounded template and validator changes.
- reviewer: inspect false positives, false negatives, regression risk, and missing tests.
- architecture-checker: verify deterministic behavior does not depend on AI, MCP, Jira, Confluence, QA/AT automation, or role inboxes.
- verification-checker: rerun evidence commands and inspect final report completeness.

Exit criteria:

- Approved artifact matrix and waiver rules are enforced as errors per the 2026-07-06 enforcement decision; no warnings-only staging period is used.
- Template placeholder mode still works.
- Real package validation rejects invalid production packages.
- Pre-commit behavior still discovers only real SDD change packages.
- OpenSpec proposals validate strictly and remain proposed.

OpenSpec and acceptance evidence:

- Tests and scenarios map back to the approved proposed requirements for artifact contracts, traceability, waivers, topology/config, and version policy.
- Any behavior not implemented yet has a recorded reason, follow-up item, or waiver.
- Implementation evidence recorded on 2026-07-09:
  - `python -m pytest tests/test_validate_change.py -v` passed 29 tests after the work item 1.8 review-finding fixes, including thin/full artifact rules, canonical statuses, placeholder-mode enum enforcement, no-spec-change handling, waiver validation, waiver-to-traceability matching, risky thin-package trigger rejection, staged discovery, and placeholder mode.
  - `python scripts/validate_change.py --allow-placeholders templates/change` passed.
  - `python scripts/validate_change.py templates/change` failed as expected on placeholder production values.
  - `openspec list`, `openspec list --specs`, and `openspec validate --all --strict` remained green, so the proposals stayed proposed and valid.

### 1.9 Traceability And Artifact Contract Scenario/Test Hardening

Objective:

- Add or refine traceability and artifact contract scenarios plus validator tests so Phase 1 evidence can support the later archive/acceptance decision.

Expected files/modules:

- Relevant OpenSpec proposal spec deltas from work items 1.2, 1.4, and 1.6
- `tests/test_validate_change.py`
- `scripts/validate_change.py` if validator behavior must change
- `templates/change/traceability.yaml`
- `templates/change/change.yaml`
- `docs/phases/PHASE_1_DISCOVERY_AND_REQUIREMENTS.md`

Verification:

- `python -m pytest tests/test_validate_change.py -v`
- Manual negative cases if not covered by automated tests, recorded with exact commands.
- `python scripts/validate_change.py --allow-placeholders templates/change`
- `openspec validate --all --strict`
- `git diff --check`

Documentation updates:

- Update this phase plan with scenario/test evidence.
- Update audit if a traceability or artifact-contract gap is fixed or remains intentionally open.
- Update context only if terms or boundary rules change.

Recommended subagents:

- worker: implement focused scenarios and tests.
- reviewer: check missing negative cases and overly strict artifact burden.
- architecture-checker: verify traceability remains derived/checkable where possible and does not become unmaintainable manual bureaucracy.
- verification-checker: rerun tests and OpenSpec validation.

Exit criteria:

- Traceability scenarios cover requirement-to-scenario, task/test/change evidence expectations, missing links, and approved waiver behavior.
- Artifact contract scenarios cover thin and full modes, required/optional/waived artifacts, and unsupported combinations.
- Validator tests match the approved Phase 1 artifact contract.

OpenSpec and acceptance evidence:

- Scenario IDs or requirement headings are traceable from proposal deltas to tests/manual commands.
- Residual manual-verification risk is recorded if any acceptance scenario lacks automated coverage.

### 1.10 Phase 1 Acceptance Readiness Review

Objective:

- Prepare the full Phase 1 OpenSpec proposal set for human acceptance review without archiving or creating accepted specs.

Expected files/modules:

- All active Phase 1 OpenSpec change folders
- `docs/phases/PHASE_1_DISCOVERY_AND_REQUIREMENTS.md`
- `docs/CURRENT_PROJECT_AUDIT.md`
- `docs/ROADMAP.md` only if phase status or gate wording changes
- `docs/AI_STEP_VERIFICATION_CHECKLIST.md` only if the human adds new verification habits

Verification:

- `openspec list`
- `openspec list --specs`
- `openspec validate --all --strict`
- `python -m pytest tests/test_validate_change.py -v`
- `python scripts/validate_change.py --allow-placeholders templates/change`
- `git diff --check`
- Manual checklist that every work item has worker/reviewer/architecture/verification evidence or a recorded blocker.

Documentation updates:

- Update this phase plan with readiness evidence, open blockers, and final human decision questions.
- Update audit for fixed/open risks backed by evidence.
- Do not update `openspec/specs/` in this work item.

Recommended subagents:

- worker: assemble readiness evidence and resolve small documentation gaps.
- reviewer: inspect proposed specs for contradictions, missing tests, and acceptance gaps.
- architecture-checker: verify alignment with the accepted implementation strategy, current docs, and OpenSpec proposals.
- verification-checker: run final evidence commands and verify report completeness.

Exit criteria:

- All proposed changes validate strictly.
- All known blockers are recorded.
- Human acceptance questions are ready and include options/tradeoffs.
- Human acceptance questions include 2-3 options, a recommended default, risks, and unresolved-decision consequences.
- No active OpenSpec change has been archived or promoted into accepted specs.

OpenSpec and acceptance evidence:

- Readiness packet maps proposed requirements to scenarios, tests/manual checks, documentation updates, and remaining risks.

### 1.11 Final Human Gate Before OpenSpec Archive/Accepted Specs

Objective:

- Stop for human approval before any Phase 1 OpenSpec changes are archived into accepted specs.

Expected files/modules:

- `docs/phases/PHASE_1_DISCOVERY_AND_REQUIREMENTS.md`
- All active Phase 1 OpenSpec change folders
- `openspec/specs/` only after explicit human approval in a later execution step
- `docs/ROADMAP.md` only after acceptance changes phase status or scope
- `docs/CURRENT_PROJECT_AUDIT.md` only after evidence changes risk status

Verification:

- Manual check that the human explicitly approves archiving OpenSpec changes into accepted specs.
- `openspec list`
- `openspec list --specs`
- `openspec validate --all --strict`
- `git diff --check`

Documentation updates:

- Before approval: record the gate as blocking in this phase plan.
- After approval in a separate execution step: update accepted specs, roadmap/audit status, and archive evidence as required.

Recommended subagents:

- worker: prepare final acceptance/archive packet.
- reviewer: check unresolved risks, missing tests, and contradictory requirements.
- architecture-checker: verify accepted specs preserve architecture boundaries.
- verification-checker: verify final OpenSpec validation and report completeness.

Exit criteria:

- Human has explicitly approved or rejected archiving.
- If approved, a separate execution step may archive changes and create accepted specs.
- If rejected or deferred, proposed changes remain active and blockers are documented.

OpenSpec and acceptance evidence:

- The final packet identifies every proposed requirement, acceptance scenario, verification command, manual-verification risk, and human decision that supports acceptance.

## Phase Gate

- Phase 1 is ready for human acceptance/archive review only when the proposed OpenSpec changes for lifecycle, artifact contracts, traceability, waivers, documentation governance, merged repo topology/config/OpenSpec version policy, and Confluence feedback loop have been drafted, validated, reviewed, and explicitly stopped at the final human archive gate.
- Phase 1 is complete only after explicit human approval plus a separate verified archive/accepted-spec execution step.
- No proposed OpenSpec change may be archived into accepted specs without explicit human approval.
- No template or validator expansion may implement any final contract before the corresponding human decision gate is approved. The artifact matrix and waiver gates were approved on 2026-07-06, as were the lifecycle naming and error-level enforcement decisions; the merged topology/config/OpenSpec-version gate (1.5) was approved on 2026-07-09.

## Human Decisions

- Completed 2026-07-06: final thin vs full artifact matrix, approved as Option A risk-oriented matrix.
- Completed 2026-07-06: waiver policy approvers/evidence, approved as Option A role-appropriate approvers and evidence.
- Completed 2026-07-06: Jira task automation, Confluence publication, QA/AT proposal generation, and role inbox remain outside the first MVP and are planned as later layers.
- Completed 2026-07-06: project memory triad accepted as the future orientation model.
- Completed 2026-07-06: existing-code onboarding accepted as `scan -> baseline -> map -> validate`.
- Completed 2026-07-06: `sync` and `upgrade` accepted as future deterministic maintenance, not AI-only skills.
- Completed 2026-07-06: PDLC narrative accepted for team-facing explanation of the process.
- Completed 2026-07-06: deploy, Zephyr/test-management integration, Jira task automation, Confluence publication, QA/AT proposal generation, and role inbox remain outside the first MVP.
- Completed 2026-07-06: lifecycle state naming вЂ” accepted specs and deterministic validation use the six internal states (`draft`, `spec_review`, `approved`, `in_implementation`, `ready_to_archive`, `archived`); simplified lifecycle names appear only in generated business-facing views.
- Completed 2026-07-06: work item 1.8 enforcement вЂ” the approved artifact matrix and waiver checks are enforced as errors immediately, with no warnings-only staging period.
- Completed 2026-07-06: canonical decision log вЂ” `docs/DECISIONS.md` with stable decision IDs is created at Phase 1 acceptance readiness (work item 1.10); until then the existing multi-file decision convention continues.
- Completed 2026-07-06: proposal merge decision - the OpenSpec version pin/upgrade policy is handled inside `define-repo-topology-config` as one platform-assumptions proposal with a single human gate (1.5); the work item 1.4 draft was created on 2026-07-09.
- Completed 2026-07-09: first supported repo topology/config format and OpenSpec version pin/upgrade policy, approved as the gate 1.5 recommended defaults: central `team-specs`, central team config plus optional project adapter, central OpenSpec `1.4.1` pin with reviewed upgrade change package, one versioned process package, and `owners.yaml` as source for generated or validated `CODEOWNERS`.
- Completed 2026-07-06: canonical language for team product analytics specs вЂ” Russian requirement/scenario prose with English structural keywords (`SHALL`, `WHEN`, `THEN`) and English stable IDs; this project's process specs stay English; the documentation-governance proposal's canonical-language requirement was updated accordingly.
- Completed 2026-07-09: migration approach for the existing Confluence analytics corpus - old Confluence analytics content is kept as a read-only archive; no bulk migration is required for the first pilot, and any reused material becomes new Git/OpenSpec source through a reviewed change instead of being edited in place. This interpretation was confirmed by the human owner after the decision summary.
- Completed 2026-07-09: storage conventions for large analytics diagrams, journey schemes, and screen assets - accepted artifacts use Git-managed source or source+export with stable IDs and generated Confluence embeds; diagrams drawn directly in Confluence may be treated as discussion drafts, but accepted/published diagrams must be exported or recreated into the Git-managed asset flow.
- Completed 2026-07-09: Confluence feedback loop owner/SLA/unresolved comments - analyst/change owner triages feedback; blocker comments block later Confluence-enabled publication/archive readiness; non-blocking comments may continue only with explicit disposition; the default SLA is triage within 1 working day for blockers and 3 working days for non-blockers, and this SLA must be editable and explicitly disableable.
- Completed 2026-07-09: generated-view selection for the first Confluence-enabled workflow is deferred to the corporate environment because it depends on real corporate templates, approval practices, and tooling constraints.
- Completed 2026-07-09: project memory/documentation quality controls for weaker corporate AI models - memory follows the future `team-specs` topology; the first graph/navigation implementation should be a lightweight deterministic index; mandatory pilot guardrails are read packs, role skills, and evidence checklists; first role guides are analyst, developer, and QA thin-change walkthroughs.
- Open: before archiving OpenSpec changes into accepted specs.
