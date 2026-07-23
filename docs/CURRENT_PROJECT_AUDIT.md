# Current Project Audit

Status: in_progress.

Phase 2 is closed and Phase 3 entry is gated by the local owner walkthrough.

Last status reconciliation: 2026-07-22.

## P3.3 Typed Analytics Package Transfer Reconciliation (2026-07-23)

- Immutable successor `p3-analytics-v0.3.6-rc2` was built and manifest-validated with payload SHA-256 `b4b9f97be4eada905a65acffa3d24f1a98c2cdfe8fa38bd90d2a2296c282db57`.
- Source evidence: `89 passed` for the P3/package/update/catalog suite; `83 passed, 1 skipped` for `tests/test_release_candidate.py`; OpenSpec strict validation passed `19` items; roadmap/OpenSpec linkage had zero errors and three lifecycle warnings: the expected analytics change awaiting human acceptance and two historical lifecycle items.
- The controlled sandbox sequence `check -> update -> rollback -> final update` proved `0.3.4 -> 0.3.6`, rollback to `0.3.4`, and final installed version `0.3.6`. `git diff --check` passed after the final update. Existing dirty OpenSpec paths `operation-history/` and `payments-screen/` were not changed or staged.
- P3.3 and Task 2.2 are implementation-complete and `pending_acceptance`. `add-typed-analytics-artifact-framework` remains active and is not accepted, synced, or archived; the next lifecycle action is human review of its acceptance packet.

## P3 Operation Catalog And Dispatcher Reconciliation (2026-07-23)

- `add-operation-catalog-and-dispatcher` has 15/16 verified tasks: versioned catalog/schema/validator, derived release/guided/read-pack/README views, local `sdd`, direct-script compatibility, four guided walkthroughs, and P3 fail-closed mutation handling.
- Focused P3/catalog/package verification passed 49 tests; four situation-first manual walkthroughs returned the expected role, human decision, fallback/evidence route, and `sdd run create-change` returned a structured no-side-effect block. `openspec validate --all --strict` passed 18/18; roadmap/OpenSpec validation reported zero errors and two unrelated historical P2 lifecycle warnings.
- The owned suite `python -m pytest -q tests` passed 776 tests with 4 skips in 298.78 seconds. This supersedes the 2026-07-22 snapshot that reported 742 passed and 18 failed.
- Task 4.2 remains open by design: it requires completion and human acceptance of the separate `harden-role-aware-guided-workflow` confirmation contract. Until then, every dispatcher mutation remains fail-closed; this change is not ready for archive or successor acceptance.
- The contract-only operation-confirmation extension has final local evidence: 54 dispatcher/guided tests, 18 package-schema tests, and 83 release-candidate tests passed with one expected skip; a valid event still leaves `sdd run` blocked and catalog validation rejects `mutate_external`. Human acceptance remains the next explicit lifecycle gate.
- Reproducible Task 17 evidence (2026-07-23): `python -m pytest -q -o addopts='' --basetemp <fresh-temp> tests/test_guided_owner_workflow.py tests/test_p3_vertical_slice.py tests/test_operation_catalog_dispatcher.py tests/test_process_package.py` returned `72 passed`; the release-candidate suite was split only for the shell time limit and returned `83 passed, 1 skipped` across exhaustive non-overlapping selections. `openspec validate --all --strict` passed; `node "$env:USERPROFILE\\.codex\\skills\\roadmap-openspec-validator\\scripts\\validate-roadmap-openspec.mjs" --root "<repository-root>"` returned zero errors and three lifecycle-only warnings. In the AI-disabled walkthrough, `python scripts/sdd.py request create-change --role Analyst --json` returned `confirmation-requested`, `authority_granted: false`, and `trusted_event_metadata_required: true`; `python scripts/sdd.py run create-change --role Analyst --json` returned `confirmation-contract-pending` with no state mutation. Independent security review of `031127b..8fe18b8` found no authority escalation: even a valid typed event leaves `run` blocked and synthetic `mutate_external` catalog data is rejected. The review approved the implementation boundary; its initial gate objection was resolved by recording this evidence and requires only a final documentation re-review.

## Project-Wide Implementation And NIS Audit (2026-07-22)

- Audit evidence and the full human-facing capability/script inventory are in `docs/audits/PROJECT_WIDE_IMPLEMENTATION_AND_NIS_AUDIT_2026-07-22.md`.
- OpenSpec strict validation passes 17/17 and roadmap/OpenSpec linkage has zero errors (two expected lifecycle warnings for P2 changes with completed tasks but no human lifecycle disposition).
- The current branch passes focused P3 tests (18/18), but the complete owned suite is red: 742 passed, 18 failed, 4 skipped. Failures are grouped into stale P3 coverage/evidence mappings, version-drifted package-update fixtures, and locally mismatching external historical raw-certification artifacts. The accepted immutable rc6 baseline is not reclassified by this observation.
- The root `pytest` command is not a valid project entry point because it recurses into ignored historical `tmp/pytest-*` evidence directories. Use `python -m pytest -q tests` for the owned suite until configuration is fixed.

## Guided Owner Workflow Intake (2026-07-20)

- Human decision `D-021` adopts a new pre-corporate Phase 3 for self-service guided operation. The current package exposes valid bounded commands but lacks a single situation-based entry point for a colleague who starts with a business requirement, an existing change, a hotfix, or a blocked operation.
- Change `add-guided-owner-workflow` owns the reusable catalog, guided CLI entry point, shared human/AI onboarding guide, authority boundary, synthetic route evidence, and successor-package verification. It is accepted for merge by `D-023`; it is not a corporate configuration task and does not modify immutable RC6, archived specs, historical raw evidence, or external systems.
- Corporate adaptation and the real governed-change pilot move to Phase 4. Post-pilot hardening moves to Phase 5. No corporate configuration, wiring, credentials, integration, or pilot may begin until the new Phase 3 completion gate is met.

## Phase 3 Documentation Reconciliation (2026-07-21)

- The documentation audit corrected the exact lifecycle metadata for
  `add-guided-owner-workflow` and `allow-certified-baseline-reuse` to
  `accepted`, matching human decision `D-023`; the roadmap inverse table now
  uses the same machine-readable status.
- `openspec validate --all --strict` passes 15/15 and the roadmap/OpenSpec
  validator reports zero errors. Two warnings remain for unrelated P2 changes
  with complete tasks but no recorded lifecycle disposition.
- Phase 3 itself remains `in_progress`: its final lifecycle disposition is not
  inferred from acceptance of the two changes. Linux/WSL2 portability evidence
  remains a mandatory Phase 4 entry condition, as recorded by `D-023`.
- Evidence: `docs/audits/PHASE_3_GUIDED_OWNER_WORKFLOW_DOCUMENTATION_RECONCILIATION_AUDIT_2026-07-21.md`.

## P3 Work-Item Status Reconciliation (2026-07-21)

- The active Phase 3 plan now provides explicit scanner-readable statuses and OpenSpec mappings for work items `3.1` through `3.3`; the roadmap links to that plan rather than incorrectly claiming no detailed P3 plan exists.
- `3.1` and `3.2` are `in_progress`; `3.3` is `planned` because package `0.3.4` is only the already-transferred baseline and the successor transfer must follow validation of both active P3 changes.
- The phase remains `in_progress`. A closed OpenSpec change is not sufficient evidence to close a roadmap work item or the phase; the mapped phase-plan exit criteria and verification gate must also be satisfied.

## Rc6 Documentation-Sync Audit (2026-07-20)

- Human decision `D-020` accepts exact immutable `phase-2-14-rc6` as the external transfer baseline and closes Phase 2. Transfer task 7.4 and NIS task 8.7 are complete; progress is now 35/36 and 42/43. Corporate configuration and pilot work remain paused until the owner completes and reviews the local synthetic walkthrough.

- Branch `codex/close-release-integrity-gaps` matches the completed remediation workstream. Source commits `5f92fc6` and `4ffc44a` precede the immutable candidate boundary; rc6 release and documentation evidence is committed in `b1e444a` and `f520ccd`.
- Roadmap, Phase 2 plan, current audit, evidence index, OpenSpec tasks, and the acceptance packet record Phase 2 as closed and `close-release-integrity-gaps` as accepted under `D-020`.
- Roadmap/OpenSpec validation reports 0 errors and two legitimate lifecycle warnings: adapter 2.2 remains in progress pending explicit disposition, and failed adapter 2.1 remains blocked historical evidence.
- `close-release-integrity-gaps` remains complete at 21/21 tasks; transfer is 35/36 and NIS is 42/43 because only later Phase 3 tasks 7.5 and 8.8 remain unchecked.
- The tracked rc6 manifest and both host-evidence copies are byte-identical to their external immutable originals. Candidate manifest validation remains `valid`; aggregate acceptance remains `evidence-complete` with an explicit human decision required.
- Final privacy search found only the intentional synthetic private-value string used by the negative acceptance matrix in `process/release_candidate.py`; no tracked personal workspace path, raw model output, real credential, email, private host, or corporate identifier was introduced.
- `CLAUDE.md` remains a thin pointer to `AGENTS.md` and has no active handoff. No duplicate canonical behavior source was created; the new audits summarize and link the OpenSpec contracts.

## Residual-Gap Reconciliation (2026-07-19)

- The 110 rc4 residual-gap rows were traced to the Phase 2.10 transition from aggregate/default coverage to exact source-local `SCENARIO_COVERAGE` bindings. They are verified missing exact evidence bindings, not 110 independently discovered product defects.
- All 110 rows have mechanically identical owner/risk/reason/compensation/follow-up metadata. The repeated `risk: medium` is therefore a fallback classification, not an individual risk assessment.
- The 2026-07-20 selector review initially resolved the 75 Phase 2 rows into 58 existing proofs, 4 focused tests, and 13 product gaps. Focused and release-integrity remediation now bind 68 Phase 2 selectors to exact tests; 22 governance rows remain linked to primary decisions/audits and 12 Phase 3/4 rows remain exact `future_work`.
- Immutable candidate `phase-2-14-rc6` is frozen with payload SHA-256 `172707ba159e1e060561d6d02ad67dcaf2fa4ce64a58c23bd9c55613713fd951`, manifest SHA-256 `0c7670637f1f59f82a6cae3bea48c53edfa3453d5fcf0c599bf013bd301c3146`, 199 payload files, and 48 exact raw references. Aggregate evaluation is `evidence-complete` with no diagnostics, and independent candidate review is `READY` with no findings.
- Package `0.3.0` implements the six prioritized release-integrity selectors and candidate coverage is `295 covered / 7 gaps / 32 future_work`. The seven remaining product gaps are explicit Phase 3/4 deferrals under `D-019` and do not block the accepted first-MVP boundary.
- Интерактивные роли P3: `Analyst`, `Tech Lead`, `Developer`, `QA`; Analyst может дать доверенное acceptance спецификации, а valid DoR ведёт только к подготовке PR для ролевого согласования; Tech Lead мониторит процесс и не является gatekeeper реализации. Current OpenSpec progress is `35/36` for `define-transfer-ready-process-package`, `42/43` for `adopt-nis-corporate-process-governance`, and `21/21` for accepted `close-release-integrity-gaps`. The local owner walkthrough is the Phase 3 entry gate before corporate work; its guided contract has passed synthetic, AI-disabled, Qwen/DeepSeek preflight, and negative-path verification. Successor `guided-owner-v0.3.1-rc4` is accepted for merge by `D-023`; Linux/WSL2 portability evidence remains a mandatory Phase 4 entry condition.
- Historical rc4 was not changed. Rc5 is retained as diagnostic rejected history: its bundle copied one undeclared top-level runtime probe, so normalized Qwen and DeepSeek validation returned `actual-model.result-inventory-mismatch`; the exact-inventory rc6 successor corrected only that derived bundle boundary.
- Durable evidence: `docs/audits/PHASE_2_RESIDUAL_GAPS_PROVENANCE_AND_ROUTING_AUDIT_2026-07-19.md`.

## Phase And OpenSpec Status Reconciliation (2026-07-18)

- Phase 2 is `closed`; work items 2.1-2.13 and all gates of 2.14 are closed under `D-020`. Exact rc6 remains immutable. Corporate configuration and the pilot are blocked by the separate local owner walkthrough gate.
- Transfer tasks 6.1-6.4 are implementation-complete: four closed schemas, five unresolved templates, two fully synthetic examples, a read-only validator/CLI, privacy and secret rejection, green-checklist gating, pilot-evidence integrity, rollback/hold coverage, and content-derived no-fork detection are registered in the versioned package. Documentation, final-verification, and review tasks 7.1-7.3 are complete; transfer progress is 34/36.
- All six work-item 2.13 task-level reviewer gates are complete. Tasks 1-4 each used one batched correction, task 5 passed cleanly, and task 6 used one final four-finding correction batch followed by `50 passed` focused and `710 passed, 4 skipped` complete verification. No real corporate configuration or pilot was performed.
- Work item 2.14.2 froze candidate `phase-2-14-rc4` with payload SHA-256 `4159e43961c5c59005d63fb6f305f9b0b5bac18517f8fd02d3e6b27e711ed6e1` and manifest SHA-256 `33aa240261ed0a660a3fc6b7ef85d847215cf5a3cd1f5afb423f28ca45cd02cb`. AI-disabled passed 11/11; Qwen and DeepSeek each passed 5/5 preflight and 15/15 matrix; Windows full rehearsal and WSL2 portability smoke passed with rollback, archive, privacy, negative, and AI-disabled evidence. Rc2 and rc3 remain diagnostic review-failed history after reviewers found stale and non-resolvable coverage provenance. Work item 2.14.3 then closed its worker, reviewer, architecture, and verification gates after one correction batch. Transfer progress is 34/36 and NIS progress is 41/43; human acceptance and Phase 3 pilot tasks remain open.

## Phase And OpenSpec Status Reconciliation (2026-07-17)

- Phase 2 remains `in_progress`; work items 2.1-2.12 are `closed`, and sequential work item 2.13 is the next planned item.
- Work item 2.12 closed with immutable candidate `phase-2-12-rc7`: Windows full rehearsal and native-WSL2 portability smoke passed, the final exact-root acceptance run returned `evidence-complete` with no diagnostics, payload/manifest hashes and required cross-host fields matched, and macOS remains explicitly not certified. Prior passing `rc6` evidence remains preserved as history.
- The dated Phase 2.11 ambiguity audit confirms that adapter `2.1` is structurally clear for the observed ten preflight responses but operationally ambiguous: exact reason codes, required source repetition, artifact kind, and some decision semantics are hidden validator expectations, while the field-blind authority regex can reject safe descriptions of required human decisions.
- OpenSpec change `determinize-weak-model-operational-decisions` is `in_progress` under P2/P3 with 13/13 implementation tasks complete. Adapter `2.2` implements deterministic operation planning, smaller branch-only model content contracts, launcher-bound provenance, field-scoped authority checks, and local diagnostics.
- Work item 2.11 is closed: frozen Qwen and DeepSeek each passed 5/5 preflight and 15/15 matrices, and AI-disabled passed 11/11. Transfer progress is now 27/36 after release tasks 5.1-5.4; NIS progress is 39/43 after task 8.4. The blocked `simplify-weak-model-decision-contract` change and adapter `1.0`/`2.0`/`2.1` evidence remain immutable history.

## Phase And OpenSpec Status Reconciliation (2026-07-16)

- Phase 0 and Phase 1 remain `closed`; no closed work item or phase was reopened.
- Phase 2 is `in_progress`: work items 2.1-2.10 remain `closed`; work item 2.11 returned from `pending_acceptance` to `in_progress` after the human rejected fallback-only acceptance and approved bounded weak-model adapter remediation.
- Phases 3-4 remain `planned`: no Phase 3 work item has started, and Phase 3 still depends on human acceptance of the Phase 2 external release candidate.
- OpenSpec change status: `define-transfer-ready-process-package` is `in_progress` with 23/36 tasks complete and 13 remaining; `adopt-nis-corporate-process-governance` is `in_progress` with 38/43 tasks complete and 5 remaining; `determinize-weak-model-operational-decisions` is `in_progress` with 13/13 implementation tasks complete; `simplify-weak-model-decision-contract` remains blocked historical evidence with 15/15 technical tasks complete. Transfer task 4.9 is complete from adapter `2.2` certification. Task 7.5 and NIS task 8.8 remain Phase 3 work.
- Historical 2026-07-16 outcome: sequential work item 2.12 remained `planned` and blocked by then-in-progress work item 2.11. That snapshot is superseded: adapter `2.2` certification and the later Windows/WSL2 release rehearsal passed, work item 2.12 is closed, and 2.13 is next.

## Historical Phase And OpenSpec Status Reconciliation (2026-07-15)

- Phase 0 is `closed`: its repository-foundation gate is satisfied, and its former Phase 1 decision items were resolved or explicitly deferred by the accepted Phase 1 package.
- Phase 1 is `closed`: all 11 work items are reconciled, the human Option A decision supplies acceptance evidence, and eight changes were archived into accepted specs on 2026-07-09.
- At the 2026-07-15 snapshot, Phase 2 was `in_progress`, work items 2.1-2.10 were `closed`, and work item 2.11 was recorded as `pending_acceptance` after fallback-disposition execution. That snapshot is superseded by the current 2026-07-17 reconciliation above: work item 2.11 is now `closed` after adapter `2.2` certification.
- Phases 3-4 are `planned`: Phase 3 depends on human acceptance of the Phase 2 external release candidate; Phase 4 depends on real pilot evidence.
- Active OpenSpec changes: `define-transfer-ready-process-package` is apply-ready with 20/33 tasks complete and 13 remaining; `adopt-nis-corporate-process-governance` has 38/43 tasks complete and 5 remaining. Transfer tasks 4.4-4.5 and NIS tasks 8.2-8.3 are execution-complete. Task 7.5 and NIS task 8.8 remain Phase 3 work. Both changes remain `in_progress`.
- This historical 2026-07-15 snapshot predates adapter `2.2` and `D-018`. Its earlier fallback-only and adapter `2.1` blockers are superseded; the current accepted contour is Windows plus Linux/WSL2 with macOS explicitly not certified, and work item 2.12 is closed.

Last updated: 2026-07-21.

## Repository Baseline

| Item | Current State |
|---|---|
| Repository root | `<repository-root>` |
| Git repository | Initialized locally on 2026-07-03 |
| Current branch | `codex/close-release-integrity-gaps` |
| Remote | `origin` is configured; inspect locally with `git remote -v` |
| Transfer-readiness audit commit | `96b3614 docs: audit transfer readiness` |
| Repository rename | The remote repository capitalization was corrected; the local folder path retains its historical capitalization |
| Architecture source of truth | Current decisions live in `docs/` and `openspec/`; stale historical architecture draft removed on 2026-07-06 |
| Implementation source code | No monolithic custom `sdd` CLI exists. Deterministic entry points include the Phase 1 compatibility validator, process/config validation, classification/migration, work item 2.5 gate/lifecycle reports, and work item 2.6 check-only Tech Lead review/control reports backed by `process/validators/`. |
| OpenSpec project artifacts | Present; 8 accepted specs cover the deterministic artifact gate plus Phase 1 lifecycle, artifact, traceability, waiver, documentation-governance, repo-topology/config/version, and Confluence feedback/publication contracts; active changes propose transfer-readiness/weak-model guardrails and NIS-aligned corporate-process governance |

## Useful Starting Points

- Documentation starts in `docs/`.
- Roadmap exists at `docs/ROADMAP.md`.
- Agent work rules are recorded in `AGENTS.md`.
- Project memory and weak-model planning input is recorded in `docs/planning/PROJECT_MEMORY_AND_WEAK_MODEL_GUARDRAILS.md`.
- The current Phase 2 execution plan is `docs/phases/PHASE_2_TRANSFER_READY_PROCESS_PACKAGE.md`.
- The active proposed behavior is under `openspec/changes/define-transfer-ready-process-package/`.
- The accepted NIS adoption direction and complete implementation plan are in `docs/planning/NIS_CORPORATE_PROCESS_ADOPTION_PLAN_2026-07-13.md` and `openspec/changes/adopt-nis-corporate-process-governance/`.
- The reproducible pre-plan evidence is `docs/audits/TRANSFER_READINESS_STATUS_2026-07-13.md`.
- The 2026-07-06 documentation/architecture review with current findings and the open decision batch is `docs/audits/FABLE5_DOCUMENTATION_ARCHITECTURE_REVIEW_2026-07-06.md`; its staged-plan companion is `docs/planning/FABLE5_FINAL_ARCHITECTURE_AND_PLAN_DRAFT_2026-07-06.md`.
- Workflow skills are global (`~/.codex/skills`); this repository intentionally has no `.codex/skills/` directory.
- Current architecture and implementation planning are in `docs/`, `openspec/`, and accepted human decisions.

## Verified Environment Evidence

| Check | Evidence |
|---|---|
| Git installed | `git version 2.54.0.windows.1` |
| Repository initialized | Yes; `git init -b main` completed |
| Git remote configured | `origin` is configured; the tracked audit does not duplicate the operator's account or remote URL |
| First push | `git push -u origin main` published `main` to the configured remote |
| Runtime installed | Python 3.13.14 is available for deterministic validation scripts and tests |
| Tests available | Focused deterministic validator and thin-CLI contract tests are present under `tests/`; no monolithic custom `sdd` CLI exists |
| Focused validator tests | `python -m pytest tests/test_validate_change.py -v` passed 34 tests after the work items 1.8/1.9 reconciliation and hardening passes, covering thin/full artifact rules, canonical statuses, placeholder-mode enum enforcement, no-spec-change handling, missing requirement scenarios, missing traceability rows, pending downstream link handling before/archive readiness, practical thin archive evidence, waiver validation, waiver-to-traceability matching, risky thin-package trigger rejection, staged discovery, and placeholder mode; `pytest.ini` uses repository-local `.pytest-tmp` because the default Windows temp pytest directory is not accessible in this environment |
| Template validation | After work item 1.8, `python scripts/validate_change.py --allow-placeholders templates/change` passed, and `python scripts/validate_change.py templates/change` rejected placeholder values as expected |
| OpenSpec CLI installed | `openspec --version` returned `1.4.1` |
| OpenSpec validation | During the Phase 1 archive batch on 2026-07-09, `openspec archive <change> -y` promoted all 8 readiness-complete changes. After the archive, `openspec list` reported no active changes, `openspec list --specs` reported 8 accepted specs, and `openspec validate --all --strict` passed all 8 specs with 0 failures. |
| Phase 2 OpenSpec proposal validation | After `D-020`, `openspec list` reports 35/36 transfer-package tasks and 42/43 NIS-governance tasks; only Phase 3 tasks 7.5 and 8.8 remain. |
| Phase 2 work item 2.1 | Closed after package/schema/template implementation, task review, architecture approval, and fresh verification: 15 focused tests, 49 full tests, legacy template validation, strict OpenSpec 10/10, and clean range diff. Evidence: `docs/phases/PHASE_2_EVIDENCE_INDEX.md`. |
| Phase 2 work item 2.2 | Closed after deterministic config discovery/compatibility implementation and three bounded review-fix waves. Final evidence: 39 focused tests, 88 full tests, 18 selected negative cases, central plus sibling/path/registry adapter CLI checks, task-review and architecture approval, strict OpenSpec 10/10, clean range/Git inventory, and no tracked local reports. Evidence: `docs/phases/PHASE_2_EVIDENCE_INDEX.md`. |
| Roadmap/OpenSpec governance linkage | The mandatory post-2.2 status audit preserved a 33-error, 0-warning validator RED baseline at `2579369`; the metadata repair removed those errors. The 2026-07-18 validator reports 0 errors and 2 explicit lifecycle warnings because both remediation changes have all tasks checked without human acceptance/lifecycle disposition. |
| NIS governance OpenSpec proposal validation | Strict validation passes; 42/43 tasks are implemented and only Phase 3 task 8.8 remains unchecked. This proves implementation and planning-contract validity, not accepted-spec promotion. |
| Pre-commit installed | Not available on PATH during Phase 1 artifact work; config is present but end-to-end hook execution still needs tool installation |
| Local app/server available | No local app/server found; this work item is script/template based |
| Documentation bootstrap | `project-starter-kit` created the repository operating/docs structure; repository-local `.codex/skills/` is intentionally absent because workflow skills are global |
| Starter structure check | `python "$env:USERPROFILE/.codex/skills/project-starter-kit/scripts/bootstrap_project.py" --target . --check` passed |
| Markdown/code whitespace check | `rg -n "[ \t]+$" AGENTS.md docs openspec templates scripts tests .pre-commit-config.yaml pytest.ini .gitignore` returned no matches |

## Known Risks And Gaps

| ID | Risk | Owner | Status |
|---|---|---|---|
| AUDIT-001 | Product scope and first-MVP boundaries are captured by accepted Phase 1 living specs after the 2026-07-09 Option A archive batch. Future corrections must be made through new OpenSpec changes over the accepted baseline. | Phase 1 | closed |
| AUDIT-002 | Environment and verification commands are now recorded for the Python/OpenSpec process package, Windows full rehearsal, and Linux/WSL2 portability smoke; real corporate integration/runtime values remain Phase 3 inputs. | Phase 1/2 | closed |
| AUDIT-003 | Historical architecture draft was removed after current decisions were captured in `docs/` and OpenSpec. Phase 1 accepted living specs now exist after the 2026-07-09 archive batch. | Phase 1/2 | closed |
| AUDIT-004 | This folder was initialized as a git repository, connected to the configured `origin`, committed, and pushed to `origin/main`. | Human/Phase 0 | closed |
| AUDIT-005 | OpenSpec folder structure for this CLI project's own requirements is initialized and now includes accepted spec `openspec/specs/change-package-foundation/spec.md`; the original `add-change-template-validation` change is archived. | Phase 1 | closed |
| AUDIT-006 | Placeholder corporate repo/owner/Jira/Confluence/Jenkins examples from the removed historical draft must not be treated as real configuration. Current docs still forbid inferring real corporate configuration from examples. | Phase 1/2 | closed |
| AUDIT-007 | Corporate environment specifics are unverified: available Qwen/DeepSeek/GigaCode model and adapter capabilities, MCP policy, Bitbucket/Jenkins/Jira/Confluence versions, secrets handling, and network/artifact restrictions. Phase 2 must prepare the inventory and compatibility checks; Phase 3 must execute them before the real pilot. | Phase 2/3 | open |
| AUDIT-008 | Automated local MCP server provisioning for employees is an untested experiment; manual setup remains the documented fallback until proven. | Later phase | open |
| AUDIT-009 | `pre-commit` is not installed on the current machine, so the hook config cannot yet be executed end-to-end locally. | Phase 1/local environment | open |
| AUDIT-010 | The generated Confluence publication model is planned, and the 2026-07-09 decisions accept analyst/change-owner triage, blocker/non-blocker comment handling, explicit dispositions, editable/disableable triage SLA defaults (1 working day for blockers, 3 working days for non-blockers), generated source warnings, and evidence-backed status display. Publication automation still remains outside the first MVP; the first generated view set is intentionally decided later inside the corporate environment using real templates, approval practices, and tooling constraints. | Phase 1/4 | open |
| AUDIT-011 | Journey and screen artifacts are now planned future contracts, but `journey.yaml`, `screens.yaml`, screen asset storage, and generated gallery views are not implemented or validated. | Phase 1/4 | open |
| AUDIT-012 | Legacy baseline mode is planned for already-written code, but no accepted workflow or template exists yet for baseline changes, observed behavior, known gaps, or legacy coverage risk reporting. | Phase 1/4 | open |
| AUDIT-013 | `D-022` makes Russian the language for new project documentation and OpenSpec prose while preserving stable English technical tokens; historical immutable evidence is not bulk-translated. A future glossary or translation-review process is optional usability work, not a blocker for the canonical language rule. | Phase 3/5 | mitigated |
| AUDIT-014 | The minimum weak-model operating kit and adapter `2.0` boundary are implemented: deterministic launcher, authority-labelled bounded read packs, generated closed role schemas, reasoning/final separation, mechanical normalization, one structural retry rule, analyst/developer/QA/Tech Lead instructions, evidence boundaries, negative cases, and AI-disabled fallback. The adapter `2.0` Qwen and DeepSeek remediation evidence is retained honestly at 0/5 per family with no retries and no matrices; fallback-only acceptance remains superseded. Broader project-map, graph/navigation, repeated-error-memory, and spec-questioning automation remains deferred to Phase 4. | Phase 2/4 | open |
| AUDIT-015 | Source ownership and write-once/reference-many documentation rules are captured in the accepted documentation-governance baseline, but deterministic linting for duplicate normative text, source links, generated blocks, stale memory, and orphan docs is not implemented yet. | Phase 1/4 | open |
| AUDIT-016 | Work item 1.8 and its review-finding follow-up reconcile the deterministic layer with the approved Phase 1 contracts: `scripts/validate_change.py` rejects the historical status vocabulary in favor of the canonical six states, keeps thin packages lightweight by default, enforces the approved full-package trigger matrix for risky thin changes, validates placeholder-mode enum structure, requires traceability waivers to match the affected requirement/scenario and evidence kind, validates canonical human approver keys or owner-group references, preserves staged discovery behavior, and `templates/change/change.yaml` no longer defaults to the contradictory `mode: thin` + `type: new_feature` combination. Work item 1.9 then hardened the evidence with explicit tests for missing requirement scenarios, missing traceability rows, pending downstream link lifecycle handling, and thin archive-ready practical verification evidence. See `docs/audits/FABLE5_DOCUMENTATION_ARCHITECTURE_REVIEW_2026-07-06.md` finding F1. | Phase 1 (work items 1.8/1.9) | closed |
| AUDIT-017 | OpenSpec `1.4.1` is pinned and enforced by the reviewed central/project discovery and compatibility validator. Work item 2.2 verifies config/package/adapter versions, the exact runtime, local-only schema graphs, registries, secrets, and human/JSON diagnostics before mutation. | Phase 2 (work item 2.2) | closed |
| AUDIT-018 | Analytics-source readiness is partially resolved: the language decision is made (Russian prose, English keywords/IDs), the corporate approval template is fully analyzed with a migration plan in `docs/planning/ANALYTIC_TEMPLATE_STRUCTURE_AND_MIGRATION_PLAN_2026-07-06.md`, and the 2026-07-09 decisions keep the existing Confluence analytics corpus as a read-only archive, avoid bulk migration for the first pilot, use Git-managed source or source+export with stable IDs for accepted diagrams/screens, and keep approval readiness minimal/validator-backed for now. Still open: concrete future schemas and validator checks for typed analytics artifacts and asset metadata. Local photos of the template live in git-ignored `arch-screenshots/analytic-template/` and must never be committed. | Phase 1/4 | open |
| AUDIT-019 | Screenshots of an internal OpenSpec customization / repository-topology approach are available locally in git-ignored `arch-screenshots/openspec-de/`; they were reviewed on 2026-07-09 against the product goal, thin-MVP boundary, analytics-template mapping, and work item 1.4 criteria. The review is captured in `docs/planning/OPENSPEC_DE_INTERNAL_SOLUTION_ANALYSIS_2026-07-09.md` with the criteria frame in `docs/planning/REPO_TOPOLOGY_EVALUATION_CRITERIA_2026-07-09.md`, and the recommendations are now routed into `define-repo-topology-config`, `define-change-artifact-contracts`, `define-change-lifecycle`, and weak-model planning docs. Binding topology/config/OpenSpec-version decisions were approved at gate 1.5 on 2026-07-09. | Phase 1 (work items 1.4/1.5) | closed |
| AUDIT-020 | Transfer readiness is explicitly defined. `D-020` accepts exact rc6 and closes Phase 2. Historical adapter `1.0`/`2.0`/`2.1` failures and candidates `phase-2-12-rc7`, rc2, rc3, rc4, and rc5 remain preserved according to their actual outcomes. Transfer progress is 35/36; no real corporate pilot was executed, and the local owner walkthrough gates corporate entry. | Phase 2/3 | closed |
| AUDIT-026 | Actual-certification execution now binds a fresh full model digest and Ollama runtime version from an immutable runtime-identity catalog into preflight evidence and re-probes immediately before every matrix model call. All phase raw/result destinations fail closed before side effects unless they are new, external, non-aliased, non-reparse, non-overlapping paths under one artifact root. Historical raw and normalized evidence remains unchanged and validation-compatible. Ollama tag invocation is not digest-addressed, so a residual observation-to-call race remains documented. | Phase 2.11 | mitigated |
| AUDIT-024 | Adapter `2.0` and `2.1` are immutable failed historical attempts. Adapter `2.2` resolves their operational ambiguity without weakening human authority; `simplify-weak-model-decision-contract` remains blocked and unpromoted because its own contract did not certify. | Phase 2.11 | mitigated |
| AUDIT-025 | The 2026-07-17 ambiguity finding is resolved for the supported catalog. An identity-bound deterministic plan owns routing metadata; the model supplies only source-linked branch content; field-scoped authority checks accept safe human-handoff language and reject positive model authority. Both frozen families passed 5/5 and 15/15, AI-disabled passed 11/11, and no classifier agent, semantic retry, generic rules engine, or parallel documentation hierarchy was added. | Phase 2.11 | closed |
| AUDIT-021 | `D-013` accepts the NIS-aligned target process. Work items 2.7 and 2.8 completed check-only flow enforcement, QA authority, scoped exceptions, release handoff, role/WIP/pilot-safety checks, append-only failed-run retention, packaged workflow operations, and broader traceability without replacing human decisions or mutating external state. Real corporate wiring and pilot execution remain Phase 3 work. | Phase 2/3 | mitigated |
| AUDIT-022 | `D-014` makes AI-disabled deterministic operation the first required delivery state and permanent fallback, not the final AI-minimal product direction. Later accepted changes are expected to progressively automate bounded orchestration, drafting, evidence assembly, routing, monitoring, tool coordination, and permitted transition preparation while deterministic checks remain the control plane and accountable human authority remains explicit. Presentation-facing and project-direction documentation now carry this two-horizon message; implementation of the later horizon remains future scope. | Phase 2/4 | open |
| AUDIT-023 | `D-016` makes broader risk-oriented positive/negative testing and end-to-end requirement/scenario evidence traceability explicit reliability mechanisms, and safe parallel AI execution an explicit throughput mechanism. The transfer change now requires independent ownership/write scopes, separate evidence, serialization of conflicts, and a deterministic combined integration gate. This is not the excluded process-effectiveness measurement program. | Phase 2/4 | open |
| AUDIT-027 | Rc4 contains the immutable historical `204 covered / 110 gaps / 20 future_work` report; its uniform residual metadata is a mechanical fallback, not an individual risk assessment. Package `0.3.0` binds 68 Phase 2 selectors to exact test evidence, 22 governance rows to primary decisions/audits, 12 Phase 3/4 rows to `future_work`, and the first-MVP boundary to `D-019`. Candidate rc6 certifies `295/7/32` and is accepted under `D-020`. | Phase 2/3/4 | closed |
| AUDIT-028 | The 13 product gaps were normalized into six intake groups. Delta semantics, archive history, and reviewed upgrade evidence are implemented and certified in package `0.3.0` with six exact tests. Feedback disposition is deferred to P4, CODEOWNERS derivation/validation to P3, and AI traceability suggestions plus legacy baseline onboarding to P4; all seven deferred selectors remain visible gaps. Immutable rc6 passed full verification and independent review and is accepted under `D-020`. | Phase 2/3/4 | mitigated |
| AUDIT-029 | The 2026-07-21 read-only GigaCode audit found that the documented guided flow is not enforced end to end: unknown role is not a validator stop, human and AI role vocabularies diverge, the implementation next action is role-neutral, acceptance provenance is reducible to an AI-writable YAML constant, spec readiness checks are incomplete, and the response-summary check does not prove what the human saw. `D-024` accepts remediation through a new P3 OpenSpec change; current successor evidence must not be used to claim this observed path is already safe. | Phase 3 | open |
| AUDIT-030 | `D-025` makes typed analytics persistence and screen/journey/integration source contracts part of pre-corporate framework readiness. The detailed corporate-template analysis and 38 git-ignored source photos are retained, but `process/schemas/` and `process/templates/` still lack status-model, channel-support, data-model, platform-services, journey, screen, and integration-descriptor contracts; `templates/team-specs/analytics/` contains only `.gitkeep`. New OpenSpec design, deterministic validators, fixtures, and one sanitized end-to-end example are required. | Phase 3/4/5 | open |
| AUDIT-031 | The exact new-chat transcript, raw GigaCode UI payload, and current change package for the payment-screen requirement were not found in the sandbox root or Git path history. The historical audit proves that an earlier `change-001` package was inspected, but it is not a substitute for the missing source content. Any detailed reconstruction of those payment screens remains `unverified` and must be re-supplied or recovered from an authoritative human/chat export. | Phase 3 | open |

## Accepted Human Decisions

Canonical decision IDs now live in `docs/DECISIONS.md`. The table below remains an audit-oriented summary for local context; when another durable doc needs to point at a specific accepted decision, reference the stable ID from `docs/DECISIONS.md`.

| Date | Decision | Impact |
|---|---|---|
| 2026-07-03 | Narrow the first MVP to `sdd change new`, `sdd change validate`, `sdd change pr`, `sdd change archive`, and basic `traceability.yaml`. | Phase 1/3 plans must not require Jira, QA/AT, Confluence publication, or role inboxes for the first usable workflow unless explicitly re-scoped. |
| 2026-07-03 | Use two Phase 1 change modes: `thin change` and `full change package`. | Historical/current implementation decision; `D-013` replaces the target vocabulary and matrix through migration to minor/major/hotfix. |
| 2026-07-03 | Formalize product OpenSpec specs first for change lifecycle, artifact contracts, traceability, and waiver behavior. | Phase 1 OpenSpec work should prioritize these specs before broad integration specs. |
| 2026-07-03 | Specify the Confluence feedback loop before implementing publication automation. | Future Confluence work must define owner, service expectation, unresolved-feedback handling, and accepted/rejected comment outcomes. |
| 2026-07-03 | Design mutating CLI/integration commands with dry-run, idempotency, JSON output, and audit logs. | Phase 2 architecture and later tests must cover these command contracts. |
| 2026-07-03 | Do not require Gherkin for every QA artifact; require at least a testable scenario, with Gherkin only for executable/exported scenarios. | Phase 1/QA artifact contracts must avoid unnecessary Gherkin bureaucracy. |
| 2026-07-03 | Deliver the SDD process without a custom `sdd` CLI first (deterministic scripts/templates in `team-specs` + standard tool features + AI role skills); build CLI parts only on the triggers in `docs/IMPLEMENTATION_STRATEGY.md`. | Phase plans must target templates, validation scripts, skills, and pipelines instead of CLI source code until a trigger fires. |
| 2026-07-03 | OpenSpec = Fission-AI/OpenSpec with team reference docs at <https://lzw.me/docs/openspec>; pin the CLI version. | Phase 1 must record the pinned version; upstream docs win over the mirror on discrepancy. |
| 2026-07-03 | Jira/Confluence access from AI tooling via MCP only (verified working by the human owner); no custom REST clients; automating local MCP server provisioning is a planned experiment. | Integration specs must define MCP usage boundaries, not API client contracts. |
| 2026-07-03 | Develop in the external environment (Claude Code) first, then transfer to the corporate environment where only GigaCode CLI was then expected. | Gates must never depend on the AI layer; skills stay tool-agnostic; the later `D-012` decision refines the target assistant set to Qwen/DeepSeek/GigaCode-class tools and requires an accepted external release candidate before adaptation. |
| 2026-07-03 | The first Phase 1 artifact is `templates/change/` + `scripts/validate_change.py` + `.pre-commit-config.yaml`, on branch `phase-1/change-template-validation`, tracked by OpenSpec change `add-change-template-validation`. | Phase 1 starts with deterministic templates and validation before broader specs, integrations, or custom CLI work. |
| 2026-07-06 | Approve the Phase 1 risk-oriented thin/full artifact matrix default. | Valid historical/current implementation evidence; `D-013` replaces the target matrix with class-aware minor/major/hotfix contracts after implementation and accepted-spec promotion. |
| 2026-07-06 | Approve role-appropriate waiver approvers and minimum evidence. | Waivers require the responsible role owner, affected requirement/scenario, reason, substitute evidence, and follow-up/expiry when residual risk remains. |
| 2026-07-06 | Reconfirm Jira task automation, Confluence publication, QA/AT proposal generation, and role inboxes outside the first MVP, with the rest planned as later layers. | Phase 1/3 must not implement those integrations in the thin MVP; Phase 1 may define proposals and future contracts for them. |
| 2026-07-06 | Treat Confluence as generated publication/read model with audience-oriented pages, source metadata, warnings, and links back to Git/OpenSpec; do not create a separate canonical MasterSpec. | Confluence publication proposals must generate views from living specs/change packages and route accepted feedback back through Git/OpenSpec. |
| 2026-07-06 | Use English for canonical OpenSpec sources and stable IDs by default; generated Confluence views may be localized in Russian. | Documentation governance must preserve stable IDs, route Russian feedback back into English source changes, and plan a bilingual glossary. |
| 2026-07-06 | Plan legacy baseline mode for already-written code. | Old behavior is documented gradually; full retroactive change packages are not required for historical changes, but touched legacy behavior needs observed/current behavior, proposed change, regression scenario, known gaps, and UI screenshots when affected. |
| 2026-07-06 | Remove stale historical architecture draft from the repository. | Current architecture truth is `docs/`, `openspec/`, and accepted human decisions; agents must not use a parallel architecture file as a source of truth. |
| 2026-07-06 | Adopt the project memory triad as the future orientation model: constitution/quality policy, project map, and OpenSpec changes/living specs. | Phase 1/2 should plan memory boundaries and validation so project memory helps agents and humans orient without becoming a second behavior source of truth. |
| 2026-07-06 | Formalize existing-code onboarding as `scan -> baseline -> map -> validate`. | Future legacy onboarding should keep scan read-only, record observed behavior/gaps/risks, update project memory, and validate memory against real code evidence. |
| 2026-07-06 | Plan `sync` and `upgrade` as deterministic maintenance, not AI-only skills. | Sync should detect drift across project map, specs, traceability, and code evidence; upgrade should migrate templates/spec-package versions only after the OpenSpec version policy is approved. |
| 2026-07-06 | Use a PDLC narrative when presenting the process to the team. | The process should be explained as shared context from analysis through tasks, tests, verification, and publication, not merely faster code generation. |
| 2026-07-06 | Keep deploy, Zephyr/test-management integration, Jira task automation, Confluence publication, QA/AT proposal generation, and role inboxes outside the first MVP. | Phase 1/3 must not make those integrations first-MVP blockers unless the human owner explicitly re-scopes the pilot. |
| 2026-07-06 | Record Graphify-like navigation, documentation boundary, weak-model support, repeated-error memory, spec-questioning, and QA/analyst usability as mandatory planning input. | Future project-memory or weak-model proposals must start from `docs/planning/PROJECT_MEMORY_AND_WEAK_MODEL_GUARDRAILS.md` before choosing schemas, tools, skills, or implementation scope. |
| 2026-07-06 | Use source ownership and write-once/reference-many rules to prevent OpenSpec/docs/memory drift. | OpenSpec owns behavior and acceptance; `docs/` owns context, rationale, phase planning, and audit; `AGENTS.md` owns agent operating rules; derived views, role guides, read packs, and project memory must reference canonical sources and be fixed or regenerated when they drift. |
| 2026-07-06 | Adopt the six internal lifecycle states (`draft`, `spec_review`, `approved`, `in_implementation`, `ready_to_archive`, `archived`) as canonical for accepted specs and deterministic validation. | Work item 1.8 reconciles the validator status vocabulary to the canonical six states; simplified lifecycle names may appear only in generated business-facing views. |
| 2026-07-06 | Enforce the approved artifact matrix and waiver checks as errors immediately in work item 1.8. | No warnings-only staging period; the expanded validator rejects non-compliant packages as soon as work item 1.8 lands. |
| 2026-07-06 | Create `docs/DECISIONS.md` as the single canonical decision log with stable decision IDs at Phase 1 acceptance readiness. | Executed in work item 1.10; see `docs/DECISIONS.md` (`D-006`). |
| 2026-07-06 | Merge the OpenSpec version pin/upgrade policy into the `define-repo-topology-config` proposal. | Work item 1.4 drafts one merged platform-assumptions proposal; decision gate 1.5 covers topology, config format, and version pin/upgrade policy together. |
| 2026-07-06 | Adopt team-facing terminology `Master Spec` (accepted living specs) and `Delta Spec` (proposed change spec deltas). | Glossary updated; canonical folder names and OpenSpec CLI terms unchanged; generated-view term renamed to `Master Spec views` to avoid collision. |
| 2026-07-06 | Treat reusability by other teams as an explicit design constraint for the repo topology/config proposal. | Work item 1.4 must show how another team bootstraps the deterministic base, templates, and skills without copying this project's history; first MVP scope is not expanded. |
| 2026-07-06 | Team product analytics specs use Russian prose with English structural keywords and English stable IDs; this project's process specs stay English. | Revises part of the earlier English-canonical decision; documentation-governance canonical-language requirement updated; bilingual glossary (AUDIT-013) remains required; analyst style guide must encode the mixed-language convention. |
| 2026-07-09 | Approve gate 1.5 recommended defaults: central `team-specs`, central config plus optional project adapter, OpenSpec `1.4.1` central pin with reviewed upgrades, one versioned process package, and `owners.yaml` as owner source. | Work item 1.8 template/validator reconciliation is no longer blocked by topology/config/version decisions; production `team-specs` setup still needs to create the actual config and package files later. |
| 2026-07-09 | Existing Confluence analytics corpus is a read-only archive for the first pilot; no bulk migration is required. | Reused legacy material must become new Git/OpenSpec source through a reviewed change instead of being edited in Confluence as canonical source. This interpretation was confirmed after the decision summary. |
| 2026-07-09 | Accepted diagrams, journey schemes, and screen assets use Git-managed source or source+export with stable IDs; Confluence drawings are drafts until exported or recreated into that flow. | Visio is allowed as one source format when practical, but not required; diagram-as-code, diagrams.net/draw.io source, Figma exports, or another agreed source+export pair can satisfy the rule if versioned and traceable. |
| 2026-07-09 | Confluence feedback uses analyst/change-owner triage, explicit dispositions, blocker/non-blocker behavior, and editable/disableable triage SLA. | Default triage SLA is 1 working day for blockers and 3 working days for non-blockers; later Confluence-enabled publication/archive is blocked by unresolved blocker comments; non-blockers may continue only with accepted/rejected/deferred/duplicate disposition. |
| 2026-07-09 | Project memory/weak-model defaults: memory follows the future `team-specs` topology, first graph/navigation is a lightweight deterministic index, mandatory pilot guardrails are read packs/role skills/evidence checklists, and the initial Phase 1 guide concept used analyst/developer/QA thin-change walkthroughs. | `D-013` supersedes the target guide set with class-aware analyst/developer/QA/Tech Lead walkthroughs; broader memory tooling remains later scope. |
| 2026-07-09 | Generated-view selection for the first Confluence-enabled workflow is deferred to the corporate environment. | See `docs/DECISIONS.md` (`D-010`). The external planning repo records source-of-truth and feedback contracts, but the actual view set depends on real corporate templates, approval practices, and tooling constraints. |
| 2026-07-09 | Accept the whole Phase 1 readiness-complete OpenSpec package and archive/promote all eight changes in one batch execution step. | See `docs/DECISIONS.md` (`D-011`). Future changes now build on accepted specs in `openspec/specs/`; publication automation remains a later layer, not implemented by this archive. |
| 2026-07-13 | Require an externally certified transfer-ready release candidate before corporate adaptation, and keep roadmap/phase/OpenSpec planning free of delivery dates or calendar deadlines. | See `docs/DECISIONS.md` (`D-012`). Phase 2 owns reusable core, deterministic gates, bootstrap/update/rollback, weak-model operating kit, actual Qwen/DeepSeek and AI-disabled certification, and transfer evidence; Phase 3 owns real configuration, approved wiring, thin adapters, and the monitored pilot. |
| 2026-07-13 | Adopt the NIS corporate process as target behavior with flat `minor|major|hotfix`, class-aware readiness/completion, Tech Lead governance, corporate flow controls, pilot safety, and failed-run retention; migrate legacy thin/full and exclude process-effectiveness measurement. | See `docs/DECISIONS.md` (`D-013`) and `docs/planning/NIS_CORPORATE_PROCESS_ADOPTION_PLAN_2026-07-13.md`. PPRB structure, NIS repository layout, comparison methodology, and effectiveness metrics remain excluded; AI is advisory and hotfix cannot bypass minimum safety or reconciliation. |
| 2026-07-14 | Adopt two automation horizons: first prove the complete process without AI, then progressively automate bounded process work with AI after the process and pilot are stable. | See `docs/DECISIONS.md` (`D-014`). Deterministic checks remain the control plane and permanent fallback; human approvals and accountable decisions do not transfer implicitly. |
| 2026-07-14 | Repair Phase 2 with clean renumbering from `2.3`, keep both active changes open through Phase 3, store normalized evidence in Git and raw outputs in a versioned artifact, make the human owner the final external acceptor with role evidence, use the risk-oriented Qwen/DeepSeek matrix, and initially target Windows, Linux, and macOS with prerequisites and MCP provisioned. | See `docs/DECISIONS.md` (`D-015`). `D-017` subsequently accepted the corrected plan; `D-018` later narrowed certification to Windows plus Linux/WSL2 and made macOS explicitly not certified. |
| 2026-07-14 | Increase reliability through broader risk-oriented tests and traceability, and increase speed through safe parallel AI work on independent tasks. | See `docs/DECISIONS.md` (`D-016`). Parallel tasks require explicit dependencies, owners, write scopes, evidence, and combined deterministic integration checks; process-effectiveness measurement remains excluded. |
| 2026-07-14 | Accept the corrected Phase 2 plan and authorize implementation from work item 2.1. | See `docs/DECISIONS.md` (`D-017`). At acceptance time Phase 2 and 2.1 became `ready`; by the 2026-07-15 baseline checkpoint, work items 2.1-2.10 were `closed` and 2.11 was `pending_acceptance`. The 2026-07-16 decision below records the later lifecycle change. |
| 2026-07-16 | Reject fallback-only acceptance of the first weak-model baseline and adopt bounded Qwen/DeepSeek adapter remediation now. | Work item 2.11 returns to `in_progress`; task 4.5 and the 2026-07-15 audits remain immutable baseline history; new transfer tasks 4.7-4.9 own the role-specific schema, reasoning/final boundary, mechanical normalization, bounded retry, preflight gate, and append-only recertification. Work item 2.12 remains blocked and Phase 3 does not start. |

## Audit Rules

- Update this file when a finding is fixed, invalidated by evidence, or moved.
- Do not mark a finding closed without verification evidence.

## 2026-07-20 Guided Owner Workflow Implementation Checkpoint

- Status: implementation in progress; OpenSpec tasks 1.1-3.3 are complete, while verification/release tasks 4.1-4.4 remain open.
- Evidence: focused RED/GREEN tests cover declared new-requirement (minor and major), existing-change missing context, urgent-hotfix fallback, blocked/unknown situations, undocumented command rejection, AI-owner rejection, guide/catalog drift checking, CWD-independent validation, and package/bootstrap integration.
- Deterministic checks: `openspec validate --all --strict` passed 14/14; roadmap/OpenSpec validation reported zero errors and two historical lifecycle warnings for unrelated changes.
- Residual verification: synthetic full-route evidence, actual available-model exercises, successor package version/release evidence, update/rollback rehearsal, and final documentation reconciliation remain required before Phase 4 corporate adaptation.
- Environment note: the original system Python runtime became unavailable during this session. Focused tests were run with the Codex bundled Python after installing the pinned test dependencies; no project dependency files changed.

## 2026-07-20 Guided Companion Agent Rule Intake

- Idea: agents must actively orient humans through the project, explain criteria/process mapping and decision reasoning, verify proportionately, expose gaps and risks, recommend the next action, and remain advisory at human decision boundaries.
- Source: human owner request on 2026-07-20.
- Type: documentation change; verification change.
- Decision: adopt now.
- Reason: it clarifies durable internal agent behavior without changing the external SDD CLI contract or transferring authority from the human.
- Canonical implementation: `AGENTS.md` owns the concise responsibility rule; `docs/AI_STEP_VERIFICATION_CHECKLIST.md` owns the operational reporting and verification checklist; `docs/CONTEXT.md` defines the term.
- Verification impact: substantive reports must map applied criteria to their sources, record evidence and limitations, state residual gaps, and recommend the next useful human action.
- Status: recorded and active.

## 2026-07-21 GigaCode And Framework-Readiness Intake

### Role-aware guided workflow remediation

- Idea: make the documented role, stage, summary, literal human evidence, and one-next-step rules mechanically enforceable in GigaCode and AI-disabled operation.
- Source: owner walkthrough and read-only sandbox audit on 2026-07-21.
- Type: `workflow_behavior_rule`, `artifact_contract`, `acceptance_criterion`, `verification_step`, `rejected_behavior`.
- Decision: `create_openspec_change`.
- Primary roadmap phase: P3; related phases: P4, P5.
- Reason: the current implementation permits a role-neutral implementation action and self-declared acceptance evidence even though prose forbids both. This changes externally visible workflow behavior and cannot be fixed as docs-only guidance.
- Human decision: `D-024` accepts the remediation direction. The new change must still present the exact role mapping, evidence schema, revision binding, UI contract, and negative scenarios for review before implementation.
- Status: active P3 OpenSpec `harden-role-aware-guided-workflow`; the local role/readiness and decision-card contract is implemented and independently reviewed, while controlled package transfer and human acceptance remain open.

### Typed analytics, integration, journey and screen framework

- Idea: promote the retained analytics-template plan into a working external artifact framework with typed storage, conditional schemas, templates, validators, integration descriptors, journey/screen catalogs, stable assets, and one sanitized business-requirement-to-review example.
- Source: owner clarification on 2026-07-21 plus `docs/planning/ANALYTIC_TEMPLATE_STRUCTURE_AND_MIGRATION_PLAN_2026-07-06.md`.
- Type: `scope_refinement`, `architecture_note`, `artifact_contract`, `data_contract_change`, `integration_change`, `verification_request`.
- Decision: `create_openspec_change`.
- Candidate primary roadmap phase: P3 for reusable external contracts and deterministic sample rendering; related phases P4 for approved live wiring and P5 for post-pilot generated-view expansion.
- Reason: `AUDIT-011` and `AUDIT-018` correctly record the concept, but no working schemas/templates/validators exist. Reusable design must be completed outside the corporate environment; real service values and mutations must remain corporate evidence.
- Human decision: `D-025` accepts that these contracts are part of framework readiness. One design boundary remains to be reviewed explicitly: whether P3 delivers only deterministic sample rendering or a broader operator-facing UI/gallery before the pilot.
- Human decision: `D-026` selects the local end-to-end P3 vertical slice and excludes MCP completely. Integration descriptors remain passive data contracts with manual evidence points; they do not configure or call Jira, Confluence, Bitbucket, or Jenkins.
- Existing conflict to resolve in the future OpenSpec change: `process/catalogs/guided-owner-workflow.yaml` still declares an `mcp` unavailable-surface fallback and `docs/runbooks/GUIDED_OWNER_WORKFLOW.md` still names MCP. P3 remediation must remove those dependencies from the local route and its verification without deleting the separate P4 corporate-environment inventory contract.
- Role evidence: neither the current chat nor an allowed `.ai-session.local.md` supplies the human role. `D-024`-`D-026` therefore record confirmed design direction and constraints, not a role-specific Spec Review, DoR, implementation, release, or archive decision.
- Status: accepted intake and delivery boundary; human role plus detailed design review remain required before role-gated OpenSpec acceptance or implementation planning.

### Распространение package-managed GigaCode-шаблона

- Идея: не допустить расхождения между исправленными в sandbox role-gate инструкциями и reusable process package.
- Источник: последующее действие после одобренного владельцем sandbox-hotfix 2026-07-21.
- Тип: `scope_refinement`, `documentation_change`, `verification_change`.
- Решение: `adopt_now` в `harden-role-aware-guided-workflow` / P3.
- Результат: `process/gigacode/` — канонический источник; bootstrap устанавливает два declared-файла, а update fail-closed блокирует конфликтующий локальный managed-файл, не затрагивая другое содержимое `.gigacode`.

## P3 Chat Decision and Discovery Intake (2026-07-21)

- Human decision adopts `adopt_now` remediation for the confirmed `payments-screen` audit findings: P3 will use a two-step `DEC-…` decision card, accept an active-card short `Подтверждаю`, preserve both verbatim human messages and revision binding, and never derive authority from AI-authored YAML/status text.
- In `обычно` intake mode, GigaCode must proactively recommend deeper discussion when a material change-specific unknown affects behavior, scope, UX, runtime, risk or verification. Silence does not accept a default or allow a readiness claim.
- Local form/command is explicitly deferred as a future stronger producer of the same confirmation-event contract; it is not a P3 dependency.
- The 2026-07-23 owner-approved extension adds a non-authoritative operation-confirmation request/event contract binding trusted role, operation ID, ordered input digest, revision digest, event chain, and expiry. It does not enable `sdd run`; trusted ingress and replay protection remain future execution-enablement work, while `mutate_external` remains forbidden in P3.
- Evidence: `sdd-workflow-playground/docs/audits/PAYMENTS_SCREEN_GUIDED_PACKAGE_AUDIT_2026-07-21.md`; execution scope: `harden-role-aware-guided-workflow`.
