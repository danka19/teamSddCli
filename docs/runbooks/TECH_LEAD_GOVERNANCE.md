# Tech Lead Governance Decision Support

Status: Phase 2 work item 2.6 implementation-worker-complete; independent task review, architecture review, verification review, and coordinator reconciliation are pending. OpenSpec tasks 4.1-4.6 remain unchecked and work item 2.6 remains active.

## Boundary

The package provides deterministic, source-linked, non-mutating Tech Lead decision support. It resolves primary/delegate authority from the versioned `owners.yaml` registry, compiles the immutable `sdd-core` policy snapshot, builds the required review views, and checks human-authored `stop | hold | escalate | resume` records.

It does not mutate control or lifecycle state. It does not implement the broader flow-enforcement/failed-run work owned by 2.7, the traceability engine owned by 2.8, release-handoff persistence, integrations, a daemon, a calendar job, or a role inbox. Synthetic AI-disabled fixtures are not actual Qwen/DeepSeek certification.

## Inputs

- `process/schemas/owners.schema.json` version `2.0` for Tech Lead governance; explicit version `1.0` remains readable by the 2.1-2.5 compatibility path but is not governance-ready.
- `process/schemas/tech-lead-review-input.schema.json` version `1.0` for canonical report/source references, affected scope, decisions, dependencies, risks, scope, exceptions, controls, and a checkpoint event/kind/source plus configured Tech Lead owner reference.
- `process/schemas/tech-lead-control-record.schema.json` version `1.0` for ordered human control records.
- One validated `sdd-core` `1.0.0` snapshot. Input, classification report, gate reports, and every control record must use the same ID, version, and digest.
- Explicit `--as-of YYYY-MM-DD`. There is no wall-clock, daemon, calendar, inbox, or due-date inference.

Owner registry v2 requires a primary Tech Lead, bounded authority list, explicit delegate grants, and an escalation route for every zone. Schema and semantic failures stop both CLI entry points with exit `3` before owner resolution; diagnostics never echo input values or private paths. When zones overlap, primary, authority, complete delegate grants, and escalation route must all agree. Registry v1 compatibility remains unchanged but cannot satisfy a Tech Lead governance resolution.

## Review command

```text
python scripts/review_tech_lead.py REVIEW.yaml \
  --owners owners.yaml \
  --projects projects.yaml \
  --config sdd.config.yaml \
  --as-of 2026-07-14 \
  --json
```

Exit `0` means the deterministic report is reviewable, not human-approved. Exit `1` means at least one blocking finding. Exit `2` is stable redacted usage/input-path failure. Exit `3` is schema or policy-contract failure.

Every report emits under-classification, missing-context, architecture, owner/dependency, scope-drift, control-state, completion/DoD, release-recommendation, waiver-expiry, hotfix-follow-up, and configured-checkpoint views. Checkpoint event, kind, and source must match the locked `tech-lead.checkpoints` policy rule, while `owner_ref` must match the resolved `tech_lead_owner` configuration. Unknown or self-asserted checkpoints block review. Findings carry the exact stable fields compiled from locked `tech-lead.finding-fields`; a missing or changed finding contract fails closed.

Classification and gate-report statuses use closed enums. A blocked or invalid classification report, review-ready report, Definition of Ready, Definition of Done, or release/transfer-readiness report blocks Tech Lead review and forces `do-not-recommend`; free-text status claims fail schema validation.

## Control-state command

```text
python scripts/check_tech_lead_control.py REVIEW.yaml \
  --owners owners.yaml \
  --projects projects.yaml \
  --config sdd.config.yaml \
  --as-of 2026-07-14 \
  --json
```

Records must be unique and source-chronological after every RFC3339 timestamp is parsed as a timezone-aware instant and normalized to UTC. Equal UTC instants are rejected as ambiguous ties. Stop, hold, and escalation remain active in the check result. A resume record must explicitly list every targeted active control-record ID and bind every resume condition from every target to corrective source evidence. A standalone resume, an inactive target, unrelated evidence, an uncovered condition, or any unaddressed active record keeps resume ineligible. A later resume can become `resume-eligible` only when all active records are addressed and the same policy snapshot, bounded human authority, configured escalation route, condition-bound corrective evidence, and human approvals validate. Invalid snapshot, trigger, owner, authority, escalation, timestamp, or ordering evidence can never produce `clear` with exit `0`. The command never clears an active record or changes canonical state.

The cutoff is part of validation and provenance: date-only `--as-of` means the inclusive end of that date in UTC (`23:59:59.999999Z`), and JSON output includes `as_of`, resolved `as_of_cutoff`, the input `evaluation_date`, and the policy `snapshot_digest`. A mismatch between `--as-of` and `evaluation_date` blocks review. Control records whose normalized UTC instant is after the cutoff are diagnosed and excluded before control-state derivation; a timestamp's display offset cannot change the result.

All outputs state:

```text
decision_only: true
control_state_mutated: false
lifecycle_mutated: false
```

AI cannot author accountable control decisions, approve resume, or clear a hold. Tech Lead recommendations never satisfy QA, product, security, release, merge, archive, or tracker authority.

## Synthetic AI-disabled evidence

`tests/fixtures/tech-lead/` provides a valid event-driven review, an ordered scheduled stop/resume eligibility case, an invalid AI resume, and an explicit certification manifest. The manifest states that actual model certification was not performed. Use these fixtures for deterministic package verification only.
