## 1. Contract and acceptance baseline

- [ ] 1.1 Review the proposal, design and all four delta specs with the human owner and record acceptance, corrections and unresolved questions without starting implementation.
- [ ] 1.2 Select one sanitized standalone-FP example and one sanitized two-FP release example that contain no corporate identifiers, credentials, screenshots or private requirement text.
- [ ] 1.3 Create an exact scenario-to-test matrix for every requirement/scenario in this change, including negative, AI-disabled, cross-FP, reconciliation and publication-failure paths.
- [ ] 1.4 Confirm the primary P5 execution boundary and record which corporate capability-probe inputs must be collected during P4 without implementing or invoking Confluence.
- [ ] 1.5 Review the agreed AI Analyst Discovery Skill design, assign ownership of its versioned output contract to a separate/explicit change, and freeze the publication-side interface without duplicating interview behavior in this change.

## 2. FP namespace and central topology

- [ ] 2.1 Write failing tests for FP catalog identity, owner mapping, FP/project many-to-many relations, duplicate IDs, dangling project IDs and ambiguous ownership.
- [ ] 2.2 Define versioned closed schemas and templates for `fp-catalog.yaml` and `fp.yaml`, including owners, participating projects, related FP and canonical analytics/OpenSpec references.
- [ ] 2.3 Implement deterministic FP/project registry loading and cross-reference validation with redacted stable diagnostics.
- [ ] 2.4 Define and validate the supported OpenSpec capability naming/mapping strategy after probing the pinned OpenSpec CLI for FP-scoped layout compatibility.
- [ ] 2.5 Add a human-readable `fps/<fp-id>/README.md` and analytics index template that explains the FP, its sources, capabilities, projects, releases and navigation.
- [ ] 2.6 Verify the standalone and shared-project fixtures work from the supported central topology without assuming `1 repo = 1 FP`.

## 3. Complete analytics source contracts

- [ ] 3.1 Write failing schema and semantic tests for the expanded analytics manifest identity, source inventory, applicability records and stable cross-references.
- [ ] 3.2 Expand status-model records to cover descriptions, client visibility, entry actions, conditional transitions, next/system statuses and requirement/scenario references.
- [ ] 3.3 Expand channel-support and data-model records to cover capability/operation matrices and master/storage/cache/masking/export attributes from the audited template.
- [ ] 3.4 Define closed schemas/templates for contacts, components/deployment, provided/consumed API catalog, security, performance/load, rollout/toggles and checklist/evidence records.
- [ ] 3.5 Replace the generic platform-services record with a versioned discriminated union for parameter store, logging, audit, monitoring, authorization, toggler, profile, confirmation, content, scheduler, secret-store and approved extension kinds.
- [ ] 3.6 Define provenance/draft metadata for AI-authored or migrated records and fail-closed human decision fields for ownership, applicability, approval and evidence.
- [ ] 3.7 Build one complete sanitized FP analytics package and prove every typed source validates with AI disabled.
- [ ] 3.8 Define or consume the versioned analyst-discovery assertion-evidence contract, keeping interaction discovery-map state separate from `confirmed | proposed | unknown | conflict` assertion truth.

## 4. Release and publication manifests

- [ ] 4.1 Write failing tests for release identity, lifecycle, owner/affected FP, included changes, source revisions, evidence, duplicate IDs and illegal state combinations.
- [ ] 4.2 Define the closed `release.yaml` schema/template with draft/candidate/published/delivered/cancelled states and explicit inclusion/dependency/reconciliation records.
- [ ] 4.3 Write failing tests that reject silent edits to a published release digest and accept a complete correction chain.
- [ ] 4.4 Define versioned publication-profile and publication-document schemas for `fp-current` and `release-increment`, including section ordering, source selectors, applicability, renderer IDs, target mapping references and digests.
- [ ] 4.5 Define local-only/corporate target mapping boundaries so space/page IDs and credentials never enter the reusable package or synthetic fixtures.
- [ ] 4.6 Validate one single-FP and one multi-FP release manifest and their two publication document types without network access.

## 5. Semantic validation and traceability

- [ ] 5.1 Write failing tests for missing owning FP, dangling capability/requirement/scenario IDs, ownership transfer, duplicate normative text and unresolved cross-FP dependency.
- [ ] 5.2 Implement release composition validation that preserves owning FP and links affected FP without copying normative requirements.
- [ ] 5.3 Write failing applicability tests for required, conditional, optional and human-approved `not_applicable`, including unapproved AI proposals.
- [ ] 5.4 Implement section completeness and applicability evaluation with section ID, expected source, owner and evidence diagnostics.
- [ ] 5.5 Write failing tests that prevent approved-not-delivered behavior from entering the delivered current-page body.
- [ ] 5.6 Implement current-baseline selection, active/approved-not-delivered blocks and last-delivered-release resolution.
- [ ] 5.7 Implement cross-FP release reconciliation checks that require a page/document/source digest or an explicit gap for every affected FP.
- [ ] 5.8 Add privacy/secret/reference checks for manifests, analytics sources, logs and bounded AI read packs.
- [ ] 5.9 Write negative tests that reject discovery summaries, partial drafts and `proposed | unknown | conflict` assertions from delivered/current truth while preserving them as source-linked WIP gaps or risks.

## 6. Normalized publication model

- [ ] 6.1 Define a renderer-independent publication-model schema for sections, blocks, tables, nested rows, anchors, links, warnings, source refs and evidence-backed statuses.
- [ ] 6.2 Write golden composition fixtures for the full `fp-current` page, including all twelve design sections, explicit `not_applicable` and work-in-progress blocks.
- [ ] 6.3 Implement deterministic `fp-current` composition from Markdown, OpenSpec, typed YAML, assets, releases and evidence.
- [ ] 6.4 Write golden composition fixtures for standalone and cross-FP `release-increment` pages, including delta, dependencies, evidence and reconciliation.
- [ ] 6.5 Implement deterministic `release-increment` composition from frozen release manifests and canonical change/spec references.
- [ ] 6.6 Implement stable ordering, anchors, source metadata, profile/renderer versions and content digest generation.
- [ ] 6.7 Prove the same validated sources always produce the same normalized publication model and digest.
- [ ] 6.8 Add publication-model blocks for discovery provenance, open assertion owners and conflicts without treating interview evidence as normative requirements.

## 7. Nested renderers and local preview

- [ ] 7.1 Write golden tests for status transitions, channel matrices, data/API wide tables, audit attributes, metrics, roles/privileges and parameter-store configurations.
- [ ] 7.2 Implement a typed renderer registry keyed by source type/schema and renderer version rather than one generic nested-table formatter.
- [ ] 7.3 Implement lossless nested/expand output, stable anchors, deterministic row order, empty/not-applicable display and declared wide-table fallback.
- [ ] 7.4 Write negative tests that reject unsupported mandatory renderer/macro combinations instead of dropping inner content.
- [ ] 7.5 Extend the local read-only preview to render complete current/release pages from the normalized publication model with no credentials, network action or external mutation.
- [ ] 7.6 Add snapshot-drift review output that identifies changed section/renderer/source IDs.
- [ ] 7.7 Run the complete standalone-FP and cross-FP preview walkthrough with AI disabled and record exact output digests.
- [ ] 7.8 Run the agreed analyst-discovery walkthrough from one vague sentence through human-confirmed summary and draft package, then prove publication remains unchanged until separate guided-change, review and delivery evidence exist.

## 8. Corporate Confluence capability probe and adapter decision

- [ ] 8.1 Prepare a non-mutating corporate capability-probe checklist for permitted adapters, authentication boundary, page hierarchy, permissions, nested/expand macros, assets, size limits, version history, rollback and comments.
- [ ] 8.2 Execute the capability probe only in the approved corporate environment and record non-secret evidence without publishing canonical content.
- [ ] 8.3 Select the permitted Confluence publication path through an explicit human decision and record unsupported features and required profile fallbacks.
- [ ] 8.4 Define dry-run create/update/no-op action plans, idempotency keys, retry behavior, redacted logs and rollback/hold behavior before any mutating adapter is implemented.
- [ ] 8.5 Write adapter contract tests for current-page update, unique release-page creation, duplicate prevention, correction revision, unavailable service and partial failure.
- [ ] 8.6 Implement the narrow adapter only after explicit scope approval; keep validation/publication-model/local-preview layers usable when the adapter is absent.

## 9. Pilot migration and reconciliation

- [ ] 9.1 Select one bounded pilot FP and one representative release increment with named owners, privacy boundary and acceptance evidence.
- [ ] 9.2 Inventory its legacy analytics as read-only input and record source provenance, duplicates, contradictions, unknowns and gaps.
- [ ] 9.3 Migrate the pilot FP incrementally into Markdown/OpenSpec/typed sources without inventing missing values or bulk-editing the legacy Confluence page.
- [ ] 9.4 Generate and human-review the pilot current-page preview and one release-increment preview, including every applicable audited template section.
- [ ] 9.5 Publish only after explicit human approval and verify stable identity, page hierarchy, navigation, permissions, nested content, source warning and rollback.
- [ ] 9.6 Record delivery and reconciliation for every affected FP, retaining an explicit gap when a current page cannot yet be updated.
- [ ] 9.7 Run feedback disposition, regeneration and correction-chain walkthroughs and preserve failed-run evidence.

## 10. Documentation, governance and acceptance

- [ ] 10.1 Update analyst, Tech Lead, developer, QA and release-owner runbooks with situation-based authoring, review, release composition, reconciliation and AI boundaries.
- [ ] 10.2 Update the product FAQ with where to find current FP analytics, how to read release increments, how cross-FP ownership works and how to request a source correction.
- [ ] 10.3 Add human-readable templates and one sanitized worked example that cover the entire current/release workflow without requiring readers to inspect raw schemas first.
- [ ] 10.4 Run focused tests, complete suite, `openspec validate --all --strict`, roadmap/OpenSpec validation, documentation drift checks and `git diff --check`.
- [ ] 10.5 Produce a dated acceptance audit with scenario/evidence mapping, corporate manual checks, privacy result, known gaps, rollback and residual risks.
- [ ] 10.6 Stop for human acceptance before syncing delta specs, archiving the change, enabling publication for additional FP or treating the model as production-ready.
- [ ] 10.7 Update the analyst-discovery and publication runbooks together so a colleague can see where interview output stops, where canonical change work begins, and when current/release pages may change.
