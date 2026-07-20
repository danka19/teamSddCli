# Classification And Legacy Migration

Status: Phase 2 work item 2.4 closed after independent task review, architecture review, fresh verification, and coordinator reconciliation.

## Authority And Scope

Canonical behavior is owned by `openspec/changes/adopt-nis-corporate-process-governance/`, especially tasks 2.1-2.6 and the `corporate-change-classification` and `change-package-foundation` deltas. The bundled `classification` and `artifact-matrix` policy records provide the exact versioned rule IDs consumed by the evaluator. This runbook is operational guidance, not a second rule source.

The evaluator and migration tools are deterministic, local, non-interactive, and do not evaluate lifecycle gates or mutate lifecycle state. AI output, free text, a waiver, or a Tech Lead statement cannot lower a route selected by canonical evidence. Final classification remains an explicit human decision recorded in schema-v2 metadata.

## Classify A Schema-V2 Change

Use the validated central config that pins current process package `0.3.0` and policy set `sdd-core` `1.0.0`:

```text
python scripts/classify_change.py PATH/TO/change.yaml --config PATH/TO/sdd.config.yaml
python scripts/classify_change.py PATH/TO/change.yaml --config PATH/TO/sdd.config.yaml --json
```

The report exposes source inputs, satisfied minor conditions, all triggered major rules, relevant unknowns, blockers, required artifacts and reviewers, policy/tool versions, corrections, and human-decision state. Exit `0` means the declared route is policy-consistent and human-confirmed; `1` means deterministic evidence blocks it; `2` is CLI usage; `3` is unreadable/unavailable input. JSON mode writes one stable object to stdout.

New authoring starts from `process/templates/change-v2/change.yaml` or the three examples under `process/examples/classification/`. These surfaces offer only `minor`, `major`, and `hotfix`. The root `templates/change/` and `scripts/validate_change.py` remain the accepted Phase 1 compatibility surface and are not silently rewritten.

## Compatibility Window

Legacy `mode` is supported only as migration input beginning with process package `0.2.0`. Its removal date/version is not yet approved. Support cannot be removed until a separately reviewed versioned OpenSpec/policy change records the affected package versions, completed migration evidence, and rollback/hold instructions. Current target writers never emit legacy mode.

The only automatic mappings are historical `thin -> minor` and `full -> major`; no input automatically maps to hotfix. Mixed, divergent, unknown, duplicate, or malformed metadata is held for human correction. Accepted specs, archived change paths, and metadata already in `archived` state are reported as historical evidence and never rewritten.

## Check Before Apply

Check is mandatory and non-mutating:

```text
python scripts/migrate_change_classification.py check PATH/TO/change.yaml --json
```

Retain the returned `plan_digest`. The plan identifies source/target schema, exact mapping, preserved fields, ambiguities, affected file, source SHA-256, deprecation diagnostic, backup strategy, and hold evidence.

Apply only the exact still-current plan:

```text
python scripts/migrate_change_classification.py apply PATH/TO/change.yaml --plan-digest PLAN_DIGEST --json
```

Apply replaces only schema/classification compatibility fields, preserves unrelated metadata and existing comments/order where safely possible, and creates `change.yaml.pre-classification-v2.bak` before writing. A stale digest, existing backup, ambiguity, unsafe source, or failed post-write check leaves the canonical file unchanged and emits hold evidence. A second apply is a no-op with `already-current` status.

## Rollback And Hold

If the migrated metadata must be rolled back before any later canonical acceptance, compare the backup SHA-256 with the apply report and restore the backup as `change.yaml` through the repository's normal reviewed file-change workflow. Do not use rollback to rewrite accepted or archived canonical history. Keep the process/config pin at the last accepted version while the hold is investigated.

Do not delete the backup until focused validation, human review, and the relevant repository commit are complete. A rollback after other edits requires a human merge decision rather than blind replacement.

## Verification

```text
python -m pytest tests/test_classification.py tests/test_classification_migration.py -q
python -m pytest tests/test_policy_schema_v2.py tests/test_validate_process_config.py tests/test_process_package.py -q
python -m pytest -q
python -m compileall -q process/validators scripts/classify_change.py scripts/migrate_change_classification.py
```

Cross-platform release certification and compatibility-window removal remain later Phase 2 work; this work item has Windows-local evidence only.
