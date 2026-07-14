# Roadmap

This roadmap is the working development plan for teamSddCli. It is phase-level; detailed implementation plans belong in `docs/phases/`.

## Current Roadmap Validation

- Current roadmap focus: execute work item 2.4 and continue the accepted Phase 2 plan sequentially toward the externally certified transfer-ready process package.
- Planning from this roadmap alone is forbidden. Detailed phase plans must reconcile roadmap intent, current docs, current implementation, environment evidence, audit findings, and human decisions.
- `sdd CLI` behavior, SDD workflow requirements, proposed process changes, artifact contracts, and acceptance criteria belong in OpenSpec artifacts under `openspec/` when SDD applies.
- New ideas during active phase work must go through change intake before they alter scope or plans.
- Accepted architecture critique decisions from 2026-07-03 narrow the first MVP to a thin change flow before Jira, QA/AT, Confluence publication, and role inbox automation.
- Human decisions from 2026-07-06 approve the risk-oriented thin/full artifact matrix, role-appropriate waiver ownership, and keeping Jira, Confluence publication, QA/AT proposal generation, and role inboxes outside the first MVP while planning them as later layers.
- Human decisions from 2026-07-06 also accept the project memory triad, existing-code onboarding flow, deterministic `sync`/`upgrade` maintenance direction, PDLC explanation narrative, and explicit exclusion of deploy/Zephyr/Jira/Confluence from the first MVP.
- Human decisions from 2026-07-06 (audit decision batch) adopt the six-state canonical lifecycle naming, error-level enforcement for work item 1.8, the canonical decision log now consolidated in `docs/DECISIONS.md` (`D-006`), and merging the OpenSpec version policy into the `define-repo-topology-config` proposal.
- Human feedback from 2026-07-06 (adoption-readiness batch) adopts `Master Spec` / `Delta Spec` team-facing terminology and the other-team reusability constraint for the topology proposal, and opens the analytics language, existing-Confluence migration, and diagram/asset storage decisions (see the Phase 1 plan and AUDIT-018).
- Human decisions from 2026-07-09 close gate 1.5 with the recommended defaults: central `team-specs`, central config plus optional project adapter, OpenSpec `1.4.1` central pin with reviewed upgrades, one versioned process package, and `owners.yaml` as owner source; they also close the existing-Confluence read-only archive, diagram/source-asset, Confluence feedback, editable/disableable SLA, weak-model guardrail, and role-guide planning defaults. The first generated Confluence view set is deferred to the corporate environment.
- Human decision Option A from 2026-07-09 accepted the whole Phase 1 readiness-complete OpenSpec package. The batch archive promoted eight changes into accepted specs and left Confluence publication automation outside the first MVP.
- Human confirmation on 2026-07-13 accepts an external transfer-ready release candidate as the boundary before corporate adaptation: reusable core, deterministic gates, package/bootstrap/update/rollback, role instructions, bounded read packs, and actual Qwen/DeepSeek certification are completed externally; corporate work is limited to real configuration, approved wiring, thin adapters, and a monitored pilot.
- Human decision `D-013` on 2026-07-13 supersedes `thin/full` as the target process classification with the flat NIS model `minor|major|hotfix`, adopts corporate DoR/DoD, Tech Lead governance, regression/scope/stop/release controls, pilot safety, and failed-run retention, and records the migration and safety corrections in active change `adopt-nis-corporate-process-governance`. Process-effectiveness measurement is excluded. Earlier Phase 1 thin/full records remain historical accepted evidence until the new change is implemented and promoted.
- Human decisions `D-014`, `D-015`, and `D-016` on 2026-07-14 establish the two-horizon automation strategy, Phase 2 remediation gate, and reliability/throughput direction: deterministic/AI-disabled operation is the foundation and fallback; the release package must cover Windows, Linux, and macOS; reliability grows through risk-oriented tests and traceability; speed grows through safe parallel AI work on independent tasks. `D-015` required explicit plan acceptance before implementation; `D-017` now closes that gate.
- Human decision `D-017` on 2026-07-14 accepts the corrected `2.1-2.14` Phase 2 plan and opens work item 2.1 as the sequential implementation start.
- Roadmap execution is gate-based. Delivery dates and calendar deadlines are intentionally managed outside this repository and are not recorded in roadmap, phase, or OpenSpec planning artifacts.
- Update this file when phase status, gates, or scope changes.

## Phase 0. Project Foundation

Status: closed.

Goal: prepare repository rules, documentation, environment notes, baseline product decisions, OpenSpec expectations, and verification habits from the initial architecture bootstrap input.

Quality gate:

- `AGENTS.md`, docs map, roadmap, audit, verification checklist, and phase template exist.
- Secrets and private-data rules are clear.
- OpenSpec expectations and phase change-intake routing are documented.
- Another agent can continue without chat history.

## Phase 1. Discovery And Requirements

Status: closed.

Goal: turn the architecture into concrete product requirements, user/role workflows, CLI command acceptance criteria, integration constraints, and OpenSpec artifacts.

Likely scope:

- Define accepted CLI personas: analyst, developer, QA, API AT, mobile AT, tech lead, CI owner, and product/business stakeholder.
- Decide the first supported repository topology and configuration format.
- Create initial OpenSpec specs for change lifecycle, artifact contracts, traceability, waiver behavior, and documentation governance.
- Define `thin change` and `full change package` modes, including which artifacts are required for each mode.
- Specify the Confluence feedback loop before implementing publication: responsible owner, service expectation, unresolved feedback, and accepted/rejected comment handling.
- Plan the generated publication model for later Confluence work: generated change/capability/customer journey/release/technical appendix/screen gallery views, source metadata, source warnings, and links back to canonical Git/OpenSpec files.
- Plan journey and screen traceability as future artifact contracts without making `journey.yaml`, `screens.yaml`, or screen assets mandatory for the first thin MVP.
- Plan legacy baseline behavior for already-written code so future pilots can document observed behavior and gaps gradually.
- Plan the project memory triad and documentation boundaries so agents and humans can orient through constitution/quality policy, project map, and OpenSpec changes/living specs without creating a second behavior source of truth.
- Plan existing-code onboarding as `scan -> baseline -> map -> validate`, with read-only scan and deterministic validation where practical.
- Plan deterministic `sync` and `upgrade` maintenance after the relevant repo topology/config and OpenSpec version policies are approved.
- Define the first pilot as a thin flow and explicitly keep Jira task automation, QA/AT proposal commands, Confluence publication, and role inboxes out of MVP unless re-scoped by the human owner.

Detailed plan:

- `docs/phases/PHASE_1_DISCOVERY_AND_REQUIREMENTS.md`
- `docs/planning/PROJECT_MEMORY_AND_WEAK_MODEL_GUARDRAILS.md` for broader memory planning; its minimum transfer-readiness subset is now promoted into active change `define-transfer-ready-process-package` and Phase 2.

Current work:

- Completed deterministic baseline artifact: `templates/change/`, `scripts/validate_change.py`, and `.pre-commit-config.yaml`.
- Completed accepted-spec baseline on 2026-07-09: immediately after the archive, `openspec list` reported no active changes and `openspec list --specs` reported eight accepted specs. Phase 2 now has active change `define-transfer-ready-process-package` against that baseline.
- Confluence feedback/source/publication-read-model contracts are accepted, but actual Confluence publication automation and first generated-view selection remain later-layer work after corporate-environment validation.

## Phase 2. Transfer-Ready Process Package And Weak-Model Readiness

Status: in_progress.

Work items 2.1-2.3 are closed; work item 2.4 is ready under the worker/reviewer/architecture/verification workflow.

Goal: build and externally certify a reusable release candidate for the deterministic class-aware corporate process so the corporate environment performs only real configuration, approved integration wiring, thin model-adapter configuration, environment checks, and a monitored pilot.

Detailed plan:

- `docs/phases/PHASE_2_TRANSFER_READY_PROCESS_PACKAGE.md`

Active OpenSpec change:

- `openspec/changes/define-transfer-ready-process-package/`
- `openspec/changes/adopt-nis-corporate-process-governance/`

Scope:

- Create the versioned `process/` package, synthetic central `team-specs` bootstrap, central/project config schemas, owner/project registries, OpenSpec pin checks, and compatibility validation.
- Replace the target legacy thin/full route with schema-versioned minor, major, and hotfix classification plus deterministic migration and class-aware artifacts.
- Package create, validate, Spec PR, DoR, implementation, DoD, release/transfer readiness, archive, traceability, update, rollback, stop/escalation, and hotfix reconciliation without AI-owned gates.
- Add deterministic task launch, authority-labelled bounded read packs, evidence output, analyst/developer/QA/Tech Lead role instructions, and thin Qwen/DeepSeek/GigaCode adapter templates.
- Add safe parallel-task contracts so AI can execute independent work concurrently with explicit ownership, non-overlapping write scopes, separate evidence, and one deterministic integration gate.
- Expand risk-oriented positive/negative tests and generate requirement/scenario-to-test/evidence coverage with visible residual gaps.
- Certify minor, major, hotfix, Tech Lead, and negative authority workflows using actual Qwen-class and DeepSeek-class runtimes plus an AI-disabled walkthrough.
- Add release manifest, equivalent Windows/Linux/macOS clean-bootstrap rehearsal, update/rollback evidence, private-data checks, transfer runbook, corporate inventory, and pilot templates.
- Keep custom Jira/Confluence clients and all later-layer automation outside the phase.

Phase gate:

- Human accepts the reproducible external release candidate after all deterministic, AI-disabled, Qwen-class, DeepSeek-class, rollback, privacy, and documentation checks pass.

## Phase 3. Corporate Adaptation And Real Governed-Change Pilot

Status: planned.

A detailed phase plan has not been accepted yet.

Goal: install the accepted Phase 2 release candidate in the corporate environment, populate real non-secret configuration, wire approved standard tools and the available weak-model adapter, and execute one monitored real minor, major, or hotfix pilot selected through the approved pilot criteria.

Dependency gate:

- Phase 3 cannot start until the Phase 2 external release candidate is explicitly accepted.
- Phase 3 must not redesign reusable process behavior or maintain an internal package fork. Reusable gaps return to the external OpenSpec/change workflow.

Likely scope:

- Verify corporate runtime, OpenSpec/Git/package compatibility, network and artifact restrictions, MCP policy, and available Bitbucket/Jenkins/Jira/Confluence capabilities.
- Populate real project paths, `projects.yaml`, `owners.yaml`, optional project adapters, policy overrides, and approved secret references.
- Configure supported standard-tool integrations and the available Qwen/DeepSeek/GigaCode adapter without moving gates into AI.
- Re-run package/config/release checks and the AI-disabled class-aware flow in the real environment.
- Select one representative bounded real change with explicit class, risk, rollback, privacy, and evidence-source justification; a minor change is the default recommendation unless representativeness requires another class.
- Execute it through triage, classification, Spec Review, DoR and human approval, implementation controls, DoD, applicable release/transfer readiness, traceability, and archive readiness.
- Record compatibility, role usability, failed attempts, interventions, deviations, rollback/hold, hotfix reconciliation where applicable, and follow-up evidence.
- Complete OpenSpec task 7.5 and stop for human pilot/contract acceptance before archive promotion.

Explicitly deferred from the first MVP:

- `sdd publish confluence --preview`
- `sdd tasks plan` / `sdd tasks create`
- `sdd qa propose`
- `sdd at propose`
- `sdd inbox`

## Phase 4. Post-Pilot Hardening And Expansion

Status: planned.

A detailed phase plan has not been accepted yet.

Goal: harden the accepted real workflow using operational findings and add later layers only through new accepted changes.

Likely scope:

- Pilot-driven reliability, usability, compatibility, and support-burden improvements.
- Broader project memory, project map drift checks, repeated-error memory, and deterministic sync/upgrade maintenance beyond the minimum Phase 2 operating kit.
- Legacy baseline workflow for existing product areas when the pilot expands beyond the first bounded change.
- Confluence preview/final publication after the feedback loop contract is specified.
- Generated publication model implementation after feedback-loop, source-warning, localization, and generated-view contracts are accepted.
- Customer journey and screen/gallery generated views after journey/screen metadata contracts are proven.
- Expanded analyst/developer/QA onboarding after the pilot validates the first role instructions.
- Jira task planning/creation after the class-aware archive and external-delivery mapping works.
- Role inbox hardening after task/status sources are stable.
- QA/AT proposal and skeleton generation after scenario and traceability contracts are validated.
- Drift detection for generated Confluence blocks.
- Bitbucket Code Insights or equivalent reporting.
- Read-only MCP exploration only after the deterministic and standard-tool flow is working.
- Progressive AI automation after the deterministic flow and monitored pilot are accepted: source-linked evidence assembly, workflow routing, bounded monitoring, role assistance, supported tool coordination, and permitted transition preparation through new OpenSpec changes.
- Deterministic fallback and verification remain supported as AI automation expands; human authority changes only through explicit accepted decisions.

## Capability Spec Ownership

| Capability spec | Roadmap phase | Related phases |
|---|---|---|
| `change-artifact-contracts` | P1 | P2, P3 |
| `change-lifecycle` | P1 | P2, P3 |
| `change-package-foundation` | P1 | P2, P3 |
| `confluence-feedback-loop` | P1 | P3, P4 |
| `documentation-governance` | P1 | P0, P2, P3, P4 |
| `repo-topology-config` | P1 | P0, P2, P3 |
| `traceability-contract` | P1 | P2, P3 |
| `waiver-policy` | P1 | P2, P3 |

## Active Change Execution

| Active change | Execution phase | Related phases | Lifecycle status |
|---|---|---|---|
| `adopt-nis-corporate-process-governance` | P2 | P3 | in_progress |
| `define-transfer-ready-process-package` | P2 | P3 | in_progress |

## Phase Planning Rule

When a phase is too large for one iteration, create or update a detailed plan under `docs/phases/` before implementation starts. Follow `docs/phases/PHASE_PLAN_TEMPLATE.md`.
