# Project Memory And Weak-Model Guardrails

Status: Phase 1 planning input; not an accepted implementation contract yet.

Date: 2026-07-06.

## Purpose

This document captures the planning direction for project memory, documentation quality, weak corporate AI model guardrails, repeated-error memory, spec-questioning, and analyst/QA usability.

It exists so the next detailed OpenSpec proposal can start from durable context instead of chat history.

## Source

Human feedback on 2026-07-06 asked to preserve these topics before deeper planning:

- Graphify-like project navigation;
- documentation boundary and quality control;
- weak model support for Qwen/DeepSeek-class assistants;
- repeated-error memory;
- Grill With Docs or equivalent spec-questioning workflow;
- QA and analyst usability.

## Current Decision Boundary

Accepted direction:

- project memory is useful and should be planned deliberately;
- memory must not become a second behavior source of truth;
- weak corporate AI models must be supported with deterministic scaffolding and small explicit workflows;
- QA and analyst onboarding must be understandable without asking them to read the whole architecture.

Not yet accepted:

- exact memory folder layout;
- exact schemas for memory index, project map, known failures, question banks, and role guides;
- whether to implement a Pangolin-backed graph tool, a simple script first, or both;
- whether any of these checks belong in the first MVP.

The current default is: these ideas are Phase 1/Phase 4 planning input and should not expand the first thin MVP unless the human owner explicitly re-scopes it.

## Core Rule

Project memory is an orientation and retrieval layer. It helps agents and humans find the right canonical source, but it does not replace canonical sources.

```text
Behavior truth       -> OpenSpec changes and accepted living specs
Process rules        -> accepted specs, AGENTS.md, strategy, phase plans
Repository reality   -> code, templates, scripts, tests, CI output
Review truth         -> PR/review surface and recorded human decisions
Project memory       -> indexed, concise, evidence-backed navigation over the above
Generated views      -> readable publication, never canonical edits
```

## 1. Graphify-Like Project Navigation

A corporate Graphify-like capability can be useful, including a Pangolin-backed implementation later, but it should start as deterministic navigation rather than AI reasoning.

Recommended shape:

- read repository files, OpenSpec changes/specs, templates, scripts, tests, traceability, and docs;
- build an explicit graph of source files, requirements, scenarios, tasks, evidence links, owners, and generated views;
- emit a small machine-readable index, such as `memory-index.json`;
- optionally emit a human-readable `memory-map.md`;
- support task-specific read packs, for example "read these 8 files before changing waiver policy";
- report broken links, stale source references, orphan docs, and unowned memory entries.

What it should not do:

- make product decisions;
- rewrite requirements by itself;
- treat generated graph data as canonical;
- hide uncertainty by producing a confident summary without source links.

Planning recommendation:

- Phase 1 proposal should define the graph/index contract.
- Phase 2/4 can decide whether Pangolin is needed or whether a small local script is enough.
- The first useful version can be file/link/index based; graph database integration should wait until the lightweight version proves value.

## 2. Documentation Boundary And Quality

The process cannot fit all useful documentation into only `constitution.md`, `project-map.md`, and `AGENTS.md`. The boundary should be based on responsibility, not file count.

Recommended documentation tiers:

| Tier | Purpose | Source of truth? |
|---|---|---|
| OpenSpec changes/living specs | product/process behavior, requirements, scenarios, acceptance | yes for behavior |
| Constitution / quality policy | stable rules, quality bars, human ownership, non-negotiable boundaries | yes for operating rules after acceptance |
| Project map | topology, modules, repos, owners, integrations, reusable assets | yes for orientation only; must be validated against reality |
| Memory notes | proven working patterns, local gotchas, legacy notes, context shortcuts | no; evidence-backed support material |
| Failure memory | repeated mistakes and verified fixes | no; prevention and retrieval layer |
| Role guides | analyst/QA/developer walkthroughs | no; onboarding layer |
| Generated views | audience-specific reading and publication | no; links back to canonical source |

Quality rules for memory documents:

- one clear target reader;
- one clear task or decision it helps with;
- source/evidence links;
- owner or responsible role;
- last verified date or review trigger;
- short enough to be read inside a weak-model context window;
- no duplicated behavior contracts that should live in OpenSpec;
- no prose that cannot be tied to an action, decision, risk, or verified fact.

Anti-water checks:

- "Would a new analyst, QA, developer, or agent make a better decision after reading this?"
- "Can a reviewer verify where this statement came from?"
- "Is this a behavior rule? If yes, why is it not in OpenSpec?"
- "Is this a stale snapshot? If yes, can it be generated or checked?"

Potential deterministic checks:

- link checker;
- stale-date checker;
- owner field checker;
- orphan document checker;
- "claims without source link" linter for memory docs;
- project map versus repository reality check;
- OpenSpec requirement/scenario reference checker.

### Source Ownership And Deduplication

The project should use a write-once, reference-many rule. Each type of knowledge has one canonical owner; every other surface links to that owner, summarizes it as orientation, or is generated from it.

| Information | Canonical owner | Allowed derived surfaces |
|---|---|---|
| Requirements, scenarios, acceptance criteria, lifecycle behavior, traceability behavior, waiver behavior | OpenSpec changes or accepted living specs | Generated Confluence views, role guides, project memory links, reports |
| SDD process lifecycle, artifact rules, quality gates, version and waiver policies | OpenSpec changes/specs after approval | `docs/` explanations, generated views, onboarding guides |
| Architecture decisions, rationale, constraints, phase direction, audit findings | `docs/`, phase plans, audit notes, accepted human decisions | OpenSpec design sections when behavior contracts are affected |
| Repository topology, modules, owners, integrations, reusable assets | Project map or future generated/validated memory artifact | Read packs, navigation index, role guides |
| Agent operating instructions | `AGENTS.md` plus global skills | Task launchers, read packs, final-report checklists |
| Analyst/QA/developer onboarding | Role guides that link to canonical sources | Generated team-facing views |
| Task execution status | Jira/tracker or future workflow/status surface after task automation exists | Reports, dashboards, generated summaries |
| Publication content | Generated view from Git/OpenSpec/docs sources | Confluence pages and other read-only publication surfaces |

Boundary rule:

- Behavior belongs in OpenSpec.
- Docs explain why, how, where, and who is responsible.
- Project memory helps find and compare sources; it must not restate a second normative version.
- Generated views are read models; they must carry source links or metadata and should be regenerated instead of hand-edited as truth.

Practical rules:

- Do not copy full requirement, scenario, or acceptance text into docs, role guides, or memory notes.
- Reference stable requirement/scenario/change IDs and source paths instead.
- Role guides describe how a role uses canonical artifacts; they do not redefine process rules.
- Project memory may summarize orientation, but normative statements must point back to the canonical owner.
- Generated views should include source commit, source file or change ID, generated timestamp, and a source warning.

Conflict resolution:

- OpenSpec wins for behavior, artifact contracts, acceptance, traceability, waivers, and lifecycle rules.
- `docs/CONTEXT.md` wins for canonical project terminology until a term is promoted into accepted OpenSpec behavior.
- `AGENTS.md` wins for agent operating rules.
- Phase plans win for temporary active-phase execution rules.
- If a derived surface conflicts with its canonical owner, fix or regenerate the derived surface instead of editing multiple copies.

Weak-model read packs should make this explicit. A read pack should say which file is canonical for each topic, which files are supporting context, and which summaries are generated or advisory.

Future deterministic checks:

- a normative-language linter that flags `SHALL`, `MUST`, `must`, `should`, `required`, `shall not`, and Russian equivalents outside allowed canonical files;
- a source-link check for memory notes, role guides, and generated views;
- a duplicate-requirement check that rejects the same stable requirement ID with different text in multiple places;
- a generated-block check that prevents hand edits to generated publication sections;
- a stale-memory check requiring `last_verified` or a review trigger for project map and memory entries;
- an orphan-doc check requiring owner, purpose, and an index/map link for each maintained document.

## 3. Weak Model Guardrails

Corporate AI may be Qwen/DeepSeek-class or GigaCode-class, so the system must assume weaker reasoning, weaker instruction following, and weaker long-context discipline than Claude or GPT.

Design principles:

- do not rely on the model to remember when a skill applies;
- do not give the model one huge architecture document and expect correct synthesis;
- prefer small explicit workflows, templates, and deterministic checks;
- every gate-like claim must be backed by script, CI, reviewer, or recorded evidence;
- AI output remains advisory until human-reviewed and committed.

Recommended guardrails:

- task launcher or wrapper selects the relevant skill/read pack before the model starts;
- task templates include mandatory checkboxes for "read", "asked", "verified", and "blocked";
- generated read packs list exact files and sections to inspect;
- skills use numbered steps, short examples, and explicit negative cases;
- prompts avoid abstract labels and use concrete examples;
- long planning tasks are split into worker/reviewer/architecture/verification roles where tooling allows;
- every final report must include what was not verified.

Useful future checks:

- skill-use declaration in task output;
- required-read-pack evidence for high-risk tasks;
- command evidence block for deterministic claims;
- "AI cannot approve" check for lifecycle, waiver, and archive decisions.

## 4. Repeated-Error Memory

Repeated mistakes should become structured prevention data, not a free-form incident diary.

Recommended artifact:

```yaml
id: failure-001
title: short name
applies_to:
  paths: []
  capabilities: []
  roles: []
trigger: when this mistake usually happens
symptom: what the human or CI sees
root_cause: why it happened
wrong_behavior_to_avoid: what the agent must not do again
correct_resolution: what fixed it
detection:
  commands: []
  manual_checks: []
prevention:
  checklist_items: []
  validator_rule: optional future rule
source_evidence: links or commit refs
owner: role or person
last_seen: YYYY-MM-DD
review_after: YYYY-MM-DD or condition
status: active | retired
```

Retrieval rule:

- do not load every failure into every task;
- retrieve only the top relevant failures by path, capability, role, change type, and trigger;
- each read pack should include a small "known traps" section.

Promotion rule:

- a repeated failure starts as a note;
- if it happens again, add it to structured failure memory;
- if it can be checked deterministically, turn it into a validator/CI/checklist rule;
- retire it only after the prevention check has made it obsolete.

## 5. Grill With Docs / Spec-Questioning Workflow

The project needs a spec-questioning workflow before implementation planning, especially for weaker models.

Purpose:

- force unclear requirements into explicit questions;
- prevent the model from inventing missing business logic;
- connect each question to existing docs, OpenSpec deltas, legacy baseline, and traceability;
- record answered, deferred, rejected, or out-of-scope decisions.

Recommended flow:

```text
spec draft
  -> read related docs/specs/project map
  -> ask targeted gap questions
  -> record answers or deferrals
  -> update proposal/design/spec delta
  -> only then plan tasks
```

Question categories:

- actor and owner;
- business goal;
- in-scope and out-of-scope behavior;
- data inputs, outputs, and state transitions;
- negative cases and error handling;
- legacy behavior and migration;
- QA evidence and manual verification;
- automation expectations;
- security, privacy, compliance, and rollback;
- integration boundaries;
- user-facing text and generated publication impact.

Guardrail:

- a spec may proceed with open questions only when each open question has an explicit disposition: `deferred`, `not_applicable`, `blocked`, or `waived`, with reason and owner.

Implementation note:

- The existing global `grill-with-docs` skill is a good conceptual fit for strong external tooling.
- The corporate version should be tool-agnostic and should include a static question bank so weaker models do not need to invent the questions.

## 6. QA And Analyst Usability

QA and analysts need role-specific workflows, not a request to understand the whole architecture.

Recommended role materials:

- analyst quickstart: create intent, clarify scope, write acceptance examples, route feedback;
- QA quickstart: read scenario, derive test plan/test cases, record evidence, request waiver if needed;
- shared glossary: stable IDs, requirement, scenario, waiver, traceability, baseline, generated view;
- one thin-change walkthrough;
- one legacy-baseline walkthrough;
- short "what must be true before I pass this on" checklist per role.

Role guide constraints:

- keep guides in Russian if they are generated team-facing onboarding views;
- keep canonical OpenSpec and stable IDs in English;
- do not require analysts/QA to read raw architecture before doing a first guided flow;
- do not hide Git/OpenSpec truth, but provide a guided path through it.

Usability evidence:

- a new analyst can complete the main analysis flow after one onboarding session;
- a new QA can produce test evidence or a waiver request from a scenario without help;
- the role walkthrough reveals fewer than the agreed number of manual steps;
- role satisfaction and confusion points are recorded after pilot use.

## Proposed Future Artifacts

Possible future repository artifacts, subject to a later proposal:

```text
memory/
  constitution.md
  project-map.yaml
  memory-index.json
  known-failures.yaml
  question-banks/
    thin-change.yaml
    full-package.yaml
    legacy-baseline.yaml
  role-guides/
    analyst.md
    qa.md
    developer.md
```

These names are placeholders, not accepted paths. The final location depends on the repo topology/config decision.

## Proposed Future Verification

Future verification should cover:

- memory index builds successfully;
- every memory entry links to source evidence;
- project map references real files or explicitly external systems;
- failure memory entries include detection and prevention;
- spec-questioning output records all open questions with disposition;
- analyst/QA role guides pass a walkthrough with a new participant;
- generated read packs do not include secrets or private dumps.

## Open Decisions For Later Planning

1. Should project memory live in `memory/`, `docs/memory/`, or under the future `team-specs` topology?
2. Should the first graph/navigation implementation be a simple local script, Pangolin-backed, or both?
3. Which memory artifacts are manually edited and which are generated?
4. Who owns project map accuracy?
5. What is the maximum allowed age for memory entries before review?
6. Which role guides are required before pilot onboarding?
7. Which spec-questioning gates are mandatory for thin changes versus full packages?
8. How should known failure memory be reviewed so it stays useful and does not become blame-oriented noise?

## Recommended Next Planning Step

Create an OpenSpec proposal for `define-project-memory-and-weak-model-guardrails` after the current Phase 1 proposal set is synchronized enough to avoid overlap with documentation governance, repo topology/config, traceability, and OpenSpec version policy.
