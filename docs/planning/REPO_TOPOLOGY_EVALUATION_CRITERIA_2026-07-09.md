# Internal OpenSpec Customization Screenshots: Evaluation Criteria And Topology Comparison Frame

Status: planning input for Phase 1 work item 1.4 (`define-repo-topology-config`). Prepared 2026-07-09 before the screenshot review. Not an accepted contract.

## 1. Input Status And Blocker

- The human owner moved the corporate analytics template photos from the earlier local `/analytic-template/` folder to `arch-screenshots/analytic-template/` (already recorded in `docs/00_FILE_STRUCTURE.md`, the Phase 1 plan, and `docs/planning/ANALYTIC_TEMPLATE_STRUCTURE_AND_MIGRATION_PLAN_2026-07-06.md`).
- The screenshots of the internal OpenSpec customization / process approach were expected in `arch-screenshots/openspec-de/`, but **as of 2026-07-09 that folder exists and is empty (0 files)**. The screenshot evaluation is blocked until the photos are re-added. Per the phase-plan intake record, readability problems must be reported explicitly before any recommendation is treated as evidence.
- The human owner reports that the internal solution recommends storing analytics separately while storing specs next to code; this claim must be confirmed against the actual screenshots before it is used as evidence.

## 2. Evaluation Criteria For The Internal Solution

Each criterion references the accepted product goal (deterministic OpenSpec/Markdown-first SDD process; see `AGENTS.md` Product Direction and `docs/IMPLEMENTATION_STRATEGY.md`) so the comparison stays grounded in what this product must guarantee, not in general taste.

1. **AI-independence of process guarantees.** Do the structure and gates work when only a weak corporate model (GigaCode CLI) or no AI at all is available? Our strategy forbids process guarantees that depend on the AI layer.
2. **Single source of truth.** Where does canonical behavior truth live (Git vs Confluence vs tracker), and does the approach create dual-truth surfaces? Our architecture: Git/OpenSpec canonical, Confluence generated, Jira status-only.
3. **Repository topology and content split.** Which artifacts live in a central specs repo versus next to code, and how do cross-repo changes work? Must be comparable with our planned `team-specs` vs project-repo split (work item 1.4 exit criteria).
4. **Authoring ergonomics for analysts and weak models.** Are artifacts forms/typed records with one naming grammar, or free prose and nested tables? Our design rule: typed YAML + generated tables, IDs never translated.
5. **Deterministic validatability.** Can a dependency-free script or CI gate check the structure (required files, IDs, links, matrices), or does correctness rely on humans reading guidance text?
6. **Human readability without tooling.** Can an analyst or reviewer understand the raw repository in Bitbucket without generators or plugins? This backed the Russian-prose-canon decision.
7. **Reusability by another team.** Is there a documented bootstrap path without copying history? Shared scripts/templates/skills distributed once (copy with version pin, submodule/subtree, or CI fetch), not maintained per repo?
8. **Ownership and review contract.** How are owners/reviewers assigned (registry, CODEOWNERS, role approvals), and does it map to our planned `owners.yaml` -> generated CODEOWNERS model?
9. **Traceability support.** Do stable IDs link requirement -> scenario -> task/test/evidence, and can a validator check the links?
10. **Corporate approval compatibility.** Can the structure produce the approval views corporate reviewers require (the unified-document layout), preferably as generated rendering rather than manual duplication?
11. **Thin-MVP compatibility.** Does the approach let small changes stay small, or does it force full-package burden on every change? Our matrix is risk-oriented.
12. **Migration path.** Does it support gradual on-touch migration of existing Confluence analytics instead of a bulk rewrite?
13. **Version/upgrade policy.** Does it pin the OpenSpec (or equivalent tooling) version and define upgrade/compatibility review, which the merged 1.4 proposal must cover?
14. **Maintenance and drift cost.** What keeps spec and code (and generated views) from drifting: process discipline only, or deterministic checks?

## 3. Two Storage Models To Explain At Gate 1.5

Work item 1.4 must present options; the screenshots reportedly use Model B, our current plan is Model A. Both must be described with tradeoffs in the proposal.

### Model A — central `team-specs` repo (current plan)

Analytics sources, Master Specs, Delta Specs/change packages, QA/AT plans, traceability, templates, validation scripts, and publishing config live in one central analyst-facing repository; project repositories keep code, tests, AT code, code-local docs, and reference change IDs instead of copying requirements.

- Strengths in our context: analysts author in one place without needing rights or Git fluency across N code repos; the corporate approval unit is solution-level and often spans several systems, matching one change package; publication and validators are implemented once; another team bootstraps by cloning one repo skeleton; process evolution happens in one PR.
- Costs: spec PR and code PR are separate (two-step review); spec-code drift is possible and must be countered with change-ID references from code PRs plus traceability checks; cross-repo CI coordination is needed for full packages.

### Model B — specs next to code, analytics elsewhere (reported internal recommendation; default OpenSpec usage)

Each project repository carries its own `openspec/` (specs change atomically with code in one PR); analytics lives in a separate space (Confluence or a docs repo).

- Strengths: atomic spec+code review, spec versioned with the release, minimal drift, obvious code ownership, no cross-repo choreography for single-repo changes; matches how OpenSpec tooling is designed to run.
- Costs in our context: analysts must work inside developer repos (permissions, unfamiliar tooling, weak-model hazards in large code trees); cross-system features fragment into per-repo spec slices with no single approval artifact; unified business/approval views must be assembled from many repos; templates/validators/skills must be synchronized across repos; separating analytics from specs re-creates the dual-truth gap between analysis and requirements that SDD is meant to close.

### Frame for the recommendation

The choice is driven by who authors specs and what the approval unit is. Developer-authored, repo-scoped specs favor Model B; analyst-authored, solution-scoped, multi-repo corporate approval favors Model A. The 1.4 proposal should present Model A as the recommended default with Model B (and a hybrid: central analytics/Master Specs plus thin per-repo references and generated CODEOWNERS) as alternatives, and record which screenshot-verified facts support or contradict each claim once the photos are available.

## 4. Next Steps

1. Human owner re-adds the internal-solution screenshots to `arch-screenshots/openspec-de/` (currently empty).
2. Run the full screenshot review against section 2 criteria; report any unreadable fragments explicitly.
3. Fold verified findings plus this comparison frame into the merged `define-repo-topology-config` proposal (work item 1.4) and the gate 1.5 decision packet.
