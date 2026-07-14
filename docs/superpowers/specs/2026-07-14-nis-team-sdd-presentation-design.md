# NIS and teamSDD Presentation Design

Date: 2026-07-14  
Status: approved narrative, awaiting written-spec confirmation  
Audience: the manager who initiated or sponsors NIS and other engineering decision-makers

## Communication Job

By the end, the audience should understand that teamSDD retains NIS as the primary corporate-process foundation and strengthens it with a deterministic, traceable, portable, and progressively automatable engineering control plane.

The presentation must demonstrate continuity and engineering development, not frame the project as a competing initiative or as a critique of NIS.

## Central Message

NIS supplies the corporate process foundation: structured change flow, explicit roles, readiness and completion gates, quality ownership, release handoff, and pilot discipline.

teamSDD preserves that foundation and adds formal OpenSpec contracts, Git-canonical change packages, deterministic verification, end-to-end evidence traceability, safe AI boundaries, risk-oriented test coverage, portable role mapping, and controlled parallel execution of independent work.

## Narrative Approach

Use the accepted narrative: **NIS is the foundation; teamSDD is its engineering development**.

The deck should progress through four questions:

1. What important foundation did NIS establish?
2. How was that foundation incorporated into teamSDD rather than replaced?
3. Which engineering additions make the process safer, more reliable, faster, and portable?
4. What is accepted today, what is still being implemented, and what must the pilot prove?

## Visual Direction

Use `outputs/team-sdd-project-overview.pptx` as the canonical visual template and source-slide inventory.

Preserve its visual language:

- dark navy opening, transition, and closing slides;
- white analytical slides with navy headings;
- pale blue content fields and amber emphasis;
- restrained iconography and simple process diagrams;
- strong takeaway titles, consistent page markers, and generous margins;
- a rhythm of overview, comparison, process, evidence, and synthesis layouts.

Use `outputs/openspec-de-vs-team-sdd.pptx` only as a narrative reference for concise side-by-side comparison and claim density. Do not combine its objects into a second visual template.

## Slide Structure

1. **NIS as the foundation of the engineering process** — establish continuity and respect for the original initiative.
2. **We retained the central NIS idea** — SDD, Git, human decisions, automated checks, and reproducible delivery.
3. **NIS was incorporated into the target architecture, not replaced** — NIS provides corporate process behavior; teamSDD provides the engineering execution and control plane.
4. **The core NIS operating practices remain** — classification, roles, readiness/completion gates, Tech Lead governance, quality, release handoff, and bounded pilot discipline.
5. **NIS ideas become formal engineering contracts** — OpenSpec requirements, change packages, deterministic schemas, and Git as the source of truth.
6. **Classification becomes a deterministic route** — `minor | major | hotfix`, conservative escalation, and explicit legacy migration.
7. **Readiness becomes provable before implementation starts** — fixed input, ownership, risks, quality strategy, regression, dependencies, and rollback.
8. **Completion is separated into auditable engineering states** — implementation complete, DoD, release ready, archive ready, archived, and external Delivered.
9. **The Tech Lead receives an engineering control plane** — source-linked review packs, scope-drift control, stop/hold/resume, and release recommendations.
10. **Reliability comes from risk-oriented checks and traceability** — requirements and scenarios remain linked to tasks, executions, decisions, failures, and evidence.
11. **Speed comes from safe parallel execution** — independent work only, explicit owners and dependencies, non-overlapping write scopes, separate evidence, and one deterministic integration gate.
12. **AI evolves through two controlled horizons** — first a complete deterministic AI-disabled process and fallback, then bounded automation without transferring accountable authority.
13. **The process is portable across teams and environments** — responsibility-based roles, system adapters, Windows/Linux/macOS support, and external certification before corporate configuration.
14. **Accepted direction is broader than the current implementation** — distinguish accepted architecture and OpenSpec changes from functionality still being implemented and certified.
15. **NIS remains the foundation; teamSDD makes it engineering-grade** — close with the practical value: safer adoption, stronger evidence, controlled automation, and a credible pilot path.

## Speaker Notes

Every slide must include brief speaker notes in Russian:

- normally 2–4 short sentences;
- explain the implication or transition rather than repeat visible copy;
- expand abbreviations or technical concepts when first needed;
- state any important implementation-status caveat where relevant;
- avoid internal production notes, timing instructions, and long scripts.

## Accuracy and Status Rules

- Clearly distinguish accepted direction from implemented behavior.
- Do not claim that schema version 2, class-aware gates, Tech Lead reports, release-package schemas, failed-run evidence, pilot controls, or expanded certification are already complete.
- Present deterministic and AI-disabled operation as the required foundation and permanent fallback, not the final AI-minimal product state.
- Present AI as advisory or bounded automation; human approvals, waivers, risk acceptance, merge, release, and archive remain human-owned.
- Present safe parallelism only for explicitly independent work with deterministic integration verification.

## Deliberate Exclusions from the Deck

The main deck must not contain a criticism section or a list of NIS weaknesses. The following material belongs only in the separate user-facing report:

- unsafe or incompatible NIS assumptions;
- elements that do not fit the project architecture or corporate transfer model;
- process-effectiveness evaluation content rejected from the target process;
- risks of direct copying and reasons for adapting rather than reproducing selected NIS mechanisms.

The deck may use positive phrasing such as “adapted for portability” or “formalized as a deterministic contract” when needed to explain the project contribution, without presenting NIS as defective.

## Deliverables

1. `outputs/nis-vs-team-sdd-engineering-evolution.pptx` — the final editable presentation.
2. A concise final report in Russian containing:
   - what was deliberately not written into the deck;
   - NIS weaknesses relevant to engineering adoption;
   - NIS elements that do not fit this project;
   - verification performed and residual limitations.

## Verification

- Inspect every inherited source slide used as a template frame.
- Render every final slide and inspect it at full size.
- Check text clipping, wrapping, overflow, unintended overlap, placeholder residue, notes presence, and visual consistency.
- Validate template fidelity and slide-canvas bounds.
- Verify all implementation-status claims against the current presentation comparison report, active OpenSpec changes, and project decisions.

