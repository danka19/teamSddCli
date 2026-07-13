## 1. Process Package And Configuration Foundation

- [ ] 1.1 Create the versioned `process/` package skeleton, metadata, workflow contract, and synthetic `team-specs` bootstrap template using the accepted central topology.
- [ ] 1.2 Add schemas and representative fixtures for `sdd.config.yaml`, `projects.yaml`, `owners.yaml`, optional `.sdd-project.yaml`, process-package metadata, and release manifest.
- [ ] 1.3 Implement deterministic configuration discovery, schema validation, OpenSpec `1.4.1` pin checking, process-package compatibility checking, and secret/private-value rejection with focused negative tests.

## 2. Deterministic Thin-Flow Package

- [ ] 2.1 Move the existing change template and validator into the versioned process package while preserving backward-compatible repository entry points and all accepted validator behavior.
- [ ] 2.2 Add non-interactive bootstrap and change-creation entry points that copy only versioned templates, reject unsupported topology or destination state, and produce machine-readable evidence.
- [ ] 2.3 Add Spec PR preparation and archive-support entry points that collect deterministic evidence without approving, merging, or archiving on behalf of a human.
- [ ] 2.4 Add update, compatibility-check, and rollback entry points that preserve accepted OpenSpec history and restore the previously pinned package/config version on failure.
- [ ] 2.5 Prove the packaged reference thin flow with focused positive and negative tests plus an AI-disabled walkthrough fixture.

## 3. Weak-Model Operating Kit

- [ ] 3.1 Define the tool-agnostic task-launch contract, authority-labelled read-pack schema, operation evidence schema, and explicit blocked/missing-context behavior.
- [ ] 3.2 Implement deterministic read-pack assembly from configured canonical sources, including source authority, stable paths or IDs, known traps, and unresolved inputs.
- [ ] 3.3 Create bounded analyst, developer, and QA thin-change role instructions with numbered steps, one-stage outputs, self-review, negative examples, and human stop points.
- [ ] 3.4 Add thin adapter templates for Qwen/DeepSeek/GigaCode-class CLIs that package the selected instruction and read pack without owning process rules.
- [ ] 3.5 Add deterministic checks that reject unsupported completion claims, AI-owned approvals or lifecycle transitions, missing evidence boundaries, and derived artifacts that lack canonical source references.

## 4. Certification Fixtures And Evidence

- [ ] 4.1 Create synthetic reference repositories, canonical change/spec inputs, expected role outputs, and deterministic golden validation results without corporate or private data.
- [ ] 4.2 Add negative certification cases for missing context, conflicting sources, fabricated evidence, forbidden approval, skipped stop point, invalid lifecycle transition, adapter failure, and context-limit failure.
- [ ] 4.3 Implement a certification runner and evidence record that captures model/runtime identifier, adapter version, process-package version, read-pack identity, validation result, human intervention, forbidden-action result, and limitations.
- [ ] 4.4 Execute and record AI-disabled certification for every gated thin-flow operation.
- [ ] 4.5 Execute and record actual Qwen/DeepSeek-class certification for analyst, developer, and QA workflows; route unreliable operations to deterministic or mandatory-human fallbacks.

## 5. Release Candidate And Transfer Runbook

- [ ] 5.1 Implement deterministic release-manifest generation and validation for package/config/OpenSpec versions, included assets, compatibility assumptions, evidence references, known limitations, and rollback reference.
- [ ] 5.2 Add clean-bootstrap and release-candidate acceptance automation that fails on missing, stale, failed, private, or AI-only evidence.
- [ ] 5.3 Write installation, compatibility inventory, approved secret setup, integration-adapter configuration, update, rollback, and no-fork feedback procedures.
- [ ] 5.4 Produce a transfer rehearsal from a clean supported environment and record the accepted external release-candidate evidence.

## 6. Corporate Adaptation And Pilot Package

- [ ] 6.1 Create a non-secret corporate environment inventory template covering runtimes, OpenSpec, Git, package distribution, network policy, Bitbucket/Jenkins/Jira/Confluence capabilities, MCP policy, and available AI CLI/model adapters.
- [ ] 6.2 Create real-configuration and pilot-entry checklists that verify installed package, project and owner mappings, approved secret references, integration wiring, rollback path, and AI-disabled gates.
- [ ] 6.3 Create a monitored thin-change pilot evidence template covering change/requirement/scenario IDs, PR and test evidence, human decisions, adapter/runtime versions, interventions, deviations, rollback or hold, and follow-up changes.
- [ ] 6.4 Verify that reusable corporate findings are routed through the external OpenSpec/change workflow and that internal package forks are detected or explicitly rejected.

## 7. Documentation, Review, And Acceptance

- [ ] 7.1 Update repository structure, setup, operations, context, roadmap, audit, and role-facing documentation to reference canonical OpenSpec requirements without duplicating normative text.
- [ ] 7.2 Run focused tests, full tests, template/config/package validation, AI-disabled certification, actual weak-model certification, `openspec list`, `openspec list --specs`, `openspec validate --all --strict`, and `git diff --check`.
- [ ] 7.3 Complete worker, reviewer, architecture-checker, and verification-checker gates for each Phase 2 work item when execution tooling is available, or record the local fallback and limitation.
- [ ] 7.4 Stop for human acceptance of the external release candidate before any corporate pilot starts.
- [ ] 7.5 After successful corporate adaptation and pilot evidence, stop for human acceptance before promoting or archiving the new OpenSpec capabilities.
