# Phase 2 Work Item 2.14.1 Documentation Reconciliation Audit

Date: 2026-07-18

Status: passed for documentation reconciliation; final candidate verification remains open in 2.14.2.

## Boundary And Criteria

This audit covers roadmap/current-audit/phase-plan consistency, repository-map completeness, OpenSpec task/status mapping, historical manifest/evidence links and checksums, coverage follow-up routing, tracked privacy/secret exposure, and the documented boundary for the final release candidate. It does not authorize or claim a new release candidate, model execution, full pytest execution, host rehearsal, reviewer acceptance, or human release acceptance.

Results are classified as `pass`, `stale doc`, `undone work`, `decision needed`, or `verified limitation`. Severity is `blocking` when 2.14.2 cannot safely proceed, `important` when final acceptance evidence would be misleading, and `minor` for non-blocking documentation drift.

## Reproducible Evidence

| Criterion | Evidence | Result |
|---|---|---|
| Branch and dependency | `git branch --show-current`; Phase 2 plan statuses and dependency sequence | pass: `codex/phase-2-transfer-readiness-plan`; 2.1-2.13 are closed and 2.14 is the next sequential work item |
| Roadmap/OpenSpec governance | global roadmap/OpenSpec validator with `--json` | pass with 0 errors and 2 explicit lifecycle warnings |
| Native OpenSpec | `openspec list`; `openspec list --specs`; `openspec validate --all --strict` | pass: transfer 32/36 after task 7.1, NIS 39/43, 8 accepted specs, strict 12/12 |
| Historical rc7 manifest | SHA-256 checks, packaged validate/accept evidence, acceptance packet cross-check | pass as immutable historical evidence only |
| Repository/evidence links | tracked-file existence scan; manifest/selection/normalized evidence path and checksum cross-check | pass for existing rc7 and documentation links |
| Coverage routing | `process/certification/coverage.yaml` plus `process/certification/evidence-manifest.yaml`; check-only certification runner | pass: 334 effective scenarios, 191 covered, 110 explicit gaps, 33 future-work scenarios; stale follow-ups rerouted from closed 2.11 to `phase-2.14-evidence-review` |
| Privacy and raw-output boundary | tracked raw-attempt scan; high-confidence credential/path/email/private-host patterns; corporate-adaptation package validator | pass after path redaction; no tracked raw model output or high-confidence secret/private endpoint evidence found |
| Whitespace | `git diff --check` | pass after reconciliation |

Exact commands used from `<repository-root>`:

```powershell
git branch --show-current
git status --short
node "$env:USERPROFILE\.codex\skills\roadmap-openspec-validator\scripts\validate-roadmap-openspec.mjs" --root . --json
openspec list
openspec list --specs
openspec validate --all --strict
```

```powershell
$rawOutput = Join-Path $env:TEMP ("phase-2-14-doc-check-" + [guid]::NewGuid() + ".yaml")
python scripts/certify_process_release.py --raw-output $rawOutput --check
Test-Path -LiteralPath $rawOutput  # expected False in check mode
python scripts/validate_corporate_adaptation.py --package --json
python "$env:USERPROFILE\.codex\skills\project-starter-kit\scripts\bootstrap_project.py" --target . --check
```

```powershell
Get-FileHash -Algorithm SHA256 process/release/release-manifest.yaml,process/release/evidence/phase-2-12-windows-2026-07-17.yaml,process/release/evidence/phase-2-12-linux-wsl2-2026-07-17.yaml,process/certification/evidence/phase-2-11-qwen-adapter-2-2-2026-07-17.yaml,process/certification/evidence/phase-2-11-deepseek-adapter-2-2-2026-07-17.yaml
$required = @(
  'process/release/release-manifest.yaml',
  'process/release/evidence/phase-2-12-windows-2026-07-17.yaml',
  'process/release/evidence/phase-2-12-linux-wsl2-2026-07-17.yaml',
  'docs/audits/PHASE_2_WORK_ITEM_2_14_DOCUMENTATION_RECONCILIATION_AUDIT_2026-07-18.md'
)
$required | ForEach-Object { "$_=$(Test-Path -LiteralPath $_)" }
```

```powershell
git ls-files | rg 'raw-artifact|attempt-[12]\.json$'  # expected no matches
$windowsUserRoot = 'C:' + [char]92 + 'Users' + [char]92
$posixWindowsUserRoot = 'C:' + '/' + 'Users' + '/'
git grep -n -I -F -e $windowsUserRoot -e $posixWindowsUserRoot -- docs process/certification/evidence process/release/evidence  # expected no concrete path matches
git grep -n -I -E -e '-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----|AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9_]{20,}|xox[baprs]-|Bearer[[:space:]]+[A-Za-z0-9._-]{16,}' -- docs process/certification/evidence process/release/evidence  # expected no matches
git check-ignore -v .claude/launch.json .vite/
git diff --check
```

## Findings And Remediation

### DOC-2141-01 — Status And Repository Map Drift

Classification: stale doc. Severity: important.

Roadmap, phase plan, current audit, README, repository map, evidence index, and the verification checklist contained stale `2.14 next`, `23/36`, `Ready Phase 2`, pre-2.13 environment counts, a duplicate audit ID, an obsolete macOS certification requirement, and incomplete remediation-change task mapping. The files now agree that 2.14 is `in_progress`, 2.14.1 is closed, 2.14.2 is next, transfer progress is 32/36, macOS is not certified, and both remediation changes retain explicit non-accepted lifecycle states.

### EVID-2141-02 — Historical rc7 Evidence Is Intact But Not Final

Classification: pass plus verified limitation. Severity: blocking for any attempt to reuse rc7 as the final candidate.

Historical `phase-2-12-rc7` remains internally consistent:

- payload SHA-256: `f0fb1d7c6478fd3eedcaa6de26242870478ebfdbc2ca6b76356dc094f1d6f63f`;
- manifest SHA-256: `9a27a2ef036ac90774b60265b39fdc298fead01170437fff0d131aa70f38b301`;
- Windows evidence SHA-256: `d3f81ae48cfdeeda8fb3dacccdc7867d4cb765f0e976e74c347e22258334c44b`;
- Linux/WSL2 evidence SHA-256: `a29ad8a3364f0ccde6b62a1051cbda33ca29598bb7001d1f667cff6f0504ae7c`;
- selected Qwen adapter `2.2` evidence SHA-256: `0bb053808d76896513a55df648c39f0324a80e30463a1f8ba0060d264022ca93`;
- selected DeepSeek adapter `2.2` evidence SHA-256: `a1f4da6625f9ed8ec1f573f87dec515b344a223f28e928e84d6b76d02d8af6ad`.

The rc7 manifest predates 2.13: six inventoried files changed and fourteen corporate-adaptation payload assets were added afterward. Therefore rc7 and its 2.12 acceptance packet remain immutable history and cannot be relabelled or partially updated into the final candidate.

### EVID-2141-03 — Coverage Follow-Ups Pointed To Closed Work

Classification: stale evidence metadata. Severity: important.

All 110 permitted residual gaps pointed to `work-item-2.11`, which is closed. They now point to `phase-2.14-evidence-review`. Final technical/review gates must either bind an exact final-candidate evidence reference, retain the gap as an explicit accepted residual risk, or route it to the real Phase 3/4 owner. Aggregate pass claims must not hide these rows.

2026-07-19 clarification: the bulk reroute repaired stale ownership but did not classify the rows. The later provenance audit proves that all 110 retained identical fallback owner/risk/reason/compensation fields and separates them into Phase 2 exact-evidence debt, governance/manual evidence, Phase 3 corporate evidence, Phase 4 publication evidence, and one Phase 2 scope-boundary record. Therefore this historical audit must not be read as 110 individual medium-risk assessments. See `docs/audits/PHASE_2_RESIDUAL_GAPS_PROVENANCE_AND_ROUTING_AUDIT_2026-07-19.md`.

Future-work selectors now distinguish:

- fresh final-candidate weak-model and release evidence: 2.14.2-2.14.4;
- reusable corporate-adaptation contracts completed in 2.13 versus real corporate values/wiring: Phase 3;
- pilot contracts completed in 2.13 versus one selected real governed-change pilot: Phase 3.

### PRIV-2141-04 — Tracked Local Identity And Path Leakage

Classification: verified defect, remediated. Severity: important.

Tracked operational documents contained the local Windows username, absolute workspace/temp paths, a fixed presentation-runtime cache version, and duplicated personal remote metadata. These values were replaced with `<repository-root>`, `<presentation-workspace>`, `$env:USERPROFILE`, the configured `origin`, and `<presentations-runtime-version>`. Synthetic example paths, hashes, model identities, and runtime versions required as release evidence remain unchanged.

No tracked raw model attempt/completion/reasoning JSON, high-confidence credential, email address, private IP, internal hostname, or production endpoint was found in the normalized certification/release evidence.

### REL-2141-05 — Final Candidate Must Reject Bytecode Residue

Classification: undone work. Severity: blocking for 2.14.2 candidate freeze.

The historical rc7 manifest honestly includes fourteen `process/validators/__pycache__/*.pyc` files. Its checksum is valid and must not be rewritten. Before the final candidate is built, 2.14.2 must enforce exclusion/rejection of `__pycache__` and `.pyc` in the builder/validator with focused regression evidence; manual source cleanup alone is insufficient.

### GOV-2141-06 — Remediation Lifecycle Warnings Need Human Disposition

Classification: decision needed. Severity: non-blocking for 2.14.2, blocking for eventual lifecycle reconciliation.

The roadmap/OpenSpec validator reports two warnings:

- `determinize-weak-model-operational-decisions`: 13/13 tasks complete, lifecycle `in_progress`;
- `simplify-weak-model-decision-contract`: 15/15 tasks complete, lifecycle `blocked`.

No lifecycle state was inferred from checked tasks. A later human decision must determine whether the first stays open through Phase 3 or moves to `pending_acceptance`, and whether the failed adapter `2.1` route remains `blocked` or becomes `superseded` with an explicit reference.

### PRIV-2141-07 — Derived NIS/PPRB Publication Classification Is Unverified

Classification: unverified suspicion. Severity: important only for external publication.

Tracked audit/presentation summaries contain abstracted NIS/PPRB terminology derived from ignored local corporate reference material. No raw identifier, credential, internal URL, or private host was found, but the repository does not prove authorization for external publication of those derived summaries. Human data-classification review is required before publishing them outside the intended project boundary; automatic deletion is not justified by current evidence.

## Final 2.14.2 Entry Conditions

2.14.2 may proceed from the reconciled source state, but it must satisfy all of the following before claiming technical completion:

1. prevent bytecode/cache files from entering the new candidate;
2. build a new immutable candidate containing the 2.13 corporate-adaptation assets;
3. create a new manifest, payload/manifest checksums, Windows/WSL2 host records, raw-artifact snapshot, normalized evidence, and separate 2.14 acceptance packet;
4. run the single approved Qwen and DeepSeek sequence and no redundant intermediate model run;
5. disposition all 110 residual coverage gaps through exact evidence, explicit residual risk, or a real Phase 3/4 route;
6. retain `human_acceptance_required: true` until the owner records a separate decision.

## Phase Status Audit

- Roadmap phases: P0 `closed`, P1 `closed`, P2 `in_progress`, P3 `planned`, P4 `planned`.
- Phase 2 work items: 2.1-2.13 `closed`; 2.14 `in_progress`; its documentation gate 2.14.1 `closed`, technical gate 2.14.2 `ready`, review gate 2.14.3 `planned`, and human gate 2.14.4 `blocked` on 2.14.2/2.14.3.
- Phase 2 parent status remains valid because 2.14 and the phase gate are unfinished; no acceptance was inferred from checked tasks or historical `evidence-complete` output.
- The repository has no separate machine consumer for work-item/sub-gate status. The roadmap/OpenSpec validator is the machine-readable consumer for phase/OpenSpec ownership and lifecycle; it reports zero errors and the two explicit remediation lifecycle warnings above.
- No old Phase 2 work item remains unmarked. Historical “next item” prose in the evidence index is labelled as a dated closure checkpoint rather than current state.

## Residual Risks

- macOS remains not certified; WSL2 is portability evidence rather than native bare-metal Linux certification.
- Real corporate configuration, integration wiring, privacy/retention values, owners, adapters, and the pilot remain Phase 3 work.
- The two OpenSpec lifecycle warnings remain explicit and unresolved.
- External publication classification for the abstracted NIS/PPRB summaries remains a human decision.
