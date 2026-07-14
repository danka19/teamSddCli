# Phase 2 Evidence Index

Status: in_progress. Work items 2.1-2.7 are closed; work item 2.8 is active.

## Work Item 2.1: Process Package And Synthetic Central Topology

### Sources

- Phase scope and acceptance mapping: `docs/phases/PHASE_2_TRANSFER_READY_PROCESS_PACKAGE.md`, work item 2.1.
- Accepted behavior: `openspec/specs/repo-topology-config/spec.md`.
- Proposed transfer boundary: `openspec/changes/define-transfer-ready-process-package/specs/transfer-readiness/spec.md`.
- Owned OpenSpec tasks: `define-transfer-ready-process-package` 1.1 and 1.2, both complete after independent review, architecture, and verification gates.

### Implementation Evidence

- Version/package/workflow: `process/VERSION`, `process/package.yaml`, `process/workflow.yaml`.
- Local schemas: `process/schemas/`.
- Synthetic central topology and optional adapter: `templates/team-specs/`, `templates/project-adapter/.sdd-project.yaml`.
- Positive and negative fixtures: `tests/fixtures/process-package/`.
- Test-only deterministic harness: `tests/test_process_package.py`.
- Setup note: `docs/runbooks/PROCESS_PACKAGE_SETUP.md`.

### Scenario And Verification Mapping

| Scenario family | Evidence |
|---|---|
| Package version and metadata agree | `test_synthetic_central_topology_is_coherent` |
| Workflow contract remains class/gate/flow-neutral while retaining the future artifact-dependency shape | `test_workflow_contract_does_not_freeze_later_flow_or_classes` |
| Package, schema, config, and canonical-source references resolve locally | `test_package_schemas_are_valid_and_use_only_local_references`; `test_fragment_only_reference_resolves_within_current_schema`; `test_synthetic_central_topology_is_coherent` |
| Synthetic central topology and optional adapter validate | `test_synthetic_central_topology_is_coherent` |
| Sibling, registry, and canonical portable relative-path references share one semantic-neutral local schema; URL/absolute/traversal/non-portable forms fail while clean committed templates remain free of sensitive values | `test_repository_reference_shape_is_shared_and_accepts_supported_forms`; `test_unsafe_repository_reference_fixtures_fail_at_reference_field`; `test_clean_templates_and_positive_fixtures_have_no_sensitive_values` |
| Release manifest represents mandatory transfer-evidence sections, typed OS/version/architecture support, and exact pinned package dependencies; incomplete base contracts fail | `test_release_manifest_base_contract_covers_accepted_transfer_evidence`; `test_incomplete_release_manifest_fails_for_new_mandatory_sections` |
| Missing package/config version and invalid schema fail | `test_invalid_schema_fixtures_fail_stably` |
| Invalid owner-zone/project/adapter reference fails | `test_invalid_cross_file_reference_fails_stably` |
| Clean assets exclude sensitive values | `test_clean_templates_and_positive_fixtures_have_no_sensitive_values` |
| Secret/private and production-looking fixtures fail with stable categories | `test_sensitive_negative_fixtures_fail_with_stable_category` |

### TDD And Verification Record

- RED: `python -m pytest tests/test_process_package.py -q` -> 9 failed because the required package, schemas, templates, and fixtures did not exist.
- Focused GREEN: `python -m pytest tests/test_process_package.py -q` -> 9 passed.
- Self-review RED: the same focused command -> 1 failed because the optional adapter did not declare the consumed central config-schema version.
- Self-review GREEN: the same focused command -> 9 passed after adding the explicit config-schema version contract.
- Earlier review-fix checkpoint: focused suite -> 10 passed; complete suite -> 44 passed.
- Architecture-gate RED: `python -m pytest tests/test_process_package.py -q` -> 5 failed and 10 passed because the workflow froze later stages, repository references lacked the shared accepted shape, and the base release manifest omitted mandatory transfer-evidence sections.
- Architecture-gate GREEN: the same focused command -> 15 passed after the scoped schema/fixture/workflow fixes.
- Architecture follow-up RED: the same focused command -> 4 failed and 11 passed because semantic ID substrings were rejected, backslash paths were accepted, hosts were untyped strings, and host architecture/package dependencies were not required.
- Architecture follow-up GREEN: the same focused command -> 15 passed after the semantic-neutral portable-reference and typed compatibility fixes.
- Current final focused test: `python -m pytest tests/test_process_package.py -q` -> 15 passed.
- Current complete test suite: `python -m pytest -q` -> 49 passed.
- Legacy template compatibility: `python scripts/validate_change.py --allow-placeholders templates/change` -> `OK`.
- OpenSpec inventory before coordinator reconciliation: `openspec list` -> both active changes had 0 tasks complete; after the reviewed gate, transfer-package tasks 1.1-1.2 are complete (2/33) while NIS governance remains 0/43. `openspec list --specs` -> 8 accepted specs.
- Strict OpenSpec validation: `openspec validate --all --strict` -> 10 passed, 0 failed.
- Whitespace check: `git diff --check` -> exit 0; Git reported only non-blocking Windows LF-to-CRLF conversion warnings for touched files.

### Review State

- Worker implementation and fix waves: complete in full commit range `d0e7521..65505e6` (implementation commits `2e2eb45` through `65505e6`).
- Independent task reviewer: approved on reviewed head `65505e6`; no Critical, Important, or Minor findings remain.
- Architecture checker: approved on reviewed head `65505e6`; no blocking finding or human decision remains.
- Independent verification checker: PASS on reviewed head `65505e6` with 15 focused and 49 full tests, legacy template validation, strict OpenSpec 10/10, range diff check, and acceptance audit.
- Coordinator reconciliation: OpenSpec tasks 1.1-1.2 complete, work item 2.1 `closed`, and work item 2.2 `ready`.

## Work Item 2.2: Configuration Discovery And Compatibility Validation

Status: closed after independent task review, architecture review, fresh verification, and coordinator reconciliation. OpenSpec task 1.3 is complete.

### Sources And Implementation Evidence

- Accepted topology/config behavior: `openspec/specs/repo-topology-config/spec.md`.
- Proposed transfer compatibility behavior: `openspec/changes/define-transfer-ready-process-package/specs/transfer-readiness/spec.md`, task 1.3.
- Discovery/loading boundary: `process/validators/config_discovery.py`.
- Pure diagnostics/validation boundary: `process/validators/config_validation.py`.
- Thin CLI: `scripts/validate_process_config.py`.
- Scenario-first evidence: `tests/test_validate_process_config.py`.
- Operator procedure: `docs/runbooks/PROCESS_PACKAGE_SETUP.md`.

### Scenario And Verification Mapping

| Scenario family | Evidence |
|---|---|
| Valid central discovery and exact compatibility JSON | `test_valid_central_mode_reports_exact_compatibility_json` |
| Adapter discovery through sibling, portable path, and explicit registry mapping | `test_valid_adapter_modes_use_only_explicit_reference_resolution` |
| Missing/ambiguous config and ambiguous resolved central root | `test_missing_and_ambiguous_discovery_fail_before_runtime_probe`; `test_adapter_rejects_ambiguous_resolved_central_root` |
| Missing registry and unsafe reference | `test_missing_registry_and_unsafe_reference_are_stable` |
| Windows rooted-without-drive package location and resolved registry symlink/junction containment | `test_windows_rooted_package_location_is_rejected_before_resolution`; `test_registry_symlink_cannot_escape_central_root` |
| Owner/project/adapter integrity | `test_invalid_owner_project_and_adapter_relations_are_reported` |
| Package/config/`VERSION`/OpenSpec mismatch and unsupported topology stop before runtime | `test_static_version_mismatches_prevent_runtime_probe`; `test_unsupported_topology_is_not_silently_accepted` |
| Malformed and duplicate-key YAML | `test_malformed_and_duplicate_key_yaml_are_rejected` |
| Missing/wrong OpenSpec runtime and static-before-runtime order | `test_runtime_is_checked_last_and_has_distinct_exit_codes` |
| Exact stable OpenSpec runtime output rejects prerelease and build suffixes | `test_runtime_requires_exact_stable_openspec_version` |
| Package schema graphs apply nested `$id` effective-base semantics before both `$ref` and `$dynamicRef`, reject remote effective targets, preserve local relative bases, remain inside the schema directory, and terminate on cycles | `test_package_schemas_reject_remote_reference_keywords`; `test_package_schema_graph_rejects_indirect_remote_references`; `test_package_schema_graph_rejects_relative_reference_under_remote_id`; `test_package_schema_graph_resolves_reference_from_local_relative_id`; `test_package_schema_graph_stays_contained_and_handles_local_cycles` |
| Schema/resource I/O stays in discovery while pure validation consumes an immutable injected snapshot | `test_schema_validation_uses_injected_immutable_resources` |
| Human/JSON parity, deterministic output, redaction, no absolute-path leak, and semantic-substring safety | `test_secret_diagnostics_are_redacted_and_human_json_codes_match`; `test_diagnostics_are_deterministic_and_do_not_false_positive_semantic_ids`; `test_schema_diagnostics_never_echo_an_absolute_reference` |
| CWD independence for imported and real script entry points | `test_behavior_is_independent_of_current_working_directory`; `test_real_entry_point_imports_package_from_any_working_directory` |
| Missing, unknown, and malformed parser failures plus malformed-registry and nonexistent-start errors use stable human/JSON usage contracts and exit 2 | `test_generic_parser_failures_use_stable_human_and_json_contracts`; `test_nonexistent_start_directory_is_usage_error`; `test_malformed_registry_has_human_json_usage_parity` |

### TDD And Current Verification Record

- Initial RED: `python -m pytest tests/test_validate_process_config.py -q` -> 13 failed because `scripts.validate_process_config` did not exist.
- First minimal GREEN: `python -m pytest tests/test_validate_process_config.py::test_valid_central_mode_reports_exact_compatibility_json -q` -> 1 passed.
- Main focused GREEN: `python -m pytest tests/test_validate_process_config.py -q` -> 14 passed after bounded discovery/validation implementation and the CWD-independent real-entry-point fix.
- Self-review RED: two focused tests failed because a resolved central root could contain both config files and schema diagnostics echoed an unsafe absolute reference.
- Pre-review focused GREEN: `python -m pytest tests/test_validate_process_config.py -q` -> 22 passed after ambiguity enforcement, generic redacted schema messages, explicit adapter-version coverage, all required high-confidence secret forms, and the final usage-exit correction.
- Final exit-code RED: 21 tests passed and 1 failed because a nonexistent explicit start directory returned operational exit `3`; GREEN changed that case to CLI usage exit `2` while retaining its safe JSON diagnostic.
- One verification orchestration attempt ran focused and full pytest concurrently against the shared repository-local `.pytest-tmp`; the focused process failed one otherwise-green central case because both processes raced on the same test temp. This failed run is retained as procedure evidence and was corrected by serial execution, not hidden or treated as a product failure.
- Pre-review serial full suite: `python -m pytest -q` -> 71 passed.
- Independent-review regression RED: the focused suite produced 5 expected failures, 23 passes, and 1 safe skip before production changes; the skipped registry-link case was then rerun with a Windows junction fallback and failed independently as expected. The failures proved the rooted package path returned `package.missing`, prerelease/build-suffixed runtimes were accepted, remote `$dynamicRef` was accepted, and malformed `--registry` raised `SystemExit` before JSON rendering.
- Independent-review regression GREEN: `python -m pytest tests/test_validate_process_config.py -q` -> 29 passed after the five scoped fixes.
- Fresh post-fix serial full suite: `python -m pytest -q` -> 78 passed.
- Architecture-postcheck regression RED was run as three isolated groups before production changes: recursive package-schema graph checks -> 3 failed; generic argparse usage-contract checks -> 3 failed; immutable schema-resource injection/pure-validation boundary -> 1 failed. The failures proved indirect remote refs and recursive schema-directory escape were accepted, generic parser errors bypassed the renderer through `SystemExit`, and schema files were still loaded inside the validation layer.
- Architecture-postcheck regression GREEN: the combined seven new/parameterized cases passed, the full focused suite reached 35 passed, and the full suite reached 84 passed after the three minimal architecture fixes.
- Final schema-base review RED: the exact remote `$id` plus existing local relative target and the valid local relative `$id` control were run for both `$ref` and `$dynamicRef`; all 4 parameterized cases failed for the expected missing effective-base behavior.
- Final schema-base review GREEN: the same 4 cases passed after the base-aware recursive fix; the full focused suite reached 39 passed and the serial full suite reached 88 passed.
- Python compilation: `python -m compileall -q process/validators scripts/validate_process_config.py` -> exit 0.
- Legacy template compatibility: `python scripts/validate_change.py --allow-placeholders templates/change` -> `OK`.
- Representative human CLI: `python scripts/validate_process_config.py <synthetic-central-root>` -> exit 0 and one safe `OK` line.
- Representative JSON CLI: the same command with `--json` -> exit 0 and exactly one valid compatibility object with OpenSpec runtime `1.4.1`.
- Worker and fix-wave inventory remained 2/33 transfer tasks and 0/43 NIS tasks until coordinator reconciliation; task 1.3 is now checked, producing 3/33 and 0/43. `openspec list --specs` reports 8 accepted specs.
- Strict OpenSpec validation: `openspec validate --all --strict` -> 10 passed, 0 failed.
- Whitespace check: `git diff --check` -> exit 0 with only non-blocking Windows LF-to-CRLF conversion warnings on touched documentation.
- Independent task review approved the final range after all security, path, runtime, schema-graph, effective-base, parser, and local-report findings were corrected.
- Independent architecture review approved the bounded discovery, pure-validation injection, local-only schema graph, thin CLI, read-only behavior, and scope boundaries.
- Fresh verification at `6ff425f` passed 39 focused tests, 88 full tests, an 18-case selected negative matrix, compilation, legacy template validation, valid central and all three adapter modes, human/JSON usage and redaction contracts, OpenSpec inventory/spec listing, strict OpenSpec 10/10, range/commit whitespace checks, and Git inventory. Only the pre-existing untracked `.claude/` and `.vite/` directories remained; no `.superpowers` file was tracked.
- Final reviewed implementation range: `597d78c..6ff425f`, restricted to nine work-item files. Unrelated presentation commits `affd105` and `597d78c` were preserved and excluded from work-item review by using commit-scoped packages.
- Residual limitation: this work-item verification ran on Windows. Equivalent clean-host Windows/Linux/macOS release certification remains owned by work item 2.12.

## Work Item 2.3: Policy Schema V2 And Class Foundation

Status: closed after independent task review, architecture review, fresh verification, and coordinator reconciliation. NIS-governance tasks 1.1-1.4 are complete.

### Sources And Implementation Evidence

- Proposed behavior and owned tasks: `openspec/changes/adopt-nis-corporate-process-governance/` tasks 1.1-1.4 and its affected capability deltas.
- Architecture boundary: ignored worker brief `.superpowers/sdd/task-2.3-architecture.md`; no human decision was blocking.
- Static schemas: `process/schemas/change-v2.schema.json`, `process/schemas/policy-manifest.schema.json`, and `process/schemas/policy-document.schema.json`.
- Manifest-driven policy set: `process/policies/manifest.yaml` plus eight versioned policy documents.
- Pure static policy resolver: `process/validators/policy_validation.py`; discovery integration remains in `process/validators/config_discovery.py`.
- Synthetic fixture families and focused scenarios: `tests/fixtures/policy-v2/` and `tests/test_policy_schema_v2.py`.

### Scenario And Verification Mapping

| Scenario family | Evidence |
|---|---|
| Explicit schema v2, canonical classes, canonical separate work-type vocabulary, separate type/class/status, tri-state source evidence, human ownership, and no native-v2 legacy fields | `test_change_v2_accepts_all_classes_and_preserves_decision_facts`; `test_change_v2_rejects_unknown_class_and_legacy_mode`; `test_native_v2_change_rejects_legacy_reference` |
| Unknown, under-classification, major-impact hotfix, and pseudo-hotfix facts remain available without a classifier verdict | `test_negative_change_fixtures_retain_facts_without_computing_a_verdict` |
| One local manifest pins eight policy kinds, exact document identity/schema/version, canonical sources, and complete item-level static catalogs for classification, artifacts, gates, regression, stop triggers, release, pilot safety, and failed runs | `test_manifest_pins_one_versioned_local_policy_set`; `test_policy_document_schema_requires_kind_specific_foundation_catalogs` |
| Effective policy values are immutable and retain source, policy ID/version, and pointer provenance | `test_policy_bundle_builds_immutable_provenance_snapshot` |
| Missing corporate values, unresolved owner references, and locked/additive/stricter-only weakening or unsafe comparison fail with stable provenance diagnostics | `test_policy_bundle_rejects_missing_values_and_weakening_with_provenance`; `test_stricter_only_rejects_boolean_and_incomparable_numeric_types`; `test_policy_weakening_has_human_json_parity_and_provenance`; `test_missing_corporate_policy_value_is_not_guessed`; `test_corporate_policy_owner_references_must_resolve_against_registry` |
| Additive central/project overrides must match the selected rule slot's declared ID-list type and fail before snapshot construction with source/pointer provenance | `test_additive_overrides_enforce_slot_value_type_with_provenance` |
| Adapter policy path injection is forbidden | `test_adapter_override_is_bounded_and_cannot_supply_policy_paths`; `test_adapter_cannot_supply_arbitrary_policy_paths` |
| Version mismatch, duplicate IDs, missing `refs`/`requires`, and cycles fail | `test_policy_integrity_rejects_versions_duplicates_missing_refs_and_cycles`; `test_policy_integrity_rejects_missing_requires_before_cycle_detection` |
| Existing config discovery, local-schema safety, redaction, human/JSON, and CWD contracts remain intact | `tests/test_validate_process_config.py`; `tests/test_process_package.py` |

### TDD And Current Verification Record

- RED: `python -m pytest tests/test_policy_schema_v2.py -q` -> collection error `ModuleNotFoundError: process.validators.policy_validation` before production policy code existed.
- Focused GREEN: the same command -> 8 passed; the final focused set reached 9 passed after the bounded central-then-adapter provenance check.
- Atomic package/config integration regression: `python -m pytest tests/test_process_package.py tests/test_validate_process_config.py -q` -> first 25 failed and 29 passed on expected old `0.1.0`/`1.0` fixture and assertion pins; after atomic test/fixture alignment -> 54 passed.
- Combined static-policy/config/package verification after CLI provenance additions: `python -m pytest tests/test_policy_schema_v2.py tests/test_validate_process_config.py tests/test_process_package.py -q` -> 66 passed.
- Worker-baseline serial full suite: `python -m pytest -q` -> 100 passed.
- Independent-review fix RED: five focused scenarios -> 7 failed, including three parameterized corporate-owner slots.
- Independent-review fix GREEN: the same focused scenarios -> 7 passed; policy/config regression -> 58 passed; final serial full suite -> 107 passed.
- Architecture-fix RED: `python -m pytest tests/test_policy_schema_v2.py -q` -> 3 failed and 11 passed for the legacy work-type enum, incomplete static catalogs, and untyped additive override values.
- Architecture-fix GREEN: focused policy/schema suite -> 14 passed; combined policy/config/package suite -> 74 passed; final serial full suite -> 108 passed.
- Python compilation: `python -m compileall -q process/validators scripts/validate_process_config.py` -> exit 0.
- Legacy template compatibility: `python scripts/validate_change.py --allow-placeholders templates/change` -> `OK`; migration remains later scope.
- Roadmap/OpenSpec governance JSON validator -> 5 phases, 8 specs, 2 active changes, 0 errors, 0 warnings.
- OpenSpec inventory -> transfer package 3/33, NIS governance 0/43; accepted specs 8. Strict validation -> 10 passed, 0 failed.
- `git diff --check` -> exit 0 with only non-blocking Windows line-ending warnings.
- This evidence does not claim classification calculation, migration, gate evaluation, artifact enforcement, workflow mutation, release/pilot approval, or failed-run persistence; those remain assigned to later work items.
- Independent task re-review approved the final five review fixes; independent architecture recheck approved the canonical work-type vocabulary, all eight complete static policy catalogs, typed additive overrides, and the foundation-only boundary.
- Fresh verification at `c245565` passed 14 focused tests, 74 policy/config/package tests, 108 full tests, an 11-case selected negative matrix, compilation, legacy template validation, representative human/JSON CLI with package `0.2.0`/config `1.1`/policy set `1.0.0`, governance 0/0, strict OpenSpec 10/10, per-commit/range diff checks, and Git inventory.
- Coordinator reconciliation changes the NIS-governance inventory from 0/43 to 4/43 by checking tasks 1.1-1.4; the transfer package remains 3/33.
- Final implementation range: `e25bed7..c245565`. Presentation files and local `.superpowers`, `.claude`, and `.vite` paths are excluded; only the pre-existing untracked `.claude/` and `.vite/` directories remain.
- Residual limitation: verification ran on Windows. Equivalent clean-host Windows/Linux/macOS release certification remains work item 2.12.

## Work Item 2.4: Classification And Legacy Migration

Status: closed after implementation, independent task review, architecture review, fresh verification, and coordinator reconciliation. NIS-governance tasks 2.1-2.6 are complete.

### Sources And Implementation Evidence

- Proposed behavior: `openspec/changes/adopt-nis-corporate-process-governance/` tasks 2.1-2.6 and its `corporate-change-classification`, `change-package-foundation`, `repo-topology-config`, `tech-lead-workflow`, and `waiver-policy` deltas.
- Policy-driven evaluator/report: `process/validators/classification.py`; thin entry point: `scripts/classify_change.py`.
- Check/apply migration: `process/validators/classification_migration.py`; thin entry point: `scripts/migrate_change_classification.py`.
- Current authoring/read surfaces: `process/templates/change-v2/`, `process/examples/classification/`, and `process/read-packs/classification.yaml`.
- Scenario-first fixtures/tests: `tests/fixtures/classification-migration/`, `tests/test_classification.py`, and `tests/test_classification_migration.py`.
- Operator procedure: `docs/runbooks/CLASSIFICATION_AND_MIGRATION.md`.

### Scenario And Verification Mapping

| Scenario family | Evidence |
|---|---|
| Minor all-conditions, unknown blockers, major any-trigger/all-trigger output, harm-based hotfix, pseudo-hotfix, and retained major-impact obligations | `test_minor_requires_every_condition_and_reports_sources`; `test_unknown_or_missing_minor_fact_blocks_minor`; `test_major_returns_every_trigger_and_rejects_minor_downgrade`; `test_pseudo_hotfix_is_rejected_without_increasing_harm`; `test_major_impact_hotfix_retains_major_and_hotfix_obligations` |
| Stable source-linked human/JSON report, policy/tool versions, configured reviewers, and human state | `test_report_is_stable_and_includes_versions_reviewers_and_human_state`; `test_classifier_cli_consumes_policy_snapshot_and_emits_stable_json` |
| Human-only confirmation, audited correction/recalculation, stricter route, and no waiver/Tech Lead/AI/free-text downgrade | `test_pending_or_ai_confirmation_never_confirms_classification`; `test_audited_correction_recalculates_source_fact`; `test_stricter_route_is_allowed_but_authority_text_cannot_downgrade_major`; `test_change_v2_schema_accepts_only_audited_human_corrections` |
| Non-mutating conservative migration plan, deprecation result, conflict/ambiguity refusal, no hotfix mapping, exact-plan apply, metadata/comment preservation, backup/hold evidence, idempotency, and archive/spec exclusion | `test_check_is_non_mutating_stable_and_never_proposes_hotfix`; `test_conflict_and_ambiguous_legacy_metadata_are_refused`; `test_apply_requires_matching_valid_plan_and_preserves_metadata_and_comments`; `test_second_apply_is_idempotent_and_does_not_rewrite_or_add_backup`; `test_archived_or_accepted_history_is_reported_but_never_rewritten` |
| Current target surfaces and stable CLI exit semantics | `test_target_template_examples_and_read_pack_offer_only_current_classes`; `test_migration_cli_has_stable_human_json_and_exit_semantics`; `test_both_clis_render_json_usage_errors_with_exit_two` |

### TDD Record

- Classifier RED: `python -m pytest tests/test_classification.py -q` failed during collection with `ModuleNotFoundError: process.validators.classification` before production code existed.
- Classifier initial GREEN: the same focused suite reached 9 passed.
- Migration/CLI RED: `python -m pytest tests/test_classification_migration.py -q` failed during collection with `ModuleNotFoundError: process.validators.classification_migration` before production migration code existed.
- Combined classifier/migration initial GREEN: 16 passed.
- Target-surface/schema RED: the two selected tests failed because audited corrections and package template/example records did not exist; GREEN added the bounded schema and registered target assets.
- Self-review RED: three selected tests failed because blocked major reports omitted obligations, human rendering omitted required report sections, and JSON usage errors escaped through `argparse`; GREEN repaired all three contracts.
- Compatibility-diagnostic RED: the selected migration check failed because a legacy-read deprecation diagnostic was absent; GREEN added the stable diagnostic.
- Final stricter-route RED: the selected authority test failed because an unexplained `major` selection over a deterministic `minor` result was accepted; GREEN requires a recorded `stricter-route-reason` without allowing that free text to downgrade any major trigger.

### Scope Boundary

- The evaluator consumes the resolved versioned policy snapshot and canonical rule IDs; it does not duplicate a separate trigger table.
- This work item does not evaluate DoR/DoD/release/archive gates, mutate lifecycle state, approve a class, clear a hold, rewrite accepted history, or remove the Phase 1 root compatibility template/validator.
- Cross-platform release certification and compatibility-window removal remain later Phase 2 work.

### Worker Verification Record

- Focused classifier/migration suite: `python -m pytest tests/test_classification.py tests/test_classification_migration.py -q` -> 19 passed.
- Policy/config/package regression: `python -m pytest tests/test_policy_schema_v2.py tests/test_validate_process_config.py tests/test_process_package.py -q` -> 74 passed.
- Full serial suite: `python -m pytest -q` -> 127 passed.
- One earlier orchestration attempt overlapped two pytest processes on the shared repository-local `.pytest-tmp`; it retained 125 passes and 2 setup errors caused by a Windows directory lock. No product assertion failed. After all Python processes exited, the required serial rerun passed 127/127.
- Compilation: `python -m compileall -q process/validators scripts/classify_change.py scripts/migrate_change_classification.py` -> exit 0.
- Phase 1 compatibility: `python scripts/validate_change.py --allow-placeholders templates/change` -> `OK`.
- Representative classifier human and JSON modes both selected `major`, returned `valid`, exposed two triggers, configured reviewers, artifacts, sources, versions, and human state.
- Representative migration check returned `ready` with `thin -> minor`; digest-guarded apply returned `applied` with a backup; the second apply returned `already-current`.
- Roadmap/OpenSpec governance JSON: 5 phases, 8 accepted specs, 2 active changes, 0 errors, 0 warnings. Before coordinator reconciliation the OpenSpec inventory remained NIS 4/43 and transfer package 3/33; strict validation passed 10/10.
- `git diff --check` passed with only Git's non-blocking LF-to-CRLF notices on existing Windows working-tree files.

### Independent Review, Architecture, And Verification

- Implementation commits: `91ae70f` (classifier, migration, target surfaces), `413210c` (metadata-derived major facts, standard-major hotfix choice, full v2 migration validation, atomic replace), `aa6c779` (supported `change.yaml` target boundary and per-target plan binding), and `cc2e0ba` (fail-closed compiled classification policy snapshot). Unrelated commit `7c27d1a` is excluded from the work-item evidence range.
- Independent task review reproduced and closed six defects: `new_feature` under-classification, arbitrary/invalid YAML migration, standard-major rejection for hotfix-eligible work, non-atomic apply, unsupported metadata target acceptance, and cross-target plan-digest reuse. Final re-review: Approved with 25 focused tests.
- Independent architecture review required the evaluator to consume and fail closed on the versioned classification policy snapshot instead of claiming a policy version while duplicating route, obligation, and reviewer truth in Python. Commit `cc2e0ba` closed the finding; final architecture recheck: Approved with 18 classifier and 14 policy-schema tests.
- Independent verification on the reviewed head: PASS. Focused classification/migration 30 passed; policy/config/package/root regression 108 passed; representative classifier matrix 8 passed; migration safety matrix 7 passed; full serial suite 138 passed; compilation exit 0; Phase 1 root validator `OK`; governance 0 errors/0 warnings; OpenSpec strict 10/10; current target surfaces contained no `thin/full` authoring options and no work item 2.5 behavior.
- Coordinator reconciliation marks NIS-governance tasks 2.1-2.6 complete, moving the inventory from 4/43 to 10/43 while the transfer-package change remains 3/33. Work item 2.4 is `closed`; work item 2.5 is `ready`.
- Residual risk remains intentionally later scope: independent verification ran on Windows only; cross-platform equivalence is work item 2.12, and actual Qwen/DeepSeek plus AI-disabled certification remains later Phase 2 work.

## Work Item 2.5: Artifact Matrices And Lifecycle Gates

Status: closed after implementation, independent task review, architecture review, fresh verification, and coordinator reconciliation. NIS-governance tasks 3.1-3.6 are complete.

### Sources And Implementation Evidence

- Proposed behavior: `openspec/changes/adopt-nis-corporate-process-governance/` tasks 3.1-3.6 and the artifact, readiness/completion, lifecycle, waiver, and classification deltas.
- Canonical rule sources: `process/policies/artifact-matrix.yaml`, `process/policies/gates.yaml`, `process/policies/release.yaml`, and `process/policies/classification.yaml`, validated by the typed policy schema and resolved into one immutable provenance-bearing contract.
- Versioned operational evidence boundary: `process/schemas/gate-evaluation-input.schema.json`, registered in `process/package.yaml`; it remains separate from canonical `change-v2` metadata. Its bounded lifecycle-history v1.0 records are source-linked, human-recorded reached-state evidence used only to keep lifecycle expiry monotonic through canonical rework.
- Pure decision support: `process/validators/artifact_gates.py`, `process/validators/lifecycle.py`, and `process/validators/gate_input.py`.
- Thin non-mutating entry points: `scripts/evaluate_change_gates.py` and `scripts/check_lifecycle_transition.py`.
- Scenario-first evidence: `tests/test_artifact_gates.py`, `tests/test_lifecycle_gates.py`, `tests/test_gate_cli.py`, plus policy/package regression coverage.
- Operator procedure: `docs/runbooks/ARTIFACT_AND_LIFECYCLE_GATES.md`.

### Scenario And Verification Mapping

| Scenario family | Evidence |
|---|---|
| Minor/major/hotfix common and class-specific obligations, including retained major-impact hotfix duties | `test_matrix_is_class_aware_and_major_impact_hotfix_retains_major_obligations` |
| Missing, placeholder, source-less, stale, invalid-date, and AI-statement evidence | `test_required_artifact_must_be_substantive_current_and_source_linked`; `test_evidence_valid_through_is_inclusive_and_stale_on_the_next_day`; `test_ai_completion_text_is_never_implementation_evidence` |
| Structured N/A, eligible waiver, and restricted hotfix deferral with configured class-authorized owner references, typed expiry, and mandatory reconciliation | `test_conditional_not_applicable_requires_structured_human_rationale`; `test_only_eligible_artifact_accepts_a_current_human_approved_waiver`; `test_hotfix_deferral_is_restricted_and_reconciliation_blocks_done`; `test_exception_expiry_schema_rejects_free_text_and_accepts_typed_conditions` |
| Stable six-report human/JSON decision model with blockers/advisories, required humans, nonzero pending-approval state, tool/policy versions, sources, and distinct external states | `test_all_named_reports_are_stable_and_keep_required_human_approval_explicit`; `test_cli_blocks_when_evidence_is_valid_but_authorized_approval_is_pending`; `test_transition_blocks_when_gate_evidence_is_valid_but_approval_is_pending`; `test_release_not_applicable_is_approved_and_does_not_infer_external_done` |
| Fail-closed missing, malformed, changed, or wrong-provenance policy rules | `test_evaluator_fails_closed_on_missing_or_wrong_policy_provenance`; `test_evaluator_fails_closed_when_canonical_gate_semantics_are_missing_or_changed`; policy schema tests |
| Exactly six accepted states, five forward-adjacent transitions, and the two canonical source-linked human-authorized rework transitions | `test_each_forward_adjacent_transition_uses_the_canonical_gate_relationship`; `test_canonical_rework_transitions_require_reason_authority_and_evidence`; `test_other_skipped_backward_same_and_unknown_transitions_are_rejected` |
| Lifecycle expiry is due at the current target state, remains due after canonical rework, and fails closed without unique, chronological, current-consistent, source-linked human history | `test_hotfix_deferral_is_restricted_and_reconciliation_blocks_done`; `test_lifecycle_expiry_remains_due_after_canonical_rework`; `test_lifecycle_expiry_fails_closed_when_prior_reach_cannot_be_determined`; `test_lifecycle_history_contract_is_versioned_source_linked_and_human_recorded`; `test_lifecycle_history_rejects_duplicate_or_inconsistent_records`; `test_cli_keeps_lifecycle_deferral_due_after_rework` |
| Human-only DoR/start/archive approvals, hotfix reconciliation, and no archive-to-delivery inference | `test_dor_start_and_archive_require_transition_specific_human_approval`; `test_archive_readiness_rejects_bad_evidence_and_unresolved_hotfix_follow_up`; `test_transition_never_infers_delivery_deployment_or_tracker_done_from_archive` |
| Schema-bound production CLI input, stable exits, deterministic output, redacted policy failure, path-bounded local schema, and non-mutation | `tests/test_gate_cli.py`; `test_transition_cli_has_stable_human_json_and_exit_contract`; package/schema regression tests |

### TDD Record

- Initial report RED: focused artifact tests failed collection because `process.validators.artifact_gates` did not exist; the first evaluator increment reached 9 passed.
- Lifecycle RED: combined focused tests failed collection because `process.validators.lifecycle` did not exist. Subsequent RED cases exposed a required boolean-field check and an incomplete major-impact hotfix fixture; the second increment reached 30 passed.
- Production-boundary RED: standalone CLI tests failed collection because `scripts.evaluate_change_gates` did not exist. Package integration then exposed the unregistered schema key, and freshness coverage exposed a misplaced test block; both were corrected before documentation.
- Independent-review hardening RED: 9 focused tests failed and 16 passed, proving arbitrary human IDs were accepted, expiry was not typed/evaluated, pending approval returned success and allowed a transition, and both canonical rework transitions were rejected. The post-fix focused set passed 54 tests.
- Architecture-fix RED: 4 selected tests failed because the evaluator used only the current state and the gate-input schema/parser had no bounded reached-state history contract. GREEN added lifecycle-history v1.0, fail-closed semantic validation, monotonic expiry evaluation, and a non-mutating CLI regression without expanding into the later traceability engine.

### Scope And Residual Risk

- These commands never mutate canonical lifecycle state. They do not approve classification, waivers, residual risk, implementation start, release, archive, tracker transitions, deployment, or external delivery.
- N/A, waiver, deferral, approval, and rework decisions must reference the class-authorized owner groups already resolved from the canonical policy/config foundation; arbitrary human IDs fail closed. Full owner-zone, delegate, escalation, and conflict governance remains work item 2.6.
- `valid_through` uses deterministic inclusive calendar-date semantics against explicit `evaluation_date`; no wall-clock or timezone inference occurs.
- Lifecycle history records only the minimum state, timestamp, source, and human recorder needed for monotonic expiry. Broader requirement/task/test/evidence chaining remains work item 2.8.
- Tech Lead scheduled/control reports, flow-control automation, traceability expansion, integrations, deploy, cross-platform release certification, and Qwen/DeepSeek certification remain later work items.

### Worker Verification Record

- Focused artifact/lifecycle/CLI/policy/package suite: 50 passed.
- Policy/config/package regression: 74 passed.
- Full serial suite: 159 passed.
- Lifecycle matrix: 6 tests passed, exercising all five forward transitions plus skipped, reverse, same-state, unknown-state, AI-approval, unresolved-hotfix, and external-state negative cases.
- Python compilation: `python -m compileall -q process/validators scripts/evaluate_change_gates.py scripts/check_lifecycle_transition.py` -> exit 0.
- Phase 1 compatibility: `python scripts/validate_change.py --allow-placeholders templates/change` -> `OK`.
- Representative human and JSON `review-ready` reports both returned exit 0 and `ready`, listed the configured human approver, returned one report, and stated `lifecycle_mutated: false`.
- Package/schema/policy manifest consistency passed in the package and policy regression sets; the package remains `0.2.0`, gate-input schema is version `1.0`, and policy set remains `sdd-core` `1.0.0` during the active unreleased Phase 2 package line.
- Roadmap/OpenSpec governance validator: 0 errors, 0 warnings. OpenSpec inventory remained transfer package 3/33 and NIS governance 10/43; no task was checked. Strict OpenSpec validation: 10 passed, 0 failed.
- `git diff --check` passed with only Git's non-blocking Windows LF-to-CRLF notices.
- Post-review verification: 54 focused, 74 policy/config/package, 26 CLI/lifecycle/legacy-migration, and 163 full serial tests passed; compilation, the legacy template validator, roadmap/OpenSpec governance 0/0, strict OpenSpec 10/10, and diff checks also passed.
- Architecture-fix verification on top of `53c7be8`: 44 focused artifact/lifecycle/CLI/policy-schema tests, 14 selected CLI/lifecycle/legacy-migration tests, and 168 full serial tests passed; compilation and the legacy template validator passed; roadmap/OpenSpec governance reported 0 errors/0 warnings; strict OpenSpec validation passed 10/10; Git diff checks passed. Work item and OpenSpec task statuses remain unchanged for coordinator review.

### Independent Review, Architecture, And Verification

- Implementation commits: `ad9a5e0` (policy-driven matrices, reports, schema-bound CLIs, lifecycle checks), `f3473d5` (role-authorized exceptions, typed expiry, approval blocking, canonical rework), `53c7be8` (authority-validation runbook clarification), `3811241` (monotonic lifecycle expiry through bounded source-linked history), and `3efc808` (malformed-history fail-closed parser guard). Unrelated `7c27d1a` is excluded.
- Independent task review reproduced four High findings: arbitrary exception authority, expired hotfix deferrals passing readiness, pending human approval reported as ready, and rejected canonical rework transitions. Fixes passed 54 focused and 163 full tests. Final re-review found only one Minor runbook wording issue; `53c7be8` closed it and the final task verdict was Approved.
- Independent architecture review required lifecycle expiry to remain due after a canonical rework loop and later found one malformed-history hash crash. Commits `3811241` and `3efc808` added the narrow lifecycle-history v1.0 contract and fail-closed schema-before-semantics ordering. Final architecture verdict: Approved with 8/8 targeted tests.
- Independent final verification on reviewed range `b40845d..3efc808`: PASS. Focused artifact/lifecycle/CLI/policy/schema 45 passed; policy/config/package regression 74 passed; full serial suite 169 passed; six report matrix, five forward and two rework transitions, authority/waiver/N/A/expiry/hotfix/stale/placeholder/AI/external-state/malformed-history negative matrices, compilation, package/schema/manifest validation, Phase 1 legacy validator, governance 0/0, and OpenSpec strict 10/10 passed. Commands remained non-mutating and no 2.6/2.8 behavior appeared.
- Coordinator reconciliation marks NIS tasks 3.1-3.6 complete, moving the NIS inventory from 10/43 to 16/43 while the transfer-package change remains 3/33. Work item 2.5 is `closed`; work item 2.6 is `ready`.
- Residual risk remains later scope: verification ran on Windows only; full Tech Lead owner-zone/delegate/conflict governance is work item 2.6; broader traceability is 2.8; cross-platform and Qwen/DeepSeek/AI-disabled certification remain later Phase 2 work.

## Work Item 2.6: Tech Lead Governance

Status: closed after implementation, independent task review, architecture review, fresh verification, and coordinator reconciliation. NIS-governance tasks 4.1-4.6 are complete; work item 2.7 is ready.

### Implementation Evidence

- Explicit owner-registry v2.0 governance with primary Tech Lead, delegates, escalation route, bounded authority, repository/path/zone coverage, overlap conflict, and uncovered-scope rejection: `process/validators/owners.py` and `process/schemas/owners.schema.json`. Legacy v1.0 remains an explicit compatibility contract and cannot be used for Tech Lead governance.
- Ninth immutable policy catalog: `process/policies/tech-lead.yaml`, registered through the policy and package manifests and compiled with the same policy snapshot/digest used by classification and gates.
- Versioned operational boundaries: `process/schemas/tech-lead-review-input.schema.json` and `process/schemas/tech-lead-control-record.schema.json`.
- Pure non-mutating reports/checks: `process/validators/tech_lead.py`; thin human/JSON entry points: `scripts/review_tech_lead.py` and `scripts/check_tech_lead_control.py`.
- Current bounded role instruction and operator procedure: `process/roles/tech-lead.md` and `docs/runbooks/TECH_LEAD_GOVERNANCE.md`.
- Synthetic AI-disabled evidence only: `tests/fixtures/tech-lead/`; the manifest explicitly records that actual Qwen/DeepSeek certification was not performed.

### TDD And Acceptance Evidence

- Owner RED failed collection because `process.validators.owners` did not exist; immutable configured-slot RED then proved policy escape was not rejected. The first GREEN reached 8 owner scenarios and preserved 74 config/policy/package regressions.
- Review/control RED failed collection because `process.validators.tech_lead` did not exist. Subsequent behavior and registration RED runs exposed missing persistent control checks, owner-policy fixture mismatch, and unregistered ninth-policy/two-schema package surfaces before GREEN.
- Final adversarial RED: 8 failures after 24 passes exposed missing duplicate/order/action/severity/trigger/AI-approval/incomplete-resume checks plus absent role/certification fixtures. The focused owner/review/control/certification GREEN reached 32 tests.
- Independent-review hardening RED: 16 failures after 3 passes exposed open classification/gate status strings, standalone or unbound resume eligibility, list-order-dependent overlap resolution, malformed owner-v2 crashes/late failures, and an unbound evaluation cutoff. The hardening GREEN reached 20/20 adversarial tests without changing work-item or OpenSpec task status.
- Architecture-remediation RED: four groups produced 11 failures for invalid authoritative records returning clear/exit 0, local-date/lexical timestamp handling, self-asserted checkpoints, and an uncompiled finding contract; a separate equal-instant RED proved timezone-offset ties could still influence state. GREEN binds all four contracts without changing work-item or OpenSpec task status.

### Scope And Residual Risk

- Every output is decision-only and records `control_state_mutated: false` and `lifecycle_mutated: false`. A `resume-eligible` result does not clear a hold or resume work.
- Tech Lead recommendations never satisfy QA, product, security, release, merge, archive, or tracker approvals. AI cannot create or approve a control decision.
- Scheduled/event-driven support means a checkpoint whose event/kind/source match locked policy and whose owner matches resolved configuration plus deterministic `--as-of`; no daemon, calendar, role inbox, inferred due date, or integration was added.
- `--as-of`, its inclusive end-of-UTC-date `as_of_cutoff`, input `evaluation_date`, and the policy snapshot digest are explicit report provenance. RFC3339 records are timezone-aware UTC instants for order/tie/future checks; representation offsets cannot change state, and an evaluation-date mismatch blocks review.
- Any invalid authoritative snapshot, trigger, owner resolution, authority, escalation route, timestamp, or ordering evidence returns an invalid or still-active held state with nonzero exit. Findings use the compiled locked `tech-lead.finding-fields` shape; missing or changed rule content fails closed.
- Resume eligibility requires explicit active-record targets and source evidence bound to every target resume condition. Standalone resume and partially addressed multi-record control state fail closed while the check-only output retains every active record.
- Actual flow mutation/enforcement, failed-run retention, and release-handoff persistence remain 2.7; full traceability remains 2.8. Actual Qwen/DeepSeek certification and cross-platform release certification remain later Phase 2 work.

### Worker Verification Record

- Focused owner/review/control/certification: 32 passed.
- Review-hardening adversarial suite: 20 passed; existing owner/review/control/certification regression: 34 passed.
- Policy/config/package/gate regression: 97 passed.
- Final focused owner/review/control/CLI/policy/package suite: 63 passed. Policy/config/package regression: 74 passed. Independent-review hardening full serial suite: 223 passed.
- Python compilation: `python -m compileall -q process scripts tests` -> exit 0. Phase 1 compatibility: `python scripts/validate_change.py --allow-placeholders templates/change` -> `OK`.
- Representative AI-disabled review: human and JSON event-driven commands returned exit 0, `reviewable`, all 11 views, zero findings, `recommend`, every independent approval `still-required`, and both mutation flags false. Representative scheduled stop/resume commands returned exit 0 and `resume-eligible` while retaining `control-stop-1` active and both mutation flags false.
- Standalone control evaluation with `--as-of 2026-07-15` against input `evaluation_date: 2026-07-14` returned exit 1, state `invalid`, exact `tech-lead.evaluation-date-mismatch`, unchanged input SHA-256, and `control_state_mutated: false`.
- Forbidden AI resume direct-process check returned exact exit 3, empty stderr, no traceback, and stable `tech-lead.input-schema-invalid` at `/control_records/0/accountable_actor/type`. Direct entry points from an unrelated working directory returned exact exit 2, stable redacted JSON-only usage diagnostics, empty stderr, and no traceback.
- Roadmap/OpenSpec governance: 5 phases, 8 accepted specs, 2 active changes, 0 errors, 0 warnings. Inventories remained transfer package 3/33 and NIS governance 16/43; tasks 4.1-4.6 were not checked. `openspec validate --all --strict` passed 10/10.
- Package/policy/schema/manifest consistency passed with process package `0.2.0`, package schema `1.1`, `sdd-core` `1.0.0`, nine pinned policy documents, owners governance v2.0 with explicit v1.0 compatibility, and Tech Lead review/control schemas v1.0. Git diff checks passed before the worker commit; this worker-only checkpoint did not itself close work item 2.6, which closed only after the later gates recorded below.

### Review, Architecture, And Coordinator Gates

- Implementation and review range: start marker `b5be3cc`; worker `68a99aa`; task-review hardening `94662dd`; architecture remediations `99e2dcd`, `d5b39ae`, and `2d63eb3`. Unrelated upstream-analysis commit `7c27d1a` predates the baseline and is not part of the reviewed range.
- Final independent task review: approved after 51 focused review tests; blocked gate statuses, resume binding, overlap order independence, malformed owner-v2 input, and evaluation-cutoff provenance are fail-closed.
- Final architecture review: approved after 94 targeted tests; invalid or malformed control records cannot be overwritten by later valid records, UTC ordering/cutoff is canonical, checkpoints and finding fields are policy-bound, active record IDs remain visible, and no lifecycle/control mutation occurs.
- Final independent verification of `b5be3cc..2d63eb3`: PASS with 123 focused tests, 74 policy/config/package regressions, 263 full serial tests, compilation exit 0, legacy validator `OK`, roadmap/OpenSpec governance 0 errors and 0 warnings, strict OpenSpec validation 10/10, and range diff check exit 0.
- AI-disabled manual evidence preserved human/JSON parity, all 11 review views, all seven independent approvals as `still-required`, scheduled resume eligibility without clearing the active stop record, no mutation, stable CWD-independent usage diagnostics, and unchanged fixture/config hashes.
- Residual limits remain explicit: Windows-only execution, synthetic rather than actual Qwen/DeepSeek certification, flow mutation/failed-run/release persistence deferred to 2.7, and full traceability deferred to 2.8.
- Coordinator reconciliation marks NIS tasks 4.1-4.6 complete, moving the NIS inventory from 16/43 to 22/43 while the transfer-package change remains 3/33. Work item 2.6 is `closed`; work item 2.7 is `ready`.

## Work Item 2.7: Corporate Flow Controls, Safety, And Failed Runs

Status: closed after implementation, combined requirements/architecture/verification review, fix/re-review, and coordinator reconciliation. NIS tasks 5.1-5.7 and 6.1-6.2 are complete; work item 2.8 is ready.

### Implementation Evidence

- Closed versioned bundle/envelope and all record-family payloads: `process/schemas/corporate-flow-input.schema.json`, registered in `process/package.yaml`.
- Pure coordinator and immutable digest/retry checks: `process/validators/corporate_flow.py`; thin human/JSON entry point: `scripts/check_corporate_flow.py`.
- Existing regression, flow-control, release, pilot-safety, failed-run, owner, expiry, secret-scan, policy snapshot, and Tech Lead control contracts are reused rather than forked.
- Scenario-first synthetic evidence: `tests/test_corporate_flow.py`; operating boundary: `docs/runbooks/CORPORATE_FLOW_CONTROLS.md`.

### TDD And Scope Evidence

- Initial RED failed collection because `process.validators.corporate_flow` did not exist. GREEN added the common envelope, triage/baseline vertical slice, then the remaining eight acceptance families under one coordinator. A secret-scan RED and an append-only correction RED then proved missing redaction and ineffective supersession before their fixes; the focused suite reached 17 passing scenarios.
- Package integration RED found the new schema missing from the exact schema inventory. The manifest regression was corrected before broader verification.
- Combined-review P1 RED reproduced four relational gaps: an unbound release substitute decision, unbound baseline/strategy/regression classes and contradictory QA approval, drive-qualified or absolute local references, and an unbound WIP exception. Seven focused negative cases failed before the fixes and then passed with active-record, scope, evidence, role-owner, expiry/follow-up, and human-authority binding.
- The implementation is check-only: `control_state_mutated`, `lifecycle_mutated`, and `external_state_mutated` are always false. Exit `0` is reserved for `may_continue`; any invalid authoritative record, active control, safety risk, unresolved retry-chain condition, missing QA authority, or incomplete release/role/WIP evidence blocks.
- This worker did not implement work item 2.8 traceability graph/workflow mutation, real integrations or pilot, actual model certification, release-candidate manifest generation, cross-platform rehearsal, or metrics.

### Worker Verification Record

- Focused corporate-flow acceptance: 17 passed after the final append-only correction fix.
- Policy/config/package/corporate-flow regression: 90 passed before the isolated supersession fix; the final 17-test focused suite and final full serial suite include that fix.
- Final full serial suite: 280 passed.
- Python compilation: `python -m compileall -q process scripts tests` -> exit 0. Phase 1 compatibility: `python scripts/validate_change.py --allow-placeholders templates/change` -> `OK`.
- AI-disabled CLI tests prove stable human/JSON parity, exits, explicit policy/cutoff provenance, false mutation flags, unchanged input bytes, and redacted secret diagnostics.
- Roadmap/OpenSpec governance: 0 errors, 0 warnings. Inventories remain transfer package 3/33 and NIS governance 22/43; tasks 5.1-5.7 and 6.1-6.2 remain unchecked. Strict OpenSpec validation: 10 passed, 0 failed.
- `git diff --check` passed with only non-blocking Windows LF-to-CRLF notices.
- Post-review hardening verification: 24 focused corporate-flow tests and 149 relevant corporate-flow/policy/package/config/owner/Tech Lead regression tests passed. The final serial suite passed 287 tests. Compilation, roadmap/OpenSpec governance, strict OpenSpec validation, and diff checks are recorded in the hardening commit handoff; OpenSpec task and work-item statuses remain unchanged for coordinator review.
- Final WIP-expiry hardening `7f0f266` restricts `authorized-exception` to a scoped, source-linked, unexpired `exception` record with follow-up, shared evidence, and mapped product-owner authority; `human-decision` cannot bypass the limit. Focused 25/25, relevant regression 150/150, full serial 288/288, compilation and diff checks passed.
- Combined reviewer final verdict: Approved. The original four P1 findings and the follow-up WIP-expiry finding have exact negative coverage; final targeted re-review passed 25 focused tests without modifying files.
- Coordinator reconciliation marks NIS tasks 5.1-5.7 and 6.1-6.2 complete, moving the NIS inventory from 22/43 to 31/43 while the transfer-package change remains 3/33. Work item 2.7 is `closed`; work item 2.8 is `ready`.

## Work Item 2.8: Packaged Deterministic Governed Flow

Status: worker implementation complete; independent task review, architecture review, fresh verification, and coordinator reconciliation remain pending. OpenSpec task checkboxes and work-item status are intentionally unchanged at this checkpoint.

### Worker Implementation Evidence

- Current versioned template and bounded legacy validator: `process/templates/change/`, `process/validators/legacy_change.py`, and thin `scripts/validate_change.py` compatibility wrapper.
- Transactional deterministic operations: `process/workflow_operations.py`; stable CLI output boundary: `process/operation_cli.py`.
- Non-interactive entry points: `scripts/bootstrap_team_specs.py`, `scripts/create_change.py`, `scripts/prepare_spec_pr.py`, `scripts/prepare_archive.py`, and `scripts/update_process_package.py`.
- Governed traceability and external mapping contracts: `process/schemas/traceability-v2.schema.json`, `process/schemas/external-mapping.schema.json`, and `process/schemas/operation-evidence.schema.json`, registered in `process/package.yaml`.
- Packaged artifact dependency graph: `process/workflow.yaml`; operator boundary and AI-disabled fallback: `docs/runbooks/PACKAGED_GOVERNED_FLOW.md`.
- Scenario-first verification: `tests/test_packaged_flow.py` and `tests/test_packaged_flow_cli.py`, plus package and legacy compatibility suites.

### TDD And Verification Record

- First RED: focused collection failed because `process.workflow_operations` did not exist. Bootstrap/create GREEN reached 2 passing tests with versioned-only copy, destination safety, class-aware draft creation, hashes, and no human-authority substitution.
- Second RED: focused collection failed on the missing preparation/traceability/mapping/fallback/update operations. GREEN reached 9 tests covering non-mutating Spec PR/archive preparation, all three classes, canonical IDs/policy versions, unknown external mapping rejection, AI-disabled unavailable-integration fallback, transactional update/rollback, pin restoration, and preserved accepted OpenSpec history.
- CLI RED: focused collection failed because the non-interactive entry points did not exist. GREEN added stable JSON evidence and redacted operator errors without traceback or overwrite.
- Workflow RED: the package dependency graph was still empty after the operations existed. GREEN declared eight evidence dependencies while keeping thresholds, classes, approvals, and lifecycle policy out of the workflow graph.
- Final worker focused cycle: `python -m pytest tests/test_packaged_flow.py tests/test_packaged_flow_cli.py tests/test_process_package.py tests/test_validate_change.py -q` -> 61 passed.
- Fresh full serial suite: `python -m pytest -q` -> 300 passed in 73.66 seconds.
- Python compilation: `python -m compileall -q process scripts tests` -> exit 0. Direct legacy compatibility: `python scripts/validate_change.py --allow-placeholders templates/change` -> `OK`.
- Roadmap/OpenSpec governance: 5 phases, 8 accepted specs, 2 active changes, 0 errors, 0 warnings. Inventories intentionally remain transfer package 3/33 and NIS governance 31/43 at this worker checkpoint. Strict OpenSpec validation passed 10/10.
- `git diff --check` passed with only non-blocking Windows LF-to-CRLF notices. The full suite includes the committed synthetic-asset secret/private-value scan and byte-for-byte accepted-history preservation during update/rollback.
- These worker checks do not close the work item without independent task review, architecture review, fresh verification, and coordinator reconciliation.

### Review Hardening Checkpoint

- Five confirmed P1 review findings were reproduced before changes: incomplete packages passed identity-only checks; recursive link/reparse and overlapping backup destinations were unsafe; downgrade and unverified rollback were accepted; traceability manual checks diverged from the schema and lacked explicit conditional evidence state; malformed CLI roots and unexpected exceptions could return the wrong exit or traceback; external mapping and fallback lacked thin entry points.
- The common standalone package validator now applies trusted package/workflow/config/schema/policy contracts and complete declared-asset references before mutation. `process/package.yaml` owns an exact root-level distribution manifest; package copying is bounded to those files/roots rather than an unrestricted tree copy.
- Bootstrap, create, check, update, and rollback recursively reject symlinks, junctions, reparse points, source/destination overlap, and package-root undeclared assets. Update is forward-semver only, validates staged package and backup snapshots before rename, records a digest-bound rollback proof, and removes partial snapshot/proof/staging state on failure. Rollback requires that verified proof.
- Traceability now validates against the trusted JSON Schema before relational checks. Each conditional evidence link records canonical ID, kind, `concrete | pending | not-applicable` state, local source, non-empty evidence IDs, and policy version. Duplicate/unknown/empty data fail; archive readiness requires concrete implementation/QA/regression/approval evidence, resolved release plus major automation/architecture evidence where applicable, no pending links, and concrete hotfix reconciliation.
- Every new file-based CLI returns stable redacted JSON/human operational error exit `3` for missing/malformed roots and unexpected exceptions without traceback. `validate_external_mapping.py` and `manual_fallback.py` are CWD-independent thin entry points with real runbook commands.
- Focused hardening/package/CLI/legacy suite: 74 passed. Relevant config/policy/classification/gate/owner/Tech Lead/corporate-flow/package regression: 264 passed. An initial regression command named a nonexistent `tests/test_tech_lead_control.py` and collected no tests; the corrected explicit suite passed and is the evidence of record.
- Fresh full serial suite after all five fixes: 313 passed in 86.20 seconds. Compilation passed; direct legacy compatibility remained `OK`.
- Roadmap/OpenSpec governance remained 0 errors and 0 warnings with inventories intentionally unchanged at transfer package 3/33 and NIS governance 31/43. Strict OpenSpec validation passed 10/10; `git diff --check` passed with only non-blocking Windows line-ending notices.

### Scope And Authority Boundary

- Bootstrap/create copy only versioned deterministic assets; existing or unsafe destinations fail before mutation.
- Spec PR and archive preparation only assemble local evidence. They do not create/approve/merge a remote PR, approve readiness, mutate lifecycle, archive, deploy, publish, or set tracker Done.
- Update/rollback touches only the declared package directory and config pin. Accepted `team-specs/openspec/` history remains outside the mutation boundary and is regression-tested byte-for-byte.
- Traceability distinguishes required source/gate links from conditional downstream evidence and requires release plus applicable hotfix reconciliation at archive readiness. External mapping keeps archive, release, deployment, acceptance, and tracker Done distinct and fails unknown mappings.
- Jira, Confluence, model runtime, MCP, and role inbox unavailability route to explicit manual AI-disabled steps; no integration, certification run, role/read-pack kit, release candidate, or pilot was implemented in this work item.
