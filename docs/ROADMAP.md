# Roadmap

This roadmap is the working development plan for teamSddCli. It is phase-level; detailed implementation plans belong in `docs/phases/`.

## Current Roadmap Validation

- Current roadmap focus: Phase 2 is `closed` after human decision `D-020` accepted immutable `phase-2-14-rc6` as the exact external transfer baseline. Decision `D-021` adds a new external Phase 3 for self-service guided operation before any corporate work. Decision `D-023` accepts successor `guided-owner-v0.3.1-rc4` for merge after the guided contract, exact baseline-reuse closure, fresh model preflight, and Windows rehearsal; Linux/WSL2 portability evidence is an explicit deferred prerequisite before Phase 4. Transfer progress remains 35/36 and NIS progress remains 42/43; former pilot tasks 7.5 and 8.8 now belong to Phase 4. Historical rc4 remains unchanged; rc5 remains diagnostic rejected history.
- Planning from this roadmap alone is forbidden. Detailed phase plans must reconcile roadmap intent, current docs, current implementation, environment evidence, audit findings, and human decisions.
- `sdd CLI` behavior, SDD workflow requirements, proposed process changes, artifact contracts, and acceptance criteria belong in OpenSpec artifacts under `openspec/` when SDD applies.
- New ideas during active phase work must go through change intake before they alter scope or plans.
- Accepted architecture critique decisions from 2026-07-03 narrow the first MVP to a thin change flow before Jira, QA/AT, Confluence publication, and role inbox automation.
- Human decisions from 2026-07-06 approve the risk-oriented thin/full artifact matrix, role-appropriate waiver ownership, and keeping Jira, Confluence publication, QA/AT proposal generation, and role inboxes outside the first MVP while planning them as later layers.
- Human decisions from 2026-07-06 also accept the project memory triad, existing-code onboarding flow, deterministic `sync`/`upgrade` maintenance direction, PDLC explanation narrative, and explicit exclusion of deploy/Zephyr/Jira/Confluence from the first MVP.
- Human decisions from 2026-07-06 (audit decision batch) adopt the six-state canonical lifecycle naming, error-level enforcement for work item 1.8, the canonical decision log now consolidated in `docs/DECISIONS.md` (`D-006`), and merging the OpenSpec version policy into the `define-repo-topology-config` proposal.
- Human feedback from 2026-07-06 (adoption-readiness batch) adopts `Master Spec` / `Delta Spec` team-facing terminology and the other-team reusability constraint for the topology proposal, and opens the analytics language, existing-Confluence migration, and diagram/asset storage decisions (see the Phase 1 plan and AUDIT-018).
- Human decision `D-022` on 2026-07-20 makes Russian the language of new project documentation and OpenSpec prose; stable IDs, technical paths/tokens, and required structural keywords remain English, while historical immutable evidence is preserved without bulk translation.
- Human decisions from 2026-07-09 close gate 1.5 with the recommended defaults: central `team-specs`, central config plus optional project adapter, OpenSpec `1.4.1` central pin with reviewed upgrades, one versioned process package, and `owners.yaml` as owner source; they also close the existing-Confluence read-only archive, diagram/source-asset, Confluence feedback, editable/disableable SLA, weak-model guardrail, and role-guide planning defaults. The first generated Confluence view set is deferred to the corporate environment.
- Human decision Option A from 2026-07-09 accepted the whole Phase 1 readiness-complete OpenSpec package. The batch archive promoted eight changes into accepted specs and left Confluence publication automation outside the first MVP.
- Human confirmation on 2026-07-13 accepts an external transfer-ready release candidate as the boundary before corporate adaptation: reusable core, deterministic gates, package/bootstrap/update/rollback, role instructions, bounded read packs, and actual Qwen/DeepSeek certification are completed externally; corporate work is limited to real configuration, approved wiring, thin adapters, and a monitored pilot.
- Human decision `D-013` on 2026-07-13 supersedes `thin/full` as the target process classification with the flat NIS model `minor|major|hotfix`, adopts corporate DoR/DoD, Tech Lead governance, regression/scope/stop/release controls, pilot safety, and failed-run retention, and records the migration and safety corrections in active change `adopt-nis-corporate-process-governance`. Process-effectiveness measurement is excluded. Earlier Phase 1 thin/full records remain historical accepted evidence until the new change is implemented and promoted.
- Human decisions `D-014`, `D-015`, and `D-016` on 2026-07-14 establish the two-horizon automation strategy, Phase 2 remediation gate, and reliability/throughput direction. `D-018` supersedes only the former three-host matrix: Windows now receives the full clean rehearsal, Linux receives a bounded equivalent WSL2 portability smoke, and macOS is not certified. Deterministic/AI-disabled operation remains the foundation and fallback; reliability grows through risk-oriented tests and traceability; speed grows through safe parallel AI work on independent tasks.
- Human decision `D-017` on 2026-07-14 accepts the corrected `2.1-2.14` Phase 2 plan and opens work item 2.1 as the sequential implementation start.
- Human decision on 2026-07-16 rejects fallback-only acceptance of the first Qwen/DeepSeek certification baseline and adopts bounded role-specific schema generation, reasoning/final separation, mechanical normalization, one append-only structural retry, and a 5/5 preflight gate before each 15/15 matrix. Work item 2.11 returns from `pending_acceptance` to `in_progress`; 2.12 remains blocked and Phase 3 does not start.
- The follow-up adapter `2.1` execution retained the same authority and safety gates while making decision branches structurally exclusive. Frozen Qwen passed 2/5 preflight cases and DeepSeek passed 0/5; all ten responses were structurally valid on attempt 1, so there were zero retries, both family gates failed, and neither matrix ran. Transfer progress remains 22/36, task 4.9 remains open, 2.11 remains `in_progress`, and 2.12 remains blocked.
- Adapter `2.2` moves deterministic action, artifact routing, reason codes, source inventory, and human route into an identity-bound pre-generation plan. The unchanged frozen Qwen and DeepSeek proxies each passed 5/5 preflight before passing 15/15 matrices, every accepted response completed on attempt 1, and AI-disabled passed 11/11. Task 4.9 is complete, transfer progress is 23/36, work item 2.11 is closed, and 2.12 becomes the next planned item.
- The 2026-07-17 ambiguity audit found that the observed failures are a mixed system/model result: the validator expects hidden exact reason codes, full source repetition, and artifact routing, while a field-blind authority regex can reject safe descriptions of required human decisions. The planned remediation keeps adapter `2.1` immutable, moves operation action and policy metadata into the deterministic launcher, narrows the model to source-grounded content, and rejects semantic retry/self-critique complexity.
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

Status: closed.

Work items 2.1-2.13 and all work item 2.14 gates are closed. Human decision `D-020` accepts immutable candidate `phase-2-14-rc6` with the exact hashes recorded in its acceptance packet. Decision `D-021` adds a successor-package usability gate in Phase 3 before corporate adaptation; tasks 7.5 and 8.8 move to the Phase 4 pilot workstream.

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
- Add release manifest, full Windows clean-bootstrap rehearsal, bounded equivalent Linux/WSL2 portability evidence, update/rollback evidence, private-data checks, transfer runbook, corporate inventory, and pilot templates; record macOS as not certified.
- Keep custom Jira/Confluence clients and all later-layer automation outside the phase.

Phase gate:

- Human accepts the reproducible external release candidate after all deterministic, AI-disabled, Qwen-class, DeepSeek-class, rollback, privacy, and documentation checks pass.

## Phase 3. Self-Service Onboarding And Guided Operation

Status: in_progress.

A detailed phase plan has not been accepted yet.

Goal: make the external reusable process package self-service for a human or AI assistant before any corporate installation. A user starts with a business situation and receives only the applicable commands, evidence expectations, deterministic fallbacks, and explicit human decision boundaries.

Dependency gate:

- The Phase 2 external release candidate is accepted under `D-020`.
- The local owner walkthrough has identified and `D-021` has accepted the self-service usability gap.
- No corporate configuration, wiring, credentials, integration, or pilot execution may begin until this phase produces and verifies a successor reusable package.

Likely scope:

- Define a versioned situation-to-operation catalog shared by human guidance, AI instructions, and a guided CLI entry point.
- Publish and validate one onboarding guide beginning with a business requirement, then progressing through Delta Spec, gates, implementation, QA, evidence, release, and archive preparation.
- Provide deterministic blocks and manual/AI-disabled fallback for missing context, unavailable models/integrations, failed operations, and human-decision gates.
- Remediate the observed GigaCode role and acceptance gap under `D-024`: unknown role is fail-closed, role authority limits every UI action, Analyst cannot receive an implementation CTA, and human acceptance is bound to a trusted event plus the exact reviewed spec revision.
- Under `D-025`, define and verify the reusable analytics package contract before calling the framework ready for an analyst: typed status/channel/data/platform-service records, journey and screen catalogs, integration references, stable asset/source metadata, conditional applicability, templates, validators, and one sanitized worked example.
- Define the source contract and a deterministic sample rendering for screen/integration/analytics views in the external package; do not use this item to perform live corporate publication or wiring.
- Prove the minor, major, hotfix, negative authority, and failed-run routes using synthetic evidence; do not use corporate data, credentials, or services.
- Version and verify the successor package before it becomes the corporate adaptation baseline.

Additional completion conditions from the 2026-07-21 owner walkthrough:

- A real GigaCode walkthrough must preserve the prompt/response/event evidence needed to prove the role gate, revision-bound summary, literal human decision, Analyst stop point, and AI-disabled fallback without private data.
- Schemas, templates, validators, examples, role instructions, guided catalog, and generated/sample views must be checked for drift from one OpenSpec contract.
- Missing chat/UI payload and missing payment-screen package content must be reported as unavailable; they cannot be reconstructed as accepted requirements.
- Under `D-026`, the complete P3 vertical slice is local and MCP-free: no MCP setup, calls, credentials, dependency, or fallback is permitted. Integration artifacts are passive descriptors and manual evidence references only.
- Live Jira/Confluence/Bitbucket/Jenkins values, credentials, approved wiring, and external mutations remain Phase 4 evidence and are not prerequisites that may be fabricated in Phase 3.

## Phase 4. Corporate Adaptation And Real Governed-Change Pilot

Status: planned.

A detailed phase plan has not been accepted yet.

Goal: install the accepted successor process package in the corporate environment, populate real non-secret configuration, wire approved standard tools and the available weak-model adapter, and execute one monitored real minor, major, or hotfix pilot selected through the approved pilot criteria.

Dependency gate:

- The Phase 2 external release candidate is accepted under `D-020` and the Phase 3 successor usability package is accepted.
- Before corporate configuration, wiring, or pilot execution starts, the human owner must complete and review the local synthetic walkthrough record.
- Phase 4 must not redesign reusable process behavior or maintain an internal package fork. Reusable gaps return to the external OpenSpec/change workflow.

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

## Phase 5. Post-Pilot Hardening And Expansion

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
| `allow-certified-baseline-reuse` | P3 | P4 | accepted |
| `add-guided-owner-workflow` | P3 | P4, P5 | accepted |
| `adopt-nis-corporate-process-governance` | P2 | P4 | in_progress |
| `close-release-integrity-gaps` | P2 | P4 | accepted |
| `determinize-weak-model-operational-decisions` | P2 | P4 | in_progress |
| `define-transfer-ready-process-package` | P2 | P4 | in_progress |
| `simplify-weak-model-decision-contract` | P2 | P4 | blocked |

## Phase Planning Rule

When a phase is too large for one iteration, create or update a detailed plan under `docs/phases/` before implementation starts. Follow `docs/phases/PHASE_PLAN_TEMPLATE.md`.
