# P3 owned-suite repair design

## Goal

Restore a truthful green owned test suite for the P3 successor without changing
the accepted immutable RC6 package `0.3.0` or its append-only raw artifacts.

## Design

The coverage inventory becomes the canonical index of active P3 Delta sources.
Implemented P3 scenarios receive exact pytest-node evidence through
source-owned `SCENARIO_COVERAGE` markers.  Scenarios that remain proposed or
unimplemented are retained as explicit gaps rather than being represented as
passing coverage.

Package-flow fixtures describe the installed successor package `0.3.4`.
Historical weak-model evidence remains bound to the catalog and baseline that
were recorded at the time of execution; current validation must not reinterpret
that immutable failed preflight with a later catalog.

Pytest discovery is restricted to `tests` so a root invocation cannot collect
historical temporary directories.

## Safety boundaries

- RC6 `0.3.0` and all raw artifacts stay unchanged.
- No external certification run, model call, credential, network action, or
  artifact rewrite is performed.
- Coverage claims are exact pytest evidence or explicit residual gaps.
