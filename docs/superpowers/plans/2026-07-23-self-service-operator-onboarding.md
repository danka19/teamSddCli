# Self-Service Operator Onboarding Implementation Plan

> **For agentic workers:** Execute tasks in order with TDD; each public behaviour starts with a focused failing test.

**Goal:** Provide a versioned installed `sdd` entrypoint with safe `setup`, `start`, and canonical `next` guidance, without weakening P3's fail-closed mutation boundary.

**Architecture:** A setuptools console script delegates to the existing dispatcher. The dispatcher owns a single continuation-result envelope and derives terminal and JSON views from it. `setup` validates and delegates only to the existing local bootstrap operation after an explicit flag; all external/release execution remains blocked.

**Tech Stack:** Python 3, setuptools, argparse, PyYAML, pytest.

## Global Constraints

- The supported public command is `sdd`; direct `scripts/*.py` remain compatible.
- No network calls, credentials, external mutations, release execution, or AI authority are introduced.
- Every mutation requires explicit confirmation and reports structured JSON when requested.
- New documentation and OpenSpec prose are Russian; stable CLI tokens remain English.

---

### Task 1: Package launcher and diagnostics

**Files:** create `pyproject.toml`; modify `scripts/sdd.py`, `process/operation_dispatcher.py`; test `tests/test_self_service_onboarding.py`.

- [ ] Add failing subprocess tests proving an installed `sdd --help` exposes `setup`, `start`, `next`, and version diagnostics.
- [ ] Add `console_scripts` packaging metadata and a callable `scripts.sdd:main` launcher.
- [ ] Run the focused launcher tests and retain direct-script tests.

### Task 2: Canonical guided routes

**Files:** modify `process/operation_dispatcher.py`; test `tests/test_self_service_onboarding.py`.

- [ ] Add failing tests for structured `start` and `next` results, including missing facts and role blocks.
- [ ] Implement a single continuation-result mapper and human/JSON renderers based on it.
- [ ] Run focused route and existing dispatcher tests.

### Task 3: Confirmed local setup

**Files:** modify `process/operation_dispatcher.py`; test `tests/test_self_service_onboarding.py`.

- [ ] Add failing tests for absent confirmation, non-empty destination, invalid package/configuration, and valid bootstrap.
- [ ] Implement preflight plus delegation to `bootstrap_team_specs`; return a canonical next action.
- [ ] Run focused setup and package-flow tests.

### Task 4: Safety, walkthrough, and documentation

**Files:** modify package/catalog/help/runbooks as required; update change tasks and phase/roadmap evidence; test `tests/test_self_service_onboarding.py`.

- [ ] Add failing negative and clean-sandbox e2e tests, including `run`/external/release fail-closed assertions.
- [ ] Add the minimal documentation and package metadata needed for the installed public route.
- [ ] Run focused then relevant regression suites; record synthetic AI-disabled and human walkthrough evidence.
- [ ] Run OpenSpec and roadmap validators, `git diff --check`, then commit the intentional change.
