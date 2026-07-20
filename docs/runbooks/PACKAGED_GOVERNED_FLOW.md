# Packaged Deterministic Governed Flow

Status: work items 2.8-2.11 are closed. Adapter `2.2` passed Qwen and DeepSeek 5/5 preflight and 15/15 matrix gates, and AI-disabled passed 11/11. Work item 2.12 is in progress.

## Boundary

The versioned `process/` package now owns current change templates, the bounded legacy validator, deterministic workflow preparation, traceability validation, external-state mapping validation, and manual fallback planning. Root scripts are thin entry points. Canonical rules remain in the accepted and active OpenSpec sources referenced by `process/package.yaml` and `process/workflow.yaml`; this runbook does not duplicate thresholds or approval rules.

Every operation works with AI disabled. Preparation output is evidence only: it never confirms classification, approves or merges a Spec PR, changes lifecycle state, archives a change, clears a hold, records tracker Done, deploys, publishes, or substitutes for a human decision.

## Bootstrap And Create

Create a new empty synthetic workspace:

```text
python scripts/bootstrap_team_specs.py C:/work/sample-workspace --json
```

The command copies only the declared versioned package and `team-specs` template, rewrites the synthetic relative package location, rejects a non-empty destination, excludes runtime caches, and returns file hashes plus package identity.

The package `distribution` manifest bounds root files and directories copied by bootstrap, update, backup, and rollback. Validation rejects missing declared assets, undeclared package-root assets, invalid schema/policy/workflow/config compatibility, symlinks, junctions, reparse points, and overlapping source/destination trees before writing.

Create a draft change from the packaged schema-v2 template:

```text
python scripts/create_change.py sample-change-001 --title "Sample change" --classification minor --type behavior_change --changes-root C:/work/sample-workspace/team-specs/openspec/changes --package-root C:/work/sample-workspace/process --json
```

`minor`, `major`, and `hotfix` are the only current classifications. The created decision remains `pending` and human-owned. Existing destinations, unsafe IDs, and unsupported types/classes fail without overwriting data.

The historical `templates/change/` surface remains readable through `scripts/validate_change.py`. Its implementation now lives in `process/validators/legacy_change.py`; it is not a current authoring template and does not reintroduce `thin | full` into current flows.

## Spec PR And Archive Preparation

```text
python scripts/prepare_spec_pr.py C:/work/sample-workspace/team-specs/openspec/changes/sample-change-001 --package-root C:/work/sample-workspace/process --json
python scripts/prepare_archive.py C:/work/sample-workspace/team-specs/openspec/changes/sample-change-001 --package-root C:/work/sample-workspace/process --json
python scripts/prepare_archive.py C:/work/sample-workspace/team-specs/openspec/changes/sample-change-001 --package-root C:/work/sample-workspace/process --archive-root C:/work/sample-workspace/team-specs/openspec/changes/archive --archive-date 2026-07-20 --approval C:/work/sample-workspace/team-specs/openspec/changes/sample-change-001/decisions/archive-approval.yaml --apply --json
```

The preparation commands hash the local package and expose canonical policy identity for human review without mutation. The explicit `--apply` archive form additionally requires `change.yaml`, `gate-input.yaml`, and `traceability.yaml` to agree on `ready_to_archive`; the deterministic `archive-readiness` gate to have no blocking gaps; complete class-applicable traceability; a matching human-approved decision record; a real ISO date; and a canonical non-link sibling archive root. Symlink, junction, reparse, collision, already-archived, and out-of-root paths fail before movement. The operation emits `spec: archive <change-id>` as the required Git subject but does not create a commit, approve, merge, release, deploy, or update any remote system.

## Delta Operation Validation

The legacy-compatible deterministic change entry point binds requirement-level Delta semantics to the accepted baseline and fails closed if that baseline cannot be resolved. `ADDED` names must be new, `REMOVED` blocks require non-empty `Reason` and `Migration`, and `RENAMED` contains only unique paired `FROM`/`TO` names; empty operation sections and embedded content changes are rejected, while behavior changes use `MODIFIED` or explicit remove/add.

```text
python scripts/validate_change.py C:/work/sample-workspace/team-specs/openspec/changes/sample-change-001 --accepted-specs-root C:/work/sample-workspace/team-specs/openspec/specs
```

## Traceability And External Mapping

`process/schemas/traceability-v2.schema.json` and `validate_traceability` keep canonical requirement, scenario, task, classification, gate, control, release, waiver/deferral, and hotfix-reconciliation references. Classification and gate references are always required. Conditional downstream links may remain empty before archive readiness; release evidence and applicable hotfix reconciliation fail closed at `ready_to_archive | archived`. Derived output contains stable record IDs and the exact `sdd-core` policy version, not copied policy rules.

`process/schemas/external-mapping.schema.json` and `validate_external_mapping` recognize exactly five separate concepts: OpenSpec archive, release readiness, deployment, consumer acceptance, and tracker Done. Missing, unknown, or collapsed mappings fail. Validation is read-only and cannot update an external system.

```text
python scripts/validate_traceability.py C:/work/sample-workspace/team-specs/openspec/changes/sample-change-001/traceability.yaml --json
python scripts/validate_external_mapping.py C:/work/sample-workspace/team-specs/external-mapping.yaml --json
```

## Compatibility, Update, And Rollback

```text
python scripts/update_process_package.py check C:/work/sample-workspace/process C:/downloads/sdd-process-0.4.0 C:/work/sample-workspace/team-specs/sdd.config.yaml --evidence C:/work/sample-workspace/team-specs/openspec/changes/process-upgrade/upgrade-evidence.yaml --json
python scripts/update_process_package.py update C:/work/sample-workspace/process C:/downloads/sdd-process-0.4.0 C:/work/sample-workspace/team-specs/sdd.config.yaml --evidence C:/work/sample-workspace/team-specs/openspec/changes/process-upgrade/upgrade-evidence.yaml --backup-root C:/work/sample-workspace/rollbacks --json
python scripts/update_process_package.py rollback C:/work/sample-workspace/process C:/work/sample-workspace/rollbacks/0.3.0 C:/work/sample-workspace/team-specs/sdd.config.yaml --json
```

Compatibility checks require matching package identity, internally matching `package.yaml`/`VERSION`, a configuration pin/location that identifies the installed package, and schema-valid reviewed upgrade evidence stored inside its bounded change-package root. The record binds the schema-v2 `change.yaml`, confirmed/corrected human decision, proposal/tasks/delta topology, from/to package and OpenSpec versions, compatibility references, passing strict validation, applicable validator/template evidence or explicit non-applicability, rollback/hold instructions, and an exact SHA-256 inventory for every referenced regular non-link file. Each referenced result must also satisfy `upgrade-check-result.schema.json` and prove the expected content-derived kind, status, producer, change, and identities. Missing, mismatched, altered, incomplete, unsafe, or AI-owned review evidence fails before staging. Update retains a complete prior package snapshot, replaces package and config pin transactionally, and restores both on failure. Rollback restores the retained package and prior pin transactionally. Neither operation enters `team-specs/openspec/`, so accepted specs and archived change history remain untouched.

Normal update accepts only a strictly forward semantic version. The prior package is first copied to a temporary manifest-bounded snapshot, validated, atomically promoted, and bound to a rollback proof containing its deterministic digest and the exact from/to versions. Rollback is the only downgrade path and refuses a missing, stale, altered, or mismatched proof. Partial package, backup, proof, and config writes are removed or restored after failure.

Linux/WSL2 uses the same arguments with portable paths:

```bash
python3 scripts/update_process_package.py check /work/sample-workspace/process /downloads/sdd-process-0.4.0 /work/sample-workspace/team-specs/sdd.config.yaml --evidence /work/sample-workspace/team-specs/openspec/changes/process-upgrade/upgrade-evidence.yaml --json
python3 scripts/update_process_package.py update /work/sample-workspace/process /downloads/sdd-process-0.4.0 /work/sample-workspace/team-specs/sdd.config.yaml --evidence /work/sample-workspace/team-specs/openspec/changes/process-upgrade/upgrade-evidence.yaml --backup-root /work/sample-workspace/rollbacks --json
python3 scripts/update_process_package.py rollback /work/sample-workspace/process /work/sample-workspace/rollbacks/0.3.0 /work/sample-workspace/team-specs/sdd.config.yaml --json
```

If update verification fails, keep the transition on hold, retain the failed
diagnostic/evidence, verify that the package/config pin and archive-tree digest
are unchanged, and roll back only from the bound snapshot proof. Do not delete
the failed attempt or reinterpret it as success.

## AI-Disabled Fallback

Unavailable Jira, Confluence, model runtime, MCP, or role inbox access does not remove a core gate. `manual_fallback_plan` produces explicit per-surface manual steps while the operator continues to use the deterministic configuration, classification, gate, Tech Lead, and corporate-flow commands. The operator records the unavailable surface and local evidence, routes the pack to the configured human owner, and leaves publication/tracker state unknown until separately evidenced. Unknown integration names fail closed.

```text
python scripts/manual_fallback.py --unavailable jira --unavailable confluence --unavailable model-runtime --unavailable mcp --unavailable role-inbox --json
```

This fallback does not implement Jira automation, Confluence publication, model/adapter certification, MCP wiring, or role inboxes. Those remain later work or environment adaptation.

## Focused Verification

```text
python -m pytest tests/test_delta_operations.py tests/test_archive_history.py tests/test_upgrade_evidence.py tests/test_packaged_flow.py tests/test_packaged_flow_cli.py tests/test_process_package.py tests/test_validate_change.py -q
python scripts/validate_change.py --allow-placeholders templates/change
```

The worker checkpoint passed 61 focused tests. Fresh independent review and full verification are still required before work item 2.8 can close.
