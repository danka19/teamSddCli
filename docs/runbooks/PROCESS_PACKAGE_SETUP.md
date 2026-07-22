# Process Package And Synthetic Topology Setup

Status: Phase 2 work items 2.1-2.13 and gates 2.14.1-2.14.4 are closed; `D-020` accepts immutable rc6 package `0.3.0` as the external transfer baseline. The current source package is `0.3.4` for in-progress P3 work and is not thereby a newly accepted transfer candidate. Rc4 is historical and rc5 is diagnostic rejected history.

## Contract Sources

- Accepted topology and configuration behavior: `openspec/specs/repo-topology-config/spec.md`.
- Proposed transfer-package boundary: `openspec/changes/define-transfer-ready-process-package/specs/transfer-readiness/spec.md`.
- Proposed class/policy boundary: `openspec/changes/adopt-nis-corporate-process-governance/` tasks 1.1-1.4 and its capability deltas.
- Documentation and scenario-first verification rules: `openspec/specs/documentation-governance/spec.md`.

This runbook does not restate those normative requirements.

## Initial Identifiers

- Process package ID: `sdd-process`.
- Process package version: `0.3.0`.
- Configuration and project-adapter schema contract version: `1.1`.
- Change metadata schema version: integer `2`.
- Policy document schema version: `1.0`.
- Policy-set ID/version: `sdd-core` / `1.0.0`.
- JSON Schema draft: Draft 2020-12.
- OpenSpec CLI pin: `1.4.1`.
- Supported first topology: `central-team-specs`.

These identifiers move atomically. A mixed `0.2.0`/`0.3.0` package, `1.0`/`1.1` config, adapter, or policy-set pin is incompatible rather than silently upgraded. Version `0.3.0` adds deterministic Delta semantics, guarded archive history, and mandatory reviewed upgrade evidence; historical `0.2.0` candidates and evidence remain immutable.

## Reference Layout

The reusable package lives under `process/`. The synthetic `templates/team-specs/` topology points to that package through `sdd.config.yaml`; it does not copy package schemas or workflow rules. The optional `templates/project-adapter/.sdd-project.yaml` identifies the registered synthetic project and consumed package version.

Work item 2.8 fills the workflow `artifact_dependencies` graph with the packaged change, classification, Spec PR preparation, readiness, control, release, traceability, and archive-preparation evidence chain. The graph declares dependencies only; classification thresholds, gate obligations, authority, and lifecycle rules remain in the pinned policies and canonical OpenSpec sources. Current template/bootstrap/create/update/rollback and AI-disabled fallback procedures are in `docs/runbooks/PACKAGED_GOVERNED_FLOW.md`.

Repository pointers use one shared local schema and may be synthetic `sibling:<id>`, configured `registry:<id>`, or portable relative `path:<relative>` references. The reusable schema validates scheme and path safety, not business semantics: legitimate IDs may contain words such as `product`, `prod`, `private`, or `internal`. Portable paths use forward-slash-separated segments and reject URLs, absolute roots/drives, backslashes, traversal or dot segments, trailing-dot/space segments, and Windows reserved device segments. Work item 2.2 implements the corresponding bounded discovery and precedence behavior.

The production validator now resolves those forms without environment, home-directory, network, or name guessing. `sibling:<id>` resolves beside the repository declaring the reference; `path:<relative>` stays inside that declaring repository after canonicalization; `registry:<id>` requires an explicit repeatable `--registry ID=PATH` argument. A central package location may also use one of these explicit schemes; the existing schema-compatible plain relative package location is resolved from the central repository and remains bounded to that declared location.

The package also pins one local `process/policies/manifest.yaml`. The validator loads the nine policy documents named there, checks local paths and schema/version agreement, unique IDs, references, acyclic requirements, required corporate values, and bounded overrides. `locked` values cannot be replaced, `additive` values cannot lose bundled minimums, and `stricter_only` values must be safely comparable and no weaker. Diagnostics retain the logical source and JSON pointer. Project adapters may provide only bounded overrides and cannot select alternate policy paths. Work item 2.4 consumes the immutable resolved snapshot for classification; work item 2.5 consumes it for read-only artifact/gate reports and lifecycle-transition decisions; work item 2.6 consumes the same snapshot and digest for non-mutating Tech Lead review and control-state checks; work item 2.7 binds corporate-flow envelopes, regression, release handoff, pilot safety, and failed-run retry evidence to that snapshot through `check_corporate_flow.py`.

The schema-v2 contract records `minor | major | hotfix` separately from work type and lifecycle status, retains source-linked `true | false | unknown` evidence, audited human corrections, and human decision ownership, and rejects legacy authoring fields in v2 documents. The target package template lives at `process/templates/change/`. The existing root `templates/change/` remains a historical Phase 1 compatibility surface; its implementation is packaged at `process/validators/legacy_change.py` and exposed by the thin `scripts/validate_change.py` wrapper. Bounded legacy check/apply behavior and its no-archive-rewrite boundary are documented in `docs/runbooks/CLASSIFICATION_AND_MIGRATION.md`.

All committed templates use `sample-*` identities and synthetic relative references. The separate committed-asset scanner and its negative fixtures reject secret/private and production-looking values without making those substrings illegal in real configured IDs. Replace template values only in an authorized environment-specific configuration; never place credentials, private specifications, real owner identities, production URLs, or secret values in the reusable package or templates.

## Release Manifest And Host Evidence Contract

The release-manifest schema, generator, semantic validator, rehearsal command, and acceptance command are implemented. The immutable candidate records versioned assets with SHA-256 checksums; Windows full-rehearsal and Linux/WSL2 portability-smoke host requirements; Python/Node/Git/MCP/shell dependencies; exact PyYAML/jsonschema pins from `requirements-test.txt`; normalized verification commands/evidence; versioned raw-artifact references; Qwen/DeepSeek certification references; limitations; and rollback reference. macOS is explicitly not certified under `D-018`; it is a limitation, not a third acceptance host. The valid synthetic fixture remains schema-only evidence, while dated release manifest and host-evidence files under `process/release/` record the observed candidate. An `evidence-complete` machine result never substitutes for the separate final human acceptance decision.

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

The validator discovers `sdd.config.yaml` for central mode or `.sdd-project.yaml` for adapter mode, then performs bounded UTF-8/duplicate-key-safe YAML loading, high-confidence inline-secret rejection, bundled JSON Schema checks, package/workflow/schema/policy checks, exact config/package/adapter/policy-set/`VERSION`/OpenSpec compatibility, registry and owner/project/adapter integrity, and only then `openspec --version`. Package schema traversal applies nested `$id` effective-base semantics before `$ref` and `$dynamicRef`: relative local bases may resolve only to files inside the package schema directory, while remote/network-backed effective targets are rejected. It never writes configuration or canonical artifacts.

Human mode writes stable error codes and remediation to stderr. `--json` writes exactly one JSON object to stdout with `schema_version`, `status`, `mode`, `diagnostics`, and `compatibility`. Diagnostics use safe logical source labels and JSON pointers; they do not echo secret values or unrestricted absolute paths.

Exit codes are `0` for valid configuration, `1` for invalid/unsafe/unsupported/incompatible input, `2` for CLI usage errors, and `3` for unavailable tooling or an unexpected validator failure. A missing registry mapping is validation error `1`; a missing OpenSpec executable is operational error `3`; an installed but non-pinned OpenSpec version is compatibility error `1`.

Focused work item 2.2 verification:

```text
python -m pytest tests/test_validate_process_config.py -q
```

Focused work item 2.3 verification:

```text
python -m pytest tests/test_policy_schema_v2.py -q
```

Focused work item 2.4 verification:

```text
python -m pytest tests/test_classification.py tests/test_classification_migration.py -q
```

Focused work item 2.5 verification:

```text
python -m pytest tests/test_artifact_gates.py tests/test_lifecycle_gates.py tests/test_gate_cli.py tests/test_policy_schema_v2.py -q
```

The gate input is a separate versioned operational record validated by `process/schemas/gate-evaluation-input.schema.json`; it does not add unreviewed free-form fields to canonical `change-v2`. Operator commands and exit semantics are documented in `docs/runbooks/ARTIFACT_AND_LIFECYCLE_GATES.md`.

Tech Lead governance uses separate `tech-lead-review-input` and `tech-lead-control-record` v1.0 schemas plus the explicit `owners` v2.0 contract. The legacy owners v1.0 contract remains accepted for work items 2.1-2.5 but cannot silently become governance-ready. See `docs/runbooks/TECH_LEAD_GOVERNANCE.md`.

Before integrating the work item, also run the complete command set recorded in `docs/phases/PHASE_2_EVIDENCE_INDEX.md`.

## Platform Installation And Inventory

Install only pinned test dependencies and the pinned OpenSpec CLI. Inventory
commands are informational inputs to rehearsal; they do not authorize a
workaround for incompatible versions.

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-test.txt
npm install --global @fission-ai/openspec@1.4.1
python --version
node --version
openspec --version
git --version
```

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-test.txt
npm install --global @fission-ai/openspec@1.4.1
python3 --version
node --version
openspec --version
git --version
```

Keep secret values in the approved local secret store. Configuration contains
only a non-secret reference such as `approved-secret:team-sdd-mcp`; do not put
the resolved value in YAML, evidence, command arguments, or the release asset.
Configure the approved MCP/adapter outside the reusable package, record either
`provisioned` plus its approved reference or `explicitly-unavailable`, and use
the deterministic AI-disabled fallback when unavailable.

Reusable defects found during setup must be reported against the external
canonical repository with candidate payload digest, package/config versions,
diagnostic code, and sanitized reproduction. Do not patch the corporate copy
or create an internal process fork.

## Управляемые GigaCode-шаблоны

Package версии `0.3.4` содержит канонические шаблоны `.gigacode/AGENTS.md` и
`.gigacode/skills/sdd-process-companion.md`; bootstrap устанавливает их в новый workspace.
Перед update детерминированная проверка сравнивает только эти declared files: локальное отличие
блокирует update с `gigacode-managed-file-conflict` и точным путём, а остальные `.gigacode`-файлы
не затрагиваются. Это сохраняет единый reusable source без перезаписи локальной работы.