# Implementation Strategy: SDD Automation Without a Custom `sdd` CLI

Status: accepted by the human owner on 2026-07-03; target classification and corporate governance refined by `D-013` on 2026-07-13; automation horizon refined by `D-014` on 2026-07-14. Обоснованный `T6` и `D-021` bounded self-service launcher реализован без изменения решения не строить монолитную CLI-платформу.

This document resolves open decision 5.2 from `docs/audits/ARCHITECTURE_CRITIQUE_2026-07-03.md`. The historical architecture draft that originally motivated the project was removed on 2026-07-06 after current decisions moved into `docs/` and `openspec/`; this strategy defines how the process is delivered first.

## 1. Decision Summary

The team is mandated to use SDD. The process is delivered without building a custom `sdd` CLI product, using three layers:

| Layer | Role | Guarantees |
|---|---|---|
| Deterministic base | Templates, validation scripts, pre-commit, Jenkinsfile — all versioned inside `team-specs` | All gates and process rules live here. The process must work with AI turned off |
| Standard tool features | Bitbucket default reviewers and branch policies, Jira Automation, markdown->Confluence publisher (e.g. kovetskiy/mark), OpenSpec CLI | Integrations without custom API clients |
| AI automation layer | Initially bounded role skills and draft/review support; later accepted changes may add workflow orchestration, evidence assembly, routing, monitoring, and permitted transition preparation | May automate work, but deterministic checks and explicit human authority remain the control boundary |

Hard rule: no gated action may depend on the AI layer. Every gate must be executable and verifiable by scripts/CI alone.

This hard rule defines the reliability floor, not the final automation ceiling. The first release proves that the process survives AI failure or absence. After the process and pilot are stable, AI is expected to automate more bounded process work while deterministic validation checks its outputs and non-delegable human decisions remain explicit.

Custom `sdd` CLI строится только после срабатывания criteria из раздела 6 и
только инкрементально для доказанной проблемы, а не как upfront platform.
`D-021` зафиксировал провал scenario-based onboarding и тем самым активировал
`T6`. Текущий установленный `sdd` — тонкий public launcher поверх существующих
deterministic modules: он даёт setup, situation-first guidance, continuation,
catalog, check, prepare и request routes. Это не централизованная автономная
платформа, а mutation execution остаётся fail-closed.

## 2. OpenSpec Reference

- Tool: Fission-AI/OpenSpec (<https://github.com/Fission-AI/OpenSpec>).
- Team reference documentation: <https://lzw.me/docs/openspec> — a community-maintained multilingual documentation mirror (includes Russian) generated from the official OpenSpec docs.
- The mirror is unofficial: on any discrepancy, the upstream repository documentation wins.
- The OpenSpec CLI version is pinned per REC-006; upgrades are deliberate, tested decisions.

## 3. Jira and Confluence Access: MCP Only

- Access to Jira and Confluence from AI tooling goes through MCP servers, not hand-written REST integrations. Custom Jira/Confluence API clients are out of scope.
- MCP viability is confirmed: the human owner verified on 2026-07-03 that the MCP setup is real, was tested, and works.
- Planned experiment: automate provisioning of a local MCP server for employees (scripted install + configuration) so onboarding does not require manual MCP setup. Treated as an experiment until proven; manual setup instructions remain the fallback.
- Deterministic CI-side actions that must not depend on AI (e.g. Jira task creation on merge) use Jira Automation rules or a standard CLI in Jenkins, not MCP.

## 4. Dual-Environment Constraint

Development happens in two environments, in order:

1. External development environment (current): Claude Code and comparable strong AI CLIs are available. The reusable toolchain is designed, implemented, and certified here, including actual Qwen-class and DeepSeek-class weak-model runs plus an AI-disabled walkthrough.
2. Internal corporate environment (target): Qwen/DeepSeek/GigaCode-class assistants may be available and perform noticeably worse than Claude for this kind of work. Only an externally accepted release candidate is transferred; internal work is limited to real configuration, approved integration wiring, thin adapter setup, environment checks, and a monitored pilot.

Before that transfer, `D-021` requires one externally maintained self-service guided-operation layer: a human or AI assistant starts from a business situation and receives the applicable commands, evidence expectations, deterministic fallback, and explicit human decision boundary. This is reusable package behavior, not corporate adaptation work.

Portability rules derived from this constraint:

- All guarantees stay in the deterministic layer (section 1 hard rule); the weaker corporate assistant only degrades convenience, never correctness.
- Skills are authored as plain markdown instruction files with tool-agnostic content; per-tool packaging for Qwen, DeepSeek, GigaCode, Claude Code, or another supported surface is a thin adapter kept separate from the instructions themselves.
- No external-only dependencies inside gates: scripts must run on the corporate stack (verify Python availability, network restrictions, artifact mirrors).
- Before transfer, accept a reproducible release candidate with clean bootstrap, package/config/OpenSpec compatibility, legacy thin/full migration, minor/major/hotfix flow evidence, Tech Lead authority checks, update/rollback, privacy checks, AI-disabled operation, and actual Qwen/DeepSeek certification.
- During corporate adaptation, verify MCP availability and policy, the available Qwen/DeepSeek/GigaCode adapter, Bitbucket/Jenkins/Jira/Confluence versions (Cloud vs Server/DC), secrets handling, network rules, and artifact distribution without redesigning reusable process behavior.
- Follow-up adjustments that affect reusable behavior return to the external OpenSpec/change workflow and a new package release rather than becoming ad-hoc internal divergence.

### Progressive AI automation horizon

The project intentionally separates two horizons:

1. **Independent foundation:** every governed action has a deterministic or explicit human path, AI-disabled certification passes, and no process guarantee depends on model behavior.
2. **Progressive automation:** later OpenSpec changes may let AI assemble read packs and evidence, draft artifacts, route work, monitor configured conditions, coordinate supported tools, and prepare permitted state-transition requests.

Progressive automation must remain observable, reversible where mutation occurs, evidence-backed, and bounded by the same dry-run, idempotency, JSON-output, audit-log, privacy, and stop/hold expectations as other mutating automation. AI does not gain approval, waiver, risk-acceptance, merge, release, archive, or accountable-owner authority by implication.

### Reliability and safe parallel throughput

`D-016` defines two linked engineering outcomes:

- reliability increases through broader risk-oriented positive and negative tests and end-to-end links from requirements/scenarios to tasks, runs, decisions, failures, and verification evidence;
- delivery speed increases when AI decomposes work into genuinely independent tasks that can run concurrently with explicit owners, non-overlapping write scopes, separate evidence, and a deterministic combined integration gate.

Parallel execution is rejected when tasks share a mutable canonical artifact, depend on unfinished output, or can make conflicting lifecycle, policy, security, or architecture decisions. This direction does not reintroduce employee/process-effectiveness experiments excluded by `D-013`; coverage and traceability are verification controls, while parallelism is a bounded execution capability.

## 5. Mandatory Gates And Role-Understanding Evidence

`D-013` keeps correctness and safety in explicit business gates. DoR, DoD, release/transfer readiness, archive readiness, required approvals, stop conditions, rollback/hold, and hotfix reconciliation cannot be waived by convenience or an AI statement.

Failed validation, AI, adapter, integration, or workflow attempts remain in source-linked execution evidence even after a successful retry. This retention supports traceability and incident diagnosis; it is not an effectiveness measurement.

The project does not maintain process-effectiveness metrics, comparison cohorts, comparison-contamination rules, missing-measurement-data rules, or sample and decision thresholds.

### Usability and role-understanding checks

| ID | Criterion | Check |
|---|---|---|
| U1 | Each role can complete its governed actions and identify its authority limits | Scenario walkthrough with positive, negative, stop, escalation, and AI-disabled cases |
| U2 | Minor work remains proportionate while major and hotfix obligations are understandable | Class-specific flow audit against canonical matrices |
| U3 | Participants can distinguish DoR, implementation complete, DoD, release ready, archive, and external Done | Role-understanding interview/walkthrough with source-linked disposition |
| U4 | Every gated action works with the AI assistant disabled | Release certification and corporate adaptation walkthrough |
| U5 | Tech Lead automation reduces evidence search without impersonating approval | Tech Lead review-pack audit and authority-boundary negative cases |

## 6. Triggers: When a Custom `sdd` CLI Becomes Justified

A trigger is a documented engineering or usability problem that remains after a reasonable remediation attempt inside the current strategy. The human owner decides whether the evidence justifies a bounded CLI addition; no effectiveness score or experiment is required.

| ID | Trigger | What it justifies building |
|---|---|---|
| T1 | Manual gluing between tools repeatedly blocks or misroutes governed work and cannot be corrected safely with the existing scripts/templates | `sdd change new/validate` ergonomics commands |
| T2 | Script sprawl: shared logic duplicated across 3+ repos, or validation scripts grow past maintainability with a rising defect rate | Consolidation of scripts into a distributed CLI |
| T3 | Cross-repo operations (multi-repo changes, coordinated branches/PRs) done by hand repeatedly every sprint | Cross-repo orchestration commands |
| T4 | The available Qwen/DeepSeek/GigaCode-class assistant cannot reliably execute a bounded role flow after one documented remediation attempt | Deterministic commands, simpler instructions, or mandatory-human execution replacing the assistant layer for affected flows |
| T5 | MCP is restricted or unavailable in the corporate environment | A packaged integration layer as MCP fallback |
| T6 | Scenario-based onboarding repeatedly fails for new team members | Unified UX entry point |

Scope rule: when a trigger fires, build only the commands that answer that trigger, reusing the existing scripts as the CLI's internals. Re-evaluate the remaining triggers afterwards; any broader CLI surface is assembled incrementally from accepted docs and OpenSpec requirements, not from a separate architecture draft.

## 7. Review Cadence

- Strategy and trigger rules are reviewed after the monitored pilot or when a material environment or process change invalidates current assumptions; schedule cadence remains an operating-calendar decision outside this repository.
