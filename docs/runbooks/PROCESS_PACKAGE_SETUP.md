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

Repository pointers use one shared local schema and may be synthetic `sibling:<id>`, configured `registry:<id>`, or safe relative `path:<relative>` references. URLs, absolute paths, parent traversal, and secret/private/production-looking values are rejected by the schema; discovery and precedence remain work item 2.2.

All committed values use `sample-*` identities and synthetic relative references. Replace them only in an authorized environment-specific configuration. Never place credentials, private specifications, real owner identities, production URLs, or secret values in the reusable package or templates.

## Release Manifest Base Contract

The release-manifest schema and valid synthetic fixture represent the accepted transfer-evidence shape: versioned assets with SHA-256 checksums, Windows/Linux/macOS compatibility assumptions and runtime dependencies, normalized verification commands/evidence, versioned raw-artifact references, Qwen/DeepSeek certification references, limitations, and rollback reference. The sample references and hashes are schema fixtures, not release acceptance evidence. Manifest generation, checksum verification, certification execution, and release acceptance belong to later Phase 2 work items.

## Test The Skeleton

From the repository root:

```text
python -m pip install -r requirements-test.txt
python -m pytest tests/test_process_package.py -q
```

The focused test loads YAML, validates every document against local JSON Schemas, checks package/config/adapter version agreement, resolves package and canonical-source paths, checks shared repository-reference forms and project/owner/adapter integrity, verifies the release-manifest base contract, and scans bounded positive/negative privacy fixtures. It is test evidence only: there is intentionally no production config-discovery or release-acceptance command in work item 2.1.

Before integrating the work item, also run the complete command set recorded in `docs/phases/PHASE_2_EVIDENCE_INDEX.md`.
