# Process Package And Synthetic Topology Setup

Status: work item 2.1 package setup plus active work item 2.2 configuration compatibility procedure. Independent review and coordinator reconciliation are still required before 2.2 closes.

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

Repository pointers use one shared local schema and may be synthetic `sibling:<id>`, configured `registry:<id>`, or portable relative `path:<relative>` references. The reusable schema validates scheme and path safety, not business semantics: legitimate IDs may contain words such as `product`, `prod`, `private`, or `internal`. Portable paths use forward-slash-separated segments and reject URLs, absolute roots/drives, backslashes, traversal or dot segments, trailing-dot/space segments, and Windows reserved device segments. Work item 2.2 implements the corresponding bounded discovery and precedence behavior.

The production validator now resolves those forms without environment, home-directory, network, or name guessing. `sibling:<id>` resolves beside the repository declaring the reference; `path:<relative>` stays inside that declaring repository after canonicalization; `registry:<id>` requires an explicit repeatable `--registry ID=PATH` argument. A central package location may also use one of these explicit schemes; the existing schema-compatible plain relative package location is resolved from the central repository and remains bounded to that declared location.

All committed templates use `sample-*` identities and synthetic relative references. The separate committed-asset scanner and its negative fixtures reject secret/private and production-looking values without making those substrings illegal in real configured IDs. Replace template values only in an authorized environment-specific configuration; never place credentials, private specifications, real owner identities, production URLs, or secret values in the reusable package or templates.

## Release Manifest Base Contract

The release-manifest schema and valid synthetic fixture represent the accepted transfer-evidence shape: versioned assets with SHA-256 checksums; typed Windows/Linux/macOS entries with version constraints and one-or-more architectures; Python/Node/Git/MCP/shell dependencies; exact PyYAML/jsonschema package pins from `requirements-test.txt`; normalized verification commands/evidence; versioned raw-artifact references; Qwen/DeepSeek certification references; limitations; and rollback reference. The sample host values, references, and hashes are schema fixtures, not release acceptance evidence. Manifest generation, checksum verification, host/package verification, certification execution, and release acceptance belong to later Phase 2 work items.

## Test The Skeleton

From the repository root:

```text
python -m pip install -r requirements-test.txt
python -m pytest tests/test_process_package.py -q
```

The package-skeleton test loads YAML, validates every document against local JSON Schemas, checks package/config/adapter version agreement, resolves package and canonical-source paths, checks shared repository-reference forms and project/owner/adapter integrity, verifies the release-manifest base contract, and scans bounded positive/negative privacy fixtures.

## Validate A Real Configuration

Run the non-mutating validator with an explicit start directory. Git determines the bounded repository root when available; otherwise the start directory itself is the root. Exactly one root config is allowed.

```text
python scripts/validate_process_config.py C:/work/team-specs
python scripts/validate_process_config.py C:/work/sample-app --json
python scripts/validate_process_config.py C:/work/sample-app --registry central=C:/work/team-specs --json
```

The validator discovers `sdd.config.yaml` for central mode or `.sdd-project.yaml` for adapter mode, then performs bounded UTF-8/duplicate-key-safe YAML loading, high-confidence inline-secret rejection, bundled JSON Schema checks, package/workflow/schema checks, exact config/package/adapter/`VERSION`/OpenSpec compatibility, registry and owner/project/adapter integrity, and only then `openspec --version`. Package schema traversal applies nested `$id` effective-base semantics before `$ref` and `$dynamicRef`: relative local bases may resolve only to files inside the package schema directory, while remote/network-backed effective targets are rejected. It never writes configuration or canonical artifacts.

Human mode writes stable error codes and remediation to stderr. `--json` writes exactly one JSON object to stdout with `schema_version`, `status`, `mode`, `diagnostics`, and `compatibility`. Diagnostics use safe logical source labels and JSON pointers; they do not echo secret values or unrestricted absolute paths.

Exit codes are `0` for valid configuration, `1` for invalid/unsafe/unsupported/incompatible input, `2` for CLI usage errors, and `3` for unavailable tooling or an unexpected validator failure. A missing registry mapping is validation error `1`; a missing OpenSpec executable is operational error `3`; an installed but non-pinned OpenSpec version is compatibility error `1`.

Focused work item 2.2 verification:

```text
python -m pytest tests/test_validate_process_config.py -q
```

Before integrating the work item, also run the complete command set recorded in `docs/phases/PHASE_2_EVIDENCE_INDEX.md`.
