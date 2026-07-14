# Phase 2 Evidence Index

Status: in_progress. Work items 2.1-2.2 are closed; work item 2.3 is active.

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
