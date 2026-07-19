# Phase 2 Residual-Gap Provenance And Routing Audit

Date: 2026-07-19.

Status: complete investigation; remediation decision remains with the human owner.

## Audit Boundary And Criteria

Target: the 110 `gap` rows in `process/certification/evidence-manifest.yaml` used by immutable release candidate `phase-2-14-rc4`.

Scope:

- establish when and why the rows were created;
- distinguish a missing exact evidence binding from an implementation defect, deferred feature, or individually assessed residual risk;
- group every row by canonical capability and requirement;
- recommend a durable owner, phase, and follow-up route without mutating rc4;
- reconcile the human-acceptance documentation with the evidence actually present.

Classification scale:

- `verified limitation`: current evidence definitively lacks an exact scenario binding;
- `verified documentation defect`: a project document overstates what the manifest proves;
- `unverified product defect`: behavior may or may not be missing; the gap row alone does not prove it;
- `pass`: count, provenance, and canonical source were reproduced;
- `decision needed`: changing the immutable candidate or accepting its residual uncertainty requires the human owner.

Severity applies to this audit finding, not to the product scenario. The manifest's repeated `risk: medium` value was not treated as an individual severity assessment.

Known limitation: this audit does not execute 110 scenario-specific tests or decide that existing similarly named tests are semantically sufficient. Such a decision requires exact requirement/scenario-to-evidence review and, for pytest evidence, a matching `SCENARIO_COVERAGE` marker.

## Executive Result

The 110 rows are real coverage-manifest entries, but they are not 110 independently discovered product defects and not 110 individually assessed medium risks.

They are the remainder produced when the Phase 2.10 coverage mechanism stopped allowing broad default/file-level evidence and began requiring exact scenario-to-source bindings. Every then-unbound effective OpenSpec scenario received the same fallback gap record. Later work closed six of the original 116 exact-binding gaps, added other covered/future-work rows, and finally routed the remaining 110 rows wholesale to the Phase 2.14 human gate.

Current rc4 composition is:

- 334 effective scenarios;
- 204 accepted exact evidence rows after future-work selectors are applied;
- 110 explicit gap rows;
- 20 later-work scenarios;
- the evidence manifest itself contains 323 rows: 213 evidence rows plus 110 gap rows, of which nine evidence rows are superseded by future-work routing in the effective report.

All 110 gap rows have the same owner, risk, reason, compensation, and follow-up. That uniformity proves they are a mechanical fallback class. It does not prove equal impact or justify calling each row an individually reviewed `medium residual risk`.

## Provenance

| Checkpoint | Manifest state | Meaning |
|---|---:|---|
| `2062fb8` (`feat: add deterministic certification fixtures and coverage`) | no evidence manifest; one `default_evidence` covered all otherwise unmatched scenarios | Initial aggregate coverage design. It made the report green without exact scenario provenance. |
| `bd47311` (`fix: harden certification evidence and coverage`) | capability-level evidence and gap rules | Broad capability/file mappings still allowed evidence to stand in for multiple scenarios. |
| `1cbf2ef` (`fix: bind certification coverage to exact evidence`) | 309 rows: 288 evidence, 21 gaps | First explicit row-per-scenario manifest. Many rows were populated from broad binding data and were not yet source-local. |
| `601c3dd` (`fix: bind certification evidence to source markers`) | 309 rows: 193 evidence, 116 gaps | Exact `SCENARIO_COVERAGE` ownership beside test functions removed unsupported broad bindings. The residual count expanded because prior aggregate claims were withdrawn, not because 95 new product bugs appeared. |
| `8d917e0` (`docs: close phase 2.12 acceptance evidence gaps`) | 310 rows: 200 evidence, 110 gaps | Six exact gaps were closed with release evidence. Remaining rows still used the generic `work-item-2.11` route. |
| `95063c2` and `588bbbd` | 323 rows: 213 evidence, 110 gaps | Final-candidate/manual evidence was added; all residual rows were mechanically rerouted to `phase-2.14-human-acceptance`. |
| `8bc7531` (rc4 review-gate close) | unchanged: 110 gaps across 46 requirements | Current immutable candidate evidence. |

The creation purpose was sound: prevent aggregate tests, unrelated pytest files, or default evidence from hiding scenarios with no exact evidence. The weakness is in later interpretation and routing: a fail-closed placeholder was described as if it were a completed risk assessment.

## Source Composition

| Source | Gap scenarios | Requirements |
|---|---:|---:|
| Accepted Phase 1 capability specs | 95 | 38 |
| Active Phase 2 delta specs | 15 | 8 |
| **Total** | **110** | **46** |

| Capability | Gap scenarios |
|---|---:|
| `change-artifact-contracts` | 5 |
| `change-lifecycle` | 7 |
| `change-package-foundation` | 8 |
| `confluence-feedback-loop` | 11 |
| `documentation-governance` | 20 |
| `repo-topology-config` | 25 |
| `traceability-contract` | 7 |
| `transfer-readiness` | 4 |
| `waiver-policy` | 12 |
| `weak-model-guardrails` | 11 |
| **Total** | **110** |

## Recommended Routing

This routing is an audit recommendation for disposition. It does not rewrite the immutable rc4 evidence manifest.

| Route | Count | Recommended owner and phase | Meaning and next evidence |
|---|---:|---|---|
| `P2-EXACT-EVIDENCE-DEBT` | 75 | transfer-readiness verification owner; Phase 2 acceptance/remediation | Implemented or package-level contract lacks an exact accepted evidence binding. Review existing tests/manual records; add a source-local marker only when semantics match, otherwise add a focused test or retain an explicitly assessed residual risk. |
| `GOVERNANCE-EVIDENCE` | 22 | documentation-governance owner; recurring across P0/P1/P2-P4 | Historical decision or operating-discipline scenario is better proved by dated decision/audit/manual evidence than by a synthetic pytest claim. Bind exact durable records and define recurrence where behavior is ongoing. |
| `P3-CORPORATE-EVIDENCE` | 2 | corporate-adaptation owner; Phase 3 | Requires real environment/configuration/pilot evidence and should be a future-work selector, not an rc4 implementation gap. |
| `P4-PUBLICATION-EVIDENCE` | 10 | publication/feedback owner; Phase 4 | Depends on the explicitly excluded Confluence/generated-publication layer and should be future work until that layer is in scope. |
| `P2-SCOPE-BOUNDARY-EVIDENCE` | 1 | transfer-readiness owner; Phase 2 human gate | Proves that later integrations do not block transfer. Bind the accepted exclusion decision and release boundary as manual evidence. |
| **Total** | **110** |  |  |

## Requirement-Level Inventory

Every gap row is covered exactly once by the table below. `Scenarios` is the number of residual scenario rows under the requirement.

| Capability | Requirement | Scenarios | Route | Why this route |
|---|---|---:|---|---|
| `change-artifact-contracts` | Artifact height rules | 2 | `P2-EXACT-EVIDENCE-DEBT` | Current artifact validation exists; exact proposal/task semantic evidence is not bound. |
| `change-artifact-contracts` | Delta Spec operation vocabulary | 3 | `P2-EXACT-EVIDENCE-DEBT` | OpenSpec delta semantics are current package/governance behavior; exact positive/negative bindings remain absent. |
| `change-lifecycle` | Archive history convention | 3 | `P2-EXACT-EVIDENCE-DEBT` | Archive tooling/history behavior is in the reusable flow and is testable or manually reproducible. |
| `change-lifecycle` | Derived approval and verification display | 3 | `P4-PUBLICATION-EVIDENCE` | The generated Confluence/public status layer is explicitly later work. |
| `change-lifecycle` | Human approval ownership: CI blocks but does not approve | 1 | `P2-EXACT-EVIDENCE-DEBT` | Deterministic gate authority is current safety behavior and needs an exact negative binding. |
| `change-package-foundation` | Change package template | 1 | `P2-EXACT-EVIDENCE-DEBT` | Template content is present; exact scenario evidence is absent. |
| `change-package-foundation` | Local change package validation | 3 | `P2-EXACT-EVIDENCE-DEBT` | Core validator positive/negative behavior is implemented and should have exact bindings. |
| `change-package-foundation` | Pre-commit validation entrypoint | 2 | `P2-EXACT-EVIDENCE-DEBT` | The entrypoint contract is current, even though the local tool installation remains an environment limitation. |
| `change-package-foundation` | Template placeholder validation mode | 2 | `P2-EXACT-EVIDENCE-DEBT` | Placeholder-versus-real-package behavior is deterministic and testable. |
| `confluence-feedback-loop` | Confluence is generated publication | 3 | `P4-PUBLICATION-EVIDENCE` | Actual generated publication is excluded from the first MVP. |
| `confluence-feedback-loop` | Evidence-backed status display | 2 | `P4-PUBLICATION-EVIDENCE` | Requires the later generated display/publication surface. |
| `confluence-feedback-loop` | Feedback loop disposition | 4 | `P2-EXACT-EVIDENCE-DEBT` | A deterministic feedback-policy boundary exists; exact accepted-spec scenario bindings are missing even though remote Confluence integration remains excluded. |
| `confluence-feedback-loop` | Generated publication assets | 2 | `P4-PUBLICATION-EVIDENCE` | Versioned publication drawings/assets belong to the later publication layer. |
| `documentation-governance` | AI verification checklist evidence | 2 | `GOVERNANCE-EVIDENCE` | Proved by completion reports, checklist use, and deterministic validation records rather than one implementation test. |
| `documentation-governance` | Canonical language and localized generated views | 3 | `GOVERNANCE-EVIDENCE` | Language/source ownership is an operating rule; generated-view execution remains later work. |
| `documentation-governance` | Docs versus OpenSpec responsibility | 2 | `GOVERNANCE-EVIDENCE` | Repository ownership discipline requires doc-sync audit evidence. |
| `documentation-governance` | Documentation update discipline | 3 | `GOVERNANCE-EVIDENCE` | Ongoing process behavior needs dated workflow/audit evidence. |
| `documentation-governance` | Human feedback memory | 2 | `GOVERNANCE-EVIDENCE` | Must be evidenced by durable intake/decision records across sessions. |
| `documentation-governance` | Source ownership and deduplication | 5 | `GOVERNANCE-EVIDENCE` | Requires source/derived-surface reconciliation evidence; a broad unit test would overstate proof. |
| `documentation-governance` | TDD-style verification discipline | 3 | `GOVERNANCE-EVIDENCE` | Requires scenario-before-implementation and report evidence across work items. |
| `repo-topology-config` | First supported topology | 3 | `P2-EXACT-EVIDENCE-DEBT` | Synthetic topology/config validators exist; exact accepted-spec bindings need review. |
| `repo-topology-config` | Human decision gate for topology and config: two Gate 1.5 decision scenarios | 2 | `GOVERNANCE-EVIDENCE` | These are historical human decision/acceptance facts owned by Phase 1 decisions and evidence. |
| `repo-topology-config` | Human decision gate for topology and config: validator enforcement follows approved scope | 1 | `P2-EXACT-EVIDENCE-DEBT` | This is current deterministic behavior, not merely a historical decision. |
| `repo-topology-config` | OpenSpec version pin and upgrade policy | 3 | `P2-EXACT-EVIDENCE-DEBT` | Package compatibility/update behavior is current and testable. |
| `repo-topology-config` | Owner registry and reviewer assignment | 4 | `P2-EXACT-EVIDENCE-DEBT` | Current configuration/ownership validation needs exact scenario bindings. |
| `repo-topology-config` | Practical developer and agent workflow | 3 | `P2-EXACT-EVIDENCE-DEBT` | Read packs, sibling repositories, and archive evidence are current package contracts; real-environment proof may supplement exact synthetic evidence. |
| `repo-topology-config` | Process configuration files | 3 | `P2-EXACT-EVIDENCE-DEBT` | Closed configuration schemas/validators exist; exact accepted-spec bindings are absent. |
| `repo-topology-config` | Process package distribution | 3 | `P2-EXACT-EVIDENCE-DEBT` | Rc4 packaging and no-fork behavior provide candidate evidence that must be assessed and bound exactly. |
| `repo-topology-config` | Repository content split | 3 | `P2-EXACT-EVIDENCE-DEBT` | Source ownership/topology is enforced by the package and requires exact evidence or explicit manual proof. |
| `traceability-contract` | AI traceability suggestions are advisory | 1 | `P2-EXACT-EVIDENCE-DEBT` | Current weak-model authority boundary is testable. |
| `traceability-contract` | Legacy baseline traceability | 2 | `P2-EXACT-EVIDENCE-DEBT` | Legacy migration/visibility behavior is part of current package scope. |
| `traceability-contract` | Review-minimum traceability | 2 | `P2-EXACT-EVIDENCE-DEBT` | Current review gate behavior should fail closed and be bound exactly. |
| `traceability-contract` | Waived traceability links | 2 | `P2-EXACT-EVIDENCE-DEBT` | Current waiver/traceability interaction needs exact positive/negative evidence. |
| `transfer-readiness` | First transfer boundary: later integrations do not block transfer readiness | 1 | `P2-SCOPE-BOUNDARY-EVIDENCE` | The accepted first-MVP exclusion and release boundary are the appropriate manual evidence. |
| `transfer-readiness` | First transfer boundary: standard integration wiring may be configured | 1 | `P3-CORPORATE-EVIDENCE` | Actual approved wiring is deliberately Phase 3 work. |
| `transfer-readiness` | Release evidence and auditability: pilot evidence identifies installed state | 1 | `P3-CORPORATE-EVIDENCE` | No real pilot has run; this belongs to Phase 3 pilot evidence. |
| `transfer-readiness` | Reproducible bootstrap and maintenance: incompatible runtime is reported before gated work | 1 | `P2-EXACT-EVIDENCE-DEBT` | Compatibility preflight is current reusable behavior and should have exact negative evidence. |
| `waiver-policy` | Waiver approval ownership | 4 | `P2-EXACT-EVIDENCE-DEBT` | Current authority and residual-follow-up policy is deterministic/human-governed and needs exact bindings. |
| `waiver-policy` | Waiver negative cases | 4 | `P2-EXACT-EVIDENCE-DEBT` | Mandatory bypass-prevention behavior needs exact negative evidence. |
| `waiver-policy` | Waiver policy baseline status | 2 | `P2-EXACT-EVIDENCE-DEBT` | Implementation provenance and accepted-spec correction behavior need exact evidence. |
| `waiver-policy` | Waiver record | 2 | `P2-EXACT-EVIDENCE-DEBT` | Closed waiver schema behavior is testable. |
| `weak-model-guardrails` | AI remains advisory and non-authoritative | 1 | `P2-EXACT-EVIDENCE-DEBT` | Current model-review boundary has deterministic and actual-model evidence candidates, but no exact selector binding. |
| `weak-model-guardrails` | Bounded authority-labelled read packs | 2 | `P2-EXACT-EVIDENCE-DEBT` | Current launcher/read-pack contract is implemented and testable. |
| `weak-model-guardrails` | Deterministic workflow launch | 2 | `P2-EXACT-EVIDENCE-DEBT` | Current launcher authority behavior needs exact binding. |
| `weak-model-guardrails` | Evidence-backed weak-model output | 1 | `P2-EXACT-EVIDENCE-DEBT` | Current normalized evidence contract is implemented; exact scenario provenance remains missing. |
| `weak-model-guardrails` | Role instructions and explicit stop points | 1 | `P2-EXACT-EVIDENCE-DEBT` | Negative-overreach handling is current certification scope. |
| `weak-model-guardrails` | Safe parallel AI execution | 3 | `P2-EXACT-EVIDENCE-DEBT` | Current parallel plan/evidence/integration contracts are deterministic and testable. |
| `weak-model-guardrails` | Weak-model artifacts preserve source ownership | 1 | `P2-EXACT-EVIDENCE-DEBT` | Current derived-instruction/source metadata behavior needs exact evidence. |

## Findings

### RG-001: Blanket metadata was presented as individual risk assessment

- Classification: verified documentation defect.
- Severity: high for the acceptance decision; it does not establish high product severity.
- Impact: the human packet asks the owner to accept 110 `medium residual risks`, although the repository contains one copied fallback assessment applied to 110 heterogeneous scenarios.
- Evidence: all 110 gap records have the same five gap fields; Git history shows the mass transition from exact-binding hardening to bulk follow-up rerouting.
- Root cause: exact-evidence fail-closed behavior and risk disposition were conflated.
- Recommended action: use the five-route inventory in the decision packet and never describe `risk: medium` as independently assessed unless each row is reviewed.

### RG-002: Future work is mixed into current-candidate residual gaps

- Classification: verified limitation.
- Severity: medium.
- Impact: at least 12 rows are better owned by Phase 3 or Phase 4, while the current manifest routes all of them to Phase 2.14 human acceptance.
- Evidence: two scenarios explicitly require corporate wiring/pilot installed state; ten scenarios require the excluded generated-publication/Confluence surface.
- Root cause: the manifest's requirement-level future-work selectors do not cover these scenario-level boundaries.
- Recommended action: if a successor candidate is built, convert these rows to exact `future_work` selectors with Phase 3/P4 ownership.

### RG-003: Exact-evidence debt does not prove missing behavior

- Classification: verified limitation with unverified product defects.
- Severity: medium.
- Impact: 75 rows may be closable by existing tests or candidate/manual evidence, but similarity is not sufficient to claim coverage.
- Evidence: repository searches find related tests and implementation for every major deterministic capability, while none of the 75 selectors has an accepted exact binding in the current report.
- Root cause: earlier broad bindings were correctly removed; semantic rebinding was only partially completed.
- Recommended action: conduct selector-by-selector evidence review before adding markers; add focused tests where no exact proof exists.

### RG-004: Governance scenarios need a different evidence model

- Classification: verified limitation.
- Severity: medium.
- Impact: 22 historical/ongoing governance scenarios are forced into the same executable-gap shape as product behavior.
- Evidence: the scenarios describe human decisions, documentation ownership, feedback memory, TDD discipline, and recurring drift control.
- Root cause: the manifest supports manual evidence but the Phase 2.10 bulk fallback did not classify evidence type before assigning gaps.
- Recommended action: bind exact dated decisions/audits/checklists and define recurrence for ongoing governance assertions.

## Acceptance And Immutability Consequences

- `phase-2-14-rc4` remains immutable. Editing `process/certification/evidence-manifest.yaml`, coverage selectors, tests, or packaged evidence would create a different candidate identity and invalidate rc4's manifest/checksum/certification chain.
- The existing 110 rows remain valid proof that exact evidence is absent from rc4's effective coverage report.
- The rows are not sufficient proof that the corresponding behavior is absent, that every item has medium risk, or that the Phase 2.14 human gate is the correct long-term owner.
- Human acceptance may still accept rc4 as a monitored-pilot candidate, but it must explicitly accept the unresolved exact-evidence debt and the coarse placeholder metadata described here. It must not be read as accepting production readiness or closing Phase 3/4 work.
- If the human requires corrected row-level metadata or exact evidence before transfer, rc4 must be rejected and a successor candidate must be built and recertified. No documentation-only edit can change the immutable candidate's evidence content.

## Reproducible Evidence

Commands run from the repository root:

```powershell
rg -n -i --hidden --glob '!\.git/**' "110|residual gaps?|residual.*gap|gap.*residual" .
python -c "import yaml,pathlib,collections; d=yaml.safe_load(pathlib.Path('process/certification/evidence-manifest.yaml').read_text(encoding='utf-8')); gaps=[x for x in d['coverage'] if 'gap' in x]; print(len(gaps)); print(collections.Counter(x['capability'] for x in gaps)); print(collections.Counter(x['gap']['follow_up'] for x in gaps))"
git log --all --oneline -- process/certification/evidence-manifest.yaml process/certification/coverage.yaml
git show <commit>:process/certification/evidence-manifest.yaml
python scripts/certify_process_release.py --root . --check
node "$env:USERPROFILE\.codex\skills\roadmap-openspec-validator\scripts\validate-roadmap-openspec.mjs" --root . --json
openspec list
openspec list --specs
openspec validate --all --strict
```

## Remediation Decision

Recommended default: do not mutate rc4. Use this routing audit for the human decision. If the human wants transfer without carrying coarse evidence debt, reject rc4 and create a successor-candidate remediation that:

1. converts the 12 Phase 3/4 rows to exact future-work selectors;
2. binds the one Phase 2 scope-boundary row to accepted manual evidence;
3. binds the 22 governance rows to exact dated decision/audit evidence with recurrence where needed;
4. reviews all 75 exact-evidence-debt rows against existing tests/manual records and adds focused tests only where exact proof is genuinely absent;
5. assigns row-specific owner, risk, reason, compensation, and follow-up for every gap that remains;
6. rebuilds and fully recertifies the successor candidate because coverage/evidence is part of candidate identity.

Residual uncertainty: individual product severity and the number of genuine missing behaviors remain unverified until that selector-level review is executed.
