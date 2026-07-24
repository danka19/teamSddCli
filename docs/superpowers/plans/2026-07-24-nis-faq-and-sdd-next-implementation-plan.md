# NIS FAQ And Canonical `sdd next` Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the missing positive NIS adoption page and make `sdd next` continue a real schema-v2 change through canonical `status`.

**Architecture:** The FAQ remains a maintained view over the NIS adoption decision and active OpenSpec contracts. The CLI fix is a narrow storage adapter: `change.yaml.status` is mapped to the existing guided fact `lifecycle_state`, whose catalog still owns allowed values.

**Tech Stack:** Russian Markdown, Python 3, PyYAML, pytest, OpenSpec `spec-driven`.

## Global Constraints

- The NIS page contains only what is adopted, how it is adapted, and what is planned.
- The NIS page must not add a rejected/not-adopted section.
- `status` is the only persisted lifecycle field accepted by `sdd next`.
- `lifecycle_state` remains only an internal guided fact and is not a storage fallback.
- `sdd next` remains read-only and fail-closed.
- OpenSpec and Git remain canonical; FAQ text is a linked user-facing view.

---

### Task 1: Positive NIS foundation page

**Files:**
- Create: `docs/faq/nis-foundation.md`
- Modify: `docs/faq/index.md`
- Modify: `docs/faq/product-and-foundation.md`
- Modify: `scripts/validate_product_faq.py`
- Test: `tests/test_product_faq_docs.py`
- Modify: `openspec/changes/add-product-faq-and-role-runbook/tasks.md`

**Interfaces:**
- Consumes: `docs/audits/NIS_V1_6_PRESENTATION_COMPARISON_REPORT_2026-07-13.md`, `docs/planning/NIS_CORPORATE_PROCESS_ADOPTION_PLAN_2026-07-13.md`, and `openspec/changes/adopt-nis-corporate-process-governance/`.
- Produces: required FAQ page `nis-foundation.md` and hub link.

- [ ] **Step 1: Write the failing page-contract test**

```python
def test_nis_foundation_page_explains_positive_adoption_route() -> None:
    faq = ROOT / "docs" / "faq"
    page = (faq / "nis-foundation.md").read_text(encoding="utf-8")
    assert "## Что уже взято из НИС" in page
    assert "## Как это адаптировано в teamSddCli" in page
    assert "## Что планируется перенести дальше" in page
    assert "## Что не взято" not in page
    assert "nis-foundation.md" in (faq / "index.md").read_text(encoding="utf-8")
```

- [ ] **Step 2: Run RED**

Run:

```text
python -m pytest -q -o addopts='' tests/test_product_faq_docs.py -k nis_foundation
```

Expected: FAIL because `docs/faq/nis-foundation.md` is absent.

- [ ] **Step 3: Create the page and navigation**

Create a concise page with exactly these user-facing sections:

```markdown
# НИС как основа корпоративного процесса

## Что уже взято из НИС
## Как это адаптировано в teamSddCli
## Что планируется перенести дальше
## Где смотреть канонические правила
```

Describe adopted classification, gates, Tech Lead governance, regression,
scope/stop/escalation, release handoff, role evidence and failed-run retention.
Describe adaptation through OpenSpec/Git, portable role ownership,
deterministic checks, AI-disabled fallback and configurable corporate mapping.
Describe later corporate configuration, real pilot, tool wiring and bounded AI
automation only as planned work.

- [ ] **Step 4: Make the page a required validated target**

Add `"nis-foundation.md"` to `REQUIRED_PAGES`; the existing
`REQUIRED_INDEX_TARGETS` derivation then requires the hub link.

- [ ] **Step 5: Run GREEN**

Run:

```text
python -m pytest -q -o addopts='' tests/test_product_faq_docs.py
python scripts/validate_product_faq.py --json
```

Expected: all FAQ tests pass and validator returns `"valid": true`.

### Task 2: Canonical `status` producer-consumer route

**Files:**
- Modify: `tests/test_self_service_onboarding.py`
- Modify: `tests/test_operation_catalog_dispatcher.py`
- Modify: `process/operation_dispatcher.py`
- Modify: `openspec/changes/fix-sdd-next-canonical-status/tasks.md`

**Interfaces:**
- Consumes: `process.workflow_operations.create_change(...) -> dict[str, Any]`.
- Produces: public `sdd next --change <path> --role <role> --json` continuation based on `change.yaml.status`.

- [ ] **Step 1: Replace the handcrafted positive fixture**

Use the real producer:

```python
from process.workflow_operations import create_change

changes = tmp_path / "changes"
create_change(
    ROOT / "process",
    changes,
    change_id="sample-minor-001",
    title="Sample minor change",
    classification="minor",
    change_type="config_ops",
)
change = changes / "sample-minor-001"
assert main(["next", "--change", str(change), "--role", "Developer", "--json"]) == 0
```

Assert `status == "guided"`, the exact role continuation, and both mutation
flags are false.

- [ ] **Step 2: Add strict negative tests**

```python
noncanonical.write_text("lifecycle_state: approved\n", encoding="utf-8")
assert main(["next", "--change", str(noncanonical), "--role", "Developer", "--json"]) == 1
assert payload["blockers"][0]["code"] == "missing-change-status"

invalid.write_text("status: impossible\n", encoding="utf-8")
assert main(["next", "--change", str(invalid), "--role", "Developer", "--json"]) == 1
assert payload["blockers"][0]["code"] == "invalid-context"
```

- [ ] **Step 3: Run RED**

Run:

```text
python -m pytest -q -o addopts='' tests/test_self_service_onboarding.py tests/test_operation_catalog_dispatcher.py -k "next"
```

Expected: real writer case and new diagnostics fail because dispatcher still
reads `lifecycle_state`.

- [ ] **Step 4: Implement the minimal adapter**

Change the `next` handler to:

```python
try:
    state = yaml.safe_load(path.read_text(encoding="utf-8")).get("status")
except (OSError, UnicodeError, yaml.YAMLError, AttributeError):
    state = None
if not isinstance(state, str) or not state:
    return _blocked("sdd-next", "missing-change-status")
result = guide(
    "existing-change",
    {
        "human_role": args.role or "",
        "change_id": path.parent.name,
        "lifecycle_state": state,
    },
    set(),
)
```

- [ ] **Step 5: Run GREEN**

Run the exact RED command again. Expected: all selected tests pass.

### Task 3: Documentation, walkthrough and gates

**Files:**
- Modify: affected `docs/faq/*.md` and `docs/faq/roles/*.md`
- Modify: `docs/audits/PRODUCT_FAQ_AND_ROLE_RUNBOOK_ACCEPTANCE_AUDIT_2026-07-24.md`
- Modify: `openspec/changes/add-product-faq-and-role-runbook/tasks.md`
- Modify: `openspec/changes/fix-sdd-next-canonical-status/tasks.md`

**Interfaces:**
- Consumes: verified producer-consumer behavior from Task 2.
- Produces: current user instructions without the obsolete blocker.

- [ ] **Step 1: Replace temporary limitation text**

State that schema-v2 stores lifecycle in `status`, `sdd next` reads that field,
and users must not create a second `lifecycle_state` field. Preserve all human
authority and mutation-boundary warnings.

- [ ] **Step 2: Run a real smoke**

Create a temporary package with `scripts/create_change.py`, invoke
`scripts/sdd.py next`, and verify a guided JSON result with no mutations.

- [ ] **Step 3: Update evidence and task status**

Record the successful smoke in the dated FAQ audit. Mark FAQ task 5.4 complete
only after FAQ validation and the real-package smoke pass. Keep human
walkthrough task 4.4 open until a new person performs it.

- [ ] **Step 4: Run final gates**

```text
python -m pytest -q -o addopts='' tests/test_self_service_onboarding.py tests/test_operation_catalog_dispatcher.py tests/test_product_faq_docs.py
python scripts/validate_product_faq.py --json
openspec list
openspec list --specs
openspec validate --all --strict
node "$env:USERPROFILE\.codex\skills\roadmap-openspec-validator\scripts\validate-roadmap-openspec.mjs" --root "<worktree>"
git diff --check
```

Expected: tests and validators pass; only pre-existing lifecycle warnings may
remain.

- [ ] **Step 5: Commit intentional changes**

Stage only the plan, OpenSpec artifacts, dispatcher, tests and affected FAQ/docs.
Do not stage temporary pytest or package metadata directories.
