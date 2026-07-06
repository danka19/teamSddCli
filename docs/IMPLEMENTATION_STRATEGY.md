# Implementation Strategy: SDD Automation Without a Custom `sdd` CLI

Status: accepted by the human owner on 2026-07-03.

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

1. External development environment (current): Claude Code and comparable strong AI CLIs are available. The toolchain (templates, scripts, skills, pipelines) is designed and proven here.
2. Internal corporate environment (target): only GigaCode CLI is available as the AI assistant, and it performs noticeably worse than Claude for this kind of work. The finished toolchain is transferred there.

Portability rules derived from this constraint:

- All guarantees stay in the deterministic layer (section 1 hard rule); the weaker corporate assistant only degrades convenience, never correctness.
- Skills are authored as plain markdown instruction files with tool-agnostic content; per-tool packaging (Claude Code skill format, GigaCode equivalent) is a thin adapter kept separate from the instructions themselves.
- No external-only dependencies inside gates: scripts must run on the corporate stack (verify Python availability, network restrictions, artifact mirrors).
- Before transfer, run an environment adaptation review: MCP availability and policy in the corporate network, GigaCode capability check against each skill flow, Bitbucket/Jenkins/Jira/Confluence versions (Cloud vs Server/DC), and secrets handling.
- Expect follow-up adjustments after transfer; record them as changes to this strategy rather than ad-hoc divergence.

## 5. Success and Usability Criteria

Measured per sprint from Git/Jira/CI data (M-metrics) and monthly per-role checks (U-criteria). Baselines are collected during the pilot's first two sprints; targets apply from sprint 3.

### Process health metrics

| ID | Metric | Target | Source |
|---|---|---|---|
| M1 | Median time from change creation to first green validation | Thin change <= 30 min; full package <= 1 working day | Git/CI timestamps |
| M2 | Spec PRs green on first CI run | >= 70% | Jenkins |
| M3 | Median time to first review on Spec PR | <= 1 working day | Bitbucket |
| M4 | Share of changes using a waiver | <= 20%, no growth two sprints in a row | Change packages |
| M5 | Requirement->scenario->test links derived automatically | >= 90%; red traceability rows resolved within a sprint | Traceability report |
| M6 | Behavior changes merged without a change package (process bypass) | <= 10% | Sprint sampling of merged PRs |
| M7 | Tooling support burden after stabilization | <= 0.5 person-day/week | DevOps/owner log |

### Usability criteria

| ID | Criterion | Check |
|---|---|---|
| U1 | Each role completes its main flow without help after one onboarding session | Checklist walkthrough with a new participant |
| U2 | Manual steps per flow stay small (analyst: template to open PR in <= 5 manual steps) | Flow audit |
| U3 | Role satisfaction >= 3.5/5, no role below 3 | Monthly short survey |
| U4 | Every gated action works with the AI assistant disabled | Quarterly walkthrough without AI |

## 6. Triggers: When a Custom `sdd` CLI Becomes Justified

A trigger fires when the condition persists for two consecutive sprints after at least one remediation attempt inside the current strategy.

| ID | Trigger | What it justifies building |
|---|---|---|
| T1 | M1 missed because of manual gluing between tools (not review wait time) | `sdd change new/validate` ergonomics commands |
| T2 | Script sprawl: shared logic duplicated across 3+ repos, or validation scripts grow past maintainability with a rising defect rate | Consolidation of scripts into a distributed CLI |
| T3 | Cross-repo operations (multi-repo changes, coordinated branches/PRs) done by hand repeatedly every sprint | Cross-repo orchestration commands |
| T4 | GigaCode CLI cannot reliably execute the skill flows in the corporate environment | Deterministic commands replacing the assistant layer for affected flows |
| T5 | MCP is restricted or unavailable in the corporate environment | A packaged integration layer as MCP fallback |
| T6 | U1 onboarding repeatedly fails for new team members | Unified UX entry point |

Scope rule: when a trigger fires, build only the commands that answer that trigger, reusing the existing scripts as the CLI's internals. Re-evaluate the remaining triggers afterwards; any broader CLI surface is assembled incrementally from accepted docs and OpenSpec requirements, not from a separate architecture draft.

## 7. Review Cadence

- Metrics reviewed at the end of every sprint by the process owner.
- Strategy (including trigger table and targets) reviewed after the pilot and then quarterly, or immediately after transfer to the corporate environment.
