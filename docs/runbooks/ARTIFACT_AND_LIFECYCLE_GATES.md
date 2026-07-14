# Artifact And Lifecycle Gate Evaluation

Status: work item 2.5 implementation-worker complete; independent task, architecture, and verification review remain required before closure.

## Boundary

The gate tools are deterministic, read-only decision support. They evaluate the resolved `sdd-core` policy snapshot and never edit `change.yaml`, advance lifecycle state, approve a waiver, accept risk, close a tracker item, report deployment, or infer external delivery from OpenSpec archive state.

Canonical behavior remains in the active OpenSpec change and the versioned `artifact-matrix`, `gates`, `classification`, and `release` policies. This runbook describes operation only.

## Input Contract

Both entry points accept YAML matching `process/schemas/gate-evaluation-input.schema.json` version `1.0`. The schema requires:

- one canonical `minor | major | hotfix` classification and one of the six lifecycle states;
- an explicit ISO `evaluation_date` used for deterministic freshness checks;
- unique typed evidence records with source references and freshness state;
- structured human approvals, N/A decisions, waivers, and hotfix deferrals;
- explicit external delivered, deployed, and tracker-Done values, defaulted by the author to `unknown` rather than inferred.

Unknown fields, duplicate evidence IDs, invalid dates, AI-owned approvals, malformed exceptions, and unsafe free-form record shapes fail before policy evaluation. `valid_through` is inclusive: evidence remains current on that date and is stale on the following date.

## Evaluate Reports

Evaluate all six reports:

```text
python scripts/evaluate_change_gates.py C:/work/gate-input.yaml --config C:/work/team-specs/sdd.config.yaml
python scripts/evaluate_change_gates.py C:/work/gate-input.yaml --config C:/work/team-specs/sdd.config.yaml --json
```

Evaluate one or more reports with repeatable `--gate`:

```text
python scripts/evaluate_change_gates.py C:/work/gate-input.yaml --gate definition-of-ready --gate definition-of-done --config C:/work/team-specs/sdd.config.yaml --json
```

Reports cover review-ready, Definition of Ready, implementation-complete, Definition of Done, release/transfer readiness, and archive readiness. Deterministic green checks may still return `awaiting_human_approval` inside a report; this is not an approval or lifecycle mutation.

## Check A Transition

```text
python scripts/check_lifecycle_transition.py C:/work/gate-input.yaml --to spec_review --config C:/work/team-specs/sdd.config.yaml
python scripts/check_lifecycle_transition.py C:/work/gate-input.yaml --to ready_to_archive --config C:/work/team-specs/sdd.config.yaml --json
```

Only the policy-defined forward-adjacent transitions are evaluated. The checker rejects skipped, reverse, same-state, and unknown transitions. Approval, implementation start, and archive transitions require the corresponding source-linked human decision. The command reports a decision and leaves the input byte-for-byte unchanged.

## Exit Codes

| Code | Meaning |
|---|---|
| `0` | Selected reports are deterministically ready, or the transition is allowed by current evidence. |
| `1` | Evidence or a gate blocks readiness/transition. |
| `2` | Command usage is invalid. |
| `3` | Input schema, local input, or resolved policy contract is missing, invalid, or incompatible. |

Before acting on a green result, a human must review blocking/advisory gaps, required approvals, policy/tool versions, source provenance, external-state fields, waiver expiry, and hotfix reconciliation. Canonical state changes remain separate human-owned operations.

## Focused Verification

```text
python -m pytest tests/test_artifact_gates.py tests/test_lifecycle_gates.py tests/test_gate_cli.py tests/test_policy_schema_v2.py -q
```

Cross-platform release certification, Tech Lead scheduled/control reports, flow-control automation, traceability expansion, integrations, and deployment are later work items.
