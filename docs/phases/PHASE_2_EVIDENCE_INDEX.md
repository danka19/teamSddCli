# Phase 2 Evidence Index

Status: in_progress. Work items 2.1-2.3 are closed; work item 2.4 is ready.

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

Status: implementation worker complete; independent task review, architecture review, fresh verification, and coordinator reconciliation remain pending. NIS-governance tasks 2.1-2.6 are intentionally not checked here.

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
- Roadmap/OpenSpec governance JSON: 5 phases, 8 accepted specs, 2 active changes, 0 errors, 0 warnings. OpenSpec inventory remains NIS 4/43 and transfer package 3/33; strict validation passed 10/10.
- `git diff --check` passed with only Git's non-blocking LF-to-CRLF notices on existing Windows working-tree files.
