# Process Package And Synthetic Topology Setup

Status: initial work item 2.1 setup note. Production configuration discovery and compatibility diagnostics belong to work item 2.2.

## Contract Sources

- Accepted topology and configuration behavior: `openspec/specs/repo-topology-config/spec.md`.
- Proposed transfer-package boundary: `openspec/changes/define-transfer-ready-process-package/specs/transfer-readiness/spec.md`.
- Documentation and scenario-first verification rules: `openspec/specs/documentation-governance/spec.md`.

This runbook does not restate those normative requirements.

## Initial Identifiers

- Process package ID: `sdd-process`.
- Process package version: `0.1.0`.
- Configuration/schema contract version: `1.0`.
- JSON Schema draft: Draft 2020-12.
- OpenSpec CLI pin: `1.4.1`.
- Supported first topology: `central-team-specs`.

These identifiers are deliberately small and reversible. Later compatibility or release behavior must change them through the active OpenSpec workflow instead of editing copied package rules.

## Reference Layout

The reusable package lives under `process/`. The synthetic `templates/team-specs/` topology points to that package through `sdd.config.yaml`; it does not copy package schemas or workflow rules. The optional `templates/project-adapter/.sdd-project.yaml` identifies the registered synthetic project and consumed package version.

The initial workflow contract intentionally contains an empty `artifact_dependencies` collection. It defines the reusable `id`/`requires` shape without choosing classes, gates, lifecycle stages, or a concrete artifact sequence before the packaged governed flow is implemented in work item 2.8.

Repository pointers use one shared local schema and may be synthetic `sibling:<id>`, configured `registry:<id>`, or portable relative `path:<relative>` references. The reusable schema validates scheme and path safety, not business semantics: legitimate IDs may contain words such as `product`, `prod`, `private`, or `internal`. Portable paths use forward-slash-separated segments and reject URLs, absolute roots/drives, backslashes, traversal or dot segments, trailing-dot/space segments, and Windows reserved device segments. Discovery and precedence remain work item 2.2.

All committed templates use `sample-*` identities and synthetic relative references. The separate committed-asset scanner and its negative fixtures reject secret/private and production-looking values without making those substrings illegal in real configured IDs. Replace template values only in an authorized environment-specific configuration; never place credentials, private specifications, real owner identities, production URLs, or secret values in the reusable package or templates.

## Release Manifest Base Contract

The release-manifest schema and valid synthetic fixture represent the accepted transfer-evidence shape: versioned assets with SHA-256 checksums; typed Windows/Linux/macOS entries with version constraints and one-or-more architectures; Python/Node/Git/MCP/shell dependencies; exact PyYAML/jsonschema package pins from `requirements-test.txt`; normalized verification commands/evidence; versioned raw-artifact references; Qwen/DeepSeek certification references; limitations; and rollback reference. The sample host values, references, and hashes are schema fixtures, not release acceptance evidence. Manifest generation, checksum verification, host/package verification, certification execution, and release acceptance belong to later Phase 2 work items.

## Test The Skeleton

From the repository root:

```text
python -m pip install -r requirements-test.txt
python -m pytest tests/test_process_package.py -q
```

The focused test loads YAML, validates every document against local JSON Schemas, checks package/config/adapter version agreement, resolves package and canonical-source paths, checks shared repository-reference forms and project/owner/adapter integrity, verifies the release-manifest base contract, and scans bounded positive/negative privacy fixtures. It is test evidence only: there is intentionally no production config-discovery or release-acceptance command in work item 2.1.

Before integrating the work item, also run the complete command set recorded in `docs/phases/PHASE_2_EVIDENCE_INDEX.md`.
