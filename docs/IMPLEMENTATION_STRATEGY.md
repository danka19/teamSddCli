# Implementation Strategy: SDD Automation Without a Custom `sdd` CLI

Status: accepted by the human owner on 2026-07-03; process measurement and target classification refined by `D-013` on 2026-07-13.

This document resolves open decision 5.2 from `docs/audits/ARCHITECTURE_CRITIQUE_2026-07-03.md`. The historical architecture draft that originally motivated the project was removed on 2026-07-06 after current decisions moved into `docs/` and `openspec/`; this strategy defines how the process is delivered first.

## 1. Decision Summary

The team is mandated to use SDD. The process is delivered without building a custom `sdd` CLI product, using three layers:

| Layer | Role | Guarantees |
|---|---|---|
| Deterministic base | Templates, validation scripts, pre-commit, Jenkinsfile — all versioned inside `team-specs` | All gates and process rules live here. The process must work with AI turned off |
| Standard tool features | Bitbucket default reviewers and branch policies, Jira Automation, markdown->Confluence publisher (e.g. kovetskiy/mark), OpenSpec CLI | Integrations without custom API clients |
| AI assistant layer | Role skills (`change-new`, `qa-propose`, `at-propose`, `dev-start`) executed by a local AI CLI | Drafts and convenience only; never a gate |

Hard rule: no gated action may depend on the AI layer. Every gate must be executable and verifiable by scripts/CI alone.

A custom `sdd` CLI is built only when the trigger criteria in section 6 fire, and then incrementally, targeting the specific proven friction (most likely `change new/validate` ergonomics first), never as an upfront platform.

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

Portability rules derived from this constraint:

- All guarantees stay in the deterministic layer (section 1 hard rule); the weaker corporate assistant only degrades convenience, never correctness.
- Skills are authored as plain markdown instruction files with tool-agnostic content; per-tool packaging for Qwen, DeepSeek, GigaCode, Claude Code, or another supported surface is a thin adapter kept separate from the instructions themselves.
- No external-only dependencies inside gates: scripts must run on the corporate stack (verify Python availability, network restrictions, artifact mirrors).
- Before transfer, accept a reproducible release candidate with clean bootstrap, package/config/OpenSpec compatibility, legacy thin/full migration, minor/major/hotfix flow evidence, Tech Lead authority checks, update/rollback, privacy checks, AI-disabled operation, and actual Qwen/DeepSeek certification.
- During corporate adaptation, verify MCP availability and policy, the available Qwen/DeepSeek/GigaCode adapter, Bitbucket/Jenkins/Jira/Confluence versions (Cloud vs Server/DC), secrets handling, network rules, and artifact distribution without redesigning reusable process behavior.
- Follow-up adjustments that affect reusable behavior return to the external OpenSpec/change workflow and a new package release rather than becoming ad-hoc internal divergence.

## 5. Success, Gate, and Usability Evidence

`D-013` removes universal thin/full thresholds and separates correctness gates from process-effectiveness metrics. Canonical proposed definitions live in `process-measurement-pilot`, `readiness-completion-gates`, and the NIS adoption plan. Exact thresholds, sample gates, comparator, and review cadence are approved before a real pilot and stored in versioned policy/configuration rather than copied into this strategy.

### Mandatory gates

DoR, DoD, release/transfer readiness, archive readiness, required approvals, stop conditions, and hotfix reconciliation protect correctness. A good or bad process metric cannot waive them, and passing them does not prove that the process improved outcomes.

### Process and outcome metrics

| ID | Metric family | Required definition/evidence |
|---|---|---|
| M1 | Cycle and flow time | Defined start/end events plus active human, automated, queue, review, external wait, and hand-off intervals |
| M2 | First-pass acceptance | Stable denominator and first deterministic/review result from Git/CI/review sources |
| M3 | Human effort and manual intervention | Approved categories, source, role boundary, and labelled manual fallback |
| M4 | Machine/runtime cost and reliability | Runtime/tool version, attempts, failures, retries, adapter/MCP availability, and cost source where approved |
| M5 | Defects, rework, and delivery stability | Materiality rule, observation window, escaped-defect/rollback/support evidence, and no fabricated production outcome |
| M6 | Engineering-package completeness | Class-specific substantive evidence matrix, not raw file or prompt count |
| M7 | Waiver, override, deferral, bypass, and follow-up behavior | Policy version, denominator, expiry, unresolved reconciliation, and accountable decision evidence |
| M8 | Repeatability and comparison integrity | Historical/control/experimental/certification/production label, process version, contamination, and missing-data treatment |
| M9 | Tooling support burden and usability | Approved event/log or survey method without personal performance ranking |

Every metric records purpose, unit, numerator/denominator, event sources, inclusions/exclusions, owner, missing-data behavior, privacy classification, aggregation, and pre-approved decision rule. Failed runs remain in the dataset. Activity proxies such as artifact count, prompt count, AI usage, or checklist completion are diagnostic only.

The first real Phase 3 change proves bounded operability and transfer compatibility only. Effectiveness or scale claims require a separately accepted later protocol with sufficient comparison and production-stability evidence; they cannot be inferred from one successful change.

### Usability and role-understanding criteria

| ID | Criterion | Check |
|---|---|---|
| U1 | Each role can complete its governed actions and identify its authority limits | Scenario walkthrough with positive, negative, stop, escalation, and AI-disabled cases |
| U2 | Minor work remains proportionate while major and hotfix obligations are understandable | Class-specific flow audit against canonical matrices |
| U3 | Participants can distinguish DoR, implementation complete, DoD, release ready, archive, and external Done | Role-understanding interview/walkthrough with source-linked disposition |
| U4 | Every gated action works with the AI assistant disabled | Release certification and corporate adaptation walkthrough |
| U5 | Tech Lead automation reduces evidence search without impersonating approval | Tech Lead review-pack audit and authority-boundary negative cases |

## 6. Triggers: When a Custom `sdd` CLI Becomes Justified

A trigger fires when the condition persists across the pre-approved observation gate after at least one remediation attempt inside the current strategy. The pilot plan defines the sample and observation rule before collection.

| ID | Trigger | What it justifies building |
|---|---|---|
| T1 | M1 shows persistent controllable delay caused by manual gluing between tools rather than review or external wait | `sdd change new/validate` ergonomics commands |
| T2 | Script sprawl: shared logic duplicated across 3+ repos, or validation scripts grow past maintainability with a rising defect rate | Consolidation of scripts into a distributed CLI |
| T3 | Cross-repo operations (multi-repo changes, coordinated branches/PRs) done by hand repeatedly every sprint | Cross-repo orchestration commands |
| T4 | The available Qwen/DeepSeek/GigaCode-class assistant cannot reliably execute a bounded role flow after one documented remediation attempt | Deterministic commands, simpler instructions, or mandatory-human execution replacing the assistant layer for affected flows |
| T5 | MCP is restricted or unavailable in the corporate environment | A packaged integration layer as MCP fallback |
| T6 | U1 onboarding repeatedly fails for new team members | Unified UX entry point |

Scope rule: when a trigger fires, build only the commands that answer that trigger, reusing the existing scripts as the CLI's internals. Re-evaluate the remaining triggers afterwards; any broader CLI surface is assembled incrementally from accepted docs and OpenSpec requirements, not from a separate architecture draft.

## 7. Review Cadence

- Metrics are reviewed at the pre-approved pilot decision gates by the process owner and required role owners.
- Strategy, trigger rules, and local thresholds are reviewed after pilot evidence or when a material environment/process change invalidates the comparison; schedule cadence remains an operating-calendar decision outside this repository.
