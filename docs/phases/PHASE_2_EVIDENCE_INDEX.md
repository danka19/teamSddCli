# Phase 2 Evidence Index

Status: in_progress. Work item 2.1 is closed; work item 2.2 is active.

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

Status: implementation evidence recorded; work item remains `in_progress` until independent review, architecture, verification, and coordinator reconciliation complete. OpenSpec task 1.3 remains unchecked for coordinator ownership.

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
| Owner/project/adapter integrity | `test_invalid_owner_project_and_adapter_relations_are_reported` |
| Package/config/`VERSION`/OpenSpec mismatch and unsupported topology stop before runtime | `test_static_version_mismatches_prevent_runtime_probe`; `test_unsupported_topology_is_not_silently_accepted` |
| Malformed and duplicate-key YAML | `test_malformed_and_duplicate_key_yaml_are_rejected` |
| Missing/wrong OpenSpec runtime and static-before-runtime order | `test_runtime_is_checked_last_and_has_distinct_exit_codes` |
| Human/JSON parity, deterministic output, redaction, no absolute-path leak, and semantic-substring safety | `test_secret_diagnostics_are_redacted_and_human_json_codes_match`; `test_diagnostics_are_deterministic_and_do_not_false_positive_semantic_ids`; `test_schema_diagnostics_never_echo_an_absolute_reference` |
| CWD independence for imported and real script entry points | `test_behavior_is_independent_of_current_working_directory`; `test_real_entry_point_imports_package_from_any_working_directory` |
| Usage exit code | `test_usage_error_exits_two` |

### TDD And Current Verification Record

- Initial RED: `python -m pytest tests/test_validate_process_config.py -q` -> 13 failed because `scripts.validate_process_config` did not exist.
- First minimal GREEN: `python -m pytest tests/test_validate_process_config.py::test_valid_central_mode_reports_exact_compatibility_json -q` -> 1 passed.
- Main focused GREEN: `python -m pytest tests/test_validate_process_config.py -q` -> 14 passed after bounded discovery/validation implementation and the CWD-independent real-entry-point fix.
- Self-review RED: two focused tests failed because a resolved central root could contain both config files and schema diagnostics echoed an unsafe absolute reference.
- Current focused GREEN: `python -m pytest tests/test_validate_process_config.py -q` -> 22 passed after ambiguity enforcement, generic redacted schema messages, explicit adapter-version coverage, all required high-confidence secret forms, and the final usage-exit correction.
- Final exit-code RED: 21 tests passed and 1 failed because a nonexistent explicit start directory returned operational exit `3`; GREEN changed that case to CLI usage exit `2` while retaining its safe JSON diagnostic.
- One verification orchestration attempt ran focused and full pytest concurrently against the shared repository-local `.pytest-tmp`; the focused process failed one otherwise-green central case because both processes raced on the same test temp. This failed run is retained as procedure evidence and was corrected by serial execution, not hidden or treated as a product failure.
- Fresh serial full suite: `python -m pytest -q` -> 71 passed.
- Python compilation: `python -m compileall -q process/validators scripts/validate_process_config.py` -> exit 0.
- Legacy template compatibility: `python scripts/validate_change.py --allow-placeholders templates/change` -> `OK`.
- Representative human CLI: `python scripts/validate_process_config.py <synthetic-central-root>` -> exit 0 and one safe `OK` line.
- Representative JSON CLI: the same command with `--json` -> exit 0 and exactly one valid compatibility object with OpenSpec runtime `1.4.1`.
- OpenSpec inventory remains 2/33 transfer tasks and 0/43 NIS tasks; task 1.3 was intentionally not checked by the worker. `openspec list --specs` reports 8 accepted specs.
- Strict OpenSpec validation: `openspec validate --all --strict` -> 10 passed, 0 failed.
- Whitespace check: `git diff --check` -> exit 0 with only non-blocking Windows LF-to-CRLF conversion warnings on touched documentation.
- These worker results are implementation evidence only; they do not replace independent review, architecture, verification, or coordinator acceptance.
