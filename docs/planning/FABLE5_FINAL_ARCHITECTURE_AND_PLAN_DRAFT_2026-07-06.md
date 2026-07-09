# Final Architecture And Staged Plan Draft (Fable 5)

Status: planning draft. It consolidates already-accepted decisions into one target picture and proposes the remaining sequence. It decides nothing new; every open item routes to a human gate. If this draft disagrees with `docs/IMPLEMENTATION_STRATEGY.md`, accepted decisions, or OpenSpec proposals, those win.

Date: 2026-07-06.

Companion audit: `docs/audits/FABLE5_DOCUMENTATION_ARCHITECTURE_REVIEW_2026-07-06.md`.

## 1. Target Architecture (consolidated from accepted decisions)

One sentence: a deterministic, Git/OpenSpec-canonical change-package process whose guarantees are scripts/CI/templates, whose conveniences are replaceable AI skills, and whose integrations are standard tool features — with a custom CLI built only where measured friction proves triggers.

Layer model (all already accepted; listed here as the single orientation picture):

| Layer | Owner surface | Contents | Guarantee level |
|---|---|---|---|
| Canonical source | `team-specs` Git repo, `openspec/` | change packages, living specs, traceability, waivers, templates | truth |
| Deterministic gates | scripts, pre-commit, Jenkins | structure/metadata/traceability/waiver validation, drift checks | hard gate; must work with AI off |
| Standard tool features | Bitbucket, Jira Automation, markdown->Confluence publisher, OpenSpec CLI | reviewers, status workflow, publication, spec tooling | configured, not built |
| AI convenience | role skills, MCP (Jira/Confluence), context packs | drafts, reviews, proposals, skeletons, spec-questioning | advisory only; never a gate |
| Orientation (future) | project memory triad: constitution/quality policy, project map, OpenSpec changes/specs | navigation index, read packs, failure memory, role guides | read model; validated against reality |
| Publication (future) | generated Confluence views | change/capability/journey/release pages with source metadata | read model; feedback routes back to Git |
| Approval | humans | Spec PR review, waivers, archive/acceptance, scope | non-delegable |

Conflict-resolution order (accepted 2026-07-06): OpenSpec wins for behavior/acceptance; `docs/CONTEXT.md` for terms; `AGENTS.md` for agent rules; phase plans for temporary execution; derived surfaces are fixed or regenerated, never patched in place.

Naming rule to keep everywhere: "`sdd change new/validate/pr/archive`" names the four thin-flow capabilities, not a shipped binary. The first delivery is `templates/change/` + `scripts/validate_change.py` + pre-commit/Jenkins + skills. A CLI wrapping those scripts appears only when the trigger table in `docs/IMPLEMENTATION_STRATEGY.md` section 6 fires.

## 2. Staged Plan From Here

Stage numbering below is execution order, not roadmap phase renumbering; roadmap phases stay authoritative for status.

### Stage A — Close Phase 1 decisions (current)

1. Answer the small decision batch from the companion audit section 5: lifecycle naming, 1.8 enforcement staging, decision-log consolidation, proposal merge. Done 2026-07-06: recommended options approved (six canonical states; error-level enforcement; `docs/DECISIONS.md` at acceptance readiness; merged proposal).
2. Draft the remaining proposal: `define-repo-topology-config` with the OpenSpec version pin/upgrade policy merged in — work item 1.4; then human gate 1.5.
3. Human gate 1.7 (Confluence feedback owner/SLA) using the recommended defaults already written in `define-confluence-feedback-loop/design.md`.
4. Record the OpenSpec version pin in the location the topology/config decision chooses (closes AUDIT-017).

Historical exit target: all Phase 1 contracts approved as proposals; no accepted specs yet. This target was superseded on 2026-07-09 when the Option A batch archive promoted the readiness-complete package into accepted specs.

### Stage B — Reconcile the deterministic layer (work items 1.8–1.9)

1. Reconcile `scripts/validate_change.py` with the approved contracts (closes AUDIT-016): lifecycle status vocabulary per the naming decision; thin/full required-file matrix per approved Option A; template default `type` made consistent with `mode: thin`; waiver-shape checks per approved waiver fields.
2. Extend tests with the negative cases the proposals already enumerate (invalid transitions, pending links at archive readiness, waiver misuse, placeholder production values).
3. Keep everything dependency-free Python; no Jira/Confluence/MCP anywhere in gates.

Exit: validator enforces exactly the approved matrix; template copies cleanly into a valid thin package.

### Stage C — Phase 1 acceptance (work items 1.10–1.11)

1. Acceptance readiness review; resolve the `define-confluence-feedback-loop` naming/scope note at this gate.
2. If decision 3 (decision log) is approved: create `docs/DECISIONS.md`, migrate decisions to stable IDs, reduce README/audit/roadmap copies to references — one mechanical commit, done at this boundary, not mid-phase.
3. Final human archive gate; only then promote changes into `openspec/specs/`. Completed on 2026-07-09 by the Option A batch archive.

Exit: first accepted living specs exist; Phase 1 complete.

### Stage D — Pilot the thin flow (roadmap Phase 3 content, delivered per strategy)

1. Run real changes through template -> validate -> Spec PR -> archive in `team-specs` topology, using skills for drafting and scripts for gates.
2. Collect M1–M7 baselines from the first two sprints (name the process owner first — audit F4.4).
3. Build nothing CLI-shaped unless a trigger fires; log friction against the trigger table.

### Stage E — Later layers (roadmap Phase 4, unchanged order)

Only after the pilot proves the thin flow, and each behind its own accepted contract: Confluence publication (after 1.7 contract), Jira task automation, QA/AT proposals, role inboxes, project memory implementation (`define-project-memory-and-weak-model-guardrails` proposal first, starting from `docs/planning/PROJECT_MEMORY_AND_WEAK_MODEL_GUARDRAILS.md`), legacy baseline workflow, deterministic sync/upgrade, navigation index (lightweight script before any Pangolin/Graphify dependency).

## 3. What Deliberately Stays Small

- No new documentation files beyond the decision log (if approved); improvements go into existing owners.
- No second architecture document: this draft is disposable planning input and should be archived or deleted once Stage C lands its content into roadmap/phase plans.
- The Phase 1 proposal count does not grow past the planned set; new ideas route through change intake to Phase 4 or the memory proposal.
- Weak-model support in the MVP is exactly two things: contradiction-free templates (Stage B) and read packs that label canonical vs supporting files (already specified in the governance proposal). Everything else in the guardrails doc waits for its own proposal.
