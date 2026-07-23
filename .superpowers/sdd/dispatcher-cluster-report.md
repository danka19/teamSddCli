# Dispatcher cluster report

## Scope
Implemented the dispatcher cluster for OpenSpec change `add-operation-catalog-and-dispatcher` (tasks 3.1-4.3), replacing the untracked `process/sdd.py` draft with the dedicated `process/operation_dispatcher.py` core and portable `scripts/sdd.py` entrypoint.

## Changes
- Added catalog-backed `guide`, `next`, `op list`, `op show`, `check`, `prepare`, `request`, and fail-closed `run` surfaces.
- Preserved stable JSON envelopes and dispatcher exits: success 0, blocked 1, operational error 3; parser misuse remains argparse 2.
- Migrated guided routes from raw script paths to operation IDs and validates route IDs through the operations catalog.
- `request` is stdout-only and hashes compact canonical JSON of operation ID plus original ordered forwarded argv.
- `check` and `prepare` reject wrong mutation classes before subprocess; child invocation uses argv, `shell=False`, and one normalized `--json`.
- Added package/release exact records and standalone `scripts/sdd.py --help` smoke.

## RED / GREEN evidence
- RED: `python -m pytest -q tests/test_operation_catalog_dispatcher.py -k dedicated` failed with `ModuleNotFoundError: No module named 'process.operation_dispatcher'`.
- GREEN: the same command passed after adding the dedicated core.
- Final focused checks: `38 passed` for dispatcher/guided/package/portable-flow tests; `2 passed` for release allowlist and standalone-candidate smokes.
- Direct checks: `python scripts/sdd.py --help` exited 0; guided JSON returned operation IDs; `python scripts/sdd.py run create-change --json` exited 1 with `confirmation-contract-pending`.
- `git diff --check` passed after newline normalization.

## Risks and unresolved items
- The broader combined target command including the entire `tests/test_release_candidate.py` suite exceeded the 60-second command limit and timed out; focused release smoke tests above pass.
- No network, MCP, credentials, or external mutation is added. `run` remains permanently fail-closed for P3.
