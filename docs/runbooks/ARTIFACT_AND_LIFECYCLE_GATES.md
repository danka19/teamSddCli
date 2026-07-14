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
- structured human approvals, N/A decisions, waivers, and hotfix deferrals whose
  approver and owner references resolve to the configured class-authorized owner groups;
- explicit external delivered, deployed, and tracker-Done values, defaulted by the author to `unknown` rather than inferred.

Unknown fields, duplicate evidence IDs, invalid dates, AI-owned authority records,
malformed exceptions, and unsafe free-form record shapes fail schema/input validation
before policy evaluation; the CLI exits `3`. A well-shaped human authority record whose
ID does not resolve to the configured class-authorized owner groups reaches policy
evaluation but blocks the gate or transition; the CLI exits `1`. Exception expiry is
typed as either an ISO date or a canonical lifecycle state; date expiry is due on the
recorded date, and a lifecycle expiry is due when that state is reached. An unreconciled
due deferral and an expired waiver block the gate. `valid_through` is inclusive:
evidence remains current on that date and is stale on the following date.

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

Reports cover review-ready, Definition of Ready, implementation-complete, Definition of Done, release/transfer readiness, and archive readiness. Evidence-complete checks may return `awaiting_human_approval`; the report and CLI remain nonzero until every configured class approver has recorded a source-linked decision. This distinguishes valid evidence from completed approval and never mutates lifecycle state.

## Check A Transition

```text
python scripts/check_lifecycle_transition.py C:/work/gate-input.yaml --to spec_review --config C:/work/team-specs/sdd.config.yaml
python scripts/check_lifecycle_transition.py C:/work/gate-input.yaml --to ready_to_archive --config C:/work/team-specs/sdd.config.yaml --json
```

The checker evaluates the five forward-adjacent transitions plus the two canonical
rework transitions `spec_review -> draft` and
`ready_to_archive -> in_implementation`. Rework requires a substantive reason,
source-linked evidence, and a configured class-authorized human owner reference.
Other skipped, backward, same-state, and unknown transitions are rejected. Gate and
transition approvals remain separate requirements. The command reports a decision and
leaves the input byte-for-byte unchanged.

## Exit Codes

| Code | Meaning |
|---|---|
| `0` | Selected reports are deterministically ready, or the transition is allowed by current evidence. |
| `1` | Evidence, pending required approval, or a gate blocks readiness/transition. |
| `2` | Command usage is invalid. |
| `3` | Input schema, local input, or resolved policy contract is missing, invalid, or incompatible. |

Before acting on a green result, a human must review blocking/advisory gaps, required approvals, policy/tool versions, source provenance, external-state fields, waiver expiry, and hotfix reconciliation. Canonical state changes remain separate human-owned operations.

## Focused Verification

```text
python -m pytest tests/test_artifact_gates.py tests/test_lifecycle_gates.py tests/test_gate_cli.py tests/test_policy_schema_v2.py -q
```

Cross-platform release certification, Tech Lead scheduled/control reports, flow-control automation, traceability expansion, integrations, and deployment are later work items.
