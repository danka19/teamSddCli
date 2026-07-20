# teamSddCli

## Summary

teamSddCli is a local SDD process-automation project for a team workflow based on OpenSpec/Markdown, Git, deterministic validation scripts, Bitbucket, Jenkins, Confluence, Jira or another task tracker, and local AI tools.

The project goal is to automate the end-to-end transition from analysis to development tasks, QA test cases, automated-test skeletons, verification, and archived living specs without introducing one centralized autonomous agent. The delivery strategy is deliberately two-stage: first make the complete governed process reliable without AI, then progressively automate bounded process work with AI over the deterministic control plane. Reliability grows through broader risk-oriented test coverage and end-to-end evidence traceability; delivery speed grows through safe parallel AI work on explicitly independent tasks.

Current checkpoint:

> Phase 1 produced the accepted OpenSpec baseline and Phase 2 is closed under `D-020`: immutable candidate `phase-2-14-rc6` is the external transfer baseline with process package `0.3.0`, payload SHA-256 `172707ba159e1e060561d6d02ad67dcaf2fa4ce64a58c23bd9c55613713fd951`, manifest SHA-256 `0c7670637f1f59f82a6cae3bea48c53edfa3453d5fcf0c599bf013bd301c3146`, and `295 covered / 7 gaps / 32 future_work`. `D-021` adds a new pre-corporate Phase 3: the reusable package must become self-service through a situation-based guided-operation contract for humans and AI assistants before any corporate configuration or pilot. The guided workflow has passed its focused synthetic, AI-disabled, local Qwen/DeepSeek preflight, and negative-path checks; its separately versioned successor candidate is still pending. RC6 remains immutable; Phase 4 performs corporate adaptation and a monitored pilot. Historical rc4 remains unchanged, rc5 is retained as diagnostic rejected history, and macOS is not certified.

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
