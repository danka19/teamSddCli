# Deterministic Certification Evidence

## Purpose And Boundary

`scripts/certify_process_release.py` runs the versioned synthetic case catalog and builds exact requirement/scenario coverage inventory. This is fixture certification only: normalized evidence always states `evidence_kind: deterministic-fixture`, `actual_model_run: false`, and `model`/`runtime: not-executed`. It is not Qwen/DeepSeek evidence, cross-platform evidence, release acceptance, or pilot evidence.

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
- Canonical files are never mutation targets. Every normalized case records `canonical_mutated: false`.

## Evidence Storage

Git stores the case catalog, golden expectations, coverage inventory, schemas, normalized semantic fields, and SHA-256 reference. The raw `bundle.json` contains captured validator streams and belongs only in the immutable versioned release artifact outside Git. Normalized evidence deliberately contains no raw stdout/stderr.

The raw artifact reference contains:

- logical artifact version (normally `raw-artifact-<process-version>`);
- filename;
- SHA-256 calculated over deterministic bundle bytes;
- `stored_in_git: false`.

## Coverage And Residual Gaps

`process/certification/coverage.yaml` composes all accepted capability specs and both active delta trees by exact capability, requirement, and scenario headings. Explicit evidence may reference an existing case ID or pytest node. Duplicate/unknown selectors, unknown case/test IDs, and invalid MODIFIED/REMOVED targets block the report.

An allowed residual gap must contain all five non-empty fields: `owner`, `risk`, `reason`, `compensation`, and `follow_up`. Future work items 2.11-2.14 remain explicit and are not reported as executed evidence.

## Manual Review

1. Run `--check` twice and compare JSON semantics.
2. Confirm no raw directory was created.
3. Run without `--check` against a new external destination.
4. Recalculate SHA-256 for `bundle.json` and compare it with normalized evidence.
5. Confirm normalized evidence says no actual model run occurred and contains no captured streams.
6. Preserve the raw artifact immutable; a repeated create attempt must fail rather than overwrite it.
