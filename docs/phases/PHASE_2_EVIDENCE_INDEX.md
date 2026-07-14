# Phase 2 Evidence Index

Status: in_progress. Work item 2.1 worker evidence is recorded; independent reviewer and verification approval remain pending.

## Work Item 2.1: Process Package And Synthetic Central Topology

### Sources

- Phase scope and acceptance mapping: `docs/phases/PHASE_2_TRANSFER_READY_PROCESS_PACKAGE.md`, work item 2.1.
- Accepted behavior: `openspec/specs/repo-topology-config/spec.md`.
- Proposed transfer boundary: `openspec/changes/define-transfer-ready-process-package/specs/transfer-readiness/spec.md`.
- Owned OpenSpec tasks: `define-transfer-ready-process-package` 1.1 and 1.2. Their checkboxes remain unchanged until coordinator review and verification approval.

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
| Sibling, registry, and safe relative path repository references share one local schema; unsafe forms fail | `test_repository_reference_shape_is_shared_and_accepts_supported_forms`; `test_unsafe_repository_reference_fixtures_fail_at_reference_field` |
| Release manifest represents mandatory transfer-evidence sections and rejects incomplete base contracts | `test_release_manifest_base_contract_covers_accepted_transfer_evidence`; `test_incomplete_release_manifest_fails_for_new_mandatory_sections` |
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
- Current final focused test: `python -m pytest tests/test_process_package.py -q` -> 15 passed in 0.25s.
- Current complete test suite: `python -m pytest -q` -> 49 passed in 0.83s.
- Legacy template compatibility: `python scripts/validate_change.py --allow-placeholders templates/change` -> `OK`.
- OpenSpec inventory: `openspec list` -> both active changes remain 0 tasks complete; `openspec list --specs` -> 8 accepted specs.
- Strict OpenSpec validation: `openspec validate --all --strict` -> 10 passed, 0 failed.
- Whitespace check: `git diff --check` -> exit 0; Git reported only non-blocking Windows LF-to-CRLF conversion warnings for touched files.

### Review State

- Worker implementation and self-review: complete; task-scoped commit identity is recorded in the worker report.
- Independent reviewer: pending.
- Independent verification checker: pending.
- Work item status remains `in_progress`; this index does not close 2.1 or advance 2.2.
