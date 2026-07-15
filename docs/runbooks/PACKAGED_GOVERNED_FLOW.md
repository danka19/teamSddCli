# Packaged Deterministic Governed Flow

Status: work items 2.8-2.9 are closed after combined review and TDD hardening. Work item 2.10 is ready but has not started.

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
```

Both commands hash the local package and expose canonical policy identity for a human review. They do not create a remote PR, approve, merge, archive, or mutate lifecycle/external state. The archive preparation output is not archive approval and must be combined with the existing gate/lifecycle reports and the configured human archive decision.

## Traceability And External Mapping

`process/schemas/traceability-v2.schema.json` and `validate_traceability` keep canonical requirement, scenario, task, classification, gate, control, release, waiver/deferral, and hotfix-reconciliation references. Classification and gate references are always required. Conditional downstream links may remain empty before archive readiness; release evidence and applicable hotfix reconciliation fail closed at `ready_to_archive | archived`. Derived output contains stable record IDs and the exact `sdd-core` policy version, not copied policy rules.

`process/schemas/external-mapping.schema.json` and `validate_external_mapping` recognize exactly five separate concepts: OpenSpec archive, release readiness, deployment, consumer acceptance, and tracker Done. Missing, unknown, or collapsed mappings fail. Validation is read-only and cannot update an external system.

```text
python scripts/validate_traceability.py C:/work/sample-workspace/team-specs/openspec/changes/sample-change-001/traceability.yaml --json
python scripts/validate_external_mapping.py C:/work/sample-workspace/team-specs/external-mapping.yaml --json
```

## Compatibility, Update, And Rollback

```text
python scripts/update_process_package.py check C:/work/sample-workspace/process C:/downloads/sdd-process-0.3.0 C:/work/sample-workspace/team-specs/sdd.config.yaml --json
python scripts/update_process_package.py update C:/work/sample-workspace/process C:/downloads/sdd-process-0.3.0 C:/work/sample-workspace/team-specs/sdd.config.yaml --backup-root C:/work/sample-workspace/rollbacks --json
python scripts/update_process_package.py rollback C:/work/sample-workspace/process C:/work/sample-workspace/rollbacks/0.2.0 C:/work/sample-workspace/team-specs/sdd.config.yaml --json
```

Compatibility checks require matching package identity, internally matching `package.yaml`/`VERSION`, and a configuration pin/location that identifies the installed package. Update retains a complete prior package snapshot, replaces package and config pin transactionally, and restores both on failure. Rollback restores the retained package and prior pin transactionally. Neither operation enters `team-specs/openspec/`, so accepted specs and archived change history remain untouched.

Normal update accepts only a strictly forward semantic version. The prior package is first copied to a temporary manifest-bounded snapshot, validated, atomically promoted, and bound to a rollback proof containing its deterministic digest and the exact from/to versions. Rollback is the only downgrade path and refuses a missing, stale, altered, or mismatched proof. Partial package, backup, proof, and config writes are removed or restored after failure.

## AI-Disabled Fallback

Unavailable Jira, Confluence, model runtime, MCP, or role inbox access does not remove a core gate. `manual_fallback_plan` produces explicit per-surface manual steps while the operator continues to use the deterministic configuration, classification, gate, Tech Lead, and corporate-flow commands. The operator records the unavailable surface and local evidence, routes the pack to the configured human owner, and leaves publication/tracker state unknown until separately evidenced. Unknown integration names fail closed.

```text
python scripts/manual_fallback.py --unavailable jira --unavailable confluence --unavailable model-runtime --unavailable mcp --unavailable role-inbox --json
```

This fallback does not implement Jira automation, Confluence publication, model/adapter certification, MCP wiring, or role inboxes. Those remain later work or environment adaptation.

## Focused Verification

```text
python -m pytest tests/test_packaged_flow.py tests/test_packaged_flow_cli.py tests/test_process_package.py tests/test_validate_change.py -q
python scripts/validate_change.py --allow-placeholders templates/change
```

The worker checkpoint passed 61 focused tests. Fresh independent review and full verification are still required before work item 2.8 can close.
