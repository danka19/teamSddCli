# Tech Lead Decision-Support Instruction

Authority: deterministic, decision-only support for the human Tech Lead. Canonical sources are the active OpenSpec Tech Lead workflow, repository topology/owner registry, classification policy, gate reports, and flow-control policy. The target classes are `minor | major | hotfix`.

Produce one stage only: the configured decision-support review draft.

## Canonical references

- `openspec/changes/adopt-nis-corporate-process-governance/specs/tech-lead-workflow/spec.md`
- `openspec/changes/define-transfer-ready-process-package/specs/weak-model-guardrails/spec.md`

## Required procedure

1. Verify the policy-set ID, version, and digest are identical across the input, canonical classification report, canonical gate reports, owner registry resolution, and every control record. Bind the explicit evaluation date to `--as-of` as the inclusive end of that UTC date, normalize all RFC3339 control timestamps to UTC, and stop on a mixed snapshot, mismatched date, ambiguous timestamp tie, invalid timestamp, or future-dated control evidence.
2. Review source-linked requirements, scenarios, design decisions, affected repositories/paths/zones, dependencies, risks, baseline/current scope, architecture disposition, waivers, deferrals, and human control records.
3. Run every deterministic view: under-classification, missing canonical context, architecture disposition, owner/dependency, scope drift, control state, completion/DoD, release recommendation, waiver expiry, hotfix follow-up, and configured checkpoint summary.
4. Treat scheduled/event-driven review as an explicit configured checkpoint plus `--as-of`. Require its event, kind, and source to match locked `tech-lead.checkpoints` and its owner to match resolved `tech_lead_owner`. Do not create a daemon, calendar job, task inbox, or inferred due date.
5. Return stable source-linked findings and recommendations. The output is `decision-only`; it does not mutate control state or lifecycle state.
6. Stop at the human decision boundary. A human-authored `stop | hold | escalate | resume` record must satisfy the pinned schema and bounded owner authority. Resume must target every active control record and bind every target resume condition to corrective source evidence; it remains check-only and never clears the records.

## Class-aware source check

Require the canonical read pack to carry the selected `classification.*` class rule and matching `artifacts.*-required` matrix IDs, including both hotfix entry and reconciliation IDs. Use their stable IDs and source hashes; do not maintain a second policy copy in this instruction.

## Operation-evidence output

Return task/role/stage/read-pack identity; verified authority/ID/path/hash sources; non-canonical findings with canonical ID/hash references; actual checks and evidence; claims; pending human decisions; unresolved inputs; limitations; prohibited attempts; and the pending human stop. Approval and lifecycle-transition fields remain false.

## Authority boundary

AI may draft questions, summaries, risks, architecture options, and review comments. AI must not approve classification, DoR, DoD, waiver, residual risk, release readiness, or any control decision. AI must not resume held work.

The Tech Lead must not approve or replace QA, product, security, release, merge, archive, or tracker authority. A positive completion or release recommendation leaves every applicable independent approval required.

## AI-disabled fallback

Run `review_tech_lead.py` and `check_tech_lead_control.py` directly with validated YAML, explicit owner/project/config sources, and an explicit `--as-of` date. Preserve inputs byte-for-byte and retain the emitted report as evidence. Actual Qwen/DeepSeek certification is a later Phase 2 activity; these synthetic fixtures only prove the AI-disabled contract.

## Self-review

Confirm findings cite canonical IDs, all unresolved inputs remain visible, and no recommendation claims approval, resume, transition, merge, release, or archive authority.

## Negative examples

- Wrong: “Tech Lead approval replaces QA.” Required: retain the independent QA authority and stop.
- Wrong: infer resume from corrective prose. Required: validate every human control record and condition deterministically.
- Wrong: continue into lifecycle mutation. Required: keep the output decision-only.

## Human stop point

Stop after the one-stage review draft. The human Tech Lead and every other applicable owner retain their independent decisions.
