# NIS v1.6 Architecture Compatibility Audit

Date: 2026-07-13.

Status: completed evidence audit with a subsequent accepted remediation decision. The original findings remain valid evidence; the original sequencing recommendation is superseded by `D-013` and active change `adopt-nis-corporate-process-governance`.

## Decision Addendum (2026-07-13)

After reviewing the audit, the human owner clarified that NIS reflects the target real corporate processes and selected its flat `minor | major | hotfix` classification. The project will adopt the business-process layer now through a dedicated OpenSpec change and Phase 2 workstream rather than leave it as research-only input.

The accepted remediation includes class criteria, `thin -> minor` and `full -> major` migration, hotfix safeguards, preliminary triage, Definition of Ready, implementation-complete and Definition of Done separation, release/archive/delivered separation, first-class Tech Lead governance and deterministic decision support, quality/regression/scope/stop/escalation/release controls, role-understanding evidence, human decision and AI-run evidence, flow-time categories, portfolio/pilot controls, and outcome measurement.

The audit's conflict findings are not discarded. They define the repairs required during adoption: one canonical OpenSpec/policy source, normalized and pre-approved thresholds, privacy/retention boundaries, failed-run retention, deterministic and AI-disabled fallbacks, no AI-owned approvals, no absolute zero-risk claim, and no inheritance of PPRB organization or NIS project structure.

Canonical follow-up:

- decision `D-013` in `docs/DECISIONS.md`;
- complete adoption plan in `docs/planning/NIS_CORPORATE_PROCESS_ADOPTION_PLAN_2026-07-13.md`;
- proposed normative behavior and implementation tasks in `openspec/changes/adopt-nis-corporate-process-governance/`;
- Phase 2 work item 2.3A in `docs/phases/PHASE_2_TRANSFER_READY_PROCESS_PACKAGE.md`.

## Executive Verdict

`NIS_Clean_v1.6_Approved_Package` is not a compatible replacement for the accepted teamSddCli architecture. It is best treated as a potentially valuable **experimental-governance overlay** and measurement source whose useful parts may be proposed later through OpenSpec.

The package has strong agreement with the project on the following foundation:

- SDD and Git-based engineering truth;
- Jira as workflow/intake rather than requirement truth;
- Confluence as generated publication rather than an editable master;
- CI/CD-backed checks and auditable evidence;
- human ownership of decisions and accountability;
- isolated pilots, explicit stop conditions, outcome metrics, and no client delivery from the experimental branch;
- MCP as an AI access boundary;
- measuring delivery outcomes rather than prompt, commit, or line-of-code activity.

The package also contains useful material that the current architecture does not yet define in comparable detail:

- a pre-registered paired experiment;
- historical, control, and experimental comparison sets;
- experiment-integrity rules and automatic data collection;
- outcome metrics covering time, human effort, cost, quality, completeness, and repeatability;
- experiment cards, execution logs, control-branch checks, CTO scorecards, role-understanding checks, and stop criteria;
- a later production-measurement layer based on delivery stability and DORA-like outcomes;
- stronger release-package and Nexus trace links for a future full production layer.

The package conflicts with accepted architecture when it is read as a production standard:

- it makes AI creation of every engineering artifact mandatory;
- it treats manual authoring, correction, and manual testing as methodology failures;
- it makes LLM/skills/MCP part of every production stage instead of an optional convenience layer;
- it lacks the required AI-disabled fallback for every gate;
- it moves from experiment to project-wide AI-only execution much faster than the accepted transfer-ready release and bounded thin-pilot gates;
- it duplicates normative rules across many documents and already contains material contradictions;
- it has no machine-readable process-package compatibility, schema, update, rollback, authority-labelled read-pack, weak-model certification, or no-fork transfer contract;
- it proposes AI-generated independent checks without clearly separating proposed test material from deterministic/human-accepted evidence.

Recommendation: preserve teamSddCli as the architecture and deterministic process core. If the human owner wants to reuse NIS, extract only the repaired experiment/measurement layer as a separate future OpenSpec change. Do not merge the NIS “AI-only production” principle into `D-001`, `D-003`, `D-012`, the accepted lifecycle/waiver/traceability contracts, or the active transfer-readiness change.

## Audit Boundary

### Target

- Accepted teamSddCli architecture and current proposed transfer-readiness architecture.
- Local reference package `docs/NIS_Clean_v1.6_Approved_Package/`.

### Explicit exclusions

- The team described in the NIS material is not the team for this project. Its composition, PPRB-specific role allocation, cluster/direction structure, staffing ratios, and reporting chain were not used as architecture acceptance criteria.
- The project/repository structure proposed by NIS was not evaluated as a competing topology because the teamSddCli topology has already been decided in `D-008` and the user explicitly excluded that comparison.
- This audit does not validate corporate runtime, Jira, Git, CI/CD, Nexus, MCP, model, security, or data-collection availability.
- The package was inspected as local reference material only. It remains git-ignored and is not copied into this audit.
- The audit authorizes findings and recommendations, not remediation or adoption into accepted OpenSpec behavior.

### Evaluation criteria

1. Source-of-truth and system boundaries.
2. Human, AI, deterministic-tool, and approval responsibilities.
3. Change lifecycle, evidence, traceability, and waiver boundaries.
4. MVP/pilot scope and rollout safety.
5. Transferability to the restricted corporate environment.
6. Weak-model and AI-disabled operation.
7. Security, privacy, rollback, and auditability.
8. Measurement validity and reproducibility.
9. Documentation governance and internal consistency.
10. Compatibility with the active Phase 2 release-candidate boundary.

### Classification and severity

- `pass`: verified agreement with accepted architecture.
- `useful complement`: adds useful material without changing accepted behavior if introduced through the proper proposal boundary.
- `verified conflict`: contradicts accepted behavior or an accepted boundary.
- `verified limitation`: required detail or evidence is absent.
- `unverified suspicion`: plausible concern that cannot be confirmed from the package.

Severity:

- `high`: would change a core architecture boundary, invalidate a gate, or create unsafe/ambiguous production behavior.
- `medium`: would weaken repeatability, evidence quality, maintainability, or adoption without immediately invalidating the architecture.
- `low`: localized inconsistency or clarity defect with a contained effect.

No `critical` issue was assigned because the package is local, ignored, and not active production behavior.

## Evidence Reviewed

### Canonical teamSddCli sources

- `AGENTS.md`.
- `docs/README.md`, `docs/00_FILE_STRUCTURE.md`, `docs/ROADMAP.md`, `docs/IMPLEMENTATION_STRATEGY.md`, `docs/CONTEXT.md`, `docs/DECISIONS.md`, `docs/CURRENT_PROJECT_AUDIT.md`, and `docs/AI_STEP_VERIFICATION_CHECKLIST.md`.
- Canonical decisions `D-001` through `D-012`.
- All eight accepted specifications under `openspec/specs/`.
- Active change `openspec/changes/define-transfer-ready-process-package/`, including proposal, design, tasks, `transfer-readiness`, and `weak-model-guardrails` deltas.
- `docs/phases/PHASE_2_TRANSFER_READY_PROCESS_PACKAGE.md`.
- `docs/planning/PROJECT_MEMORY_AND_WEAK_MODEL_GUARDRAILS.md`.
- Historical architecture audits and planning records used only to distinguish accepted decisions from rejected, superseded, or still-proposed material.

### NIS package evidence

- 22 files: 16 Markdown files, 3 CSV files, 1 PDF, 1 PPTX, and 1 verified montage image.
- All Markdown and CSV content was inspected.
- The 12-slide PPTX text was extracted and checked.
- The 12-page PDF was rendered and the supplied 12-slide montage was visually inspected.
- The PDF is unencrypted, has no JavaScript, and contains 12 pages.
- The deck has no observed clipping or layout defect that changes the architecture reading.

Principal source SHA-256 values:

| Source | SHA-256 |
|---|---|
| `NIS_Clean_v1.6_Standard.md` | `AB9A32A59859D500DD40592F8A7123CEADE2FB1A46770AC4996D7A07213DA2D1` |
| `NIS_Clean_v1.6_Experiment_Protocol.md` | `D36698865D8CFAE45ACD72011859CCBDF46FCCDF2A10E61A6E53CA4C960D366D` |
| `NIS_Clean_v1.6_Metrics_Guide.md` | `E65FD15F2E8B3436E9244706DF614856BC9441E32B11FC37C57830DF611F603F` |
| `NIS_Clean_v1.6_Implementation_Plan.md` | `D8FEB76A2BFA774C04BFEA37E59BDAD6A18B057E19E3572384E567E30B6A0950` |
| `NIS_Clean_v1.6_CTO_Decision_Memo.md` | `D084E5862AF0F5F8F83072B766605EAB085890BAD4918613116581F8E147519D` |
| `NIS_CTO_Executive_Deck_v1.6.pdf` | `9976E2B836664B023009D85592E4693A3F0334B8CB61A615B3C408E5EC5896EE` |
| `NIS_CTO_Executive_Deck_v1.6.pptx` | `D36D960BE69FE36FD50987D706DDA47F0CC5CB5B26DCC3EE8D3AB31749D936D5` |

### Reproducible inspection commands

```text
rg --files docs/NIS_Clean_v1.6_Approved_Package
Get-ChildItem -File -Recurse docs/NIS_Clean_v1.6_Approved_Package
Get-Content -Raw -Encoding UTF8 <package-file>
Get-FileHash -Algorithm SHA256 <principal-package-files>
git check-ignore -v docs/NIS_Clean_v1.6_Approved_Package
git ls-files | Select-String NIS_Clean_v1.6_Approved_Package
pdfinfo NIS_CTO_Executive_Deck_v1.6.pdf
pdftoppm -png -r 120 NIS_CTO_Executive_Deck_v1.6.pdf <temporary-output-prefix>
```

The PPTX text was read directly from the 12 slide XML parts. Temporary PDF renders were written outside the repository.

## Accepted Architecture Baseline

The comparison used these accepted boundaries rather than the removed historical architecture draft:

| Decision group | Accepted position | Canonical evidence |
|---|---|---|
| Source of truth | Git/OpenSpec is canonical; Confluence is a generated read model; Jira/tracker owns workflow/status; PR review and CI own review/evidence surfaces. | `D-001`, `D-009`, `D-010`; accepted Confluence and documentation-governance specs |
| Delivery mechanism | Deterministic templates, scripts, CI, and standard tool features come first; a custom CLI is trigger-gated. | `D-001`, `D-003`; `docs/IMPLEMENTATION_STRATEGY.md` |
| Human/AI boundary | AI drafts and reviews; humans own approval, merge, correctness, waiver, archive, and business/engineering decisions. Every gate works without AI. | `D-001`, `D-003`, `D-012`; accepted lifecycle/waiver specs; proposed weak-model guardrails |
| MVP | First prove a thin change flow and basic traceability. Jira task automation, Confluence publication, QA/AT proposal generation, deploy, Zephyr, and role inboxes remain later layers. | `D-002`, `D-012`; accepted artifact and lifecycle specs |
| Change evidence | Thin/full risk-oriented artifact contracts, scenario-first evidence, traceability, structured waivers, and six explicit lifecycle states. | `D-004`, `D-006`, `D-011`; accepted artifact/lifecycle/traceability/waiver specs |
| Reuse and topology | Central `team-specs`, central config plus optional project adapter, pinned OpenSpec `1.4.1`, one versioned process package, and `owners.yaml`. | `D-008`; accepted repo-topology-config spec |
| Transfer | Externally build and certify the reusable release candidate; corporate work is configuration, approved wiring, thin adapters, environment checks, and one monitored pilot. | `D-012`; active transfer-readiness change |
| Weak models | Deterministic launcher, bounded authority-labelled read packs, explicit stop points, evidence boundaries, negative cases, actual Qwen/DeepSeek certification, and AI-disabled fallback. | `D-012`; active weak-model-guardrails delta |
| Documentation | Write once/reference many; normative behavior stays in OpenSpec; derived artifacts cite canonical sources. | `D-005`, `D-006`; accepted documentation-governance spec |

## NIS Architecture Summary

NIS v1.6 describes two overlapping things:

1. A controlled experiment comparing current delivery with an AI-executed branch.
2. A target corporate production standard in which AI creates and changes every engineering artifact while humans state intent and approve results.

Its system model is:

```text
Jira intent
  -> SDD specification
  -> Git engineering truth
  -> AI-generated code/tests/documentation
  -> CI/CD validation
  -> Nexus artifact/release package
  -> human readiness decision
  -> metrics and CTO rollout decision
```

The experiment uses historical data plus isolated comparison branches, attempts to hold task input and acceptance criteria constant, records AI and human activity, forbids experimental output from reaching clients, retains failed runs, and evaluates time, human effort, cost, quality, package completeness, manual share, and repeatability.

This distinction is decisive. As an experiment treatment, “AI creates everything and manual correction is forbidden” can be a legitimate variable. As a production constitution, the same rule contradicts the accepted teamSddCli safety and fallback model.

## What Directly Aligns

| ID | NIS position | Alignment result | Canonical teamSddCli evidence |
|---|---|---|---|
| A-01 | SDD turns intent into testable specification. | pass | `D-001`; artifact and lifecycle specs |
| A-02 | Git holds engineering truth. | pass at the architectural level; repository placement was excluded from comparison | `D-001`, `D-008` |
| A-03 | Jira manages idea/intake/flow rather than canonical requirements. | pass | `D-001`, `docs/CONTEXT.md` |
| A-04 | Confluence is published from Git and is not the requirement source. | strong pass | `D-001`, `D-009`, `D-010`; Confluence spec |
| A-05 | CI/CD provides automatic verification. | pass, provided human approval is not inferred from green checks | lifecycle and documentation-governance specs |
| A-06 | Humans decide and remain accountable; AI is not the legal/business owner. | pass in principle | `D-001`; lifecycle and waiver specs |
| A-07 | MCP provides managed AI access to systems/context. | pass for AI-side Jira/Confluence access | `D-003`; implementation strategy |
| A-08 | Every change should be reconstructable from input through decisions, artifacts, tests, release evidence, and metrics. | strong pass | traceability contract; `D-004` |
| A-09 | Experimental output is isolated and does not reach clients. | pass | `D-012`; transfer-readiness safety boundary |
| A-10 | Failed runs remain visible; thresholds are registered before results. | pass and useful | documentation-governance evidence discipline |
| A-11 | Success is outcome-based, not prompt/commit/LOC activity. | strong pass | `docs/IMPLEMENTATION_STRATEGY.md` metrics and usability criteria |
| A-12 | Productive rollout should be measured for delivery speed and stability after pilot evidence exists. | pass as a later layer | roadmap and Phase 3/4 direction |

## What Would Usefully Complement The Architecture

These items are not accepted behavior. They are good candidates for a later OpenSpec proposal after their inconsistencies are repaired.

| ID | Candidate addition | Value | Required adaptation | Best timing |
|---|---|---|---|---|
| E-01 | Pre-registered experiment protocol | Prevents target/threshold changes after results and makes rollout evidence reviewable. | Define one canonical protocol schema and approval record. | Phase 3 pilot evidence or a post-pilot scaling change |
| E-02 | Historical + control + experimental comparison | Separates model effect from project history and one control worker's speed better than a simple before/after story. | Correct confounding, define control, and avoid claiming causality beyond the design. | Post-release-candidate evaluation |
| E-03 | Multi-dimensional outcome metrics | Adds end-to-end time, active human time, cost, first-pass acceptance, defects, package completeness, and repeatability to current process-health metrics. | Preserve current M1-M7/U1-U4; add a separate outcome metric dictionary with stable event definitions. | Pilot/scale evaluation |
| E-04 | Automatic event collection | Reduces self-report bias and supports reproducibility. | Define privacy, retention, data owner, event schema, clock source, missing-event behavior, and redaction. | Before any real monitored pilot |
| E-05 | Experiment integrity and stop rules | Client isolation, common input, no branch leakage, failed-run retention, safety stops, and data-collection stops are valuable controls. | Convert prose to deterministic/checklist evidence; remove absolute “no risk” claims. | Phase 3 pilot runbook |
| E-06 | Experiment card and task record | Creates an auditable unit for project/task selection, inputs, owners, thresholds, changes, and outcomes. | Link to change/requirement/scenario IDs; use structured schema rather than a detached Markdown form. | Phase 3 pilot package |
| E-07 | AI execution log | Captures model, context, MCP/tools, elapsed time, iterations, human decision, and stop reason. | Add model/runtime/package/read-pack IDs, canonical/evidence status, privacy filtering, and deterministic validation. | Phase 2 certification and Phase 3 pilot |
| E-08 | Role-understanding and team-lead checks | Makes onboarding expectations and stop authority explicit. | Derive role guides from canonical OpenSpec IDs; do not duplicate normative rules. | Role-kit and pilot onboarding |
| E-09 | Independent quality evaluation | Reduces solution-author bias and strengthens negative/security/architecture checks. | AI may propose tests, but deterministic checks and human QA ownership must define evidence; do not accept an AI checker as independent proof by itself. | Certification and pilot QA |
| E-10 | Release package + Nexus linkage | Extends traceability from requirements/tests to immutable build, rollback, deployment/support instructions, and operational handoff. | Keep outside the first thin MVP; introduce through a future full-package/release contract. | Later production layer |
| E-11 | Controlled/external wait-time measurement | Separates team-controlled flow from external queues and handoffs. | Define event ownership and avoid attributing external delay to team performance. | Pilot metrics |
| E-12 | DORA-like production validation | Tests whether experiment improvements survive real delivery. | Run only after bounded pilot acceptance; preserve rollback and incident safeguards. | Post-pilot rollout |

### Metrics relationship

The NIS metrics should complement, not replace, existing metrics:

- Current teamSddCli `M1-M7` and `U1-U4` measure process usability, review, traceability, bypass, waivers, support burden, and AI-disabled operation.
- NIS measures end-to-end treatment outcomes: calendar time, human effort, cost, quality, artifact completeness, manual share, and repeatability.
- A future metric contract should keep both layers and define exact events, denominators, comparison cohorts, missing-data behavior, and review cadence.

The 4-6 week protocol duration is not automatically a conflict with `D-012`. `D-012` forbids delivery dates and calendar deadlines in durable product/roadmap contracts; a pre-registered observation window may be a valid experiment parameter if it is stored in the experiment record rather than turned into a roadmap promise.

## What Conflicts With Accepted Decisions

| ID | Conflict | Severity | Accepted boundary violated | Impact |
|---|---|---|---|---|
| C-01 | Mandatory AI creation and modification of every engineering artifact | high | `D-001`, `D-003`, `D-012`; deterministic and human-authored fallback | Makes process success depend on the AI layer and can block safe completion when AI is unavailable or inadequate. |
| C-02 | Manual authoring/correction is a methodology failure and target manual share is zero | high | weak-model deterministic fallback; accepted evidence and waiver contracts | Removes the safe human path and turns a treatment variable into a production rule. |
| C-03 | Manual testing is prohibited; inability to automate is treated as methodology failure | high | traceability contract accepts manual QA evidence; waiver policy provides reviewed exceptions | Rejects valid evidence modes and is unsafe for scenarios that cannot yet be automated. |
| C-04 | LLM + skills + MCP participate at every stage | high | every gate must work with AI disabled | Creates an architectural dependency on AI/model/integration availability. |
| C-05 | A separate AI checker creates hidden acceptance, security, and architecture checks | high when treated as evidence | AI output is advisory; CI/human evidence owns gates | The evaluator shares AI failure modes and is not independent proof unless outputs are deterministically validated and human-owned. |
| C-06 | After a successful experiment, all new project functions move to NIS before the production-validation period | high | `D-012` requires accepted external RC, green adaptation, and one bounded monitored thin change | Expands exposure before bounded real-pilot evidence and rollback behavior are proven. |
| C-07 | Initial validation must use the busiest/highest-load project in each cluster/direction | medium/high for the first pilot | accepted first step is one bounded real thin change after transfer gates | Maximizes representativeness but also blast radius, confounding, coordination burden, and data exposure; better suited to later scale validation. |
| C-08 | NIS is framed as the production method, not a convenience layer over deterministic process | high | no autonomous central agent; standard tools and deterministic transitions own guarantees | Encourages orchestration around AI availability instead of reusable deterministic contracts. |
| C-09 | Normative rules are duplicated across the standard, memo, guide, deck, CSVs, and templates | high | write-once/reference-many documentation governance | The copies already disagree, so no reviewer can know which threshold or sample rule is authoritative. |
| C-10 | NIS v1.6 lacks process-package/config/schema/version compatibility, update/rollback, weak-model read-pack authority, AI-disabled certification, and no-fork transfer behavior | high limitation | `D-008`, `D-012`; active transfer-readiness change | It is not a transfer-ready executable process contract even though it is called an approved package. |
| C-11 | “Production risk is absent” is stated as an absolute | medium | risk must be evidence-backed; corporate/security/runtime facts remain unknown | Branch isolation reduces delivery risk but not data leakage, access, secret, cost, infrastructure, model, or accidental-merge risk. |
| C-12 | Package-wide rollout decisions depend on internally inconsistent success rules | high | deterministic evidence and human decision gates need one validated contract | The same results can lead to different decisions depending on which package artifact is used. |

## Verified Internal Package Inconsistencies

### I-01: “Approved package” contains a “working draft” standard

- Classification: verified defect.
- Severity: medium.
- Evidence: package name and README say approved; `NIS_Clean_v1.6_Standard.md` says `Статус: рабочая редакция для проверочного эксперимента`.
- Impact: approval status and normative authority are ambiguous.
- Root cause: not verified; likely different publication stages were assembled without one authority manifest.
- Residual uncertainty: a separate approval record may exist outside the package.
- Recommended action: add a signed/versioned manifest identifying normative, supporting, generated, template, and superseded artifacts.

### I-02: Viability thresholds disagree

- Classification: verified defect.
- Severity: high.
- Evidence:
  - CTO memo and slide 8 use roughly 30% faster, 50% less human involvement, and 80% AI-complete functions.
  - Standard section 18 and Metrics Guide section 7 use 20% faster, 40% less human involvement, 100% package completeness, zero manual execution, and effect in at least 70% of projects.
  - `NIS_Clean_v1.6_Metrics.csv` and `templates/cto-scorecard.csv` use -20% and -40%.
- Impact: the CTO can reach different viability decisions from the same data.
- Root cause: not verified; the executive deck/memo and detailed method were not regenerated from one metric contract.
- Residual uncertainty: none about the textual conflict; intended final thresholds are unknown.
- Recommended action: one typed metric/decision schema must generate the memo, deck, guide, CSV, and scorecard.

### I-03: Manual-execution rule disagrees

- Classification: verified defect.
- Severity: high.
- Evidence:
  - CTO memo accepts at least 80% of functions completed without manual artifact creation.
  - Standard and Metrics Guide require 0% manual execution and classify any manual change as failure/stop evidence.
  - The “requires refinement” range in the Standard allows isolated manual violations, which conflicts with the absolute stop/failure wording.
- Impact: experiment integrity and outcome classification are not deterministic.
- Root cause: not verified.
- Residual uncertainty: whether a stopped task may later be counted as a refined-but-viable result is unclear.
- Recommended action: define task-level contamination status separately from project-level decision thresholds.

### I-04: Minimum sample disagrees

- Classification: verified defect.
- Severity: high.
- Evidence:
  - CTO memo, Implementation Plan, and deck require at least 5 functions.
  - Standard and Experiment Protocol require at least 8 NIS changes, at least 3 major changes, at least 4 control implementations, and at least 8 historical changes.
  - Some selection/slide text uses at least 2 major changes; the detailed protocol uses at least 3.
- Impact: stopping and sufficiency rules are ambiguous and can enable selective reporting.
- Root cause: not verified.
- Residual uncertainty: whether 5 is a project-entry minimum and 8 is an experiment-completion minimum is not stated.
- Recommended action: define distinct entry, interim, minimum-analysis, and decision-ready sample gates.

### I-05: Project-selection formula disagrees

- Classification: verified defect.
- Severity: medium.
- Evidence:
  - Slide 9 weights changes 30%, releases 20%, production load 25%, active plan 15%, integrations/dependencies 10%.
  - `NIS_Clean_v1.6_Project_Selection.csv` weights changes 30%, feature flow 25%, complexity diversity 15%, historical data 15%, isolation 10%, owner stability 5%.
  - Standard and checklists use descriptive criteria rather than either exact formula.
- Impact: different teams can choose different “most active” projects under the same package.
- Root cause: not verified.
- Residual uncertainty: the deck may be an executive simplification, but it claims one formula.
- Recommended action: one selection schema and generated views; executive simplification must retain the same fields and weights.

### I-06: Control definition is not stable across documents

- Classification: verified limitation.
- Severity: medium.
- Evidence: some documents describe the current production team/main branch as the comparison; the detailed Standard and Experiment Protocol add a separate one-person control branch plus historical baseline; the Implementation Plan mainly describes the normal production branch and the experimental branch.
- Impact: the causal question changes between “AI specialist vs team,” “AI specialist vs manual specialist,” and “AI treatment vs history.”
- Root cause: not verified.
- Residual uncertainty: the intended primary estimator is not named.
- Recommended action: define the estimand, primary comparator, secondary comparator, staffing equivalence, and analysis plan before data collection.

### I-07: Rollout rule can precede organization-level evidence

- Classification: verified defect.
- Severity: high.
- Evidence: Implementation Plan step 7 moves all new functions of a project to NIS after the CTO decision, while the detailed viability rule requires effect across at least 70% of participating projects and the package also calls for later production validation.
- Impact: project-wide exposure may occur before cross-project evidence exists or before production stability is known.
- Root cause: not verified.
- Residual uncertainty: the CTO may make separate project and organization decisions, but the artifacts do not define this hierarchy.
- Recommended action: separate task, project, portfolio, production-pilot, and organization rollout gates.

## Evidence-Audit Findings

### NIS-AUD-001: Foundation boundaries substantially agree

- Classification: pass.
- Severity: none.
- Affected behavior: source-of-truth, publication, workflow, audit, and human-accountability architecture.
- Evidence: NIS Standard sections 1, 3, 4, 7, 8; deck slides 3, 4, 7, 11; teamSddCli `D-001`, `D-003`, accepted lifecycle, traceability, documentation-governance, and Confluence contracts.
- Root cause: not applicable.
- Residual uncertainty: NIS uses “Git” broadly and does not express teamSddCli source-ownership detail; repository topology was intentionally excluded.
- Recommended action: retain these shared principles; do not duplicate them into a second normative standard.

### NIS-AUD-002: The package is usable only after separating experiment treatment from production constitution

- Classification: verified conflict.
- Severity: high.
- Affected behavior: human fallback, AI-disabled operation, role responsibility, and rollout.
- Evidence: Standard sections 2, 5, 10, and 11 make AI-only artifact production and no manual testing part of the target process; `D-001`, `D-003`, `D-012`, active weak-model guardrails, and accepted traceability/waiver contracts require AI to remain optional and advisory.
- Root cause: the package intentionally tests a strong AI-only treatment but reuses the same statement as its target production standard.
- Residual uncertainty: the authors may intend the AI-only restriction only during the experiment, but the Standard explicitly calls it the target mode.
- Recommended action: split the package into an experiment protocol and a production architecture. Only the experiment protocol is a candidate for adaptation.

### NIS-AUD-003: Experimental measurement design is valuable but not yet decision-safe

- Classification: useful complement with verified limitations.
- Severity: high until normalized.
- Affected behavior: pilot acceptance and rollout evidence.
- Evidence: paired task inputs, historical/control/experimental groups, automatic events, medians, failed-run retention, pre-registered thresholds, and outcome metrics are described in the Experiment Protocol, Metrics Guide, Methodological Basis, and Standard; I-02 through I-07 show contradictory decision rules.
- Root cause: multiple hand-maintained audience documents were assembled without one typed metric/experiment contract.
- Residual uncertainty: no raw data, analysis code, statistical plan, or actual experiment results were supplied.
- Recommended action: define one canonical experiment and metric schema plus deterministic score generation before using the package for a decision.

### NIS-AUD-004: “No production risk” is only partially supported

- Classification: verified limitation.
- Severity: medium.
- Affected behavior: pilot authorization and safety representation.
- Evidence: branch isolation, no client merge, and stop rules reduce client-delivery risk; the package does not define secret handling, private-data controls, log redaction, retention, access review, model data policy, adapter failure recovery, or accidental-merge technical enforcement.
- Root cause: the package focuses on delivery isolation and measurement rather than the full security/data boundary.
- Residual uncertainty: corporate controls may exist outside the package.
- Recommended action: replace the absolute claim with a risk register and require transfer-readiness privacy/security evidence before any real data is used.

### NIS-AUD-005: Independent QA is only independent if evidence ownership is external to the model

- Classification: verified conflict with a salvageable idea.
- Severity: high.
- Affected behavior: acceptance, security, and architecture evidence.
- Evidence: Experiment Protocol section 3 delegates public/hidden acceptance, security, and architecture checks to a separate AI checker; teamSddCli requires deterministic checks and human-owned QA/approval, and rejects unsupported AI claims as evidence.
- Root cause: NIS equates separation of agent roles with independence of evidence.
- Residual uncertainty: the checker may emit executable tests that are later validated, but that acceptance boundary is not stated.
- Recommended action: let a separate model propose adversarial tests, but freeze the test strategy before implementation, validate tests deterministically, preserve human QA ownership, and keep a non-AI path.

### NIS-AUD-006: Initial rollout order is incompatible with the active transfer gate

- Classification: verified conflict.
- Severity: high.
- Affected behavior: external release acceptance, corporate pilot entry, and rollout blast radius.
- Evidence: NIS starts with the busiest projects, multiple parallel functions, and a possible whole-project switch; `D-012` and the transfer-readiness delta require an externally accepted release candidate, green adaptation evidence, and one bounded real thin-change pilot before expansion.
- Root cause: NIS optimizes for statistical representativeness, while teamSddCli currently optimizes for safe transfer and first-flow validation.
- Residual uncertainty: NIS may be suitable after the bounded pilot, not before it.
- Recommended action: preserve Phase 2/3 ordering. Consider NIS-style multi-project evaluation only as a later scaling experiment.

### NIS-AUD-007: NIS adds a valuable later release/operations layer but not first-MVP scope

- Classification: useful complement.
- Severity: medium scope risk.
- Affected behavior: full-package release evidence, Nexus traceability, rollback, installation/support instructions, and operational metrics.
- Evidence: Standard sections 8, 12, and 19; teamSddCli `D-002` and active transfer change explicitly defer deploy and broad production integration from the thin MVP.
- Root cause: NIS targets the full engineering cycle; teamSddCli intentionally stages adoption.
- Residual uncertainty: corporate Nexus and deployment boundaries remain unverified.
- Recommended action: route this into a later full-package/release OpenSpec change; do not add it to Phase 2 release-candidate scope except where process-package rollback is already required.

### NIS-AUD-008: Documentation architecture is not safe for weak models or deterministic enforcement

- Classification: verified conflict.
- Severity: high.
- Affected behavior: authority selection, thresholds, sampling, rollout, and evidence interpretation.
- Evidence: I-01 through I-07; accepted documentation-governance requires one canonical owner, derived metadata, and conflict correction from source.
- Root cause: normative content is copied into the standard, memo, deck, guides, CSVs, and templates rather than generated from one canonical contract.
- Residual uncertainty: no external manifest or generation pipeline was supplied.
- Recommended action: normalize to typed canonical records and generate audience views. Label every package artifact as canonical, supporting, generated/advisory, template, or evidence.

### NIS-AUD-009: Transfer readiness and weak-model safety are absent

- Classification: verified limitation.
- Severity: high.
- Affected behavior: reusable installation, compatibility, corporate adaptation, weak-model authority, privacy, update, rollback, and certification.
- Evidence: no process-package manifest/schema, version compatibility, clean bootstrap, AI-disabled walkthrough, Qwen/DeepSeek certification, authority-labelled read pack, negative certification suite, release manifest, or no-fork path exists in the package; these are mandatory under `D-012` and the active change.
- Root cause: NIS is a policy/experiment package, not an executable transfer-ready process distribution.
- Residual uncertainty: implementation may exist elsewhere but was not included.
- Recommended action: do not treat NIS “approved package” status as transfer evidence. Complete the active Phase 2 architecture first.

### NIS-AUD-010: Organizational conclusions are intentionally not assessed

- Classification: audit limitation.
- Severity: none.
- Affected behavior: staffing, team composition, portfolio governance, cluster/direction participation, PPRB roles, and role ratios.
- Evidence: explicit user instruction that the documented PPRB team is a different team.
- Root cause: not applicable.
- Residual uncertainty: none of the staffing or governance recommendations can be assumed applicable to the target team.
- Recommended action: if organizational adoption is later considered, run a separate role/process fit audit against the real team and owner model.

## Recommended Integration Boundary

### Adopt as already-compatible principles

- Git/SDD engineering truth.
- Jira workflow/intake boundary.
- Generated Confluence publication.
- CI/CD and audit evidence.
- Human decision/accountability ownership.
- Isolated non-client experiment outputs.
- Outcome-focused measurement.
- Pre-registered thresholds and failed-run retention.

These should remain referenced through current canonical decisions/specs rather than copied from NIS.

### Propose later after repair

1. A canonical experiment protocol and evidence schema.
2. A metric dictionary and deterministic scorecard generator.
3. Historical/control/experimental comparison records with an explicit primary comparator and analysis plan.
4. Event collection, privacy, retention, and missing-data contracts.
5. Experiment/task cards linked to change, requirement, scenario, PR, test, and release evidence.
6. An AI execution/certification log extended with exact model/runtime, adapter, package, and read-pack identity.
7. Role-understanding checks and stop authority derived from canonical OpenSpec sources.
8. Independent/adversarial test generation as advisory input to deterministic/human QA evidence.
9. Later full-package release/Nexus/rollback/support traceability.
10. Post-pilot DORA-like production measurement.

### Reject as architecture defaults

- AI-only production of all engineering artifacts.
- Zero-manual-authoring as a permanent process gate.
- No manual testing as a permanent policy.
- AI checker output as self-sufficient independent evidence.
- Mandatory LLM/MCP availability for every stage.
- Busiest-project-first as the initial corporate pilot.
- Whole-project AI-only conversion before a bounded production pilot and rollback proof.
- Absolute claims that branch isolation removes all production/security risk.
- Hand-maintained normative copies across deck, standard, guides, CSVs, and templates.

## Decision And Sequencing Recommendation

Historical note: the recommendation in this section was the auditor's pre-decision default. It is superseded by the human decision addendum above. The risk evidence and required corrections remain applicable.

### Current Phase 2

Do not add the full NIS experiment to Phase 2. Phase 2 must remain focused on the accepted transfer-ready deterministic process package, weak-model operating kit, AI-disabled operation, real Qwen/DeepSeek certification, bootstrap/update/rollback, release manifest, and transfer runbooks.

The only immediately reusable NIS idea that already fits Phase 2 is the shape of richer certification evidence: exact inputs, model/tool activity, human decisions, retries, stop reason, deterministic result, and limitations. Even that should be implemented from the active weak-model-guardrails requirements, not copied as a second contract.

### Phase 3 bounded pilot

Use a small subset of NIS measurement ideas for the already-approved one real thin-change pilot:

- fixed input and acceptance criteria;
- event timestamps;
- human intervention;
- deterministic results;
- defects/deviations;
- rollback/hold evidence;
- installed package/model/adapter identifiers.

Do not require a second full manual implementation of the same real change unless separately approved; that can double cost, expose data, and delay the safety pilot without proving the release-candidate gate.

### Post-pilot scale experiment

If the bounded pilot is accepted, create a separate OpenSpec change for an NIS-derived scale experiment. That proposal should first resolve I-01 through I-07, define privacy and analysis contracts, and decide whether a paired control is worth the cost. Only then consider active/high-load projects and cross-project repeatability.

## Residual Risks And Unknowns

- No actual NIS experiment data or result set was included, so no effectiveness claim is verified.
- No corporate access, data protection, model policy, cost model, runtime, integration, or retention rule was inspected.
- No evidence proves that the standard, deck, memo, metrics guide, and templates are generated from one approved source; observed differences indicate they are not currently safe to treat as one contract.
- No evidence establishes that AI-only artifact generation or zero manual testing is viable for security, compliance, accessibility, exploratory testing, operations, or incident-response scenarios.
- The busiest-project selection rule may improve external validity but worsens blast radius and confounding; the right population and sampling design remain a human/methodology decision.
- The package's organization and PPRB assumptions were intentionally excluded and cannot be reused without a separate audit.

## Documentation Impact

- This dated audit is the durable owner of the comparison evidence and recommendations.
- The audit itself did not modify accepted behavior. The later human remediation decision created `D-013`, a dedicated active OpenSpec change, an adoption plan, and a Phase 2 workstream; accepted specs and implementation remain unchanged until that change is applied and promoted.
- `docs/00_FILE_STRUCTURE.md` should reference this audit.
- The local NIS package remains ignored and untracked.

## Remediation Decision

Resolved by the human owner on 2026-07-13: adopt the repaired NIS corporate process through `adopt-nis-corporate-process-governance` and Phase 2 work item 2.3A. The choice is the flat NIS classification and a strong corporate-process foundation, not a research-only metrics overlay.

Implementation remains pending. Phase 2 work item 2.1 stays ready because package/config/schema foundation is still the prerequisite; class-dependent reference-flow, role, certification, release, and pilot work must consume the new governance contracts before final acceptance.
