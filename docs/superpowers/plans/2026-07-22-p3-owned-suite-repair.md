# P3 Owned Suite Repair Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `python -m pytest -q tests` truthful and green for the P3 successor while preserving RC6 evidence.

**Architecture:** Register active P3 Delta scenarios in the deterministic coverage inventory and bind each covered selector to an exact test node. Align package-flow test data to the current package identity, and validate historical failed-preflight artifacts against their recorded catalog identity rather than the mutable current catalog.

**Tech Stack:** Python 3.13, pytest, PyYAML, OpenSpec Markdown, YAML certification inventories.

## Global Constraints

- Immutable RC6 remains package `0.3.0`; current P3 successor remains `0.3.4`.
- Historical raw evidence is append-only and must not be edited.
- Every pytest evidence reference requires an exact `SCENARIO_COVERAGE` binding.
- Root pytest discovery must be limited to `tests`.

---

### Task 1: P3 scenario coverage

**Files:**
- Modify: `process/certification/coverage.yaml`
- Modify: `process/certification/evidence-manifest.yaml`
- Modify: `tests/test_p3_vertical_slice.py`
- Test: `tests/test_certification.py`

- [ ] Add the two active P3 Delta sources and `tests/test_p3_vertical_slice.py` to the inventory.
- [ ] Run `python -m pytest -q tests/test_certification.py tests/test_p3_vertical_slice.py --tb=short` and observe `coverage.unmapped-scenario`.
- [ ] Bind implemented scenarios to the exact P3 test nodes and add explicit gaps for remaining proposed scenarios.
- [ ] Re-run the focused coverage tests and confirm that every selector is either evidenced or explicitly gapped.

### Task 2: Successor-version package fixtures

**Files:**
- Modify: `tests/test_packaged_flow_hardening.py`
- Modify: `tests/test_upgrade_evidence.py`

- [ ] Preserve the failing expectations that currently require `0.3.0`.
- [ ] Run `python -m pytest -q tests/test_packaged_flow_hardening.py tests/test_upgrade_evidence.py --tb=short` and observe the `0.3.4` identity mismatch.
- [ ] Update only fixture identities and assertions that represent the installed P3 successor.
- [ ] Re-run both test modules and confirm their upgrade evidence binds `0.3.4`.

### Task 3: Historical failed-preflight compatibility

**Files:**
- Modify: `process/actual_certification.py`
- Modify: `tests/test_actual_certification.py`

- [ ] Preserve the four failing historical-evidence parameterizations.
- [ ] Run `python -m pytest -q tests/test_actual_certification.py --tb=short` and observe stale catalog/baseline diagnostics.
- [ ] Add a narrow compatibility path that validates historical catalog identity and failed-preflight retention without substituting current catalog semantics.
- [ ] Re-run `tests/test_actual_certification.py` and confirm all available external raw-artifact assertions pass.

### Task 4: Root pytest discovery

**Files:**
- Create or modify: `pyproject.toml`
- Test: `python -m pytest -q`

- [ ] Add pytest `testpaths = ["tests"]` without changing test markers or warning policy.
- [ ] Run `python -m pytest -q` and confirm collection stays within `tests`.

### Task 5: Full verification and documentation

**Files:**
- Modify: `docs/CURRENT_PROJECT_AUDIT.md` if a durable audit finding needs closure.

- [ ] Run `python -m pytest -q tests`.
- [ ] Run `python -m pytest -q`.
- [ ] Run `git diff --check` and inspect `git status --short`.
- [ ] Commit intentional changes with a focused message.
