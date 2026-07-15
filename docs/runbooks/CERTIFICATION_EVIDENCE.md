# Deterministic Certification Evidence

## Purpose And Boundary

`scripts/certify_process_release.py` runs the versioned synthetic case catalog and builds exact requirement/scenario coverage inventory. This is fixture certification only: normalized evidence always states `evidence_kind: deterministic-fixture`, `actual_model_run: false`, and structured model/adapter fields with `not-executed` values. It is not Qwen/DeepSeek evidence, cross-platform evidence, release acceptance, or pilot evidence. The closed evidence schema can represent later actual-model records, but this runner cannot produce one.

The runner is check-only with `--check`. Without `--check`, a passing run creates one new raw bundle directory outside the repository. It never overwrites a bundle, writes to a symlink/reparse destination, or allows source/output overlap.

## Commands

From any working directory:

```powershell
python <repository>/scripts/certify_process_release.py `
  --root <repository> `
  --raw-output <external-artifact-root>/raw-artifact-v0.2.0 `
  --check
```

Remove `--check` only when intentionally creating the immutable raw artifact. Exit `0` means every case matched its golden semantic result and coverage inventory was valid. Exit `1` means a golden mismatch. Exit `3` means unsafe input/output, privacy failure, unknown selector/evidence, invalid coverage gap, or another contract error.

## Execution Safety

- External dispatch is an allowlist in `process/certification.py`; command vectors use `sys.executable`, argument lists, `shell=False`, repository-root working directory, and a timeout.
- YAML cannot supply an executable or arbitrary arguments. Certification-specific negative families use internal preflight signals and do not execute commands.
- Fixture paths must be repository-relative under `process/certification/`; absolute, traversal, credential-like, URL, and production-looking values fail closed.
- Fixture payloads use the explicit `synthetic | example` namespace allowlist. Email, IP, URL, corporate/internal/production identifiers, and secret-like content fail before dispatch. Canonical OpenSpec paths remain trusted source metadata and may contain domain words without becoming fixture values.
- Canonical files are never mutation targets. Every case records before/after SHA-256 snapshots across process, OpenSpec, templates, scripts, and docs; `canonical_mutated` is derived from those snapshots.

## Evidence Storage

Git stores the case catalog, golden expectations, coverage inventory, schemas, normalized semantic fields, and SHA-256 reference. The raw `bundle.json` contains captured validator streams and belongs only in the immutable versioned release artifact outside Git. Normalized evidence deliberately contains no raw stdout/stderr.

The raw artifact reference contains:

- logical artifact version (normally `raw-artifact-<process-version>`);
- filename;
- SHA-256 calculated over deterministic bundle bytes;
- `stored_in_git: false`.

## Coverage And Residual Gaps

`process/certification/coverage.yaml` composes all accepted capability specs and both active delta trees by exact capability, requirement, and scenario headings. `MODIFIED` replaces the accepted requirement scenarios and `REMOVED` removes them; duplicate change ownership and unknown targets fail closed. `evidence-manifest.yaml` contains one explicit row per applicable effective selector. `tests/certification-evidence-bindings.yaml` independently binds that selector and binding ID to exact pytest node(s), certification cases, or manual evidence. Bare pytest-file references, unrelated existing-node substitution, missing rows, and binding disagreement fail closed.

There is no aggregate default evidence. An allowed residual gap contains all five non-empty fields: `owner`, `risk`, `reason`, `compensation`, and `follow_up`, wins over any capability rule, increments the gap count, and makes report status `gaps`. Structured future-work selectors remove unperformed 2.11-2.14 scenarios from covered/gap rows and count them separately.

The CLI exposes one canonical JSON representation only; it does not maintain a second human-output projection. Operators may format that JSON externally without changing semantic fields.

The eight NIS feedback/publication-boundary scenarios use `process/feedback_policy.py` and exact nodes in `tests/test_feedback_policy.py`. This pure check validates SLA configuration/defaults, comment dispositions/follow-up, no fabricated core-route evidence, future class-aware ownership, read-only legacy input, and corporate generated-view selection. It does not call Confluence or publish anything.

Concrete analyst/minor, developer/major, QA/hotfix, and Tech Lead/major expected-output goldens live under `process/certification/expected-role-outputs/`. The catalog binds each by path and SHA-256; schema and semantic role/class checks run before certification. All remain `executed: false`.

## Manual Review

1. Run `--check` twice and compare JSON semantics.
2. Confirm no raw directory was created.
3. Run without `--check` against a new external destination.
4. Recalculate SHA-256 for `bundle.json` and compare it with normalized evidence.
5. Confirm normalized evidence says no actual model run occurred and contains no captured streams.
6. Preserve the raw artifact immutable; a repeated create attempt must fail rather than overwrite it.
