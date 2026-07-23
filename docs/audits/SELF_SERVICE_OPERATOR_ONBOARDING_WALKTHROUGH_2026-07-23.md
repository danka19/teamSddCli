# Self-service operator onboarding: synthetic walkthrough

Status: deterministic synthetic evidence; it neither represents human approval nor enables external operations.

## Purpose

Record an AI-disabled and human-readable P3 walkthrough for the proposed
`add-self-service-operator-onboarding` change without credentials, network
access, external calls, or private data.

## Executed route

1. Install the local Python distribution in an isolated environment with
   `pip install --no-deps <repository>` and invoke the generated `sdd` console
   script. `sdd --version --json` returns package `sdd-process` version `0.3.6`.
2. Invoke `sdd setup <empty-workspace>` without `--confirm`; it returns
   `confirmation-required` and leaves the destination absent.
3. Invoke the same command with `--confirm`; it creates only the declared
   local `process/` and `team-specs/` workspace and returns
   `sdd start new-requirement --role Analyst --json` as the next action.
4. Create a synthetic `minor` change using the retained direct compatibility
   entrypoint, then invoke public `sdd prepare prepare-spec-pr` and
   `sdd prepare prepare-archive` with the prepared arguments. Both produce
   local preparation evidence; neither mutates lifecycle or external state.
5. Invoke `sdd start` with no situation and select `new-requirement` at the
   local prompt; the same continuation envelope is returned as for structured
   input. Invoke it with missing classification. The result is blocked,
   lists `classification` as a missing fact, and supplies no next command.
6. Existing `sdd run` coverage continues to return
   `confirmation-contract-pending`; P3 external mutations remain forbidden
   before an entrypoint is spawned.

## Automated evidence

`python -m pytest tests/test_self_service_onboarding.py tests/test_operation_catalog_dispatcher.py tests/test_packaged_flow.py tests/test_packaged_flow_cli.py tests/test_process_package.py -q`

Result: `70 passed`.

## Limitations

This is local synthetic evidence only. It does not certify a published package
repository, a corporate environment, a model runtime, release execution, or a
human lifecycle/approval decision.
