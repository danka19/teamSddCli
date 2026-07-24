# Corporate Analytics Template: Structure Analysis And SDD Migration Plan

Status: historical planning input from the 2026-07-06 review of the corporate "unified solution document" template (V.4). Updated with 2026-07-09 human decisions: the existing Confluence analytics corpus is a read-only archive for the first pilot, accepted diagrams/assets use Git-managed source or source+export with stable IDs, and approval readiness stays minimal/validator-backed until a later full-package contract. Updated on 2026-07-14 with the deferred upstream business-analysis-to-system-analysis flow described in section 8. The 2026-07-24 decision `D-029` supersedes this document's earlier capability/change-view assembly: the target is one full current analytics page per FP plus one page per release increment, with no mandatory generated change page. Normative proposed behavior and the complete updated design live in `openspec/changes/define-fp-analytics-publication-model/`.

Source: the human owner photographed the corporate Confluence template and two example pages into the local-only folder `arch-screenshots/analytic-template/` (moved from the earlier local `analytic-template/` location; photos reviewed in full). That folder contains corporate URLs, internal system names, and employee names, so it is git-ignored and must never be committed; this document deliberately abstracts all corporate identifiers.

## 1. What The Template Is

One large Confluence page per solution/release ("unified document"), section-numbered, with fill-in tables, mandatory-warning callouts, guidance panels, and links to platform checklists. It is the corporate approval unit: the analyst fills it, named role owners approve it. Structurally it is the corporate analog of our full change package.

Top-level structure (V.4):

| # | Section | Content shape |
|---|---|---|
| 1 | Solution card | Key-value table: tribe, team, component ID, links to release task, concept architecture, previous unified document, tracker story/release, template version |
| 2 | Key contacts | Flat table: person / process role (author, participant, approver) / responsibility area |
| 3 | Business requirements and constraints | Prose + links; answers "what must be done"; new-vs-modified application rules |
| 4 | Functional requirements | Answers "how it will work": 4.1 screen forms (versioned mockups); 4.2 user scenarios (BPMN/sequence-diagram guidance); 4.3 operation-history scenarios — 4.3.1 status model, 4.3.2 channel-support matrix, 4.3.3/4.3.4 operation detail attributes and employee confirmation; 4.4 technical scenarios (degraded mode, stand-in, reverse flows) |
| 5 | Solution architecture | Answers "how it is built": 5.1 data model table (entity/attributes/master system/caching/masking/export); 5.2 components and deployment table; 5.3 provided API (4 audience subsections); 5.4 consumed API (2 subsections) |
| 6 | Cybersecurity requirements | Masking meta-model, secrets interaction, expert approval callouts |
| 7 | Non-functional requirements | 7.1 platform-service interaction (the nested-table core, see section 2); 7.2 load/TPS; 7.3 rollout mechanics (feature toggles, channels, blocks); 7.4 exception approvals table |
| 8 | Checklist registry | Links to external architecture/security/migration checklists |
| 9 | Change history | Manual dated changelog of the template itself |

Example pages reviewed: a status-model example (state diagram + wide transition table) and a step-by-step user-scenario example (workflow gate/name, numbered steps, per-step entry/exit events, sequence diagram with notes).

## 2. The Nested-Table Patterns (the hard part)

Four recurring structures explain almost all of the template's complexity. None of them is prose; all four are typed records that render as tables — which is exactly why they map well to structured Git artifacts and badly to hand-written nested Markdown.

1. **Status model** (4.3.1 example): per status — status code, client-facing label, description, actions leading into the status, then N transition sub-rows (condition -> next status, system status code). The sub-rows nest inside the status row.
2. **Channel-support matrix** (4.3.2): rows = channels/workstations, columns = capabilities (create, fraud-confirm, degraded-mode duplicate, list display, detail display, cross-channel display), cells = yes/no/n-a plus occasional sub-cells with qualifiers.
3. **Platform-service interaction** (7.1): outer table rows = one per platform service (~20: parameter store, logging, audit, monitoring, authorization, healthcheck, stand-in, tech-breaks, launcher, toggler, client profile, session data, content broker, print service, dictionaries, CLOB storage, secrets operator, then order-processing services: operation history, compliance, confirmation, fraud component, confirmation-event dispatcher, archive delivery, async-job service). Each row's "configuration" cell contains its own typed inner table (e.g. parameters: name/key/description/type/default/role; logging events: event/level/journal type/condition; audit events: code/trigger condition/attributes; metrics: name/description/monitoring point/value; roles: role/description/privilege code/channels; secrets: what/where/engine/TTL/hot-reload; launcher features and options; toggler module/feature keys).
4. **Attribute/data-model tables** (4.3.4, 5.1): attribute name, value-type code, data type, confidentiality class, masked/unmasked examples; entity/attributes/master-system/caching/masking/export.

Everything else is flat tables (contacts, deployment, API endpoints, exceptions) or guided prose with diagrams.

## 3. Design Rule For Git/OpenSpec: Forms, Not Nested Tables

Weak corporate models reliably fail at drawing and editing nested Markdown tables, and Markdown itself cannot express them. The base to lay now:

- **Typed records live in YAML files with fixed schemas; tables are generated, never hand-drawn.** Each nested-table pattern becomes a flat, named list: `status-model.yaml` (statuses with a `transitions:` list — nesting becomes an ordinary YAML list), `channel-support.yaml` (matrix as a list of channel records with named capability fields), `platform-services.yaml` (one typed section per service kind), data-model/attribute tables likewise. A weak model fills a form with named fields far more reliably than it edits table markup, and a validator can check every field deterministically.
- **Diagrams are generated from the same source where possible.** The status diagram is derived from `status-model.yaml` (Mermaid state diagram) instead of maintained as a second hand-drawn artifact — one source, no drift between diagram and transition table. Sequence diagrams are authored as Mermaid text next to the scenario; large process schemes keep source + exported SVG/PNG with stable IDs (per the open diagram-storage decision).
- **Confluence rendering reassembles the corporate look.** The publication layer (later phase) renders the YAML records back into the familiar nested-table layout for approvers. Analysts read/approve the generated page; the Git source stays flat and validatable.
- **The template's red mandatory-warning callouts are validator/checklist rules, not prose.** Examples observed: "this section is mandatory when the solution interacts with operation history", "masking meta-model must be approved by the security expert", "toggles must be described for every business feature". These become required-field checks, conditional-section checks, and approval-evidence checks in the change validator or review checklist — the same guarantee, but deterministic instead of relying on someone reading a red box.

### When the template or corporate requirements mandate nested tables

The corporate template prescribes how the approval document must look, not how our source must be stored; approvers see the rendered Confluence page, never the Git internals. So the obligation is satisfied at the view layer:

- **Source layer (Git): nested tables are forbidden.** Every nested structure is normalized into one of: (a) a typed YAML record with a list field (outer row -> record, inner table -> list of sub-records); (b) a Markdown subsection per outer row (`### <service>` heading + flat table below) when the content is prose-heavy; (c) two flat tables linked by a key column when both levels are genuinely tabular. Markdown cannot express nested tables and weak models cannot reliably edit them, so this is a hard authoring rule, and a future lint check should reject table markup (or raw HTML tables) inside spec table cells.
- **View layer (generated Confluence): nested tables are reassembled.** Confluence storage format supports nested tables natively, so a deterministic renderer can rebuild the exact template layout (outer service table with inner configuration tables) from the flat source. Template compliance becomes a rendering contract with a golden-example test, not an authoring burden.
- **Transition period (before publication automation exists):** the corporate Confluence template keeps being filled manually for official approval as today, and the pilot change package in Git is the engineering source. To avoid dual-truth drift, the package records the link to the approved corporate document as approval evidence, and the on-touch migration rule applies: content is normalized into Git when a pilot change touches it, not wholesale.
- **If manual dual-entry proves unacceptable during the pilot,** the fallback is a minimal one-way renderer for only the nested-table sections (status model, channel matrix, platform services). That would pull a slice of Confluence publication into an earlier phase, which is an explicit human re-scope decision (gate 1.7 territory), not a default.

### Existing Confluence pages and analyst-drawn diagrams

Human decision on 2026-07-09:

- old Confluence analytics pages are read-only archive/reference material for the first pilot, not a bulk-migration target;
- if old content is reused for a new change, the accepted source is created in Git/OpenSpec through the reviewed change, while the legacy page remains evidence/reference;
- diagrams drawn directly in Confluence are allowed as discussion drafts, but accepted/published diagrams must be exported or recreated into the Git-managed asset flow;
- Visio can be used when it is the team's convenient diagram source format, but it is not mandatory. Mermaid/PlantUML for generated diagrams, diagrams.net/draw.io source files, Figma source+export, or another versioned source+export pair are also valid when they keep stable IDs and generated-view traceability.

## 4. Mapping Template Sections To SDD Artifacts

| Template section | SDD change-package artifact | Notes |
|---|---|---|
| 1 Solution card | `change.yaml` metadata + links | Tracker/architecture links become metadata fields; template version -> package schema version |
| 2 Contacts | `change.yaml` review/owner groups + owners registry | Role-based, not person-based, where possible |
| 3 Business requirements | `proposal.md` (why/what) | Constraints and assumptions belong here |
| 4.2/4.3 user scenarios | OpenSpec Delta Spec scenarios (Russian prose, English keywords) | Per-step entry/exit events fit WHEN/THEN naturally; sequence diagram as Mermaid next to the scenario |
| 4.1 screen forms | screen catalog + versioned assets (planned contract) | Already planned as `screens.yaml`/assets; not first-MVP |
| 4.3.1 status model | `status-model.yaml` + generated diagram | New typed artifact, full packages with stateful operations only |
| 4.3.2 channel matrix | `channel-support.yaml` | New typed artifact, conditional |
| 4.3.4/5.1 attributes/data model | `data-model.yaml` (or design.md section with generated table) | Masking/confidentiality fields map 1:1 |
| 5.2-5.4 deployment/API | `design.md` + typed API/deployment records | Flat tables; may stay as Markdown tables initially |
| 6 security | `design.md` security section + checklist/waiver rules | Expert approval = review evidence, not prose |
| 7.1 platform services | `platform-services.yaml` | The big win: one schema per service kind |
| 7.2-7.4 load/rollout/exceptions | `design.md` NFR section; exceptions -> waiver records | The exception-approval table is literally our waiver contract |
| 8 checklist registry | links from tasks.md/checklists | External checklists stay external links |
| 9 change history | Git history | Free: no manual changelog in Git |

Thin changes never touch most of this: the matrix stays risk-oriented, and the typed artifacts above are conditional full-package sections (statefulness, UI, platform integration), not new thin-change burden. This mapping must not silently expand the first MVP.

## 5. Staged Plan

1. **Now (Phase 1, no new scope):** this analysis feeds `define-repo-topology-config` and the Confluence feedback/publication proposal. Gate 1.5 approved central `team-specs`; the diagram/asset-storage decision is Git-managed source or source+export with stable IDs. No template/validator changes yet.
2. **Phase 1 proposal work (after gate 1.5):** extend `define-change-artifact-contracts` (or a dedicated follow-up proposal) with the conditional typed artifacts — status model, channel support, platform services, data model — as full-package sections with YAML schemas and validator expectations. Russian-prose examples per the language decision.
3. **Analyst source preparation (P3/P4):** retain the accepted local typed-analytics foundation, prepare one sanitized full-FP example, and collect real corporate renderer constraints without treating the existing compact P3 schemas as the final publication contract.
4. **Publication layer (P5 under `D-029`):** implement the proposed `define-fp-analytics-publication-model` after human acceptance and the corporate capability probe. Generated Confluence views render one current page per FP and one page per release increment.

## 6. Worked Example: Analytics Package Layout In Git

Recommended default for the topology proposal (gate 1.5 decides final placement; the internal layout below is designed to survive either topology choice). One capability = one folder; fixed file names per artifact type; all assembly is driven by naming, never by prose.

### 6.1 File tree

```text
team-specs/
  openspec/
    specs/                                      # Master Specs (accepted truth)
      transfers-by-phone/                       # capability, kebab-case English
        spec.md                                 # requirements + scenarios (RU prose, EN keywords/IDs)
        status-model.yaml                       # typed record: statuses + transitions
        channel-support.yaml                    # typed record: channel/capability matrix
        data-model.yaml                         # typed record: entities, attributes, masking
        platform-services.yaml                  # typed record: platform integration config
        screens.yaml                            # screen catalog: ID -> file, state, requirement refs
        assets/
          screens/
            SCR-TRANSFERS-001-amount-entry.png  # versioned UI screenshot
            SCR-TRANSFERS-002-refusal.png
        diagrams/
          order-flow.mmd                        # Mermaid source (sequence/state)
          order-flow.svg                        # export, same basename (generated)
          journey-map.drawio                    # heavy scheme source
          journey-map.svg                       # export, same basename
    changes/                                    # Delta Specs (change packages)
      CHANGE-2026-042-transfer-limits/          # matches validator ID pattern
        change.yaml
        proposal.md
        tasks.md
        design.md                               # full packages only
        specs/
          transfers-by-phone/
            spec.md                             # ADDED/MODIFIED requirement deltas only
            status-model.yaml                   # whole updated file when the model changes
        traceability.yaml
```

Rules that make this work:

- **Typed YAML artifacts are whole-file replacements, not deltas.** A change package carries the full updated `status-model.yaml`; the PR diff *is* the delta, and archive copies the file into the Master Spec folder. No merge logic, no partial-update ambiguity.
- **Diagram source and export share a basename** (`order-flow.mmd` + `order-flow.svg`). Markdown embeds only the export (renders in Bitbucket, Confluence, and editors); a future CI check regenerates or rejects stale exports. Mermaid-expressible diagrams should be generated from YAML where a typed source exists (status model -> state diagram) instead of hand-drawn.
- **Images are referenced only through stable IDs in `screens.yaml`**; markdown embeds use the catalog path. Renaming a file means updating one catalog row, and the link checker can verify every reference.

### 6.2 Naming and ID grammar

| Thing | Grammar | Example |
|---|---|---|
| Capability folder | kebab-case English | `transfers-by-phone` |
| Capability code (in IDs) | SCREAMING short English | `TRANSFERS` |
| Change package | `CHANGE-<YYYY>-<NNN>-<slug>` | `CHANGE-2026-042-transfer-limits` |
| Requirement | `REQ-<CAP>-<NNN>` in the heading, Russian title after it | `### Requirement: REQ-TRANSFERS-012 Лимиты перевода` |
| Scenario | `SCEN-<REQ number>-<NN>` in the heading | `#### Scenario: SCEN-TRANSFERS-012-01 Превышение лимита` |
| Screen asset | `SCR-<CAP>-<NNN>-<slug>.<ext>` | `SCR-TRANSFERS-002-refusal.png` |
| Status / system status | SCREAMING English enum values | `WAIT_CONFIRM`, `REFUSED_TIMEOUT` |
| Diagram files | `<slug>.<mmd\|drawio>` + `<slug>.svg` | `order-flow.mmd` / `order-flow.svg` |
| YAML artifact files | fixed names, one per type | `status-model.yaml`, never `statuses-v2.yaml` |

IDs are never translated, never renumbered, and never reused after deletion. Weak models get one grammar to follow and validators get one grammar to check.

### 6.3 Example content (mixed-language convention)

`spec.md` delta:

```markdown
## MODIFIED Requirements

### Requirement: REQ-TRANSFERS-012 Лимиты перевода по номеру телефона
Система SHALL отклонять перевод, если сумма превышает доступный лимит клиента,
и SHALL показывать клиенту причину отказа на экране [SCR-TRANSFERS-002].

#### Scenario: SCEN-TRANSFERS-012-01 Превышение лимита
- **WHEN** клиент вводит сумму перевода больше доступного лимита
- **THEN** система показывает экран отказа [SCR-TRANSFERS-002] с причиной отказа
  и не создаёт заявку

#### Scenario: SCEN-TRANSFERS-012-02 Лимит недоступен
- **WHEN** сервис лимитов не отвечает в течение таймаута
- **THEN** система предлагает повторить попытку и записывает событие в журнал
```

`status-model.yaml` (the 4.3.1 nested table, flattened):

```yaml
document_type: TransferByPhone
statuses:
  - id: SAVED
    client_label: "Заявка сохранена"
    client_visible: false
    description: >
      Заявка создана после успешных проверок на шаге выбора счёта списания.
    entry_action: "Клиент заполнил форму и нажал «Продолжить»"
    transitions:
      - condition: "Фрод-мониторинг вернул вердикт REVIEW"
        next_status: WAIT_CONFIRM
      - condition: "Проверки фрод-мониторинга завершены успешно"
        next_status: DISPATCHED
      - condition: "Подтверждение вернуло ошибку"
        next_status: REFUSED
        system_status: ERROR_CONFIRM
```

`screens.yaml` row:

```yaml
screens:
  - id: SCR-TRANSFERS-002
    file: assets/screens/SCR-TRANSFERS-002-refusal.png
    title: "Экран отказа в переводе"
    journey_step: refusal
    state: "лимит превышен"
    requirements: [REQ-TRANSFERS-012]
    source: "design mockup"
    last_verified: 2026-07-06
```

### 6.4 How documentation assembles from this

Deterministic assembly uses only fixed names and the ID grammar — no AI in the pipeline:

1. **Current FP analytics page** (accepted direction `D-029`): composes all capabilities owned by one FP, renders the typed models and assets, shows delivered state in the main body, lists active/approved-not-delivered changes separately, and links release history. It carries source commit, profile/renderer versions, generated timestamp, digest and a source warning.
2. **Release increment page**: reads a frozen release manifest plus included change packages, spec deltas, traceability, PR/CI evidence and waivers. It may aggregate changes from several FP without copying normative requirements or moving ownership. A separate generated page for every change is not required.
3. **Cross-references resolve by grammar**: `[SCR-TRANSFERS-002]` in prose links to the catalog entry; `REQ-`/`SCEN-` IDs anchor traceability rows, test cases, and generated-view anchors. A link checker can verify every bracket reference against the catalogs.
4. **Bitbucket remains readable without any tooling**: markdown renders, SVG exports render, YAML diffs review cleanly — an analyst or reviewer can always "пойти и разобраться" from the raw repository, which was the reason for the Russian-canon decision.

## 7. Open Questions Routed To Existing Gates

- Which template sections must appear in the generated approval view verbatim — depends on the approval requirements the owner is gathering (gate 1.7 input).
- Whether typed YAML artifacts enter the artifact-contract proposal as one follow-up change or an extension of `define-change-artifact-contracts` (decide at work item 1.4/1.9 planning; keep the proposal count from growing past the planned set).
- Diagram/asset storage conventions (already an open decision in the Phase 1 plan).
- How much of section 5 (architecture/API tables) is analyst-owned versus developer-owned in our process — affects who fills which artifact; route to the role-guide planning input.

## 8. Deferred Upstream Business-To-System Analysis Flow

Human direction on 2026-07-14 clarifies the future process before a specification becomes ready for implementation planning. This section is planning input only: it does not change the active Phase 2 scope, current validators, active OpenSpec changes, or the first transfer-ready release candidate. Phase 3 may observe and document the real corporate handoffs during the monitored pilot; if this flow is promoted into normative behavior or automation, its primary roadmap owner should be Phase 4 and it requires a dedicated reviewed OpenSpec change.

Update 2026-07-24: the agreed interaction design for the upstream AI-assisted
part is `docs/superpowers/specs/2026-07-24-ai-analyst-discovery-skill-design.md`.
The publication proposal `define-fp-analytics-publication-model` consumes only
its human-confirmed/reviewed canonical output. Interview summaries and
`proposed | unknown | conflict` assertions do not become delivered analytics
without the normal change, review and release path.

The intended end-to-end sequence is:

1. **Business-requirements intake:** preserve the received business requirements, source, accountable business/product owner, expected value, constraints, assumptions, and open questions. Received business requirements are input evidence, not a ready engineering specification.
2. **Business analysis — analyst-owned:** clarify ambiguity, reconcile stakeholders, define scope and exclusions, business rules, terminology, priorities, process or journey models, user stories or use cases, acceptance direction, and applicable diagrams or corporate-template sections. AI may draft structured artifacts, diagrams, user stories, scenarios, or populated template views, but the analyst reviews and corrects them and remains accountable for meaning and completeness. The analyst's non-template work includes elicitation, conflict resolution, domain judgment, prioritization, discovering missing cases, and recording human decisions; it must not be reduced to AI template filling.
3. **System analysis — system-analyst-owned:** translate the reviewed business analysis into affected-system boundaries, functional and non-functional requirements, interfaces, data and status models, error and degraded flows, dependencies, security and operational constraints, technical scenarios, and traceable acceptance criteria. The system analyst involves the Tech Lead, architecture, security, QA, or other owners where their authority applies and sends unresolved business gaps back to the analyst or product owner instead of guessing.
4. **Specification assembly and readiness:** assemble or refine the change package, including `proposal.md`, `design.md`, Delta Specs, draft task decomposition, and traceability. The package may be opened earlier as a working container, but its existence does not mean that the specification is ready. The specification becomes implementation-ready only after the required business and system analysis is complete, blocking questions are resolved or explicitly dispositioned, Spec Review and class-aware Definition of Ready pass, and the accountable humans approve the transition.
5. **Jira planning and task creation:** only an implementation-ready specification may be used to create or commit Jira implementation tasks. Jira tasks reference stable change, requirement, and scenario IDs; Jira remains the workflow/status system and does not become the source of requirement meaning. Draft decomposition may exist inside the change package before approval, but it must not be represented as approved Jira work. Manual task creation remains a valid fallback; automation is a later layer.

This direction is compatible with the existing documentation but was not previously stated as one explicit flow:

- section 4 already maps business requirements to `proposal.md` and user scenarios to Delta Spec scenarios;
- the accepted lifecycle already requires Spec Review, class-aware Definition of Ready, human approval, and source-linked traceability;
- current architecture already limits AI to proposal/draft work and keeps Jira as workflow/status rather than requirement truth;
- the missing part was an explicit business-analysis-to-system-analysis ownership and handoff model, including the rule that ready specs and committed Jira work come only after both analysis layers.

Future OpenSpec design must define the exact entry/exit evidence for both analysis stages, artifact ownership, rework loops, class-aware exceptions such as hotfix entry, and deterministic checks. It must include negative scenarios for AI-authored artifacts treated as approved, unresolved business ambiguity passed into system analysis, incomplete system analysis marked ready, and Jira tasks created from an unapproved specification.

```text
Idea: Make the upstream path explicit: business requirements -> analyst-owned business artifacts and judgment -> system analysis -> ready specification -> Jira implementation work.
Source: Human process clarification on 2026-07-14.
Type: scope_refinement, documentation_change
Decision: defer
Reason: The direction fills a real process gap, but implementing or normatively enforcing it would expand the active Phase 2 release-candidate scope and requires new artifact, handoff, readiness, and verification contracts.
Affected specs: None now; a future change will likely refine change-artifact-contracts, readiness-completion-gates, corporate-flow-controls, and traceability-contract.
Affected architecture: Adds an explicit upstream authoring and review flow before implementation-ready Delta Specs and Jira work while preserving Git/OpenSpec and Jira ownership boundaries.
Data contract impact: None now; future work must define business-analysis and system-analysis handoff evidence without creating a second requirement source.
Verification impact: Future positive and negative scenarios must prove role ownership, AI proposal-only behavior, handoff completeness, readiness gating, and rejection of premature Jira task creation.
Status: Recorded as deferred planning input; Phase 2 remains unchanged. Candidate primary roadmap owner is Phase 4 after Phase 3 pilot evidence.
```
