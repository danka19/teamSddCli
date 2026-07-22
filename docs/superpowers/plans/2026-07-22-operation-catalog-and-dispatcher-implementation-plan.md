# Operation Catalog And Dispatcher Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Сделать все локальные операции discoverable и policy-controlled через versioned catalog и тонкий локальный `sdd` dispatcher, не меняя полномочия человека и не ломая прямые script entrypoint'ы.

**Architecture:** `process/catalogs/operations.yaml` и `process/operations_catalog.py` являются единственным operation source. `process/operation_dispatcher.py` использует каталог и существующий JSON boundary `process/operation_cli.py`, но не получает domain logic. Guided routes, allowlist и README становятся derived/validated surfaces; `scripts/sdd.py` — переносимый Python entrypoint контракта `sdd`.

**Tech Stack:** Python 3, PyYAML, JSON Schema Draft 2020-12, `argparse`, `pytest`, OpenSpec 1.4.1, локальные Markdown/YAML/JSON artifacts.

## Global Constraints

- Выполнять на ветке P3 и в отдельном worktree, созданном через `superpowers:using-git-worktrees` непосредственно перед реализацией.
- P3 MCP-free: не добавлять credentials, сеть, external state mutation или корпоративную конфигурацию.
- `operations.yaml` — единственный нормативный registry (`D-CAT-1`); direct script entrypoint'ы сохраняются (`D-CAT-2`).
- До accepted completion `harden-role-aware-guided-workflow` каждый `sdd run` для `mutate_*` блокируется до entrypoint (`D-CAT-3`).
- Weak-model/certification operations — internal; `preview_analytics` public; raw certification writers high-risk (`D-CAT-4`).
- Не чинить известные 18 failures полного owned-suite этим change; не заявлять P3 acceptance при их сохранении.

---

## File Structure

| Путь | Ответственность |
|---|---|
| `process/schemas/operations-catalog.schema.json` | JSON Schema catalog record и enum. |
| `process/catalogs/operations.yaml` | Ровно 30 operation records; единственный policy source. |
| `process/operations_catalog.py` | Dataclasses, YAML/schema load, semantic invariants, README renderer. |
| `process/operation_dispatcher.py` | Pure routing/permission layer, без domain logic. |
| `scripts/sdd.py` | Переносимый `python scripts/sdd.py …` entrypoint. |
| `scripts/validate_operations_catalog.py` | Drift validator и generated README check. |
| `process/catalogs/guided-owner-workflow.yaml` | Operation IDs вместо raw script paths. |
| `process/guided_workflow.py` | Route validation через catalog, без hardcoded whitelist. |
| `process/release-allowlist.yaml`, `process/release_candidate.py` | Derived package/release smoke contract. |
| `tests/test_operations_catalog.py`, `tests/test_operation_dispatcher.py` | TDD contract tests. |

## Shared Interfaces

```python
@dataclass(frozen=True)
class OperationDefinition:
    id: str
    entrypoint: str
    visibility: str
    allowed_roles: Sequence[str]
    situations: Sequence[str]
    mutation_level: str
    risk_level: str
    automation_class: str
    human_decision_required: str | None
    exit_codes: Mapping[str, int]

@dataclass(frozen=True)
class OperationsCatalog:
    schema_version: str
    catalog_id: str
    operations: Mapping[str, OperationDefinition]

Public function contracts: `load_operations_catalog(path) -> OperationsCatalog`; `catalog_readme_table(catalog) -> str`; `validate_catalog_assets(catalog, repository_root) -> list[dict[str, str]]`; `dispatch(argv, catalog_path) -> dict[str, Any]`.
```

Blocked payloads exit `1`; operational errors exit `3`; all payloads are JSON-serializable. `scripts/sdd.py` renders through existing `operation_cli.execute` or the same stable blocked renderer as `scripts/guided_owner_workflow.py`.

### Task 1: TDD fixture и schema/loader

**Files:** Create `tests/fixtures/operations-catalog/valid.yaml`, `tests/test_operations_catalog.py`, `process/schemas/operations-catalog.schema.json`, `process/operations_catalog.py`; modify `process/package.yaml`, `tests/test_process_package.py`.

**Produces:** `OperationDefinition`, `OperationsCatalog`, `load_operations_catalog()`.

- [ ] **Step 1: Write failing tests**

```python
def test_load_operations_catalog_returns_indexed_records(tmp_path: Path) -> None:
    catalog = load_operations_catalog(write_valid_catalog(tmp_path))
    assert catalog.operations["classify-change"].mutation_level == "read_only"

def test_loader_rejects_mutation_without_confirmation(tmp_path: Path) -> None:
    path = write_valid_catalog(tmp_path, mutation_level="mutate_local", confirmation_requirements=None)
    with pytest.raises(OperationError, match="operations-catalog-invalid"):
        load_operations_catalog(path)
```

Also parameterize invalid `visibility`, `mutation_level`, `automation_class`, duplicate ID/entrypoint, owner outside `allowed_roles`, and `mutate_external`.

- [ ] **Step 2: Run RED**

Run: `python -m pytest -q tests/test_operations_catalog.py`  
Expected: import/collection failure because `process.operations_catalog` is absent.

- [ ] **Step 3: Implement minimal schema and loader**

```python
DEFAULT_OPERATIONS_CATALOG = PACKAGE_ROOT / "catalogs" / "operations.yaml"
MUTATING_LEVELS = frozenset({"mutate_local", "mutate_release", "mutate_external"})

def load_operations_catalog(path: Path = DEFAULT_OPERATIONS_CATALOG) -> OperationsCatalog:
    raw = _load_yaml_mapping(path)
    _validate_schema(raw, "operations-catalog.schema.json")
    records = tuple(_to_operation(item) for item in raw["operations"])
    _validate_semantics(records)
    return OperationsCatalog(raw["schema_version"], raw["catalog_id"], {item.id: item for item in records})
```

Reject all RED cases with `OperationError("operations-catalog-invalid", "catalog record violates the operation contract")`. Register schema key `operations_catalog`, catalog key `operations`, and `operations_catalog.py` in `process/package.yaml`; add schema filename to `SCHEMA_FILES`.

- [ ] **Step 4: Run GREEN and commit**

Run: `python -m pytest -q tests/test_operations_catalog.py tests/test_process_package.py`  
Expected: focused tests pass.

```powershell
git add process/schemas/operations-catalog.schema.json process/operations_catalog.py process/package.yaml tests/fixtures/operations-catalog/valid.yaml tests/test_operations_catalog.py tests/test_process_package.py
git commit -m "feat: add operation catalog loader"
```

### Task 2: Complete 30-record catalog and distribution

**Files:** Create `process/catalogs/operations.yaml`; modify `process/package.yaml`, `tests/test_operations_catalog.py`, `tests/test_release_candidate.py`.

**Produces:** exactly one record for each `scripts/*.py`, declared package asset.

- [ ] **Step 1: Write RED completeness tests**

```python
def test_catalog_has_exactly_one_record_for_every_script() -> None:
    catalog = load_operations_catalog()
    scripts = {f"scripts/{item.name}" for item in (ROOT / "scripts").glob("*.py")}
    assert {item.entrypoint for item in catalog.operations.values()} == scripts

def test_d_cat_4_visibility_defaults_are_fixed() -> None:
    catalog = load_operations_catalog()
    assert catalog.operations["preview-analytics"].visibility == "public"
    assert catalog.operations["run-actual-certification"].risk_level == "high"
```

- [ ] **Step 2: Run RED**

Run: `python -m pytest -q tests/test_operations_catalog.py::test_catalog_has_exactly_one_record_for_every_script`  
Expected: fail because catalog is missing/incomplete.

- [ ] **Step 3: Add exactly 30 records**

Use kebab-case IDs from script names. Set internal for `build-read-pack`, `launch-role-task`, `check-weak-model-evidence`, `check-parallel-plan`, `certify-process-release`, `check-actual-certification-gate`, `run-actual-certification`, `normalize-actual-certification`; public for `preview-analytics`; deprecated lifecycle for `validate-change`. Map each record to existing test file and runbook. Do not create a script record for library-only `archive_change`.

- [ ] **Step 4: Update distribution and GREEN verification**

Add `operations_catalog.py` to `distribution.files`; update release candidate assertions only after it is declared.

Run: `python -m pytest -q tests/test_operations_catalog.py tests/test_process_package.py tests/test_release_candidate.py`  
Expected: catalog count 30 and package tests pass.

- [ ] **Step 5: Commit**

```powershell
git add process/catalogs/operations.yaml process/package.yaml tests/test_operations_catalog.py tests/test_release_candidate.py
git commit -m "feat: catalog all process operations"
```

### Task 3: Validator and derived release allowlist

**Files:** Create `scripts/validate_operations_catalog.py`; modify `process/release-allowlist.yaml`, `process/release_candidate.py`, `tests/test_operations_catalog.py`, `tests/test_release_candidate.py`.

**Produces:** `validate-operations-catalog` JSON, exit 0/1/3; derived allowlist validation.

- [ ] **Step 1: Write RED negative cases**

```python
def test_validator_rejects_unregistered_script(tmp_path: Path) -> None:
    root = copy_valid_operations_tree(tmp_path)
    (root / "scripts" / "unregistered.py").write_text("print('unsafe')\n", encoding="utf-8")
    assert validator_main(["--repository-root", str(root), "--json"]) == 1

def test_validator_rejects_missing_runbook_reference(tmp_path: Path) -> None:
    root = copy_valid_operations_tree(tmp_path)
    replace_catalog_value(root, "documentation_location", "docs/runbooks/MISSING.md")
    assert validator_main(["--repository-root", str(root), "--json"]) == 1

def test_validator_rejects_allowlist_drift(tmp_path: Path) -> None:
    root = copy_valid_operations_tree(tmp_path)
    remove_allowlist_entry(root, "create_change.py")
    assert validator_main(["--repository-root", str(root), "--json"]) == 1
```

Each copies a valid tree, makes one bad change, invokes `validator_main(["--repository-root", str(root), "--json"])`, expects `status == "invalid"` plus stable diagnostic code.

- [ ] **Step 2: Run RED**

Run: `python -m pytest -q tests/test_operations_catalog.py -k validator`  
Expected: failing/missing validator.

- [ ] **Step 3: Implement through existing output boundary**

```python
def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return execute(lambda: validate_operations_catalog(args.catalog, args.repository_root), args.json)
```

Validate unregistered/duplicate scripts, broken entrypoint/test/runbook reference, bad policy combination and P3 external mutation. Keep allowlist committed as a derived release artifact; validator checks it but never silently rewrites it.

- [ ] **Step 4: Run GREEN and commit**

Run: `python -m pytest -q tests/test_operations_catalog.py tests/test_release_candidate.py`  
Expected: drift/release tests pass.

```powershell
git add scripts/validate_operations_catalog.py process/release-allowlist.yaml process/release_candidate.py tests/test_operations_catalog.py tests/test_release_candidate.py
git commit -m "feat: validate operation catalog drift"
```

### Task 4: Guided routes and read-pack through operation IDs

**Files:** Modify `process/catalogs/guided-owner-workflow.yaml`, `process/guided_workflow.py`, `process/read-packs/guided-owner-workflow.yaml`, `scripts/validate_guided_owner_workflow.py`, `docs/runbooks/GUIDED_OWNER_WORKFLOW.md`, `tests/test_guided_owner_workflow.py`, `tests/test_operations_catalog.py`.

**Produces:** `guide()` returns stable operation IDs; it resolves all IDs through `load_operations_catalog()` instead of `ALLOWED_COMMANDS`.

- [ ] **Step 1: Change tests first**

```python
assert payload["commands"] == ["create-change", "classify-change"]

def test_catalog_rejects_route_with_unknown_operation(tmp_path: Path) -> None:
    path = write_guided_catalog(tmp_path, commands=["not-a-real-operation"])
    with pytest.raises(OperationError, match="catalog-invalid"):
        load_catalog(path)
```

- [ ] **Step 2: Run RED**

Run: `python -m pytest -q tests/test_guided_owner_workflow.py`  
Expected: route assertions fail while paths are still returned.

- [ ] **Step 3: Resolve commands against catalog**

```python
def load_catalog(path: Path = DEFAULT_CATALOG, *, operations_path: Path = DEFAULT_OPERATIONS_CATALOG) -> dict[str, Any]:
    operations = load_operations_catalog(operations_path)
    commands = route.get("commands")
    if not isinstance(commands, list):
        raise OperationError("catalog-invalid", "guided workflow route commands are malformed")
    if not all(command in operations.operations for command in commands):
        raise OperationError("catalog-invalid", "guided workflow route references unknown operation")
```

Remove `ALLOWED_COMMANDS`; retain role/missing-context/fallback logic unchanged. Replace all route YAML paths with operation IDs.

- [ ] **Step 4: Update read-pack and checksum guide**

Add `catalogs/operations.yaml` to `canonical_sources`. State exactly: AI must not select an operation outside the catalog and must not invoke `mutate_*`. Regenerate the existing guided catalog SHA marker in `GUIDED_OWNER_WORKFLOW.md`.

- [ ] **Step 5: Run GREEN and commit**

Run: `python -m pytest -q tests/test_guided_owner_workflow.py tests/test_p3_vertical_slice.py tests/test_operations_catalog.py`  
Expected: four routes, role boundaries and unknown-operation negative pass.

```powershell
git add process/catalogs/guided-owner-workflow.yaml process/guided_workflow.py process/read-packs/guided-owner-workflow.yaml scripts/validate_guided_owner_workflow.py docs/runbooks/GUIDED_OWNER_WORKFLOW.md tests/test_guided_owner_workflow.py tests/test_operations_catalog.py
git commit -m "feat: route guided workflow through operations"
```

### Task 5: Generated README and situation-first runbook

**Files:** Create `docs/runbooks/OPERATIONS_AND_SDD.md`; modify `docs/README.md`, `scripts/validate_operations_catalog.py`, `.pre-commit-config.yaml`, `tests/test_operations_catalog.py`, `docs/00_FILE_STRUCTURE.md`.

**Produces:** committed generated README block and a concise manual route for a person who does not know script names.

- [ ] **Step 1: Write RED generated-table test**

```python
def test_readme_generated_operation_block_matches_catalog() -> None:
    expected = catalog_readme_table(load_operations_catalog())
    actual = extract_generated_block((ROOT / "docs/README.md").read_text(encoding="utf-8"))
    assert actual == expected
```

- [ ] **Step 2: Run RED**

Run: `python -m pytest -q tests/test_operations_catalog.py::test_readme_generated_operation_block_matches_catalog`  
Expected: fail because marker block/renderer does not exist.

- [ ] **Step 3: Implement renderer and explicit markers**

Use only these markers:

```markdown
<!-- operations-catalog:start -->
<!-- operations-catalog:end -->
```

`catalog_readme_table()` sorts public by ID, deprecated next, then internal in a separately labelled section. It uses catalog fields only; never copies audit prose as a second policy source.

- [ ] **Step 4: Validate, do not silently mutate**

Add `--check-readme` (byte compare) and explicit `--write-readme` to validator. Add a local pre-commit hook:

```yaml
- id: validate-operations-catalog
  entry: python scripts/validate_operations_catalog.py --check-readme --json
  language: system
  pass_filenames: false
  stages: [pre-commit]
```

- [ ] **Step 5: Write human runbook**

Document exact initial commands: `python scripts/sdd.py guide …`, `op list`, `op show`, `check`, `prepare`, `request`. Explain that `request` is stdout-only/non-authoritative and `run` is expected to block in P3. Link to OpenSpec requirements, not duplicated authority rules.

- [ ] **Step 6: Run GREEN and commit**

Run: `python -m pytest -q tests/test_operations_catalog.py; python scripts/validate_operations_catalog.py --check-readme --json`  
Expected: all pass; JSON reports `status: valid`.

```powershell
git add docs/README.md docs/runbooks/OPERATIONS_AND_SDD.md docs/00_FILE_STRUCTURE.md scripts/validate_operations_catalog.py .pre-commit-config.yaml tests/test_operations_catalog.py
git commit -m "docs: generate operation catalog guide"
```

### Task 6: Dispatcher foundation and portable entrypoint

**Files:** Create `process/operation_dispatcher.py`, `scripts/sdd.py`, `tests/test_operation_dispatcher.py`; modify `process/package.yaml`, `tests/test_process_package.py`, `process/catalogs/operations.yaml`, `process/release-allowlist.yaml`, `tests/test_release_candidate.py`.

**Produces:** parser for `guide`, `next`, `op`, `check`, `prepare`, `request`, `run`; `python scripts/sdd.py --help` exits 0.

- [ ] **Step 1: Write RED parser tests**

```python
def test_op_list_renders_public_operation_cards(capsys) -> None:
    assert sdd_main(["op", "list", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["operation"] == "sdd-op-list"

def test_unknown_subcommand_is_parser_error() -> None:
    with pytest.raises(SystemExit) as error:
        sdd_main(["invent"])
    assert error.value.code == 2
```

- [ ] **Step 2: Run RED**

Run: `python -m pytest -q tests/test_operation_dispatcher.py -k "op_list or unknown_subcommand"`  
Expected: import failure because `scripts.sdd` does not exist.

- [ ] **Step 3: Implement parser and stable render path**

```python
def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    payload = dispatch(args.raw_argv, catalog_path=args.catalog)
    return _render_payload(payload, args.json)
```

Keep `operation_cli.execute` unchanged. The dispatcher has its own `_render_blocked()` mirroring `guided_owner_workflow._render_block`; never use `shell=True`.

- [ ] **Step 4: Register and smoke**

Add `operation_dispatcher.py` to package distribution and `scripts/sdd.py` as a catalog/release smoke entrypoint with `--help`, expected exit 0.

- [ ] **Step 5: Run GREEN and commit**

Run: `python -m pytest -q tests/test_operation_dispatcher.py tests/test_process_package.py tests/test_release_candidate.py`  
Expected: parser/package checks pass.

```powershell
git add process/operation_dispatcher.py scripts/sdd.py tests/test_operation_dispatcher.py process/package.yaml process/catalogs/operations.yaml process/release-allowlist.yaml tests/test_process_package.py tests/test_release_candidate.py
git commit -m "feat: add sdd dispatcher foundation"
```

### Task 7: Discovery commands `guide`, `next`, `op list`, `op show`

**Files:** Modify `process/operation_dispatcher.py`, `scripts/sdd.py`, `tests/test_operation_dispatcher.py`.

**Produces:** situation-first JSON discovery; no operation execution.

- [ ] **Step 1: Write RED behavior tests**

```python
def test_guide_forwards_facts_and_preserves_human_decision(capsys) -> None:
    assert sdd_main(["guide", "new-requirement", "--fact", "human_role=Analyst", "--fact", "classification=minor", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["human_decision"]["id"] == "classification-confirmation"

def test_op_show_exposes_confirmation_boundary_without_executing(capsys) -> None:
    assert sdd_main(["op", "show", "create-change", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["mutation_level"] == "mutate_local"

def test_next_uses_recorded_lifecycle_state_and_blocks_missing_change(capsys) -> None:
    assert sdd_main(["next", "--change", "missing-change", "--json"]) == 1
    assert json.loads(capsys.readouterr().out)["blockers"][0]["code"] == "missing-change"
```

The Analyst fixture must assert no implementation CTA. `op list` defaults to public and requires `--include-internal` for service records.

- [ ] **Step 2: Run RED**

Run: `python -m pytest -q tests/test_operation_dispatcher.py -k "guide or op_show or next"`  
Expected: missing/failing handlers.

- [ ] **Step 3: Implement handlers**

`guide` delegates to existing `guide(situation, facts, unavailable)`. `op show` returns title, roles, inputs/outputs, risk/mutation, evidence, fallback and human decision. `next` reads local `change.yaml` only; absent/malformed state returns `blocked/missing-change` or `blocked/missing-lifecycle-state`, never inferred state.

- [ ] **Step 4: Run GREEN and commit**

Run: `python -m pytest -q tests/test_operation_dispatcher.py tests/test_guided_owner_workflow.py`  
Expected: all discovery routes pass.

```powershell
git add process/operation_dispatcher.py scripts/sdd.py tests/test_operation_dispatcher.py
git commit -m "feat: add sdd operation discovery"
```

### Task 8: Safe `check`, `prepare`, `request` bridge

**Files:** Modify `process/operation_dispatcher.py`, `scripts/sdd.py`, `tests/test_operation_dispatcher.py`.

**Produces:** explicit subprocess bridge for read-only/prepare only; stdout-only confirmation draft.

- [ ] **Step 1: Write RED safety tests**

```python
def test_check_rejects_prepare_operation_before_subprocess(monkeypatch, capsys) -> None:
    monkeypatch.setattr(operation_dispatcher, "_run_entrypoint", pytest.fail)
    assert sdd_main(["check", "prepare-spec-pr", "--json"]) == 1

def test_prepare_rejects_read_only_operation_before_subprocess(monkeypatch, capsys) -> None:
    monkeypatch.setattr(operation_dispatcher, "_run_entrypoint", pytest.fail)
    assert sdd_main(["prepare", "classify-change", "--json"]) == 1

def test_request_returns_sha256_of_normalized_arguments(capsys) -> None:
    assert sdd_main(["request", "create-change", "--", "sample-001", "--json"]) == 0
    assert len(json.loads(capsys.readouterr().out)["input_digest"]) == 64
```

Monkeypatch subprocess and assert it is never called by rejected class. Request asserts `status == "confirmation-requested"`, `authority_granted is False`, operation ID and deterministic `input_digest`.

- [ ] **Step 2: Run RED**

Run: `python -m pytest -q tests/test_operation_dispatcher.py -k "check or prepare or request"`  
Expected: class enforcement/digest cases fail.

- [ ] **Step 3: Implement explicit child invocation**

```python
def _run_entrypoint(operation: OperationDefinition, forwarded: Sequence[str]) -> dict[str, Any]:
    completed = subprocess.run(
        [sys.executable, str(REPOSITORY_ROOT / operation.entrypoint), *forwarded, "--json"],
        capture_output=True, text=True, check=False, shell=False,
    )
    return _decode_entrypoint_result(completed, operation)
```

Reject caller-supplied duplicate `--json`; append it once. Preserve child exit 0/1/3; redact unexpected stderr into stable operational error. Normalise `(operation.id, list(forwarded))` through sorted compact JSON then SHA-256 for `request`. `request` does not write YAML, alter lifecycle or execute a script.

- [ ] **Step 4: Run GREEN and commit**

Run: `python -m pytest -q tests/test_operation_dispatcher.py tests/test_packaged_flow_cli.py`  
Expected: allowed evidence is delegated; rejected classes have no subprocess side effect.

```powershell
git add process/operation_dispatcher.py scripts/sdd.py tests/test_operation_dispatcher.py
git commit -m "feat: dispatch safe catalog operations"
```

### Task 9: Fail-closed `run`, direct compatibility and release evidence

**Files:** Modify `process/operation_dispatcher.py`, `scripts/sdd.py`, `tests/test_operation_dispatcher.py`, `tests/test_packaged_flow_cli.py`, `tests/test_release_candidate.py`, `openspec/changes/add-operation-catalog-and-dispatcher/tasks.md`.

**Produces:** P3 `run` always blocks mutation before side effect; later confirmation enablement remains outside this execution.

- [ ] **Step 1: Write RED blockers**

```python
def test_run_mutation_blocks_before_subprocess_until_confirmation_contract_is_accepted(monkeypatch, capsys) -> None:
    assert sdd_main(["run", "create-change", "--json"]) == 1
    assert json.loads(capsys.readouterr().out)["blockers"][0]["code"] == "confirmation-contract-pending"

def test_run_high_risk_internal_operation_blocks_in_p3(capsys) -> None:
    assert sdd_main(["run", "run-actual-certification", "--json"]) == 1
    assert json.loads(capsys.readouterr().out)["blockers"][0]["code"] == "confirmation-contract-pending"
```

- [ ] **Step 2: Run RED**

Run: `python -m pytest -q tests/test_operation_dispatcher.py -k run`  
Expected: handler missing or not fail-closed.

- [ ] **Step 3: Implement permanent P3 blocker**

```python
def _block_mutating_run(operation: OperationDefinition) -> dict[str, Any]:
    return {
        "operation": "sdd-run", "status": "blocked", "schema_version": "1.0",
        "blockers": [{"code": "confirmation-contract-pending", "operation_id": operation.id}],
        "lifecycle_mutated": False, "external_state_mutated": False,
    }
```

Call before parsing/forwarding mutating args. No bypass flag. A future accepted change alone may add actor role, input/revision digest and expiry validation.

- [ ] **Step 4: Add direct compatibility smokes**

In release/package tests invoke `python scripts/create_change.py --help`, `python scripts/guided_owner_workflow.py --help`, `python scripts/validate_operations_catalog.py --help`, and `python scripts/sdd.py --help`; preserve established exit codes.

- [ ] **Step 5: Run focused GREEN and commit**

Run: `python -m pytest -q tests/test_operation_dispatcher.py tests/test_packaged_flow_cli.py tests/test_release_candidate.py`  
Expected: mutation blocked without side effects; direct scripts remain usable.

```powershell
git add process/operation_dispatcher.py scripts/sdd.py tests/test_operation_dispatcher.py tests/test_packaged_flow_cli.py tests/test_release_candidate.py openspec/changes/add-operation-catalog-and-dispatcher/tasks.md
git commit -m "feat: fail close sdd mutations"
```

### Task 10: Integration verification and human walkthrough

**Files:** Modify `openspec/changes/add-operation-catalog-and-dispatcher/tasks.md`; modify `docs/CURRENT_PROJECT_AUDIT.md`, README, roadmap or P3 plan only if evidence changes their recorded state.

**Produces:** exact evidence, no automatic archive/acceptance.

- [ ] **Step 1: Run focused deterministic suite**

```powershell
python -m pytest -q tests/test_operations_catalog.py tests/test_operation_dispatcher.py tests/test_guided_owner_workflow.py tests/test_process_package.py tests/test_release_candidate.py tests/test_packaged_flow_cli.py tests/test_p3_vertical_slice.py
```

Expected: zero failures in this focused scope.

- [ ] **Step 2: Run four manual JSON walkthroughs**

```powershell
python scripts/sdd.py guide new-requirement --fact human_role=Analyst --fact classification=minor --json
python scripts/sdd.py guide existing-change --fact human_role=Analyst --fact change_id=sample-minor-001 --fact lifecycle_state=spec_review --json
python scripts/sdd.py guide urgent-incident --fact human_role=Tech Lead --fact incident_ref=INC-001 --json
python scripts/sdd.py guide blocked-operation --fact human_role=Tech Lead --fact failed_run_ref=RUN-001 --json
python scripts/sdd.py run create-change --json
```

Expected: four routes show evidence/human decision; none mutates state. The final command exits 1 with `confirmation-contract-pending`; unsupported `mutate_external` catalog records are rejected by the Task 3 validator.

- [ ] **Step 3: Run package/documentation gates**

```powershell
python scripts/validate_operations_catalog.py --check-readme --json
python scripts/validate_guided_owner_workflow.py --json
openspec validate --all --strict
node "$env:USERPROFILE\.codex\skills\roadmap-openspec-validator\scripts\validate-roadmap-openspec.mjs" --root "$PWD" --json
git diff --check
```

Expected: all exit 0. Report existing P2 lifecycle warnings separately.

- [ ] **Step 4: Run full suite honestly**

Run: `python -m pytest -q tests`  
Expected: record actual result. If known 18 failures persist, do not mark this change/P3 accepted; link the evidence to separate remediation.

- [ ] **Step 5: Update evidence and commit**

```powershell
git add openspec/changes/add-operation-catalog-and-dispatcher/tasks.md docs
git commit -m "test: verify operation catalog dispatcher"
```

Do not sync/archive the change; human acceptance and later mutation enablement are separate gates.

## Self-Review Matrix

| OpenSpec requirement | Plan tasks |
|---|---|
| Catalog, all scripts, visibility/risk invariants | 1–3 |
| Derived routes/allowlist/read-pack | 3–4 |
| Generated README and human guide | 5 |
| Situation-first discovery | 6–7 |
| Safe check/prepare/request | 8 |
| Fail-closed mutation/direct compatibility | 9 |
| Automated/manual/full-suite evidence | 10 |

## Execution Order And Gates

Tasks 1–5 are serial because they mutate canonical catalogs and derived documents. Tasks 6–9 follow only after the catalog validator is green. Task 10 starts only after focused tests are green. Do not parallelise shared canonical YAML, package manifest, release allowlist or README generation.

The plan deliberately stops before real mutation enablement. Task 9 is the safe P3 delivery; the future operation-ID/role/input-digest/revision/expiry confirmation binding cannot start until `harden-role-aware-guided-workflow` is complete and separately accepted.
