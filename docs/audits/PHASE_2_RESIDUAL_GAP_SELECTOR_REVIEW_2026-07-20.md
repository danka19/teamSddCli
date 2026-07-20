# Phase 2 Residual Gap Selector Review

Date: 2026-07-20  
Scope: work item 2.14.4 successor-candidate preparation  
Baseline: immutable `rc4` release evidence  
Decision authority: no human acceptance decision is made by this audit

## Executive result

The 110 `rc4` residual rows were not 110 equivalent product defects. The source inventory used one conservative fallback record for several materially different states. Exact selector review produced this routing:

| Route | Count | Meaning |
|---|---:|---|
| Phase 2 evidence already exists | 58 | An existing test or primary audit/decision directly exercises or proves the selector; only the selector binding was missing. |
| New focused test is required | 4 | Relevant behavior or structure exists, but no current test asserts the exact selector. |
| Genuine product gap | 13 | The deterministic behavior, artifact contract, or workflow does not exist and cannot be closed by relabelling a nearby test. |
| Phase 3/4 `future_work` | 12 | The selector depends on real corporate adaptation/pilot evidence or the later Confluence publication layer. |
| Governance evidence | 22 | The selector is a documentation/decision-governance rule and is proven by an exact primary decision, phase record, checklist, or audit rather than a product test. |
| Human Phase 2 scope decision | 1 | The first-MVP exclusion boundary still requires explicit human acceptance. |

The initial review result was `334 effective = 284 covered + 18 gaps + 32 future_work`: 4 focused-test rows, 13 product gaps, and 1 human scope-boundary row. The accepted follow-up recorded below changes the working successor source to `289 covered + 13 gaps + 32 future_work`.

## Immutability boundary

No file under the `rc4` release snapshot was edited. This review changes the working coverage source and test-owned selector metadata only. It therefore prepares a successor candidate; it does not rewrite, re-label, or re-certify `rc4`.

Any release claim based on the remediated `289/13/32` inventory requires a newly built candidate and candidate-bound certification. The historical `rc4` result remains `204 covered / 110 gaps / 20 future_work`.

## List 1 — existing Phase 2 evidence (58)

The table records the exact exercising node or primary evidence. Adding `SCENARIO_COVERAGE` metadata does not create a new behavioral test; it makes the existing proof selector-owned and machine-checkable.

| Capability / requirement | Scenario | Existing evidence |
|---|---|---|
| change-lifecycle / Archive history convention | Archive convention does not replace approval | `test_dor_start_and_archive_require_transition_specific_human_approval` |
| change-lifecycle / Human approval ownership | CI blocks but does not approve | `test_transition_blocks_when_gate_evidence_is_valid_but_approval_is_pending` |
| change-package-foundation / Change package template | Template contains required artifacts | `test_template_skeleton_validates_in_placeholder_mode` |
| change-package-foundation / Local change package validation | Valid package passes validation | `test_valid_thin_change_package_passes_validation` |
| change-package-foundation / Local change package validation | Missing artifact fails validation | `test_missing_full_package_artifacts_are_reported_without_waiver` |
| change-package-foundation / Local change package validation | Missing traceability fails validation | `test_missing_traceability_row_is_reported` |
| change-package-foundation / Pre-commit validation entrypoint | Plain OpenSpec project change is ignored | `test_staged_discovery_ignores_plain_project_openspec_changes` |
| change-package-foundation / Pre-commit validation entrypoint | SDD package is validated | `test_staged_discovery_ignores_plain_project_openspec_changes` |
| change-package-foundation / Template placeholder validation mode | Template validates in placeholder mode | `test_template_skeleton_validates_in_placeholder_mode` |
| change-package-foundation / Template placeholder validation mode | Real package rejects placeholders | `test_placeholder_values_are_rejected_in_production_mode` |
| confluence-feedback-loop / Feedback loop disposition | Deferred comment records follow-up | `test_non_blocking_comment_still_needs_disposition` |
| repo-topology-config / First supported topology | Central team-specs is the recommended first topology | `test_synthetic_central_topology_is_coherent` |
| repo-topology-config / First supported topology | Specs-next-to-code remains a future topology | `test_unsupported_topology_is_not_silently_accepted` |
| repo-topology-config / First supported topology | Unsupported topology is not silently accepted | `test_unsupported_topology_is_not_silently_accepted` |
| repo-topology-config / Human decision gate for topology and config | Validator enforcement follows approved implementation scope | `D-008` in `docs/DECISIONS.md` |
| repo-topology-config / OpenSpec version pin and upgrade policy | OpenSpec version is pinned centrally | `test_synthetic_central_topology_is_coherent` |
| repo-topology-config / OpenSpec version pin and upgrade policy | Version mismatch is reported before gated validation | `test_static_version_mismatches_prevent_runtime_probe` |
| repo-topology-config / Owner registry and reviewer assignment | owners.yaml is the owner source | `test_valid_owner_governance_resolves_bounded_immutable_coverage` |
| repo-topology-config / Owner registry and reviewer assignment | Multi-zone changes require all affected owners | `test_valid_owner_governance_resolves_bounded_immutable_coverage` |
| repo-topology-config / Owner registry and reviewer assignment | Unowned paths are visible | `test_uncovered_affected_repository_or_path_fails_closed` |
| repo-topology-config / Practical developer and agent workflow | Developer receives a bounded read pack | `test_build_read_pack_is_authority_labelled_bounded_and_stable` |
| repo-topology-config / Practical developer and agent workflow | Agent can work with sibling repositories | `test_valid_adapter_modes_use_only_explicit_reference_resolution` |
| repo-topology-config / Practical developer and agent workflow | Archive readiness links implementation evidence | `test_spec_pr_and_archive_preparation_collect_evidence_without_authority` |
| repo-topology-config / Process configuration files | Central config declares supported process assumptions | `test_synthetic_central_topology_is_coherent` |
| repo-topology-config / Process configuration files | Project adapter config points to central process config | `test_valid_adapter_modes_use_only_explicit_reference_resolution` |
| repo-topology-config / Process configuration files | Config names are approved defaults | `D-008` in `docs/DECISIONS.md` |
| repo-topology-config / Process package distribution | One versioned folder carries process assets | `test_bootstrap_and_create_copy_only_versioned_assets_with_json_evidence` |
| repo-topology-config / Process package distribution | Artifact dependencies are shared by skills and validators | `test_workflow_contract_declares_packaged_flow_dependencies_without_owning_policy` |
| repo-topology-config / Repository content split | team-specs owns process and requirement truth | `test_synthetic_central_topology_is_coherent` |
| repo-topology-config / Repository content split | Code PR references canonical specs | `test_spec_pr_and_archive_preparation_collect_evidence_without_authority` |
| traceability-contract / Review-minimum traceability | Requirement links to scenario | `test_valid_thin_change_package_passes_validation` |
| traceability-contract / Review-minimum traceability | Missing scenario blocks review readiness | `test_requirement_without_scenario_is_reported` |
| traceability-contract / Waived traceability links | Missing automation link requires waiver | `test_full_archive_rejects_non_automation_waiver_for_missing_automation_evidence` |
| traceability-contract / Waived traceability links | Waiver does not hide requirement coverage | `test_full_archive_requires_waiver_to_match_same_requirement_and_scenario` |
| transfer-readiness / Reproducible bootstrap and maintenance | Incompatible runtime is reported before gated work | `test_runtime_requires_exact_stable_openspec_version` |
| waiver-policy / Waiver approval ownership | AI cannot approve a waiver | `test_waiver_approver_rejects_bot_or_unknown_labels` |
| waiver-policy / Waiver approval ownership | Approver matches waived obligation | `test_waiver_approver_accepts_owner_group_reference_from_metadata` |
| waiver-policy / Waiver approval ownership | Role-appropriate approver is required | `test_waiver_approver_rejects_bot_or_unknown_labels` |
| waiver-policy / Waiver approval ownership | Residual risk requires follow-up | `test_invalid_waiver_shape_is_reported` |
| waiver-policy / Waiver negative cases | Waiver cannot replace human approval | `test_dor_start_and_archive_require_transition_specific_human_approval` |
| waiver-policy / Waiver negative cases | Waiver cannot hide behavior scenario coverage | `test_requirement_without_scenario_is_reported` |
| waiver-policy / Waiver negative cases | Non-behavior work is reclassified instead of waived | `test_refactor_can_use_no_spec_change_rationale` |
| waiver-policy / Waiver negative cases | Waiver cannot bypass mandatory risk review | `test_thin_package_rejects_risky_quality_triggers` |
| waiver-policy / Waiver policy baseline status | Validator implementation evidence is recorded | `AUDIT-016` in `docs/CURRENT_PROJECT_AUDIT.md` |
| waiver-policy / Waiver policy baseline status | Future corrections use accepted-spec workflow | `D-011` in `docs/DECISIONS.md` |
| waiver-policy / Waiver record | Waiver has required audit fields | `test_invalid_waiver_shape_is_reported` |
| waiver-policy / Waiver record | Free-text exception is rejected | `test_behavior_change_rejects_no_spec_change_rationale` |
| weak-model-guardrails / AI remains advisory and non-authoritative | Model draft becomes evidence only after review | `test_operation_evidence_accepts_supported_advisory_completion` |
| weak-model-guardrails / Bounded authority-labelled read packs | Read pack identifies source authority | `test_build_read_pack_is_authority_labelled_bounded_and_stable` |
| weak-model-guardrails / Bounded authority-labelled read packs | Read pack stays task specific | `test_build_read_pack_is_authority_labelled_bounded_and_stable` |
| weak-model-guardrails / Deterministic workflow launch | User starts a bounded role operation | `test_launcher_selects_instruction_and_stop_point_outside_model` |
| weak-model-guardrails / Deterministic workflow launch | Model does not select its own authority | `test_launcher_selects_instruction_and_stop_point_outside_model` |
| weak-model-guardrails / Evidence-backed weak-model output | Completion output includes evidence boundaries | `test_operation_evidence_accepts_supported_advisory_completion` |
| weak-model-guardrails / Role instructions and explicit stop points | Negative examples prevent common overreach | `test_role_instructions_are_bounded_and_reference_canonical_contract` |
| weak-model-guardrails / Safe parallel AI execution | Independent tasks run concurrently | `test_parallel_plan_allows_only_independent_scopes_with_complete_gates` |
| weak-model-guardrails / Safe parallel AI execution | Shared mutation prevents unsafe parallelism | `test_parallel_plan_serializes_or_blocks_unsafe_work` |
| weak-model-guardrails / Safe parallel AI execution | Parallel outputs pass an integration gate | `test_parallel_promotion_requires_each_focused_and_combined_pass_evidence` |
| weak-model-guardrails / Weak-model artifacts preserve source ownership | Derived instruction references canonical contracts | `test_operation_evidence_rejects_derived_canonical_artifact_without_source_reference` |

## List 2 — new focused test required (4)

These are not product gaps yet. The relevant artifact or topology behavior exists, but selector closure would currently rely on inference from a broader test.

| Selector | Missing focused assertion | Concrete next test |
|---|---|---|
| Artifact height rules / Proposal stays business and scope focused | The artifact gate checks substance/currentness/source linkage, not implementation-detail leakage. | Add negative proposal fixtures with code-level design content and require a stable rejection code. |
| Artifact height rules / Tasks stay executable and parseable | A template exists, but stable task IDs and checkbox/executable structure are not tested as a contract. | Add valid and malformed `tasks.md` parser cases. |
| Process package distribution / Manual forks are not the default reuse model | Bootstrap/update reuse a versioned package, but the anti-fork invariant is not directly asserted. | Add a distribution test proving no writable copied policy fork becomes canonical. |
| Repository content split / Project repos own implementation truth | The central topology separates repositories structurally, but no exact negative test rejects implementation artifacts in `team-specs`. | Add a topology/content-boundary fixture and deterministic diagnostic. |

All four were initially kept visible with owner `phase-2-verification-owner` and follow-up `successor-candidate-focused-tests`; the follow-up below closes them with exact pytest evidence.

## List 3 — genuine product gaps (13)

| Selectors | Why this is a product gap | Required OpenSpec intake |
|---|---|---|
| Delta Spec vocabulary: added behavior; removal reason/migration; rename hiding content change (3) | The current parser consumes OpenSpec operations for certification composition but no product validator enforces their semantic contract. | `enforce-delta-operation-contract` |
| Archive history: dated history path; greppable archive commit (2) | The packaged flow prepares evidence and explicitly avoids mutation; no archive executor/convention validator exists. | `implement-archive-history-convention` |
| Feedback disposition: accepted→source change; rejected reason; duplicate source link (3) | The schema accepts disposition labels but lacks required source-change, reason, and duplicate-link fields. | `strengthen-feedback-disposition-records` |
| Upgrade requires reviewed evidence (1) | Update/rollback is transactional, but reviewed change-package evidence is not an input or gate. | `govern-process-package-upgrades` |
| CODEOWNERS generated or validated from owners registry (1) | No generator or consistency validator exists. | `derive-codeowners-from-owner-registry` |
| AI proposes missing traceability links (1) | Advisory-model guardrails exist, but no bounded suggestion operation exists. | `add-advisory-traceability-suggestions` |
| Legacy baseline records gaps and generated views do not hide them (2) | Existing-code onboarding is planned only; there is no accepted baseline artifact workflow or generated-view behavior. | `implement-existing-code-baseline` |

These selectors must not be closed with nearby tests. Each requires change intake, accepted delta scenarios, RED evidence, implementation, GREEN evidence, and then a new candidate-bound certification.

## Phase 3/4 future work (12)

| Phase | Requirement / scenarios | Count | Reason |
|---|---|---:|---|
| Phase 3 | transfer-readiness / `Standard integration wiring may be configured` | 1 | Requires approved real corporate wiring. |
| Phase 3 | transfer-readiness / `Pilot evidence identifies installed state` | 1 | Requires a real installation and monitored pilot. |
| Phase 4 | change-lifecycle / Derived approval and verification display (all scenarios) | 3 | Generated Confluence lifecycle views are a later publication layer. |
| Phase 4 | confluence-feedback-loop / Confluence is generated publication (all scenarios) | 3 | Publication is excluded from the first MVP. |
| Phase 4 | confluence-feedback-loop / Evidence-backed status display (all scenarios) | 2 | Depends on generated publication. |
| Phase 4 | confluence-feedback-loop / Generated publication assets (all scenarios) | 2 | Versioned diagrams and draft-only drawings belong to later analytics/publication work. |

These declarations were removed from the evidence manifest and added to `coverage.yaml::future_work`; they are no longer reported as Phase 2 gaps.

## Governance linkage (22)

| Governance selector group | Count | Primary evidence |
|---|---:|---|
| AI verification checklist evidence | 2 | `docs/AI_STEP_VERIFICATION_CHECKLIST.md`; Phase 2.14 final technical audit |
| Canonical language and localized generated views | 3 | `D-007`, `D-009`; Phase 1 decision record |
| Docs versus OpenSpec responsibility | 2 | `D-006`; Phase 1 decision record |
| Documentation update discipline | 3 | `D-006`, `D-011`; AI checklist; Phase 2.14 documentation reconciliation audit |
| Human feedback memory | 2 | `D-009`; Phase 1 decision record |
| Source ownership and deduplication | 5 | `D-006`, `D-009`; Phase 2.14 reconciliation/final technical audits; Phase 1 plan |
| TDD-style verification discipline | 3 | AI checklist; Phase 2.14 final technical audit |
| Gate 1.5 practical options and approved defaults | 2 | `D-008`; Phase 1 Gate 1.5 decision record |

Every row is now bound to one or more exact `manual:` paths. The certification engine validates that every referenced file exists and is inside the repository. The detailed decision IDs above identify the relevant sections inside those files.

## What remains blocked

1. The 13 product gaps cannot be implemented as incidental Phase 2.14 cleanup; they require explicit change intake and accepted OpenSpec deltas.
2. The working-source improvement does not certify a release. A successor candidate must be frozen and certified after the selected remediation scope is complete.

## Recommended execution sequence

1. Accept or reject the first-MVP boundary explicitly.
2. Implement the four focused tests as one bounded successor-candidate verification change.
3. Triage the six proposed product-gap OpenSpec changes; prioritize Delta vocabulary, archive convention, and reviewed upgrades as release-integrity controls.
4. Keep Phase 3/4 declarations out of Phase 2 acceptance calculations.
5. Freeze a new candidate only after the chosen Phase 2 remediation set is complete, then run candidate-bound certification and independent review.

## Accepted follow-up: boundary and focused tests

Human decision `D-019` confirms that explicitly deferred integrations do not block first-MVP transfer readiness while deterministic fallback, visible deferral, mandatory human gates, and named Phase 3/4 ownership remain intact. This closes `Later integrations do not block transfer readiness` with `manual:docs/DECISIONS.md`; it does not accept rc4 or start Phase 3.

Four exact pytest nodes close the test-only debt without production-code changes:

- `test_proposal_templates_stay_business_and_scope_focused`;
- `test_task_templates_are_executable_and_parseable`;
- `test_bootstrap_reuses_one_versioned_package_without_policy_fork`;
- `test_central_specs_and_project_implementation_truth_stay_separate`.

Working successor-source coverage after this follow-up is `334 effective = 289 covered + 13 gaps + 32 future_work`. All 13 remaining gaps are genuine product gaps listed above.
