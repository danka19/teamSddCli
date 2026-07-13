# Architecture Critique, Recommendations, and Alternatives

Status: recorded review output. Recommendations are proposed inputs for Phase 1/2 planning; final scope decisions remain with the human owner.

Date: 2026-07-03.

Source under review: historical architecture draft `sdd_final_architecture.md` (v1.0), removed from the repository on 2026-07-06 after current decisions moved into `docs/` and `openspec/`.

## 1. Evaluation Criteria

Criteria were built around two axes: usability (effort each role pays) and real-world applicability (whether the process survives contact with a live team).

| ID | Criterion | What it measures |
|---|---|---|
| K1 | Overhead per change | Artifacts/steps required for a typical (especially small) change |
| K2 | Role entry barrier | Whether analysts/QA without Git experience can work in the process |
| K3 | Traceability durability | Who maintains requirement->test links and whether they degrade |
| K4 | Integration surface | Number of external systems the toolchain must integrate and maintain |
| K5 | Incremental adoption | Whether value is achievable with a small part of the system |
| K6 | Human-factor resilience | What happens when people cut corners |
| K7 | Component maturity | Availability of proven off-the-shelf components vs custom builds |
| K8 | Non-technical stakeholder value | Readability and participation for business roles |

## 2. Review Summary

### Strengths (validated by external practice)

1. One-way `Git -> Confluence` publication matches the proven docs-as-code pattern (kovetskiy/mark and similar tools run this model in CI for years). Drift detection is a mature detail most analogs lack.
2. "Automate state transitions, not one big agent" is a sober bet: deterministic CLI/CI automation is cheaper, auditable, and predictable; advisory-only AI avoids the "illusion of work" failure mode reported for GitHub Spec Kit.
3. Change-type differentiation plus the thin path for small changes directly answers the main practitioner criticism of SDD (spec cost exceeding fix cost for small changes).
4. Waiver mechanism with owner and evidence is a rare, valuable escape hatch that keeps the process honest.
5. Phased rollout plan and reuse of the corporate stack lower political friction.

### Weaknesses (highest risk first)

1. Integration surface of the custom CLI (K4): Bitbucket, Jenkins, Jira, Confluence, OpenSpec, Git, and AI tooling in one in-house tool is a multi-year build; the "minimal start set" in section 28 of the architecture includes four external systems and contradicts the accepted narrowed MVP.
2. Artifact burden on `new_feature` (K1): six-plus mandatory artifacts risk reproducing the measured Spec Kit failure (thousands of markdown lines and hours of artifact review per small feature; iterative flow ~10x faster in the Scott Logic test).
3. Manual `traceability.yaml` (K3, K6): RTM practice is unambiguous — manually maintained traceability degrades; only derived/automated traceability survives.
4. Change status lives in three places (`change.yaml`, Jira workflow, PR state); the two-sources-of-truth problem excluded for Confluence returns through Jira.
5. Analyst entry barrier (K2): the least technical role is the process entry point and must work through Git, PRs, YAML, and CLI; requirements-as-code tools (Doorstop, StrictDoc, Sphinx-Needs) stayed niche largely for this reason.
6. Dependency on young OpenSpec (K7): the upstream project already rebuilt its workflow once; the change-package format can shift underneath the toolchain.
7. Confluence comment loop is manual and has no owner/SLA (already covered by the accepted 2026-07-03 decision requiring explicit specification before implementation).

### Comparison scoring (1-5, higher is better)

| Criterion | This architecture | OpenSpec (solo) | Spec Kit | mark (docs-as-code) | StrictDoc/Doorstop |
|---|---|---|---|---|---|
| K1 Overhead per change | 2 | 4 | 2 | 5 | 3 |
| K2 Role entry barrier | 2 | 4 | 3 | 4 | 2 |
| K3 Traceability durability | 3 | 3 | 2 | n/a | 4 |
| K4 Integration surface | 1 | 5 | 4 | 5 | 4 |
| K5 Incremental adoption | 3 | 5 | 4 | 5 | 3 |
| K6 Human-factor resilience | 4 | 3 | 2 | 4 | 3 |
| K7 Component maturity | 2 | 3 | 3 | 5 | 4 |
| K8 Business stakeholder value | 5 | 1 | 1 | 3 | 2 |

Interpretation: the concept is stronger than any found analog (none solve the team/QA/analyst case), but the implementation scale and per-change overhead are the two dominant risks.

## 3. Recommendations

| ID | Recommendation | Rationale | Status |
|---|---|---|---|
| REC-001 | Keep the MVP narrowed to the spec-change loop (`sdd change new/validate/pr/archive` + basic traceability); remove stale broad-start guidance from the current source-of-truth path | External evidence confirms the accepted 2026-07-03 narrowing; value must be proven before integration spend | Accepted; stale architecture draft removed on 2026-07-06 |
| REC-002 | Make `thin change` the default path; require `full change package` only for feature/API/cross-repo/high-risk changes | Spec Kit experience shows heavy-by-default processes die in the first sprint | Historical proposal; superseded by `D-013` minor/major/hotfix classification |
| REC-003 | Do not build a Confluence publisher from scratch; wrap an existing markdown->Confluence tool (e.g. kovetskiy/mark or markdown-confluence) and keep only drift detection and page mapping custom | Mature tools already run this exact one-way model in CI; removes a large slice of K4 risk | Proposed |
| REC-004 | Derive traceability instead of hand-editing it: generate `traceability.yaml` from tags in `.feature` files, PR links, and task ids in branches; humans resolve conflicts only | Manually maintained traceability matrices reliably degrade; derived ones survive | Proposed |
| REC-005 | Define a single status owner per lifecycle segment: `change.yaml` is authoritative until `approved`, Jira after `tasks_created`; everything else is derived | Three concurrent status owners recreate the dual-source-of-truth problem | Proposed |
| REC-006 | Pin the OpenSpec version and isolate it behind an adapter layer in the CLI | Upstream is young and has already changed its workflow once | Proposed |
| REC-007 | Require a bounded, reviewable pilot decision before expanding Jira/QA automation | Expansion should follow verified operational behavior and explicit human acceptance | Superseded: process-effectiveness evaluation was excluded on 2026-07-13 |

## 4. Alternative Solution Paths

Context: how to solve the same problem — automating the team flow from analysis to dev/QA/AT and production with AI as a local CLI assistant (no autonomous agent) — without building the full custom architecture.

### Alternative A. Conventions + existing AI CLI + thin glue (no custom `sdd` CLI)

- Process lives in repository conventions: change-package templates, `AGENTS.md`/`CLAUDE.md` operating rules, and slash-command skills for the AI CLI already in use (Claude Code/Codex/Cursor), exactly like this repo's `.codex/skills/`.
- Validation is a few small CI scripts (JSON-schema check of `change.yaml`, required-file check, tag lint) — hundreds of lines, not a product.
- Publication via an existing markdown->Confluence tool in CI; reviewer assignment via Bitbucket default reviewers per path; Jira issue creation via built-in Jira automation rules on merge events.
- AI context packs are unnecessary: the AI CLI reads the repo directly, guided by skills.
- Pros: weeks instead of years; every component replaceable; no version-skew of a custom binary across machines.
- Cons: weaker guarantees (conventions drift), no role inbox, process knowledge spread across configs of several systems.

### Alternative B. Skill/prompt pack as the product + MCP for integrations

- The deliverable is a versioned skill pack (prompts, templates, checklists) that any local AI CLI executes; deterministic actions are performed by the AI invoking standard CLIs (`git`, `jira-cli`) or read-only MCP servers (e.g. the Atlassian Remote MCP Server for Jira/Confluence) instead of hand-written API clients.
- Write actions stay human-confirmed, matching the architecture's own MCP staging plan (read-only first).
- Pros: near-zero custom integration code; upgrades are prompt edits; naturally fits the "AI assists, humans decide" principle.
- Cons: non-deterministic execution needs CI backstops for anything gate-like; per-seat AI licensing; harder to audit than a deterministic CLI.

### Alternative C. CI-first / comment-ops (no local tool at all)

- All automation is server-side: Jenkins jobs react to PR events and PR comments (`/publish preview`, `/create-tasks`) to validate, publish, and create issues; users interact only through Git and the PR UI.
- Pros: zero install and zero local state, one central version, fully deterministic and auditable.
- Cons: slower feedback loop (push to see validation), no local AI context preparation, DevOps team becomes the bottleneck for every process change.

### Alternative D. Adopt instead of build for traceability

- Keep specs in Git, but hold traceability in an existing test-management layer (Xray/Zephyr/TestRail/Allure TestOps) already linked to Jira, instead of a custom `traceability.yaml` + gates.
- Pros: mature reporting/coverage UIs for QA and management with no custom code; QA works in familiar tooling.
- Cons: traceability source of truth leaves Git; per-tool lock-in; requirement->scenario linkage is only as good as tagging discipline.

### Recommended combination

Start with A + B (conventions, skills, thin CI scripts, existing publisher, Jira automation rules, read-only MCP). Add comment-ops (C) for anything that must be enforced rather than assisted. Introduce a custom `sdd` CLI only where recurring documented friction shows conventions are not enough — most likely candidates: `change new/validate` ergonomics and traceability derivation (REC-004). This keeps the full architecture as the target picture while making every intermediate stage independently useful.

## 5. Open Human Decisions

1. Adopt REC-002..REC-007 as accepted decisions, or defer specific ones to Phase 1 planning.
2. RESOLVED 2026-07-03: the human owner accepted the A+B combination (conventions + skills + thin scripts + standard tool features, no custom `sdd` CLI upfront) with explicit triggers for starting CLI development. Details, success criteria, and CLI triggers are recorded in `docs/IMPLEMENTATION_STRATEGY.md`.
3. Historical item superseded on 2026-07-06: stale architecture draft removed instead of being aligned in place; narrowed MVP lives in current docs and OpenSpec proposals.

## 6. Sources

- OpenSpec: <https://github.com/Fission-AI/OpenSpec>
- GitHub Spec Kit: <https://github.com/github/spec-kit>
- Spec Kit "illusion of work" discussion: <https://github.com/github/spec-kit/discussions/1784>
- Scott Logic Spec Kit field test: <https://blog.scottlogic.com/2025/11/26/putting-spec-kit-through-its-paces-radical-idea-or-reinvented-waterfall.html>
- HN: Spec-Driven Development — The Waterfall Strikes Back: <https://news.ycombinator.com/item?id=45935763>
- Spec-Driven Development in practice (Medium): <https://medium.com/@lookoutking/spec-driven-development-in-practice-my-experience-with-spec-kit-8f250b47d677>
- kovetskiy/mark: <https://github.com/kovetskiy/mark>
- markdown-confluence: <https://github.com/markdown-confluence/markdown-confluence>
- Markdown->Confluence via GitHub Actions: <https://dev.to/vearutop/publishing-markdown-to-confluence-using-github-actions-1k4g>
- Doorstop: <https://github.com/doorstop-dev/doorstop>
- StrictDoc FAQ: <https://strictdoc.readthedocs.io/en/latest/latest/docs/strictdoc_03_faq.html>
- RTM maintenance in agile (Ketryx): <https://www.ketryx.com/blog/best-practices-for-maintaining-a-requirement-traceability-matrix-in-agile>
