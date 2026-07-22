# Corporate Flow Controls, Safety, And Failed Runs

Status: Phase 2 work item 2.7 and the later external rc6 acceptance are closed under `D-020`. OpenSpec tasks 5.1-5.7 and 6.1-6.2 are complete; the controls remain a deterministic package capability while P3 successor work is in progress.

## Boundary

`scripts/check_corporate_flow.py` validates a local, versioned governance bundle and emits a deterministic decision-support report. It never changes lifecycle, Tech Lead control, tracker, release, delivery, pilot, or external state. Exit `0` means `may_continue`; exit `1` means a valid bundle is blocked; exit `2` is stable usage failure; exit `3` is schema, policy, or owner-contract failure.

This work item does not add the work item 2.8 traceability graph or workflow commands. It does not call integrations, run a real pilot, certify Qwen/DeepSeek, generate the release-candidate manifest, or collect process-effectiveness metrics.

## Record Contract

`process/schemas/corporate-flow-input.schema.json` closes the bundle, common record envelope, evidence catalog, and every record-family payload. Each governance record carries a globally unique ID, type, scope, RFC3339 instant, local source reference, immutable policy snapshot, typed local evidence references, and accountable human decision. Corrections append through `supersedes`; they do not overwrite prior content. Duplicate IDs, changed policy digests, unknown or scope-mismatched evidence, future records, equal UTC instants, and invalid correction ancestry fail closed.

The same bundle may contain existing `tech-lead-control-record.schema.json` records. They remain the single stop/hold/escalate/resume ledger: a waiver or deviation cannot clear a control, AI cannot resume work, partial resume remains blocked, and invalid control history cannot be hidden by a later valid record.

## Checked Families

- Preliminary triage supports `proceed | hold | split | redirect | reject`; `proceed` still requires a separately approved baseline and never means Definition of Ready.
- Material scope drift covers behavior, systems, risk, dependencies, acceptance criteria, and release outcome and requires classification, readiness, owners, regression, estimates, and human approval reassessment.
- Class-aware quality strategy, locked nine-field regression rows, and configured QA-owner decisions expose gaps, stale/not-run evidence, wrong authority, class mismatch, mismatched decision kind, and positive QA dispositions that contradict material failures or missing evidence.
- Deviation, waiver, deferral, human-decision, and AI-execution records retain expiry/follow-up and human authority. AI evidence remains advisory and reproducible.
- Per-change release handoff keeps tracker, Git/OpenSpec, implementation, CI/test, artifact repository when applicable, release, and external delivery evidence distinct. An unavailable repository requires an active, same-scope, source-linked human release decision for approved substitute evidence; consumer acceptance is a separate record.
- Portable role maps require real human/group owners and scenario-based walkthrough evidence. Checklist-only evidence and AI/generic-owner substitution fail closed.
- WIP and synthetic pilot-selection records require an approved limit, explicit over-limit disposition, representative scope, and verified rollback feasibility. An over-limit exception binds to an active, same-scope, unexpired exception or human decision whose actor resolves through the portable product-owner map.
- Failed validation, AI, adapter, integration, and workflow attempts form an immutable retry chain. A successful retry links the retained failed predecessor and its digest.
- Pilot safety covers the locked privacy/data, secrets, access, accidental-delivery, rollback/hold, adapter/MCP, model/runtime, logging, dependency, support, evidence-corruption, and bypass risks plus the AI-disabled path.

## Operator Check

```powershell
python scripts/check_corporate_flow.py <bundle.yaml> `
  --owners <owners.yaml> `
  --projects <projects.yaml> `
  --config <sdd.config.yaml> `
  --as-of YYYY-MM-DD `
  --json
```

The report includes the inclusive UTC cutoff, policy snapshot and rule provenance, triage outcome, findings, active record IDs, and explicit false mutation flags. Keep the input and all referenced evidence in an approved local bundle; do not place secrets, real corporate exports, credentials, or production identifiers in reusable fixtures.
