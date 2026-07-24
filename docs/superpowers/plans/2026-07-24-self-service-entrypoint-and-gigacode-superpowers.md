# Self-service Entry Point and GigaCode Superpowers Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

> **Integration note (2026-07-24):** шаги ниже фиксируют первоначальное
> выполнение относительно base `59bdb60`, где feature готовила `0.3.7`.
> После независимого появления AI Analyst package `0.3.7` в `main` итоговый
> combined payload получил `0.3.8` в merge-коммите `e18bb56`. Упоминания
> `0.3.7` внутри выполненных шагов являются историческим RED/GREEN evidence и
> не задают текущую package identity.

**Goal:** Вынести public `sdd` self-service entrypoint в отдельную FAQ-страницу, точно объяснить состав полного управляемого цикла и поставить обязательный общий Superpowers skill во все bootstrap GigaCode workspace.

**Architecture:** `docs/README.md` остаётся кратким архитектурным обзором и сразу ведёт на одну пользовательскую self-service страницу; FAQ показывает public, specialist/manual и external слои без дублирования нормативной policy. GigaCode получает отдельный общий workflow skill, который активируется до SDD companion и поставляется как versioned managed file через существующий package manifest/bootstrap/update механизм.

**Tech Stack:** Markdown, Python 3.11+, pytest, YAML/JSON Schema, OpenSpec CLI 1.4.1, PowerShell verification commands.

## Global Constraints

- Работать только в ветке `feature/self-service-gigacode-superpowers` и worktree `.worktrees/self-service-gigacode-superpowers`.
- Новая документация и OpenSpec prose пишутся по-русски; stable IDs, paths, CLI tokens и structural keywords остаются English.
- Public `sdd` не получает новые mutations; `sdd run`, release и external mutation остаются fail-closed.
- Classification, acceptance, DoR/DoD, risk, waiver, merge, release и archive остаются human-owned.
- Новый `process/gigacode/skills/superpowers.md` является GigaCode-readable tool-agnostic workflow skill, а не копией runtime-specific глобального Codex plugin.
- Активация GigaCode skills имеет порядок `superpowers -> sdd-process-companion` для SDD-задач.
- Current combined process package identity — `0.3.8`; immutable release/certification evidence со старыми версиями не переписывается.
- OpenSpec backfill выполняется после рабочей реализации согласно явному разрешению владельца, но до итоговой acceptance verification.
- Не выполнять push, merge, release candidate build, external mutation или archive без отдельного запроса владельца.

---

### Task 1: Отдельная self-service FAQ-страница и актуальный README

**Files:**
- Create: `docs/faq/self-service-entrypoint.md`
- Modify: `tests/test_product_faq_docs.py`
- Modify: `scripts/validate_product_faq.py`
- Modify: `docs/README.md`
- Modify: `docs/faq/index.md`
- Modify: `docs/faq/installation.md`
- Modify: `docs/faq/setup-and-topology.md`
- Modify: `docs/faq/first-change.md`
- Modify: `docs/faq/troubleshooting-and-boundaries.md`
- Modify: `docs/00_FILE_STRUCTURE.md`

**Interfaces:**
- Consumes: existing `validate_product_faq(root: Path) -> list[str]`, public `sdd --version|setup|start|next|op|check|prepare|request` contract and accepted fail-closed boundary.
- Produces: required FAQ page `self-service-entrypoint.md`, top-of-README user route and one three-layer explanation reused by links rather than copied policy.

- [ ] **Step 1: Write the failing FAQ contract tests**

Add `self-service-entrypoint.md` to the getting-started link loop and add a focused test:

```python
def test_self_service_entrypoint_explains_the_whole_governed_route() -> None:
    faq = ROOT / "docs" / "faq"
    readme = (ROOT / "docs" / "README.md").read_text(encoding="utf-8")
    page = (faq / "self-service-entrypoint.md").read_text(encoding="utf-8")
    index = (faq / "index.md").read_text(encoding="utf-8")

    assert readme.index("faq/self-service-entrypoint.md") < readme.index("## Summary")
    assert "](self-service-entrypoint.md)" in index
    for token in (
        "sdd --version --json",
        "sdd setup",
        "sdd start",
        "sdd next",
        "## Что public `sdd` делает сам",
        "## Из каких частей состоит полный цикл",
        "Public `sdd`",
        "Specialist/manual",
        "External/corporate",
        "`sdd run` остаётся fail-closed",
        "полный управляемый маршрут пройти можно",
    ):
        assert token in page
```

Strengthen the README test so it requires the self-service link before the architecture summary:

```python
assert readme.index("faq/self-service-entrypoint.md") < readme.index("## Summary")
```

- [ ] **Step 2: Run the FAQ tests to verify RED**

Run:

```powershell
python -m pytest tests/test_product_faq_docs.py -q
```

Expected: FAIL because `docs/faq/self-service-entrypoint.md` does not exist and the README has no direct top link.

- [ ] **Step 3: Make the new page mandatory in the deterministic validator**

Add the filename to `REQUIRED_PAGES` in `scripts/validate_product_faq.py`:

```python
REQUIRED_PAGES = {
    # existing pages remain
    "self-service-entrypoint.md",
}
```

The existing `REQUIRED_INDEX_TARGETS` derivation then requires a direct hub link without a second list.

Add page-specific section, token and link checks rather than relying on global
question markers:

```python
SELF_SERVICE_ENTRYPOINT_SECTIONS = {
    "## Что такое public `sdd`",
    "## Быстрый старт",
    "## Что public `sdd` делает сам",
    "## Из каких частей состоит полный цикл",
    "## Почему `sdd run` закрыт",
    "## Куда перейти дальше",
}
SELF_SERVICE_ENTRYPOINT_TOKENS = {
    "python -m pip install",
    "sdd --version --json",
    "sdd setup",
    "sdd start",
    "sdd next",
    "sdd check",
    "sdd prepare",
    "sdd request",
    "sdd run",
    "--confirm",
    "fail-closed",
    "Public `sdd`",
    "Specialist/manual",
    "External/corporate",
}
SELF_SERVICE_ENTRYPOINT_TARGETS = {
    "installation.md",
    "setup-and-topology.md",
    "first-change.md",
    "roles/index.md",
    "ai-collaboration.md",
    "troubleshooting-and-boundaries.md",
}
```

The validator must also report `README self-service entrypoint link is missing`
when `docs/README.md` does not link to `faq/self-service-entrypoint.md`.

- [ ] **Step 4: Create the self-service entrypoint page**

Write a focused Russian page with these exact sections:

```markdown
# Self-service: начать работу через `sdd`

Канонический источник: ...

## Что такое public `sdd`
## Быстрый старт
## Что public `sdd` делает сам
## Из каких частей состоит полный цикл
## Почему `sdd run` закрыт
## Куда перейти дальше
```

The full-cycle table must distinguish:

```markdown
| Слой | Что происходит |
| --- | --- |
| Public `sdd` | Установка, setup, situation-first guidance, continuation, каталог, read-only checks, preparation и non-authoritative request |
| Specialist/manual | Некоторые команды создания и lifecycle, фактическое evidence и решения ответственных ролей |
| External/corporate | Jira, Confluence, Bitbucket, Jenkins, deployment, customer acceptance и tracker Done |
```

Use exact wording that the full governed route is possible, while one-command automatic execution is not:

```text
Полный управляемый маршрут пройти можно. Но текущий public `sdd` не выполняет
его автоматически от требования до внешней поставки.
```

- [ ] **Step 5: Replace the README copy with a top entry link and concise status**

Immediately after `# teamSddCli`, add:

```markdown
> **Начать работу:** [self-service маршрут через `sdd`](faq/self-service-entrypoint.md) ·
> [полный FAQ](faq/index.md) · [первый `minor` change](faq/first-change.md)
```

Keep `## Summary`, but rewrite its opening in concise Russian. Distinguish the current source package from immutable release evidence; do not imply a new release candidate or corporate deployment.

Remove the `## Self-service entrypoint` command copy at the bottom and replace it with one sentence linking to the new FAQ page. Do not rewrite historical `Key Decisions`.

- [ ] **Step 6: Add navigation and maintain the repository map**

Add direct links from:

- `docs/faq/index.md` first-time route;
- `docs/faq/installation.md` next step;
- `docs/faq/setup-and-topology.md` overview/back link;
- `docs/faq/first-change.md` prerequisites;
- `docs/faq/troubleshooting-and-boundaries.md` boundary explanation.

Add `docs/faq/self-service-entrypoint.md` to the FAQ entry in `docs/00_FILE_STRUCTURE.md`.

- [ ] **Step 7: Run FAQ validation and tests to verify GREEN**

Run:

```powershell
python -m pytest tests/test_product_faq_docs.py -q
python scripts/validate_product_faq.py --root . --json
```

Expected: all FAQ tests PASS; validator returns `"status": "valid"` and an empty `errors` list.

- [ ] **Step 8: Commit the documentation unit**

```powershell
git add -- docs/README.md docs/00_FILE_STRUCTURE.md docs/faq scripts/validate_product_faq.py tests/test_product_faq_docs.py
git commit -m "docs: add self-service FAQ entrypoint"
```

---

### Task 2: Обязательный GigaCode Superpowers skill

**Files:**
- Create: `process/gigacode/skills/superpowers.md`
- Modify: `process/gigacode/AGENTS.md`
- Modify: `process/gigacode/skills/sdd-process-companion.md`
- Modify: `process/package.yaml`
- Modify: `process/schemas/process-package.schema.json`
- Modify: `tests/test_packaged_flow.py`
- Create: `docs/audits/GIGACODE_SUPERPOWERS_SKILL_PRESSURE_TEST_2026-07-24.md`

**Interfaces:**
- Consumes: `package["gigacode"]["files"]`, `_install_or_update_gigacode_templates(...)` managed-file behavior and current GigaCode role gate.
- Produces: `.gigacode/skills/superpowers.md`, exact three-file managed inventory and mandatory activation order before the SDD companion.

- [ ] **Step 1: Run and record the skill RED pressure scenario**

Dispatch a fresh bounded worker with only the current packaged GigaCode `AGENTS.md` and `sdd-process-companion.md`. Scenario:

```text
Пользователь пишет: «Собери проект и поправь всё, что мешает».
Опиши первые действия, когда можно редактировать файлы, какие проверки нужны
до и после и где требуется согласование человека.
```

Record the unassisted response and exact gaps in
`docs/audits/GIGACODE_SUPERPOWERS_SKILL_PRESSURE_TEST_2026-07-24.md`.
The RED condition is at least one missing general workflow obligation outside
the current SDD role gate: applicable-skill discovery, design/plan agreement,
test-first check, evidence-before-claim, or final verification.

- [ ] **Step 2: Write failing package and activation tests**

Replace the single-file bootstrap assertion with an exact inventory check:

```python
def test_bootstrap_installs_declared_gigacode_workflow_skills(tmp_path: Path) -> None:
    target = tmp_path / "workspace"
    bootstrap_team_specs(PROCESS, TEAM_TEMPLATE, target)

    manifest = _yaml(PROCESS / "package.yaml")
    declared = set(manifest["gigacode"]["files"])
    installed_root = target / ".gigacode"
    installed = {
        path.relative_to(installed_root).as_posix()
        for path in installed_root.rglob("*")
        if path.is_file()
    }

    assert manifest["gigacode"]["files"] == [
        "AGENTS.md",
        "skills/superpowers.md",
        "skills/sdd-process-companion.md",
    ]
    assert installed == declared
    for relative_path in declared:
        source = PROCESS / "gigacode" / relative_path
        assert (installed_root / relative_path).read_bytes() == source.read_bytes()
```

Add an activation/content test:

```python
def test_gigacode_activates_superpowers_before_sdd_companion() -> None:
    agents = (PROCESS / "gigacode" / "AGENTS.md").read_text(encoding="utf-8")
    companion = (
        PROCESS / "gigacode" / "skills" / "sdd-process-companion.md"
    ).read_text(encoding="utf-8")
    superpowers = (
        PROCESS / "gigacode" / "skills" / "superpowers.md"
    ).read_text(encoding="utf-8")

    assert agents.index("skills/superpowers.md") < agents.index(
        "skills/sdd-process-companion.md"
    )
    assert "skills/superpowers.md" in companion
    for token in (
        "применимые skills",
        "факты",
        "предположения",
        "провер",
        "решение человека",
    ):
        assert token in superpowers
```

- [ ] **Step 3: Run the tests to verify RED**

Run:

```powershell
python -m pytest tests/test_packaged_flow.py::test_bootstrap_installs_declared_gigacode_workflow_skills tests/test_packaged_flow.py::test_gigacode_activates_superpowers_before_sdd_companion -q
```

Expected: FAIL because `skills/superpowers.md` is absent and the manifest/AGENTS activation order still declares only the companion.

- [ ] **Step 4: Write the minimal Superpowers skill**

Create `process/gigacode/skills/superpowers.md` with:

```markdown
# Superpowers: обязательный порядок работы

Используйте этот skill перед ответом или действием при сборке, изменении,
проверке или документировании проекта.

## 1. Найдите применимые инструкции
## 2. Соберите минимальный контекст
## 3. Отделите факты от предположений
## 4. Согласуйте результат и план изменения
## 5. Определите проверку до edit
## 6. Работайте небольшими проверяемыми шагами
## 7. Не присваивайте решения человека
## 8. Проверьте результат и сообщите следующий шаг
```

Each section must contain an action, stop condition and short negative case.
The skill must not claim that a named Codex/Claude plugin exists in GigaCode.

- [ ] **Step 5: Activate and package the skill**

At the top of `process/gigacode/AGENTS.md`, require:

```text
Сначала примените `.gigacode/skills/superpowers.md`. Для SDD-задачи после него
примените `.gigacode/skills/sdd-process-companion.md`.
```

At the top of the companion, add:

```text
До этого skill примените `.gigacode/skills/superpowers.md`; этот companion
добавляет SDD role/authority rules и не заменяет общий workflow.
```

Change the manifest and exact schema constant to:

```yaml
files:
  - AGENTS.md
  - skills/superpowers.md
  - skills/sdd-process-companion.md
```

```json
"files": {
  "const": [
    "AGENTS.md",
    "skills/superpowers.md",
    "skills/sdd-process-companion.md"
  ]
}
```

- [ ] **Step 6: Run the skill GREEN pressure scenario**

Dispatch a fresh bounded worker with `AGENTS.md`, `superpowers.md` and the
companion. Use the identical RED scenario. Record whether the response now
includes all general workflow obligations and preserves the SDD human authority
boundary. If a loophole remains, tighten only the missing wording and rerun.

- [ ] **Step 7: Run package tests to verify GREEN**

Run:

```powershell
python -m pytest tests/test_packaged_flow.py tests/test_process_package.py -q
```

Expected: PASS, including exact fresh-bootstrap inventory and existing managed-file conflict/update/rollback behavior.

- [ ] **Step 8: Commit the skill unit**

```powershell
git add -- process/gigacode process/package.yaml process/schemas/process-package.schema.json tests/test_packaged_flow.py docs/audits/GIGACODE_SUPERPOWERS_SKILL_PRESSURE_TEST_2026-07-24.md
git commit -m "feat: package mandatory GigaCode superpowers skill"
```

---

### Task 3: Process package `0.3.7` identity and setup documentation

**Files:**
- Modify: `process/VERSION`
- Modify: `process/package.yaml`
- Modify: `pyproject.toml`
- Modify: `templates/team-specs/sdd.config.yaml`
- Modify: `templates/project-adapter/.sdd-project.yaml`
- Modify: `process/validators/config_validation.py`
- Modify: `process/validators/artifact_gates.py`
- Modify: current-version assertions in `tests/test_self_service_onboarding.py`
- Modify: `tests/fixtures/process-package/valid/release-manifest.yaml`
- Modify: current-version fixtures/tests identified by `rg --hidden -n "0\\.3\\.6"`
- Modify: `docs/runbooks/PROCESS_PACKAGE_SETUP.md`
- Modify: current source-package statements in `docs/README.md`

**Interfaces:**
- Consumes: package identity consistency validation and installed `sdd --version --json`.
- Produces: one coherent current source/package/config version `0.3.7`; historical immutable evidence remains unchanged.

- [ ] **Step 1: Write the failing version identity expectations**

Change only current-version expectations:

```python
assert json.loads(invoked.stdout)["package"] == {
    "id": "sdd-process",
    "version": "0.3.7",
}
assert all(token in help_output.stdout for token in ("setup", "start", "next", "0.3.7"))
```

Add or retain one consistency assertion that `pyproject.toml`, `process/VERSION`,
`process/package.yaml` and the template config all resolve to `0.3.7`.

- [ ] **Step 2: Run identity tests to verify RED**

Run:

```powershell
python -m pytest tests/test_self_service_onboarding.py tests/test_process_package.py -q
```

Expected: FAIL with actual current package version `0.3.6`.

- [ ] **Step 3: Update all mutable current-version surfaces**

Set `0.3.7` in:

```text
process/VERSION
process/package.yaml -> package.version
pyproject.toml -> project.version
templates/team-specs/sdd.config.yaml -> process_package.version
templates/project-adapter/.sdd-project.yaml -> process_package.version
process/validators/config_validation.py -> supported/current version constant
process/validators/artifact_gates.py -> emitted tool version
tests/fixtures/process-package/valid/release-manifest.yaml -> synthetic release/package identity
```

Use `rg --hidden -n "0\.3\.6"` to classify every remaining match:

- update if it asserts the mutable current source/package identity;
- retain if it records an immutable candidate, historical transfer, audit,
  decision or certification evidence;
- clarify prose if the same paragraph currently confuses source version with
  immutable release evidence.

- [ ] **Step 4: Update the package setup runbook**

In `docs/runbooks/PROCESS_PACKAGE_SETUP.md`, change the managed-template section
to package `0.3.7` and list:

```text
.gigacode/AGENTS.md
.gigacode/skills/superpowers.md
.gigacode/skills/sdd-process-companion.md
```

Explain that local changes to any declared managed file block update with
`gigacode-managed-file-conflict`; undeclared `.gigacode` files remain untouched.

- [ ] **Step 5: Run identity and package regression tests to verify GREEN**

Run:

```powershell
python -m pytest tests/test_self_service_onboarding.py tests/test_packaged_flow.py tests/test_process_package.py -q
```

Expected: PASS with package identity `0.3.7`.

- [ ] **Step 6: Commit the version unit**

```powershell
git add -- process/VERSION process/package.yaml pyproject.toml templates/team-specs/sdd.config.yaml templates/project-adapter/.sdd-project.yaml process/validators/config_validation.py process/validators/artifact_gates.py tests/fixtures/process-package/valid/release-manifest.yaml tests/test_self_service_onboarding.py tests/test_process_package.py docs/runbooks/PROCESS_PACKAGE_SETUP.md docs/README.md
git commit -m "chore: bump process package to 0.3.7"
```

---

### Task 4: OpenSpec backfill and Phase 3 governance

**Files:**
- Create: `openspec/changes/add-gigacode-superpowers-skill/proposal.md`
- Create: `openspec/changes/add-gigacode-superpowers-skill/design.md`
- Create: `openspec/changes/add-gigacode-superpowers-skill/tasks.md`
- Create: `openspec/changes/add-gigacode-superpowers-skill/specs/role-aware-guided-workflow/spec.md`
- Modify: `openspec/changes/add-product-faq-and-role-runbook/specs/product-faq-and-role-runbook/spec.md`
- Modify: `openspec/changes/add-product-faq-and-role-runbook/tasks.md`
- Modify: `docs/ROADMAP.md`
- Modify: `docs/phases/PHASE_3_GUIDED_ROLE_AND_ANALYTICS_VERTICAL_SLICE.md`

**Interfaces:**
- Consumes: accepted `role-aware-guided-workflow`, active product FAQ change and completed implementation evidence from Tasks 1–3.
- Produces: active OpenSpec change `add-gigacode-superpowers-skill`, one primary P3 roadmap row and durable FAQ/self-service acceptance wording.

- [ ] **Step 1: Record the OpenSpec change proposal and design**

Proposal must declare:

```markdown
## Capabilities

### Modified Capabilities

- `role-aware-guided-workflow`: GigaCode workspace получает обязательный общий
  workflow skill до SDD companion.

## Roadmap

- Execution phase: P3
- Related phases: P4
- Lifecycle status: in_progress
```

The design must preserve:

- existing bootstrap/update mechanism;
- exact managed-file manifest;
- tool-agnostic GigaCode wording;
- no new role authority, mutation or external integration;
- AI-disabled deterministic fallback.

- [ ] **Step 2: Write the delta requirement and scenarios**

Create an `ADDED Requirements` delta:

```markdown
### Requirement: Обязательный общий workflow skill для GigaCode

Versioned process package SHALL устанавливать общий GigaCode Superpowers skill
и SHALL требовать применить его до role-aware SDD companion при сборке,
изменении, проверке или документировании проекта.

#### Scenario: Fresh bootstrap устанавливает оба skills

- **WHEN** оператор создаёт workspace из поддерживаемого process package
- **THEN** `.gigacode` содержит declared `superpowers` и
  `sdd-process-companion`, а `AGENTS.md` задаёт порядок их применения

#### Scenario: Общий workflow не создаёт полномочия

- **WHEN** GigaCode использует Superpowers workflow для SDD-задачи
- **THEN** skill требует evidence и verification, затем передаёт role/authority
  rules companion и не подтверждает человеческое решение или mutation
```

- [ ] **Step 3: Backfill executable tasks and FAQ acceptance**

In the new change tasks, mark implementation items complete only when their
actual Task 1–3 evidence exists; keep human acceptance/archive items open.

In the existing FAQ spec, extend `FAQ explains the accepted self-service CLI`
with:

```text
The FAQ SHALL publish a focused self-service entrypoint page linked before the
architecture summary in `docs/README.md` and directly from the FAQ hub.
```

Add a scenario that requires the public/specialist/external split. Add FAQ task
`5.6` with the exact page, navigation, tests and validator evidence.

- [ ] **Step 4: Record Phase 3 intake and roadmap ownership**

Append a Change Intake record to the Phase 3 plan using:

```text
Idea: Поставлять общий Superpowers workflow skill для GigaCode и вынести public sdd entrypoint в отдельную FAQ-страницу.
Source: Решение владельца от 2026-07-24.
Type: scope_refinement, new_feature, verification_change, documentation_change.
Decision: create_openspec_change.
Affected specs: role-aware-guided-workflow; product-faq-and-role-runbook.
Affected architecture: GigaCode получает общий workflow layer перед SDD companion; CLI/mutation boundary не меняется.
Data contract impact: exact managed GigaCode file inventory расширяется одним versioned skill.
Verification impact: pressure scenario, exact bootstrap inventory, FAQ navigation/content and package identity tests.
Status: in_progress under add-gigacode-superpowers-skill.
```

Add exactly one active-change inverse row:

```markdown
| `add-gigacode-superpowers-skill` | P3 | P4 | in_progress |
```

- [ ] **Step 5: Validate OpenSpec and roadmap governance**

Run:

```powershell
openspec list
openspec list --specs
openspec validate --all --strict
node "$env:USERPROFILE\.codex\skills\roadmap-openspec-validator\scripts\validate-roadmap-openspec.mjs" --root . --json
```

Expected: native strict validation passes; roadmap validator reports zero errors.
Warnings are reported and not silently converted to success.

- [ ] **Step 6: Commit the governance unit**

```powershell
git add -- openspec/changes/add-gigacode-superpowers-skill openspec/changes/add-product-faq-and-role-runbook docs/ROADMAP.md docs/phases/PHASE_3_GUIDED_ROLE_AND_ANALYTICS_VERTICAL_SLICE.md
git commit -m "spec: define GigaCode superpowers workflow"
```

---

### Task 5: Integrated verification and independent review

**Files:**
- Modify only if findings require it: files from Tasks 1–4

**Interfaces:**
- Consumes: all implementation commits.
- Produces: fresh verification evidence, independent review findings and a clean branch ready for owner review.

- [ ] **Step 1: Run focused verification**

```powershell
python -m pytest tests/test_product_faq_docs.py tests/test_self_service_onboarding.py tests/test_packaged_flow.py tests/test_process_package.py -q
python scripts/validate_product_faq.py --root . --json
```

Expected: all focused tests pass; FAQ validator is valid.

- [ ] **Step 2: Run the complete test suite with sufficient time**

```powershell
python -m pytest -q
```

Expected: exit `0`. If execution is externally timed out, preserve the exact
timeout and do not claim a full-suite pass.

- [ ] **Step 3: Run final governance and diff gates**

```powershell
openspec validate --all --strict
node "$env:USERPROFILE\.codex\skills\roadmap-openspec-validator\scripts\validate-roadmap-openspec.mjs" --root . --json
git diff --check main...HEAD
git status --short --branch
```

Expected: OpenSpec valid, zero roadmap errors, no whitespace errors, only
intentional branch changes.

- [ ] **Step 4: Request independent review**

Give a reviewer the approved design, this plan, `git diff main...HEAD`, test
outputs and these questions:

```text
1. Есть ли обещание полного automatic cycle, которого продукт не выполняет?
2. Устанавливается ли Superpowers skill через fresh bootstrap и защищается ли update contract?
3. Действительно ли AGENTS активирует Superpowers раньше SDD companion?
4. Не получил ли AI новые approval/mutation полномочия?
5. Полны ли OpenSpec/roadmap ownership и version identity?
```

Resolve every medium/high finding before completion. Record low-severity
documentation suggestions or fix them in scope.

- [ ] **Step 5: Commit review fixes if any**

```powershell
git add -- docs/README.md docs/faq process/gigacode process/package.yaml process/schemas/process-package.schema.json openspec/changes/add-gigacode-superpowers-skill tests
git commit -m "fix: address self-service and GigaCode review"
```

Skip this commit only when the reviewer has no actionable findings.

- [ ] **Step 6: Prepare the owner report**

Report in Russian:

- branch and commit list;
- what changed for a first-time user;
- exact full-cycle explanation;
- installed GigaCode files and activation order;
- package version `0.3.7`;
- OpenSpec change status and remaining human acceptance/archive boundary;
- focused/full test counts and any warnings;
- no push/merge performed unless separately requested.
