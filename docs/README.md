# teamSddCli`r`n`r`n## Начать с FAQ`r`n`r`nДля первого знакомства с продуктом, безопасного запуска `sdd` и роли в процессе используйте [человекочитаемый FAQ и role runbooks](faq/index.md). Канонические OpenSpec-спецификации и specialist runbooks остаются источниками правил.

## Summary

teamSddCli is a local SDD process-automation project for a team workflow based on OpenSpec/Markdown, Git, deterministic validation scripts, Bitbucket, Jenkins, Confluence, Jira or another task tracker, and local AI tools.

The project goal is to automate the end-to-end transition from analysis to development tasks, QA test cases, automated-test skeletons, verification, and archived living specs without introducing one centralized autonomous agent. The delivery strategy is deliberately two-stage: first make the complete governed process reliable without AI, then progressively automate bounded process work with AI over the deterministic control plane. Reliability grows through broader risk-oriented test coverage and end-to-end evidence traceability; delivery speed grows through safe parallel AI work on explicitly independent tasks.

Current checkpoint:

> Phase 1 produced the accepted OpenSpec baseline and Phase 2 is closed under `D-020`: immutable candidate `phase-2-14-rc6` is the external transfer baseline with process package `0.3.0`, payload SHA-256 `172707ba159e1e060561d6d02ad67dcaf2fa4ce64a58c23bd9c55613713fd951`, manifest SHA-256 `0c7670637f1f59f82a6cae3bea48c53edfa3453d5fcf0c599bf013bd301c3146`, and `295 covered / 7 gaps / 32 future_work`. `D-021` adds a new pre-corporate Phase 3: the reusable package must become self-service through a situation-based guided-operation contract for humans and AI assistants before any corporate configuration or pilot. The guided workflow has passed its focused synthetic, AI-disabled, local Qwen/DeepSeek preflight, and negative-path checks; its separately versioned successor candidate is still pending. RC6 remains immutable; Phase 4 performs corporate adaptation and a monitored pilot. Historical rc4 remains unchanged, rc5 is retained as diagnostic rejected history, and macOS is not certified.

РўРµРєСѓС‰РёР№ РїР°РєРµС‚ `0.3.1` СЃРѕРґРµСЂР¶РёС‚ РїСЂРѕРІРµСЂСЏРµРјС‹Р№ `baseline-reuse`: СЃРІРµР¶РёРµ Qwen Рё
DeepSeek preflight РїСЂРѕС€Р»Рё, Р° РїРѕР»РЅР°СЏ matrix `0.3.0` СЃРІСЏР·Р°РЅР° СЃ РЅРёРјРё С‚РѕС‡РЅС‹РјРё
hashes. РСЃС‚РѕСЂРёС‡РµСЃРєРёРµ raw-artifact roots РЅР°Р№РґРµРЅС‹ РІ Р»РѕРєР°Р»СЊРЅРѕРј Р°СЂС…РёРІРµ
`C:\Users\danoc\Documents\certifications`: 48 Р·Р°СЏРІР»РµРЅРЅС‹С… С„Р°Р№Р»РѕРІ СЃРІРµСЂРµРЅС‹ РїРѕ
SHA-256 Рё СЃРѕР±СЂР°РЅ С‡РёСЃС‚С‹Р№ exact bundle Р±РµР· Р»РёС€РЅРёС… runtime probe. Р”РёР°РіРЅРѕСЃС‚РёС‡РµСЃРєРёР№
`rc3` Р±С‹Р» РѕС‚РєР»РѕРЅС‘РЅ, РїРѕС‚РѕРјСѓ С‡С‚Рѕ РµРіРѕ СѓРїСЂР°РІР»СЏСЋС‰РёР№ CLI Р·Р°РїРёСЃС‹РІР°Р» Python bytecode РІ
payload; РїСЂРёС‡РёРЅР° СѓСЃС‚СЂР°РЅРµРЅР° РѕС‚РґРµР»СЊРЅС‹Рј СЂРµРіСЂРµСЃСЃРёРѕРЅРЅС‹Рј С‚РµСЃС‚РѕРј. РќРѕРІС‹Р№ immutable
candidate `guided-owner-v0.3.1-rc4` СЃРѕР±СЂР°РЅ, РµРіРѕ manifest РІР°Р»РёРґРµРЅ РґРѕ Рё РїРѕСЃР»Рµ
Windows full-clean rehearsal, РєРѕС‚РѕСЂР°СЏ passed. Р’Р»Р°РґРµР»РµС† РїСЂРёРЅСЏР» СЌС‚РѕС‚ РєР°РЅРґРёРґР°С‚ РїРѕ
`D-023` Рё СЂР°Р·СЂРµС€РёР» РµРіРѕ СЃР»РёСЏРЅРёРµ РІ `main`. РђРІС‚РѕРјР°С‚РёС‡РµСЃРєРёР№ `accept` РЅРµ РјРѕР¶РµС‚
РІРµСЂРЅСѓС‚СЊ `evidence-complete`, РїРѕС‚РѕРјСѓ С‡С‚Рѕ РЅР° РјР°С€РёРЅРµ РЅРµС‚ WSL-РґРёСЃС‚СЂРёР±СѓС‚РёРІР° РґР»СЏ
Linux/WSL2 portability smoke; СЌС‚Рѕ СЏРІРЅРѕ РїСЂРёРЅСЏС‚РѕРµ РѕСЃС‚Р°С‚РѕС‡РЅРѕРµ РѕРіСЂР°РЅРёС‡РµРЅРёРµ, Р° РЅРµ
СЃС„Р°Р±СЂРёРєРѕРІР°РЅРЅС‹Р№ passed result. Linux/WSL2 РїСЂРѕРІРµСЂРєР° РѕР±СЏР·Р°С‚РµР»СЊРЅР° РґРѕ Phase 4.

## Scope

In scope:

- OpenSpec/Markdown-first workflow where Git/OpenSpec is the canonical engineering source.
- Deterministic SDD process capabilities for change creation, validation, PR support, archiving, traceability, and later publication/task/QA/AT support, delivered first through templates, validation scripts, CI/pre-commit checks, standard tool features, and role skills.
- Integration boundaries for Bitbucket, Jenkins, Confluence, Jira or an equivalent tracker, code repositories, QA repositories, and AT repositories.
- Change packages with proposal, design, tasks, spec deltas, QA plans, test cases, automation plans, and traceability.
- Local AI support for drafts, reviews, context packs, and test or automation skeletons.
- Later progressive AI automation of bounded orchestration, evidence assembly, routing, monitoring, and transition preparation after the deterministic process and pilot are stable.
- Risk-oriented positive and negative test expansion plus requirement/scenario-to-task/test/evidence traceability as primary reliability mechanisms.
- AI-assisted task decomposition and parallel execution when dependencies, ownership, write scopes, evidence, and integration checks prove that the work is independent and safe to combine.
- External certification of minor, major, hotfix, and Tech Lead workflows with Qwen/DeepSeek-class assistants while all gates remain executable with AI disabled.
- Phase-based delivery of a minimal pilot, task automation, QA/AT automation, and process hardening.

Out of scope:

- Treating Confluence as the editable source of truth for requirements.
- Bidirectional Git/Confluence synchronization.
- Letting AI approve, merge, own process state, or replace human accountability.
- Building a centralized background autonomous agent as the first architecture.
- Assuming concrete corporate credentials, project owners, repository URLs, or production deployment details before they are verified.

## Key Decisions

Canonical decision IDs now live in `docs/DECISIONS.md`. The bullets below remain an orientation summary and should not be treated as the canonical log.

- 2026-07-03: Use the historical architecture draft as the initial bootstrap input.
- 2026-07-03: Use OpenSpec/Markdown in Git as the canonical source and Confluence as a generated publication layer.
- 2026-07-03: Automate artifact state transitions through deterministic checks, CI, templates, and standard tool features rather than centralizing control in one autonomous agent.
- 2026-07-03: Keep human ownership over approvals, merges, business decisions, correctness, and review outcomes.
- 2026-07-03: Use this starter-kit documentation set as the durable operating system for future Codex work.
- 2026-07-03: Narrow the first implemented MVP to a thin change flow: create a change package from templates, validate it deterministically, support Spec PR review, archive approved changes into living specs, and keep basic `traceability.yaml`; Jira task automation, QA/AT proposal generation, Confluence publication, and role inboxes are later layers unless explicitly re-scoped.
- 2026-07-03: Support two change modes in future requirements: a lightweight `thin change` path for small bugfix/refactor/small behavior patches and a `full change package` path for feature, API, mobile, cross-repo, or high-risk changes.
- 2026-07-03: The first product OpenSpec specs should focus on change lifecycle, artifact contracts, traceability, and waiver behavior before broad integration coverage.
- 2026-07-03: Confluence feedback handling must be explicitly specified before implementation: owner, service expectation, unresolved-feedback handling, and how comments become accepted deltas or rejected notes.
- 2026-07-03: Future mutating automation or integration entry points should be designed with dry-run behavior, idempotency, machine-readable JSON output, and auditable action logs.
- 2026-07-03: Gherkin is not mandatory for every QA artifact; every requirement needs at least a testable scenario, while Gherkin should be required only when a scenario is executable or exported to AT.
- 2026-07-03: Deliver the SDD process through the deterministic base first: templates, validation scripts, pre-commit/Jenkins checks in `team-specs`, standard tool features (Bitbucket default reviewers, Jira Automation, markdown->Confluence publisher, OpenSpec CLI), and AI role skills as a convenience layer. A custom wrapper is optional future ergonomics only when the trigger criteria in `docs/IMPLEMENTATION_STRATEGY.md` fire.
- 2026-07-03: OpenSpec means Fission-AI/OpenSpec; the team reference documentation is <https://lzw.me/docs/openspec> (community multilingual mirror; upstream docs win on discrepancy); the CLI version is pinned.
- 2026-07-03: Jira and Confluence access from AI tooling goes through MCP servers, not hand-written REST integrations; MCP was tested by the human owner and works. Automating local MCP server provisioning for employees is a planned experiment.
- 2026-07-03, refined 2026-07-13: Development happens externally and produces an accepted transfer-ready release candidate before entry into the internal corporate environment. The external package is certified with actual Qwen-class and DeepSeek-class assistants plus an AI-disabled walkthrough; the internal environment may expose Qwen/DeepSeek/GigaCode-class tools and is limited to real configuration, approved wiring, thin adapters, and a monitored pilot.
- 2026-07-03: Start Phase 1 with the deterministic base artifact `templates/change/` + `scripts/validate_change.py` + `.pre-commit-config.yaml`, tracked as project OpenSpec change `add-change-template-validation`.
- 2026-07-06: Approve the risk-oriented thin/full artifact matrix as the Phase 1 default: thin behavior-changing SDD changes need intent, OpenSpec delta, scenario, traceability, and verification evidence; full packages are required for new feature, public API, mobile, cross-repo, data/security, high-risk, or broad behavior changes.
- 2026-07-06: Approve role-appropriate waiver ownership: QA owners approve test evidence gaps, AT owners approve automation gaps, tech leads approve design/risk exceptions, and analyst/product owners approve scope or documentation exceptions, with reason, affected requirement/scenario, approver, substitute evidence, and follow-up/expiry when risk remains.
- 2026-07-06: Reconfirm the first MVP boundary: Jira task automation, Confluence publication, QA/AT proposal generation, and role inboxes remain outside the first MVP and are planned as later layers.
- 2026-07-06: Treat Confluence publication as generated audience views, not raw OpenSpec 1:1 and not a separate MasterSpec source; generated pages must carry source commit, change/PR ID, timestamp, source warning, and links back to canonical Git/OpenSpec files.
- 2026-07-06: Earlier English-by-default source-language guidance was revised by the later canonical-language decision below; this project's process specs stay English, while team product analytics specs use Russian prose with English structural keywords and stable IDs.
- 2026-07-06: Add a future legacy baseline mode for already-written code so the team records observed behavior, gaps, risks, and regression scenarios gradually instead of retroactively creating full historical change packages.
- 2026-07-06: Remove the stale historical architecture draft from the repository; current architecture decisions and product contracts live in `docs/`, `openspec/`, and accepted human decisions.
- 2026-07-06: Plan a project memory triad for agent and team orientation: constitution/quality policy for rules and boundaries, project map for topology/config/repository map, and OpenSpec changes/living specs for behavior contracts.
- 2026-07-06: Formalize existing-code onboarding as a future `scan -> baseline -> map -> validate` flow: scan is read-only, baseline records observed behavior/gaps/risks, map updates project memory, and validate checks memory against real code.
- 2026-07-06: Plan `sync` and `upgrade` as deterministic maintenance, not agent magic: `sync` checks drift across project map, specs, traceability, and code evidence; `upgrade` migrates templates/spec-package versions only after the OpenSpec version policy is approved.
- 2026-07-06: Use a PDLC narrative when explaining the process to the team: the goal is shared context from analysis through tasks, tests, verification, and publication, not merely faster code generation.
- 2026-07-06: Keep deploy, Zephyr/test-management integration, Jira task automation, Confluence publication, QA/AT proposal generation, and role inboxes outside the first MVP unless the human owner explicitly re-scopes the pilot.
- 2026-07-06: Use source ownership and write-once/reference-many documentation rules: OpenSpec owns behavior and acceptance, while docs, memory, role guides, and generated views reference canonical source IDs or metadata instead of carrying divergent copies.
- 2026-07-06: Adopt the six internal lifecycle states (`draft`, `spec_review`, `approved`, `in_implementation`, `ready_to_archive`, `archived`) as canonical for accepted specs and deterministic validation; simplified lifecycle names may appear only in generated business-facing views.
- 2026-07-06: Enforce the approved artifact matrix and waiver checks as errors immediately when work item 1.8 expands the validator; no warnings-only staging period.
- 2026-07-06 / 2026-07-09: The canonical human decision log now exists as `docs/DECISIONS.md`; see `D-006` for the consolidation decision and use decision IDs from that file when updating derived docs.
- 2026-07-06: Merge the OpenSpec version pin/upgrade policy into the `define-repo-topology-config` proposal as one platform-assumptions contract with a single human decision gate.
- 2026-07-06: Adopt team-facing terminology `Master Spec` (accepted living specs) and `Delta Spec` (proposed change spec deltas) so the company understands the concept; canonical folder names and OpenSpec CLI terms stay unchanged, and the generated-view term is renamed to `Master Spec views` to avoid collision.
- 2026-07-06: Treat reusability by other teams - easy bootstrap of the deterministic base, templates, and skills in another team - as an explicit design constraint for the `define-repo-topology-config` proposal, without expanding the first MVP.
- 2026-07-06: Revise the canonical-language decision: team product analytics specs (requirements/scenarios prose) are written in Russian with English structural keywords (`SHALL`, `WHEN`, `THEN`) and English stable IDs; this project's own process specs stay English; a strict-mode probe confirmed OpenSpec validates Russian prose. Generated business views remain Russian and a bilingual glossary is still required for IDs and terms.
- 2026-07-20, `D-022`: supersede the remaining English-process-spec rule for new work. New project documentation and OpenSpec prose are written in Russian; stable IDs, file paths, CLI/API tokens, and structural OpenSpec keywords remain English where tooling or cross-references require them. Historical accepted and immutable evidence is preserved without bulk translation.
- 2026-07-09: Accept the full Phase 1 readiness-complete OpenSpec package and archive/promote all eight changes into accepted specs in one batch execution step; future corrections now use new OpenSpec changes against `openspec/specs/`.
- 2026-07-13, refined 2026-07-20 by `D-021`: Require an externally completed transfer-ready release candidate before corporate adaptation. Reusable core, deterministic gates, process package, bootstrap/update/rollback, role instructions, bounded read packs, actual Qwen/DeepSeek certification, and self-service guided operation are external work; the corporate environment is limited to real configuration, approved wiring, thin adapters, and a monitored pilot. Planning is gate-based and does not record delivery dates or calendar deadlines.
- 2026-07-13: Adopt NIS v1.6 as primary corporate-process input and the flat target classification `minor | major | hotfix`. Migrate legacy `thin -> minor` and `full -> major`, never infer hotfix, and add class-aware DoR/DoD, separate release/archive/delivered states, Tech Lead decision support, regression/scope/stop/escalation/release controls, role verification, pilot safety, and failed-run retention. Exclude process-effectiveness evaluation and correct unsafe AI-only/zero-risk assumptions; do not inherit PPRB organization or NIS project structure. See `D-013` and active change `adopt-nis-corporate-process-governance`.
- 2026-07-14: Adopt the two-horizon automation strategy in `D-014`: AI-disabled deterministic operation is the first delivery requirement and permanent fallback, while later accepted changes should progressively automate bounded process execution with AI. Human authority and deterministic verification remain explicit boundaries rather than accidental limitations of the first release.
- 2026-07-14: Adopt `D-016`: improve reliability through broader risk-oriented testing and end-to-end traceability, and improve speed through AI-assisted parallel execution of independent tasks with explicit ownership, separate evidence, and deterministic integration checks.

## Architecture Sources

The historical architecture draft was removed on 2026-07-06 after its useful decisions had been captured in durable project documentation and Phase 1 OpenSpec proposals.

A recorded critique of that now-removed draft, with evaluation criteria, external comparison, recommendations (REC-001..REC-007), and alternative lightweight solution paths, lives in `docs/audits/ARCHITECTURE_CRITIQUE_2026-07-03.md`. Its recommendations are historical planning inputs; only items already listed under Key Decisions or accepted OpenSpec specs/changes are accepted.

Current architecture sources:

- `docs/README.md` for product summary, scope, key decisions, and first valuable outcome.
- `docs/CONTEXT.md` for canonical terms and boundary rules.
- `docs/IMPLEMENTATION_STRATEGY.md` for the accepted deterministic-process-first delivery strategy.
- `docs/ROADMAP.md` and `docs/phases/` for phase scope, gates, and current work.
- `docs/planning/PROJECT_MEMORY_AND_WEAK_MODEL_GUARDRAILS.md` for the broader memory/guardrail source analysis; its minimum transfer subset is promoted into the active Phase 2 change.
- `docs/planning/NIS_CORPORATE_PROCESS_ADOPTION_PLAN_2026-07-13.md` for the complete NIS source-to-target adoption matrix, terminology migration, business gates, Tech Lead automation, flow controls, failed-run retention, and sequencing.
- `openspec/changes/define-transfer-ready-process-package/` for the proposed transfer-readiness and weak-model-guardrail behavior, design, and implementation tasks.
- `openspec/changes/adopt-nis-corporate-process-governance/` for the proposed canonical minor/major/hotfix, DoR/DoD, Tech Lead, corporate flow, release, pilot-safety, and failed-run-retention behavior.
- `openspec/specs/` for accepted SDD workflow, artifact, traceability, waiver, documentation, topology/config, and Confluence feedback contracts; `openspec/changes/` for future proposed changes and archived source packages.

Important concepts preserved in current docs:

- Accepted first canonical source pattern: central `team-specs` repository with `openspec/` artifacts, central config plus optional project adapters, OpenSpec `1.4.1` pin, one versioned process package, and `owners.yaml` as owner source.
- Publication: generated Confluence pages from Markdown/OpenSpec.
- Review and audit: Bitbucket PRs with reviewer assignment from owners registry.
- Validation and automation: Jenkins pipelines.
- Workflow status: Jira or another task tracker.
- Traceability path: requirement -> scenario -> dev task -> test case -> automated test.
- Project memory triad: constitution/quality policy, project map, and OpenSpec changes/living specs.
- Existing-code onboarding path: read-only scan -> legacy baseline -> project map update -> validation against real code.
- Maintenance path: deterministic sync and upgrade checks after the related topology/config and OpenSpec version policies are approved.
- Historical broad pilot picture: `team-specs`, OpenSpec CLI, deterministic validation, Jenkins Spec PR pipeline, Bitbucket reviewer assignment, Confluence preview, Jira task creation, and `traceability.yaml`.

The accepted Phase 1 MVP was narrower than the historical broad pilot picture and proved the legacy thin-flow baseline. Decision `D-013` now requires the Phase 2 target to migrate that baseline to minor/major/hotfix and class-aware corporate gates before the real pilot. Jira task automation, Confluence publication, QA/AT proposal generation, and broad role inboxes remain later layers.

## First Valuable Outcome

The first useful release candidate should prove the smallest complete class-aware SDD flow before corporate pilot scale:

1. Triage and create a versioned change package.
2. Classify it as minor, major, or hotfix and validate the applicable evidence matrix.
3. Pass Spec Review, class-aware Definition of Ready, and human approval.
4. Implement with scope, regression, stop/escalation, and traceability controls.
5. Pass implementation-complete, Definition of Done, applicable release/transfer readiness, and human archive readiness.
6. Preserve explicit separation between archived specs and external delivered/Done state.

Before that flow moves into the corporate environment, Phase 2 must package it as a reproducible external release candidate, prove all gates with AI disabled, certify bounded analyst/developer/QA/Tech Lead workflows and all three classes using actual Qwen-class and DeepSeek-class assistants, and provide migration, installation, compatibility, transfer, and rollback evidence. Phase 3 then adds self-service guided operation for humans and AI assistants; only Phase 4 supplies real project/owner/path/workflow configuration, approved integration wiring, the available model adapter, and one monitored real pilot selected through the approved criteria.

After the deterministic flow and monitored pilot are accepted, later phases may automate more of the operating process with AI: assembling source-linked evidence, routing work, preparing drafts and transition requests, monitoring configured conditions, and coordinating tool actions within explicit permissions. The deterministic layer remains available to validate and complete the workflow when AI is unavailable or unreliable; human accountability is not silently replaced.

Confluence publication, Jira task creation, QA/AT proposal generation, and role inboxes remain important, but they are not required for the first MVP unless the human owner explicitly re-scopes the pilot.

Future publication layers should generate audience-oriented views from canonical OpenSpec sources, including change pages, capability pages, customer journey pages, release/change summaries, technical appendices, and screen galleries where useful. Those generated views must preserve traceability back to requirements, scenarios, source commits, and verification evidence.

## Documentation Rules

- `AGENTS.md` is the canonical agent operating guide.
- `docs/00_FILE_STRUCTURE.md` is the repository map and must be updated when files or folders are added.
- `docs/CURRENT_PROJECT_AUDIT.md` is an active planning input and must be updated when findings are fixed or invalidated by evidence.
- Detailed phase plans live under `docs/phases/` and must use `docs/phases/PHASE_PLAN_TEMPLATE.md`.
- New human feedback that affects SDD workflow behavior, automation safety, integration usability, acceptance, or verification must be persisted in the correct durable document.
- Behavior and acceptance text should not be duplicated across specs, docs, project memory, generated views, or role guides; derived surfaces link to the canonical owner and are fixed or regenerated when they drift.
## Self-service entrypoint

РћРїРµСЂР°С‚РѕСЂ СѓСЃС‚Р°РЅР°РІР»РёРІР°РµС‚ Р»РѕРєР°Р»СЊРЅС‹Р№ РїР°РєРµС‚ РєРѕРјР°РЅРґРѕР№ `python -m pip install .` Рё
СЂР°Р±РѕС‚Р°РµС‚ С‡РµСЂРµР· `sdd --version`, `sdd setup`, `sdd start` Рё `sdd next`.
`sdd setup` С‚СЂРµР±СѓРµС‚ `--confirm` Рё СЃРѕР·РґР°С‘С‚ С‚РѕР»СЊРєРѕ РїСѓСЃС‚РѕР№ local workspace;
`start` Рё `next` РІРѕР·РІСЂР°С‰Р°СЋС‚ РѕРґРёРЅ structured continuation result СЃ СЂРѕР»СЊСЋ,
РЅРµРґРѕСЃС‚Р°СЋС‰РёРјРё С„Р°РєС‚Р°РјРё, human boundary, fallback Рё С‚РѕС‡РЅРѕР№ СЃР»РµРґСѓСЋС‰РµР№ РєРѕРјР°РЅРґРѕР№.
Р’ P3 `sdd run`, release Рё external mutation РѕСЃС‚Р°СЋС‚СЃСЏ fail-closed. РљР°РЅРѕРЅРёС‡РµСЃРєРёРµ
С‚СЂРµР±РѕРІР°РЅРёСЏ РЅР°С…РѕРґСЏС‚СЃСЏ РІ OpenSpec change `add-self-service-operator-onboarding`;
РїРѕРґСЂРѕР±РЅС‹Р№ bootstrap вЂ” РІ `docs/runbooks/PACKAGED_GOVERNED_FLOW.md`.

## РљР°С‚Р°Р»РѕРі Р»РѕРєР°Р»СЊРЅС‹С… СЃРєСЂРёРїС‚РѕРІ

### Р”РѕСЃС‚СѓРїРЅС‹Рµ РѕРїРµСЂР°С†РёРё

Р­С‚Рѕ РіРµРЅРµСЂРёСЂСѓРµРјРѕРµ Рё РїСЂРѕРІРµСЂСЏРµРјРѕРµ РїСЂРµРґСЃС‚Р°РІР»РµРЅРёРµ `process/catalogs/operations.yaml`; РѕРЅРѕ РѕРїРёСЃС‹РІР°РµС‚
РіСЂР°РЅРёС†С‹ РѕРїРµСЂР°С†РёРё, РЅРѕ РЅРµ Р·Р°РјРµРЅСЏРµС‚ СЂР°Р·СЂРµС€С‘РЅРЅСѓСЋ СЂРѕР»СЊ РёР»Рё СЂРµС€РµРЅРёРµ С‡РµР»РѕРІРµРєР°.

<!-- operation-table:begin -->
| Operation | Role | Situation | Boundary | Runbook |
| --- | --- | --- | --- | --- |
| classify-change | Analyst, Tech Lead, Developer, QA | new-requirement, urgent-incident | read_only/low | [docs/README.md](docs/README.md) |
| create-change | Analyst, Tech Lead, Developer, QA | new-requirement, urgent-incident | mutate_local/medium | [docs/README.md](docs/README.md) |
| evaluate-change-gates | Analyst, Tech Lead, Developer, QA | existing-change, urgent-incident | read_only/low | [docs/README.md](docs/README.md) |
| guided-owner-workflow | Analyst, Tech Lead, Developer, QA | new-requirement, existing-change, urgent-incident, blocked-operation | read_only/low | [docs/README.md](docs/README.md) |
| manual-fallback | Analyst, Tech Lead, Developer, QA | blocked-operation | prepare/low | [docs/README.md](docs/README.md) |
| prepare-archive | Analyst, Tech Lead, Developer, QA | existing-change | prepare/low | [docs/README.md](docs/README.md) |
| prepare-spec-pr | Analyst, Tech Lead, Developer, QA | existing-change | prepare/low | [docs/README.md](docs/README.md) |
| preview-analytics | Analyst, Tech Lead, Developer, QA | on demand | read_only/low | [docs/README.md](docs/README.md) |
| sdd-dispatcher | Analyst, Tech Lead, Developer, QA | new-requirement, existing-change, urgent-incident, blocked-operation | read_only/low | [docs/README.md](docs/README.md) |
<!-- operation-table:end -->

РќРёР¶Рµ РїСЂРёРІРµРґРµРЅР° РёСЃС‚РѕСЂРёС‡РµСЃРєР°СЏ РёРЅРІРµРЅС‚Р°СЂРёР·Р°С†РёСЏ 30 Р»РѕРєР°Р»СЊРЅС‹С… CLI РЅР° 2026-07-22. РћРЅР° РЅРµ СЏРІР»СЏРµС‚СЃСЏ РїРѕР»РёС‚РёРєРѕР№ РїРѕР»РЅРѕРјРѕС‡РёР№. РђРєС‚СѓР°Р»СЊРЅРѕРµ РіРµРЅРµСЂРёСЂСѓРµРјРѕРµ РїСЂРµРґСЃС‚Р°РІР»РµРЅРёРµ public/deprecated РѕРїРµСЂР°С†РёР№ РЅР°С…РѕРґРёС‚СЃСЏ РїРѕСЃР»Рµ РёРЅРІРµРЅС‚Р°СЂРёР·Р°С†РёРё Рё СЃС‚СЂРѕРёС‚СЃСЏ С‚РѕР»СЊРєРѕ РёР· `process/catalogs/operations.yaml`.

| РЎРєСЂРёРїС‚ | Р§С‚Рѕ РґРµР»Р°РµС‚ | РљРѕРіРґР° РЅСѓР¶РµРЅ С‡РµР»РѕРІРµРєСѓ |
|---|---|---|
| `bootstrap_team_specs.py` | РљРѕРїРёСЂСѓРµС‚ РІРµСЂСЃРёРѕРЅРёСЂСѓРµРјС‹Р№ РїР°РєРµС‚ РїСЂРѕС†РµСЃСЃР° Рё С†РµРЅС‚СЂР°Р»СЊРЅС‹Р№ РєР°СЂРєР°СЃ СЂР°Р±РѕС‡РµРіРѕ РїСЂРѕСЃС‚СЂР°РЅСЃС‚РІР°. | РџСЂРё СЃРѕР·РґР°РЅРёРё С‡РёСЃС‚РѕРіРѕ СЂР°Р±РѕС‡РµРіРѕ РїСЂРѕСЃС‚СЂР°РЅСЃС‚РІР°; РЅРµ РїРѕРІРµСЂС… РЅРµРїСЂРѕРІРµСЂРµРЅРЅРѕР№ СѓСЃС‚Р°РЅРѕРІРєРё. |
| `build_read_pack.py` | РЎРѕР±РёСЂР°РµС‚ РѕРіСЂР°РЅРёС‡РµРЅРЅС‹Р№ РєРѕРЅС‚РµРєСЃС‚ СЃ РјР°СЂРєРёСЂРѕРІР°РЅРЅС‹РјРё РїРѕР»РЅРѕРјРѕС‡РёСЏРјРё РґР»СЏ РѕРґРЅРѕР№ СЂРѕР»Рё AI. | РџРµСЂРµРґ РѕРґРЅРѕР№ Р·Р°РґР°С‡РµР№ СЃР»Р°Р±РѕР№ РјРѕРґРµР»Рё РІ РѕРїСЂРµРґРµР»С‘РЅРЅРѕР№ СЂРѕР»Рё. |
| `certify_process_release.py` | Р—Р°РїСѓСЃРєР°РµС‚ allowlisted СЃРёРЅС‚РµС‚РёС‡РµСЃРєСѓСЋ СЃРµСЂС‚РёС„РёРєР°С†РёСЋ РїР°РєРµС‚Р° Рё РїРѕРєСЂС‹С‚РёРµ. | РџСЂРё СЃРµСЂС‚РёС„РёРєР°С†РёРё РєР°РЅРґРёРґР°С‚Р°; raw-СЂРµР·СѓР»СЊС‚Р°С‚С‹ С…СЂР°РЅСЏС‚СЃСЏ РІРЅРµ Git. |
| `check_actual_certification_gate.py` | РџСЂРѕРІРµСЂСЏРµС‚ РёС‚РѕРі РѕРґРЅРѕР№ С„Р°РєС‚РёС‡РµСЃРєРѕР№ model preflight/matrix-РїСЂРѕРІРµСЂРєРё. | РџРѕСЃР»Рµ Р·Р°РІРµСЂС€РµРЅРёСЏ РєР°Р¶РґРѕР№ С„Р°Р·С‹ СЃРµСЂС‚РёС„РёРєР°С†РёРё РјРѕРґРµР»Рё. |
| `check_corporate_flow.py` | Р¤РѕСЂРјРёСЂСѓРµС‚ РґРµС‚РµСЂРјРёРЅРёСЂРѕРІР°РЅРЅС‹Р№ РѕС‚С‡С‘С‚ В«РјРѕР¶РЅРѕ РїСЂРѕРґРѕР»Р¶Р°С‚СЊ / Р±Р»РѕРєРёСЂРѕРІРєР°В». | РџРµСЂРµРґ РїРµСЂРµС…РѕРґРѕРј РІ СѓРїСЂР°РІР»СЏРµРјРѕРј РєРѕСЂРїРѕСЂР°С‚РёРІРЅРѕРј РїРѕС‚РѕРєРµ. |
| `check_lifecycle_transition.py` | РџСЂРѕРІРµСЂСЏРµС‚ Р·Р°РїСЂРѕС€РµРЅРЅС‹Р№ lifecycle-РїРµСЂРµС…РѕРґ Р±РµР· РµРіРѕ РёР·РјРµРЅРµРЅРёСЏ. | Р”Рѕ С‚РѕРіРѕ, РєР°Рє С‡РµР»РѕРІРµРє СЂР°СЃСЃРјР°С‚СЂРёРІР°РµС‚ СЌС‚РѕС‚ РїРµСЂРµС…РѕРґ. |
| `check_parallel_plan.py` | РћС‚РєР»РѕРЅСЏРµС‚ РїРµСЂРµСЃРµРєР°СЋС‰РёРµСЃСЏ РёР»Рё Р·Р°РІРёСЃРёРјС‹Рµ РїР»Р°РЅС‹ РїР°СЂР°Р»Р»РµР»СЊРЅРѕР№ СЂР°Р±РѕС‚С‹ AI. | Р”Рѕ Р·Р°РїСѓСЃРєР° РїР°СЂР°Р»Р»РµР»СЊРЅС‹С… Р·Р°РґР°С‡. |
| `check_tech_lead_control.py` | РџСЂРѕРІРµСЂСЏРµС‚ Р·Р°РїРёСЃРё С‡РµР»РѕРІРµРєР° Рѕ stop/hold/escalate/resume. | РџСЂРё РїСЂРѕРІРµСЂРєРµ control state РёР»Рё РІРѕР·РѕР±РЅРѕРІР»РµРЅРёСЏ СЂР°Р±РѕС‚С‹. |
| `check_weak_model_evidence.py` | РћС‚РєР»РѕРЅСЏРµС‚ РЅРµРїРѕРґС‚РІРµСЂР¶РґС‘РЅРЅС‹Рµ Р·Р°СЏРІР»РµРЅРёСЏ AI Рѕ Р·Р°РІРµСЂС€РµРЅРёРё РёР»Рё РїРѕР»РЅРѕРјРѕС‡РёСЏС…. | РџРѕСЃР»Рµ СЂРµР·СѓР»СЊС‚Р°С‚Р° РѕРіСЂР°РЅРёС‡РµРЅРЅРѕР№ Р·Р°РґР°С‡Рё РјРѕРґРµР»Рё. |
| `classify_change.py` | РћРїСЂРµРґРµР»СЏРµС‚ РєР»Р°СЃСЃ РёР·РјРµРЅРµРЅРёСЏ РїРѕ Р·Р°РєСЂРµРїР»С‘РЅРЅРѕР№ РїРѕР»РёС‚РёРєРµ Рё С„Р°РєС‚Р°Рј. | РќР° intake Рё РїСЂРё СЃСѓС‰РµСЃС‚РІРµРЅРЅРѕРј РёР·РјРµРЅРµРЅРёРё scope/РІР»РёСЏРЅРёСЏ. |
| `create_change.py` | РЎРѕР·РґР°С‘С‚ С‡РµСЂРЅРѕРІРѕР№ change schema-v2. | РџРѕСЃР»Рµ РѕРїСЂРµРґРµР»РµРЅРёСЏ change ID, workspace Рё РєРѕРЅС„РёРіСѓСЂР°С†РёРё. |
| `evaluate_change_gates.py` | РџРѕРєР°Р·С‹РІР°РµС‚ class-aware evidence РґР»СЏ DoR/DoD/release/archive, РЅРѕ РЅРµ РѕРґРѕР±СЂСЏРµС‚ РµС‘. | РџРµСЂРµРґ С‡РµР»РѕРІРµС‡РµСЃРєРёРј gate-СЂРµС€РµРЅРёРµРј. |
| `guided_owner_workflow.py` | Р’С‹РґР°С‘С‚ СЃР»РµРґСѓСЋС‰РёР№ С€Р°Рі, Р±Р»РѕРєРёСЂРѕРІРєСѓ РёР»Рё fallback, РѕР±СЉСЏРІР»РµРЅРЅС‹Рµ РІ РєР°С‚Р°Р»РѕРіРµ РјР°СЂС€СЂСѓС‚РѕРІ. | Р’ РїРµСЂРІРѕР№ СЂР°Р±РѕС‡РµР№ СЃРёС‚СѓР°С†РёРё РёР»Рё РїСЂРё Р±Р»РѕРєРёСЂРѕРІРєРµ. |
| `launch_role_task.py` | Р’С‹Р±РёСЂР°РµС‚ РёРЅСЃС‚СЂСѓРєС†РёСЋ СЂРѕР»Рё, read-pack, РѕР¶РёРґР°РµРјС‹Р№ СЂРµР·СѓР»СЊС‚Р°С‚ Рё stop point РІРЅРµ РјРѕРґРµР»Рё. | РќРµРїРѕСЃСЂРµРґСЃС‚РІРµРЅРЅРѕ РїРµСЂРµРґ РѕРґРЅРѕР№ AI-Р·Р°РґР°С‡РµР№ СЂРѕР»Рё. |
| `manage_release_candidate.py` | РЎРѕР·РґР°С‘С‚ РёР»Рё РїСЂРѕРІРµСЂСЏРµС‚ РЅРµРёР·РјРµРЅСЏРµРјС‹Р№ transfer candidate. | РўРѕР»СЊРєРѕ РїСЂРё РєРѕРЅС‚СЂРѕР»РёСЂСѓРµРјРѕРј freeze/rehearsal. |
| `manual_fallback.py` | Р¤РѕСЂРјРёСЂСѓРµС‚ AI-disabled РїР»Р°РЅ СЂСѓС‡РЅРѕРіРѕ РїСЂРѕРґРѕР»Р¶РµРЅРёСЏ. | Р•СЃР»Рё РјРѕРґРµР»СЊ РёР»Рё РёРЅС‚РµРіСЂР°С†РёСЏ РЅРµРґРѕСЃС‚СѓРїРЅР° Р»РёР±Рѕ Р·Р°РІРµСЂС€РёР»Р°СЃСЊ РѕС€РёР±РєРѕР№. |
| `migrate_change_classification.py` | РџСЂРµРґРІР°СЂРёС‚РµР»СЊРЅРѕ РїРѕРєР°Р·С‹РІР°РµС‚ РёР»Рё РїСЂРёРјРµРЅСЏРµС‚ СЂР°Р·СЂРµС€С‘РЅРЅСѓСЋ РјРёРіСЂР°С†РёСЋ `thin -> minor`, `full -> major`. | Р”Р»СЏ РїРѕРґС…РѕРґСЏС‰РµР№ РЅРµР°СЂС…РёРІРЅРѕР№ legacy-РјРёРіСЂР°С†РёРё; hotfix РЅРµ РІС‹РІРѕРґРёС‚СЃСЏ Р°РІС‚РѕРјР°С‚РёС‡РµСЃРєРё. |
| `normalize_actual_certification.py` | РЎРѕР·РґР°С‘С‚ Git-safe РЅРѕСЂРјР°Р»РёР·РѕРІР°РЅРЅРѕРµ evidence РёР· РїРѕР»РЅРѕРіРѕ raw-РёРЅРІРµРЅС‚Р°СЂСЏ. | РџРѕСЃР»Рµ С‡РµСЃС‚РЅРѕРіРѕ С„Р°РєС‚РёС‡РµСЃРєРѕРіРѕ СЂРµР·СѓР»СЊС‚Р°С‚Р° Р·Р°РїСѓСЃРєР° РјРѕРґРµР»Рё. |
| `prepare_archive.py` | РЎРѕР±РёСЂР°РµС‚ evidence РіРѕС‚РѕРІРЅРѕСЃС‚Рё Рє Р°СЂС…РёРІРёСЂРѕРІР°РЅРёСЋ. | Р”Рѕ СЂРµС€РµРЅРёСЏ С‡РµР»РѕРІРµРєР° РѕР± archive. |
| `prepare_spec_pr.py` | РЎРѕР±РёСЂР°РµС‚ РґРµС‚РµСЂРјРёРЅРёСЂРѕРІР°РЅРЅРѕРµ evidence РїРѕРґРіРѕС‚РѕРІРєРё Spec PR. | Р”Рѕ С‡РµР»РѕРІРµС‡РµСЃРєРѕРіРѕ review Delta Spec. |
| `preview_analytics.py` | Р›РѕРєР°Р»СЊРЅРѕ РїСЂРѕРІРµСЂСЏРµС‚ Рё РїРѕРєР°Р·С‹РІР°РµС‚ РїРµСЂРµРґР°РЅРЅС‹Р№ typed analytics package; С‚РѕР»СЊРєРѕ С‡С‚РµРЅРёРµ. | Р”Р»СЏ РїСЂРѕСЃРјРѕС‚СЂР° РѕС‡РёС‰РµРЅРЅС‹С… P3-РґР°РЅРЅС‹С…. |
| `review_tech_lead.py` | РЎРѕР±РёСЂР°РµС‚ РґРµС‚РµСЂРјРёРЅРёСЂРѕРІР°РЅРЅС‹Рµ РїСЂРµРґСЃС‚Р°РІР»РµРЅРёСЏ РґР»СЏ Tech Lead review. | РџСЂРё review РєР»Р°СЃСЃРёС„РёРєР°С†РёРё, readiness, СЂРёСЃРєР° РёР»Рё release-СЂРµРєРѕРјРµРЅРґР°С†РёРё. |
| `run_actual_certification.py` | Р’С‹РїРѕР»РЅСЏРµС‚ append-only СЃРµСЂС‚РёС„РёРєР°С†РёРѕРЅРЅС‹Р№ СЃСЂРµР· Qwen/DeepSeek. | РџСЂРё Р·Р°РїР»Р°РЅРёСЂРѕРІР°РЅРЅРѕР№ СЃРµСЂС‚РёС„РёРєР°С†РёРё СЃ Р±РµР·РѕРїР°СЃРЅРѕР№ РІРЅРµС€РЅРµР№ raw-РґРёСЂРµРєС‚РѕСЂРёРµР№. |
| `update_process_package.py` | РџСЂРѕРІРµСЂСЏРµС‚, РѕР±РЅРѕРІР»СЏРµС‚ РёР»Рё РѕС‚РєР°С‚С‹РІР°РµС‚ РїР°РєРµС‚ С‚СЂР°РЅР·Р°РєС†РёРѕРЅРЅРѕ. | РџСЂРё СЃРѕРіР»Р°СЃРѕРІР°РЅРЅРѕРј РєРѕРЅС‚СЂРѕР»РёСЂСѓРµРјРѕРј upgrade/rollback. |
| `validate_change.py` | РџСЂРѕРІРµСЂСЏРµС‚ С‚РѕР»СЊРєРѕ legacy-РїР°РєРµС‚С‹ thin/full. | Р”Р»СЏ СЃРѕРІРјРµСЃС‚РёРјРѕСЃС‚Рё Рё РјРёРіСЂР°С†РёРё, РЅРѕ РЅРµ РґР»СЏ РЅРѕРІРѕР№ schema-v2 СЂР°Р±РѕС‚С‹. |
| `validate_corporate_adaptation.py` | РџСЂРѕРІРµСЂСЏРµС‚ РґРѕРєСѓРјРµРЅС‚С‹ Рё С€Р°Р±Р»РѕРЅС‹ adaptation/pilot/no-fork. | РџСЂРё РїРѕРґРіРѕС‚РѕРІРєРµ Phase 4; РЅРµ РїРѕСЃС‚Р°РІР»СЏРµС‚ С„Р°РєС‚С‹ Рё РЅРµ РїРѕРґРєР»СЋС‡Р°РµС‚ СЃРёСЃС‚РµРјС‹. |
| `validate_external_mapping.py` | РџСЂРѕРІРµСЂСЏРµС‚ mapping РјРµР¶РґСѓ РІРЅСѓС‚СЂРµРЅРЅРёРј Рё tracker-СЃРѕСЃС‚РѕСЏРЅРёРµРј. | Р”Рѕ Р±СѓРґСѓС‰РµР№ Р°РІС‚РѕРјР°С‚РёР·Р°С†РёРё РІРЅРµС€РЅРµРіРѕ СЃРѕСЃС‚РѕСЏРЅРёСЏ. |
| `validate_guided_owner_workflow.py` | РџСЂРѕРІРµСЂСЏРµС‚ СЃРёРЅС…СЂРѕРЅРёР·Р°С†РёСЋ checksum guide Рё РєР°С‚Р°Р»РѕРіР° РјР°СЂС€СЂСѓС‚РѕРІ. | РџРѕСЃР»Рµ РёР·РјРµРЅРµРЅРёСЏ guide/catalog Рё РґРѕ transfer. |
| `validate_process_config.py` | РќР°С…РѕРґРёС‚ Рё РїСЂРѕРІРµСЂСЏРµС‚ РєРѕРЅС„РёРіСѓСЂР°С†РёСЋ, СЂРµРµСЃС‚СЂС‹, pins Рё OpenSpec runtime. | РџРµСЂРµРґ СѓРїСЂР°РІР»СЏРµРјРѕР№ СЂР°Р±РѕС‚РѕР№ РІ РєРѕРЅРєСЂРµС‚РЅРѕРј workspace. |
