# Project-Wide Implementation And NIS Audit

Status: completed read-only audit on 2026-07-22. Remediation is not included.

## Purpose, Boundary, And Criteria

This audit covers all tracked `docs/`, phase plans, accepted OpenSpec specs, active changes, `process/`, `scripts/`, templates and tests. It distinguishes accepted behavior, active/proposed behavior, partial implementation, deferred scope and historical evidence. Checked tasks do not imply human acceptance. No corporate system, credential, MCP surface, raw model transcript or external installation was mutated.

Criteria: source ownership must be explicit; Roadmap/phase/OpenSpec/repository status must agree; claimed deterministic controls need inspectable evidence; NIS is assessed only through `D-013` and its adoption plan; findings are classified as pass, limitation, verified drift, verified defect or unverified suspicion.

## Evidence

| Check | Result |
|---|---|
| Git | Clean worktree before audit; branch `phase-3/p3-vertical-slice`. |
| OpenSpec | 8 accepted specs, 9 active changes; `openspec validate --all --strict`: 17 passed, 0 failed. |
| Roadmap/OpenSpec validator | 0 errors; 2 valid lifecycle warnings: complete `determinize-weak-model-operational-decisions` is still `in_progress`, and complete `simplify-weak-model-decision-contract` is `blocked`. |
| Focused P3 tests | `tests/test_p3_vertical_slice.py` + `tests/test_guided_owner_workflow.py`: 18 passed. |
| Complete owned suite | `python -m pytest -q tests`: 742 passed, 18 failed, 4 skipped in 274.93 seconds. |
| Root pytest | `python -m pytest -q` produced 25 collection errors from ignored historical `tmp/pytest-*` evidence directories before owned tests ran. |

## Delivered From The Original SDD Direction

| Capability | State | What it does and how it changes human work | See without scripts |
|---|---|---|---|
| Git/OpenSpec as source of truth | accepted | Git/OpenSpec owns behavior and acceptance; Confluence is only a future generated read model and tracker is status. A person reviews Delta Specs/PRs, not AI prose or editable pages as truth. | `docs/CONTEXT.md`, `openspec/specs/`. |
| Change packages, Delta Specs and traceability | accepted | Creates one reviewable proposal/design/tasks/spec/QA/traceability package and rejects missing core evidence. Analysts, developers and QA work from the same linked source. | `templates/change/`, accepted artifact and traceability specs. |
| Lifecycle and human approvals | accepted baseline | Deterministic checks expose evidence for six lifecycle states but cannot approve, merge or archive. Green output is evidence, never authority. | `openspec/specs/change-lifecycle/spec.md`, archive packets. |
| Waivers and source-linked gaps | accepted | Exceptions require structured reason, suitable human owner, residual risk and follow-up; AI cannot approve them. | waiver spec and `templates/change/waivers.yaml`. |
| Transfer-ready deterministic package | rc6 `0.3.0` accepted under `D-020` | Packages schemas, policies, templates, bootstrap/update/rollback, role guides, read packs and certification. Another team can inspect it before real corporate values exist. | rc6 manifest/evidence YAML and transfer runbooks. |
| Weak-model + AI-disabled guardrails | rc6 implementation certified; lifecycle proposal open | A model gets bounded source-labelled context, one role stage, output contract and stop point; failed attempts stay visible. The human retains every gate. | `process/roles/`, `process/read-packs/`, certification evidence. |
| Guided owner workflow | first slice accepted | Maps a business situation to only catalog-declared next commands, blocks, fallback and human decision owner. A colleague can orient without inventing a flow. | `docs/runbooks/GUIDED_OWNER_WORKFLOW.md`, catalog YAML. |
| P3 role/readiness baseline | implemented, successor not accepted | Blocks unknown roles, prevents Analyst implementation CTA, rejects bare `Да`, binds evidence to shown spec revision and requires DoR. | active hardening change, integrity module and focused tests. |
| Typed analytics local slice | partial active implementation | Provides seven schema shapes, passive-only integration checks and a local parsed preview; no shipped sanitized whole-package example or final semantic gate yet. | analytics schemas/templates; P3 task list. |

## Delivered From The NIS Direction

`D-013` is accepted direction; its governance OpenSpec change is active at 42/43 tasks, so it is not yet an accepted capability-spec baseline.

| NIS alignment | Actual effect on a human | Visible evidence |
|---|---|---|
| `minor | major | hotfix` | Person supplies factual impact; policy selects minimum safe class and rejects under-classification/pseudo-hotfix. Hotfix shortens sequence, not safety. | classification runbook, policies, schemas. |
| DoR, implementation complete, DoD, release, archive, delivered separated | Person sees exact missing evidence and cannot equate archive or tracker Done with another state. | gates runbook and active NIS deltas. |
| Tech Lead governance | Tech Lead receives source-linked classification/risk/hold/escalation/resume/release-review reports; tools do not approve for them. | Tech Lead runbook and validators. |
| Regression, scope, stop/escalation, release and failed-run retention | Holds and follow-ups remain explicit; reports may block but never mutate external state. | corporate-flow runbook and policy bundle. |
| Corporate adaptation/no fork | Real values, approved wiring and one pilot are Phase 4 only; reusable defects return upstream. | adaptation/pilot templates and runbook. |
| Deliberate exclusions | No process-effectiveness experiment, PPRB structure, custom REST, automatic Jira/Confluence mutation or AI authority. | `D-013`, context and roadmap. |

## What A Human Can Inspect Today

There is no web UI, dashboard, generated Confluence view, live integration or corporate pilot. The intended interface is Markdown plus versioned YAML/JSON evidence.

1. Read `docs/README.md` and `docs/ROADMAP.md` for boundary and phase state.
2. Read `docs/runbooks/GUIDED_OWNER_WORKFLOW.md` for situation-first guidance; it is checksum-bound to the route catalog.
3. Read `openspec/changes/<change>/specs/` and its `tasks.md` for proposed behavior and real task state.
4. Open `process/release/phase-2-14-rc6-release-manifest.yaml` and bound evidence files for the accepted external baseline.
5. For P3, inspect roles, catalog, schemas and focused tests, but do not treat them as successor acceptance.

The sole preview surface is a local JSON read model for a supplied analytics package. It shows parsed journey, screen and passive integration descriptors; it never renders product payment UI, calls a service or changes external state.

## Script Catalog

All scripts are local CLIs, not background services or autonomous agents. Check-only commands never mutate lifecycle, tracker, release, integration or human decision state.

| Script | Purpose | Invoke when |
|---|---|---|
| `bootstrap_team_specs.py` | Copies the versioned package and central skeleton. | Creating a clean workspace; never over an unreviewed installation. |
| `build_read_pack.py` | Builds bounded authority-labelled model context. | Before one weak-model role task. |
| `certify_process_release.py` | Runs allowlisted synthetic certification and coverage. | Candidate certification; raw output stays outside Git. |
| `check_actual_certification_gate.py` | Validates one model preflight/matrix summary. | After each actual model phase. |
| `check_corporate_flow.py` | Returns deterministic may-continue/block report. | Before a governed flow advances. |
| `check_lifecycle_transition.py` | Checks a requested lifecycle transition without mutation. | Before human review of that transition. |
| `check_parallel_plan.py` | Rejects overlapping/dependent parallel AI plans. | Before concurrent task launch. |
| `check_tech_lead_control.py` | Validates human stop/hold/escalate/resume records. | At control-state or resume review. |
| `check_weak_model_evidence.py` | Rejects unsupported AI completion/authority claims. | After bounded model output. |
| `classify_change.py` | Selects class from pinned policy and facts. | Intake and material scope/impact change. |
| `create_change.py` | Creates schema-v2 draft change. | After change ID/workspace/config are known. |
| `evaluate_change_gates.py` | Reports class-aware DoR/DoD/release/archive evidence. | Before the human gate; never as approval. |
| `guided_owner_workflow.py` | Gives catalog-declared next step/block/fallback. | First business situation or blocked work. |
| `launch_role_task.py` | Selects role instruction/read-pack/output/stop point outside model. | Immediately before one AI role task. |
| `manage_release_candidate.py` | Builds/validates immutable transfer candidate. | Controlled freeze/rehearsal only. |
| `manual_fallback.py` | Emits AI-disabled fallback plan. | Model/integration unavailable or failed. |
| `migrate_change_classification.py` | Previews/applies supported `thin→minor`, `full→major`. | Eligible non-archived legacy migration; never infer hotfix. |
| `normalize_actual_certification.py` | Produces Git-safe normalized evidence from complete raw inventory. | After honest model run result. |
| `prepare_archive.py` | Collects archive-readiness evidence. | Before human archive decision. |
| `prepare_spec_pr.py` | Collects deterministic Spec PR preparation evidence. | Before human Delta Spec review. |
| `preview_analytics.py` | Validates/previews supplied typed analytics package locally. | Inspecting sanitized P3 data; read-only. |
| `review_tech_lead.py` | Builds deterministic Tech Lead review views. | Classification/readiness/risk/release recommendation review. |
| `run_actual_certification.py` | Runs append-only Qwen/DeepSeek certification slice. | Planned certification with safe external raw destination. |
| `update_process_package.py` | Checks, updates or rolls back package transactionally. | Reviewed controlled upgrade/rollback. |
| `validate_change.py` | Validates legacy thin/full packages only. | Compatibility/migration, not new schema-v2 work. |
| `validate_corporate_adaptation.py` | Validates adaptation/pilot/no-fork documents/templates. | Phase 4 preparation; it cannot supply facts or connect systems. |
| `validate_external_mapping.py` | Validates internal-to-tracker state mapping. | Before future external-state automation. |
| `validate_guided_owner_workflow.py` | Verifies guide/catalog checksum synchronization. | After catalog/guide change and before transfer. |
| `validate_process_config.py` | Discovers/validates config, registries, pins and OpenSpec runtime. | Before gated work in a concrete workspace. |
| `validate_traceability.py` | Validates links and emits canonical-ID view. | Before review, archive or audit. |

## Status Review

P0, P1 and P2 are closed; rc6 `0.3.0` has explicit `D-020` acceptance. P3 is `in_progress` (3.1/3.2 in progress, 3.3 planned) and the branch matches it. P4/P5 remain planned; no real corporate configuration/pilot started. `add-guided-owner-workflow`, `allow-certified-baseline-reuse` and `close-release-integrity-gaps` are explicitly accepted. Complete tasks in the two warned P2 changes do not imply acceptance and must remain lifecycle-open/blocked until a human decision.

## Findings

### AUD-2026-07-22-01: complete owned regression gate is red

Classification: verified high-severity defect. `python -m pytest -q tests` has 18 failures. Nine certification/coverage tests fail because new active P3 Delta Spec scenarios are absent from coverage/evidence mapping (`coverage.unmapped-scenario` masks downstream expected negatives). Five update/hardening tests retain `0.3.0` identities after working source moved to `0.3.4`. Four actual-certification tests reject local external historical raw roots with baseline-hash, matrix-not-run or preflight-log mismatch. Rc6 immutable acceptance is not invalidated; current P3 successor verification is.

### AUD-2026-07-22-02: root pytest command is invalid

Classification: verified medium-severity defect. `pytest.ini` has a basetemp but no test path/recursion exclusion, so root pytest enters ignored historical `tmp/pytest-*` evidence and returns 25 import/permission errors. Do not delete evidence to hide it; repair test discovery. Until then use `python -m pytest -q tests`.

### AUD-2026-07-22-03: superseded P2 runbook status

Classification: verified medium-severity documentation drift, corrected in this session. Four runbooks claimed that P2 gates/work items were still open or ready despite `D-020`; their status lines now distinguish accepted rc6 `0.3.0` from working P3 `0.3.4`.

### AUD-2026-07-22-04: repository map drift

Classification: verified low-severity documentation drift, corrected in this session. `docs/00_FILE_STRUCTURE.md` now lists the P3 plan and correct working/immutable package identities.

## Limitations And Remediation Decision

P3 still lacks decision-card confirmation/proactive discovery, full typed analytics contract completion, sanitized package example, final verification and successor transfer. Linux/WSL2 successor smoke remains a Phase 4 entry condition, not a fabricated pass. No live corporate integration/mutation exists.

Recommended next action: create one bounded remediation change for findings 01 and 02, first deciding P3 coverage ownership, updating identity-bound fixtures, reconciling or explicitly isolating historical raw roots, and restoring a green full owned suite. Should this remediation be started now? Deferring leaves P3 with useful focused features but no trustworthy full regression gate.