# Central team-specs and AI Role Workflow FAQ Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Дополнить FAQ проверенной практической инструкцией по central `team-specs`, работе с двумя репозиториями и безопасному старту Analyst, Developer и QA с AI и без AI.

**Architecture:** Одна новая общая страница владеет понятиями repository/project/ФП, назначением `team-specs`, sibling/registry layout, актуализацией и cross-project маршрутом. Installation/setup и role runbooks ссылаются на неё, но содержат собственные исполнимые шаги. OpenSpec задаёт acceptance, а deterministic FAQ validator/tests защищают обязательные объяснения и AI write boundaries.

**Tech Stack:** Markdown, Python 3.11+, pytest, существующий `scripts/validate_product_faq.py`, OpenSpec CLI 1.4.1, roadmap/OpenSpec validator.

## Global Constraints

- Пользовательский текст писать по-русски; exact IDs, команды, пути и OpenSpec structural keywords сохранять на английском.
- Объяснять сначала обычными русскими словами и только затем, при необходимости,
  давать точный английский идентификатор в скобках. Не использовать внутренние
  термины процесса там, где человеку достаточно ответа «что это», «зачем»,
  «где лежит», «кто обновляет» и «что сделать дальше».
- Один code repository **обычно** регистрируется как один technical project ID; не изображать это validator-enforced uniqueness invariant.
- Technical project не равен ФП; project ↔ FP many-to-many storage остаётся planned в `define-fp-analytics-publication-model`, `0/70`.
- `team-specs` описывать как центральный каталог и управляющий слой, а не «главный проект», code monorepo или хранилище всего.
- `add-ai-analyst-discovery` считать реализованным на уровне package/FAQ, но не human-accepted: `12/13`, first-time walkthrough открыт.
- Developer/QA AI читает `team-specs`, пишет только в назначенный code/test repository и требует отдельного разрешения перед central evidence update.
- Analyst AI начинает read-only; один non-authoritative draft в named path разрешается отдельно и не означает acceptance.
- Не придумывать публичные `sdd context`, `sdd config`, clone, pull или multi-repository orchestration commands.
- `validate_process_config.py` и `build_read_pack.py` показывать как specialist routes, отсутствующие в публичном `sdd op list`.
- Не закрывать FAQ task 4.4 или AI discovery task 5.3; automated checks не заменяют human walkthrough.
- Не менять `.pytest-tmp-faq-20260724/`.

---

## File Structure

**Create:**

- `docs/faq/multi-repository-workspace.md` — единое человекочитаемое объяснение central topology, двух checkout, AI context, maintenance и cross-project work.

**Modify:**

- `docs/faq/index.md` — прямой вход на новую страницу.
- `docs/faq/installation.md` — короткое правило repository/project/FP и следующий topology step.
- `docs/faq/setup-and-topology.md` — точный adapter layout, current/planned boundary и три практических сценария.
- `docs/faq/glossary.md` — короткие определения repository, technical project, ФП, `team-specs`, adapter, bounded read pack.
- `docs/faq/roles/process-owner.md` — onboarding и event-driven maintenance.
- `docs/faq/roles/analyst.md` — полный старт с central repo и implemented discovery.
- `docs/faq/roles/developer.md` — полный two-repository AI-assisted implementation route.
- `docs/faq/roles/qa.md` — полный two-repository scenario-to-test route.
- `docs/faq/ai-collaboration.md` — role-specific permission matrix, multi-root и read-pack fallback.
- `scripts/validate_product_faq.py` — required page/questions/tokens и role-specific diagnostics.
- `tests/test_product_faq_docs.py` — positive/negative contract tests.
- `openspec/changes/add-product-faq-and-role-runbook/proposal.md` — approved intake.
- `openspec/changes/add-product-faq-and-role-runbook/design.md` — shared-page и permission decisions.
- `openspec/changes/add-product-faq-and-role-runbook/specs/product-faq-and-role-runbook/spec.md` — acceptance scenarios.
- `openspec/changes/add-product-faq-and-role-runbook/tasks.md` — task 5.7 и evidence.
- `docs/audits/PRODUCT_FAQ_AND_ROLE_RUNBOOK_ACCEPTANCE_AUDIT_2026-07-24.md` — finding и verification evidence.
- `docs/CURRENT_PROJECT_AUDIT.md` — текущий FAQ status.
- `docs/00_FILE_STRUCTURE.md` — новая FAQ page и этот plan.

**Reference only:**

- `docs/superpowers/specs/2026-07-24-central-team-specs-and-ai-role-workflow-faq-design.md`.
- `docs/audits/CENTRAL_TEAM_SPECS_AI_ROLE_WORKFLOW_REALITY_AUDIT_2026-07-24.md`.
- `openspec/specs/repo-topology-config/spec.md`.
- `openspec/changes/define-fp-analytics-publication-model/`.
- `openspec/changes/add-ai-analyst-discovery/`.
- `templates/project-adapter/.sdd-project.yaml`.
- `docs/runbooks/PROCESS_PACKAGE_SETUP.md`.
- `docs/runbooks/WEAK_MODEL_OPERATING_KIT.md`.

---

### Task 1: Extend the governed FAQ contract

**Files:**

- Modify: `openspec/changes/add-product-faq-and-role-runbook/proposal.md`
- Modify: `openspec/changes/add-product-faq-and-role-runbook/design.md`
- Modify: `openspec/changes/add-product-faq-and-role-runbook/specs/product-faq-and-role-runbook/spec.md`
- Modify: `openspec/changes/add-product-faq-and-role-runbook/tasks.md`

**Interfaces:**

- Consumes: approved design, reality audit, accepted `repo-topology-config`.
- Produces: task 5.7 and acceptance scenarios used by validator/tests.

- [ ] **Step 1: Add the approved intake**

Append to `proposal.md`:

```markdown
## Change Intake — central team-specs and AI role workflow

```text
Idea: Объяснить repository/project/ФП, назначение central team-specs, работу
Analyst/Developer/QA с двумя репозиториями и безопасный AI-assisted route.
Source: Human feedback and explicit permission decision 2026-07-24.
Type: scope_refinement, documentation_change, verification_change
Decision: adopt_now
Reason: Existing setup and role pages do not let a first-time participant use
the accepted central topology in daily work without reconstructing specialist
contracts.
Affected specs: product-faq-and-role-runbook; references accepted
repo-topology-config and planned define-fp-analytics-publication-model.
Affected architecture: No topology change.
Data contract impact: None.
Verification impact: New required page, role sections, permission tokens and
positive/negative documentation tests.
Status: Queued as task 5.7; task 4.4 remains the human walkthrough gate.
```
```

- [ ] **Step 2: Add design decisions**

Add to `design.md` under `## Decisions`:

```markdown
- Repository topology получает одну общую FAQ-страницу
  `multi-repository-workspace.md`. Она владеет понятиями repository/project/ФП,
  назначением `team-specs`, sibling/registry layout, maintenance и
  cross-project route; role pages не копируют весь topology contract.
- Первый поддерживаемый default формулируется как «один code repository обычно
  регистрируется как один technical project ID». Это не hard uniqueness
  invariant: monorepo и несколько project IDs на repository требуют отдельного
  принятого topology contract.
- Для Developer/QA AI `team-specs` read-only, а write scope ограничен
  назначенным code/test repository. Central traceability/evidence обновляется
  только отдельным разрешённым действием. Analyst draft также требует
  отдельного разрешения на named path и остаётся non-authoritative.
- Sibling multi-root является основным local route. `validate_process_config.py`
  и `build_read_pack.py` описываются как specialist fallback; несуществующие
  public context/clone/pull commands не документируются.
```

- [ ] **Step 3: Add acceptance scenarios**

Add to the `Navigable product FAQ` requirement:

```markdown
#### Scenario: Пользователь понимает центральную topology

- **WHEN** новый участник открывает страницу multi-repository workspace
- **THEN** он отличает code repository, technical project и ФП
- **AND** понимает, что `team-specs` — центральный каталог, а не главный проект
- **AND** видит, что one-repo/one-project является default, а project ↔ FP many-to-many storage пока planned
```

Add to `Role-oriented start runbooks`:

```markdown
#### Scenario: Developer и QA начинают работу с двумя репозиториями

- **WHEN** Developer или QA получает change из central `team-specs`
- **THEN** runbook показывает sibling checkout, project adapter validation, multi-root workspace, exact bounded sources, write scope, проверки, handoff и separate central evidence permission
- **AND** не требует копировать specification text в code repository
```

Add to `AI collaboration rules`:

```markdown
#### Scenario: AI помогает реализации без изменения canonical requirements

- **WHEN** Developer или QA разрешает AI анализировать change и project code
- **THEN** AI читает bounded `team-specs` context, сначала строит scenario-to-code/test plan и пишет только в разрешённые project paths
- **AND** central traceability/evidence update требует отдельного human permission
- **AND** при недоступном sibling root используется authority-labelled specialist read pack
```

- [ ] **Step 4: Add task 5.7**

Append:

```markdown
- [ ] 5.7 Добавить человекочитаемый central `team-specs` и multi-repository
  workflow: repository/project/ФП, актуализация, sibling/registry setup,
  zero-start Analyst/Developer/QA, AI read/write boundaries, specialist
  read-pack fallback и cross-project decomposition; закрепить validator/tests.
```

- [ ] **Step 5: Validate the contract**

Run:

```powershell
openspec validate add-product-faq-and-role-runbook --strict
openspec instructions apply --change add-product-faq-and-role-runbook --json
```

Expected: valid; progress `18/20`, with tasks 4.4 and 5.7 open.

- [ ] **Step 6: Commit**

```powershell
git add -- openspec/changes/add-product-faq-and-role-runbook
git commit -m "spec: require central specs ai role faq"
```

---

### Task 2: Add RED tests and deterministic content contracts

**Files:**

- Modify: `tests/test_product_faq_docs.py`
- Modify: `scripts/validate_product_faq.py`

**Interfaces:**

- Produces: `REQUIRED_MULTI_REPO_TOKENS` and `ROLE_WORKSPACE_TOKENS`.
- Diagnostic strings:
  - `multi-repository FAQ detail is missing`
  - `role workspace detail is missing`

- [ ] **Step 1: Write the failing positive test**

Add:

```python
def test_multi_repository_workspace_and_role_routes_are_practical() -> None:
    faq = ROOT / "docs" / "faq"
    index = (faq / "index.md").read_text(encoding="utf-8")
    assert "](multi-repository-workspace.md)" in index

    workspace = (faq / "multi-repository-workspace.md").read_text(
        encoding="utf-8"
    )
    for token in (
        "один code repository обычно регистрируется как один technical project ID",
        "technical project не равен ФП",
        "many-to-many",
        "`team-specs` — не «главный проект»",
        "sibling:team-specs",
        "registry:central",
        "build_read_pack.py",
        "не входит в публичный `sdd op list`",
        "AI читает `team-specs`",
        "отдельное разрешение",
        "Central change",
        "отдельный code PR",
        "`define-fp-analytics-publication-model`",
        "0/70",
        "`add-ai-analyst-discovery`",
        "12/13",
    ):
        assert token in workspace

    role_tokens = {
        "analyst.md": (
            "## Настройка рабочего места с нуля",
            "analyst-discovery",
            "named draft path",
        ),
        "developer.md": (
            "## Настройка двух репозиториев",
            "team-specs: read-only",
            "requirement/scenario -> current code -> proposed files -> required tests",
        ),
        "qa.md": (
            "## Настройка двух репозиториев",
            "project/tests: write",
            "scenario-to-test matrix",
        ),
    }
    for name, tokens in role_tokens.items():
        text = (faq / "roles" / name).read_text(encoding="utf-8")
        for token in tokens:
            assert token in text, f"{name}: missing {token}"
```

- [ ] **Step 2: Write the failing negative test**

Add:

```python
def test_validator_requires_multi_repository_and_role_permission_contract(
    tmp_path: Path,
) -> None:
    from scripts.validate_product_faq import validate_product_faq

    faq = tmp_path / "docs" / "faq"
    roles = faq / "roles"
    roles.mkdir(parents=True)
    (faq / "multi-repository-workspace.md").write_text(
        "# Workspace\nКанонический источник: x\n"
        "<!-- faq-question: multi-repository-workspace -->\n"
        "Используйте две репы.\n",
        encoding="utf-8",
    )
    for name in ("analyst.md", "developer.md", "qa.md"):
        (roles / name).write_text(
            f"# {name}\nКанонический источник: x\n",
            encoding="utf-8",
        )

    errors = validate_product_faq(tmp_path)
    assert any("multi-repository FAQ detail is missing" in error for error in errors)
    assert any("role workspace detail is missing" in error for error in errors)
```

- [ ] **Step 3: Run RED**

```powershell
python -m pytest tests/test_product_faq_docs.py::test_multi_repository_workspace_and_role_routes_are_practical tests/test_product_faq_docs.py::test_validator_requires_multi_repository_and_role_permission_contract -q
```

Expected: both FAIL because the page and diagnostics do not exist.

- [ ] **Step 4: Add validator constants**

Add `"multi-repository-workspace"` and `"central-team-specs-purpose"` to
`REQUIRED_QUESTIONS`, and `"multi-repository-workspace.md"` to
`REQUIRED_PAGES`.

Add:

```python
REQUIRED_MULTI_REPO_TOKENS = frozenset(
    {
        "один code repository обычно регистрируется как один technical project ID",
        "technical project не равен ФП",
        "many-to-many",
        "`team-specs` — не «главный проект»",
        "sibling:team-specs",
        "registry:central",
        "build_read_pack.py",
        "не входит в публичный `sdd op list`",
        "AI читает `team-specs`",
        "отдельное разрешение",
        "Central change",
        "отдельный code PR",
        "define-fp-analytics-publication-model",
        "0/70",
        "add-ai-analyst-discovery",
        "12/13",
    }
)

ROLE_WORKSPACE_TOKENS = {
    "analyst.md": {
        "## Настройка рабочего места с нуля",
        "analyst-discovery",
        "named draft path",
    },
    "developer.md": {
        "## Настройка двух репозиториев",
        "team-specs: read-only",
        "requirement/scenario -> current code -> proposed files -> required tests",
    },
    "qa.md": {
        "## Настройка двух репозиториев",
        "project/tests: write",
        "scenario-to-test matrix",
    },
}
```

- [ ] **Step 5: Add page and role diagnostics**

Inside `for page in pages` add:

```python
        if page.name == "multi-repository-workspace.md":
            for token in sorted(REQUIRED_MULTI_REPO_TOKENS):
                if token not in text:
                    errors.append(
                        "multi-repository FAQ detail is missing: "
                        f"{page.relative_to(root)} -> {token}"
                    )
        if page.parent == faq / "roles" and page.name in ROLE_WORKSPACE_TOKENS:
            for token in sorted(ROLE_WORKSPACE_TOKENS[page.name]):
                if token not in text:
                    errors.append(
                        "role workspace detail is missing: "
                        f"{page.relative_to(root)} -> {token}"
                    )
```

- [ ] **Step 6: Run negative GREEN**

```powershell
python -m pytest tests/test_product_faq_docs.py::test_validator_requires_multi_repository_and_role_permission_contract tests/test_product_faq_docs.py::test_validator_reports_missing_required_page_and_role_section -q
```

Expected: `2 passed`; positive test remains RED until Tasks 3–6.

- [ ] **Step 7: Commit**

```powershell
git add -- scripts/validate_product_faq.py tests/test_product_faq_docs.py
git commit -m "test: require multi repository role faq"
```

---

### Task 3: Add the shared multi-repository workspace page

**Files:**

- Create: `docs/faq/multi-repository-workspace.md`
- Modify: `docs/faq/index.md`
- Modify: `docs/faq/glossary.md`
- Modify: `docs/00_FILE_STRUCTURE.md`

**Interfaces:**

- Consumes: required tokens from Task 2.
- Produces: canonical human-readable explanation linked by all role pages.

- [ ] **Step 1: Create the page header and terminology**

Start the page with:

```markdown
# Как работать, когда требования и код находятся в разных репозиториях

Канонический источник: [topology contract](../../openspec/specs/repo-topology-config/spec.md),
[process setup](../runbooks/PROCESS_PACKAGE_SETUP.md),
[AI operating kit](../runbooks/WEAK_MODEL_OPERATING_KIT.md),
[reality audit](../audits/CENTRAL_TEAM_SPECS_AI_ROLE_WORKFLOW_REALITY_AUDIT_2026-07-24.md)
и [planned FP model](../../openspec/changes/define-fp-analytics-publication-model/).

<!-- faq-question: multi-repository-workspace -->
<!-- faq-question: central-team-specs-purpose -->

Короткое правило: один code repository обычно регистрируется как один technical project ID.
Technical project не равен ФП. Одна ФП может использовать несколько проектов,
а один проект может обслуживать несколько ФП — это many-to-many связь.

`team-specs` — не «главный проект». Это центральный каталог: здесь находятся
общие требования, changes, владельцы, связи, решения и ссылки на результаты.
Код и тесты остаются в project repositories.
```

- [ ] **Step 2: Add current versus planned boundaries**

Add a table:

```markdown
## Что работает сейчас, а что только запланировано

| Возможность | Статус |
| --- | --- |
| Один adapter с одним `project_id` | Работает сейчас как поддерживаемый default |
| `sibling:`, bounded `path:` и explicit `registry:` | Работает сейчас |
| Specialist config validation | Работает через `validate_process_config.py` |
| Specialist authority-labelled read pack | Работает через `build_read_pack.py` |
| Analyst discovery companion | Реализован change `add-ai-analyst-discovery`, `12/13`; human walkthrough открыт |
| FP catalogue, `fps/` и project ↔ FP registry | Запланировано в `define-fp-analytics-publication-model`, `0/70` |
| Автоматический clone/pull/context orchestration | Недоступно |
```

State directly that `build-read-pack` and `validate-process-config` do not
appear in public `sdd op list`.

- [ ] **Step 3: Add exact sibling and registry examples**

Use:

```text
C:/work/product/
├── team-specs/
├── client-profile/
├── confirmation/
└── common-platform/
```

and:

```yaml
schema_version: "1.1"
config_schema_version: "1.1"
project_id: client-profile
team_specs:
  reference: sibling:team-specs
  config_path: sdd.config.yaml
```

Explain `registry:central` as the fallback and show the real specialist check:

```text
python scripts/validate_process_config.py C:/work/product/client-profile --registry central=C:/work/product/team-specs --json
```

Do not show an absolute path inside committed YAML.

- [ ] **Step 4: Add source ownership and maintenance**

Include two lists (`team-specs` owns / project repository owns), the role table
from the approved design, and the event sequence:

```text
project onboarding -> change -> code PR -> tests -> release -> FP reconciliation -> publication
```

Explain that central storage is justified only for information connecting
several projects, FP areas or releases.

- [ ] **Step 5: Add practical AI context**

Include:

```markdown
AI читает `team-specs`, но в Developer/QA session не изменяет его.
Write-доступ выдаётся только к named project paths. Для записи PR/test links,
traceability или evidence в `team-specs` человек даёт отдельное разрешение.
```

Add direct multi-root steps. For the specialist fallback, link to
`docs/runbooks/WEAK_MODEL_OPERATING_KIT.md` and explain that it requires a
separately prepared YAML request with labelled sources. Do not publish a
copy-paste command with a fictional request path and do not call this a public
self-service flow. The runbook is the canonical source for the current
`build_read_pack.py` invocation and request prerequisites.

- [ ] **Step 6: Add cross-project example**

Use:

```text
Central change
├── client-profile task -> отдельный code PR
├── confirmation task -> отдельный code PR
└── frontend task -> отдельный code PR
```

Explain one project ID, one non-overlapping write scope, separate checks and a
combined integration check. Release aggregation must preserve FP ownership.

- [ ] **Step 7: Update navigation and glossary**

Add to `index.md`:

```markdown
- [Как работать с `team-specs`, code repositories и AI](multi-repository-workspace.md)
```

Add glossary definitions for `Code repository`, `Technical project`, `ФП`,
`team-specs`, `Project adapter`, `Bounded read pack`.

Register the page in `docs/00_FILE_STRUCTURE.md`.

- [ ] **Step 8: Run the shared-page checks**

```powershell
python scripts/validate_product_faq.py --json
python -m pytest tests/test_product_faq_docs.py::test_validator_requires_multi_repository_and_role_permission_contract -q
```

Expected: validator still invalid only for missing role tokens; negative test
passes.

- [ ] **Step 9: Commit**

```powershell
git add -- docs/faq/multi-repository-workspace.md docs/faq/index.md docs/faq/glossary.md docs/00_FILE_STRUCTURE.md
git commit -m "docs: explain central multi repository workspace"
```

---

### Task 4: Expand installation, setup and process-owner operations

**Files:**

- Modify: `docs/faq/installation.md`
- Modify: `docs/faq/setup-and-topology.md`
- Modify: `docs/faq/roles/process-owner.md`

**Interfaces:**

- Consumes: shared page from Task 3.
- Produces: executable setup route without duplicating role implementation.

- [ ] **Step 1: Add installation orientation**

Before `## Следующий шаг` add:

```markdown
## Где будут лежать требования и код

Установка `sdd` не объединяет все проекты в одну репу. В первом поддерживаемом
default один code repository обычно регистрируется как один technical project
ID. Общие requirements и changes хранятся в central `team-specs`, а код и
тесты — в project repository. Technical project не равен ФП.

Перед первым рабочим change прочитайте
[как подготовить два репозитория](multi-repository-workspace.md).
```

- [ ] **Step 2: Clarify setup topology**

After the generated tree add:

```markdown
`team-specs` — не главный бизнес-проект и не папка со всем кодом. Это
центральный каталог общих требований, изменений, владельцев и ссылок на
проверяемые результаты. Текущий `teamSsdCli` разрабатывает framework и не
должен использоваться как production `team-specs`.
```

Add the default/caveat and label FP many-to-many as planned at `0/70`.

- [ ] **Step 3: Add three practical setup scenarios**

Create sections:

```markdown
## Сценарий 1. Подключить новый code repository
## Сценарий 2. Зарегистрировать или изменить ФП
## Сценарий 3. Подготовить cross-FP release
```

Scenario 1 must include `projects.yaml`, owner zones, adapter copy, specialist
validation and Tech Lead review.

Scenario 2 must explicitly stop:

```markdown
FP catalogue и `fps/<fp-id>/` пока planned. До реализации
`define-fp-analytics-publication-model` не создавайте локальный несовместимый
registry как будто он поддерживается framework.
```

Scenario 3 must explain current manual references and planned release manifests
without claiming publisher availability.

- [ ] **Step 4: Expand process-owner maintenance**

Add `## Поддержание central каталога` under the existing route with:

1. onboarding trigger;
2. rename/split/retire trigger;
3. owner-zone review;
4. process/OpenSpec pin update through reviewed change;
5. dangling ID/version validation;
6. no secrets;
7. no silent removal of historical IDs.

- [ ] **Step 5: Verify documented specialist commands**

Run:

```powershell
python -m pytest tests/test_validate_process_config.py -q
python scripts/sdd.py op list --json
```

Expected: the focused validator contract tests pass; the public list omits
`validate-process-config` and `build-read-pack`, matching the wording. Do not
use `--help`: this specialist script intentionally exposes only the positional
`START`, repeatable `--registry ID=PATH`, and optional `--json` contract.

- [ ] **Step 6: Commit**

```powershell
git add -- docs/faq/installation.md docs/faq/setup-and-topology.md docs/faq/roles/process-owner.md
git commit -m "docs: add central topology setup from zero"
```

---

### Task 5: Expand the Analyst zero-start route

**Files:**

- Modify: `docs/faq/roles/analyst.md`
- Modify: `docs/faq/ai-collaboration.md`

**Interfaces:**

- Consumes: implemented `add-ai-analyst-discovery` contract.
- Produces: Analyst-specific bounded draft permission.

- [ ] **Step 1: Add workspace setup**

Add:

```markdown
## Настройка рабочего места с нуля

1. Установите и проверьте package `0.3.7`.
2. Получите read-доступ к отдельному repository `team-specs`.
3. Обновите checkout и запишите current commit в рабочую сводку.
4. Найдите change/FP по stable ID; не просматривайте все project specs.
5. Для supporting code context подключайте только названный project repository.
6. Не добавляйте credentials, private exports или production data в AI context.
```

- [ ] **Step 2: Add the practical discovery route**

Document the implemented flow:

```text
простая идея
-> показать план тем
-> получить разрешение
-> задавать по одному вопросу
-> confirmed/proposed/unknown/conflict
-> подтвердить итоговую сводку
-> отдельное разрешение на один named draft path
-> отдельное предложение перейти к первой команде
```

State: change `add-ai-analyst-discovery` is `12/13`; human walkthrough remains.

- [ ] **Step 3: Add a copyable Analyst prompt**

Use a full synthetic prompt with:

```text
Роль человека: Analyst.
Central repository: C:/work/product/team-specs.
Идея: добавить фильтрацию клиентского профиля по региону.
Начни в режиме analyst-discovery.
Сначала покажи темы интервью и спроси разрешение.
Задавай по одному вопросу.
Разделяй confirmed, proposed, unknown и conflict.
До подтверждения итоговой сводки ничего не записывай.
После подтверждения предложи только один следующий draft и назови exact path.
Не подтверждай classification, DoR или technical impact.
```

- [ ] **Step 4: Explain candidate project mapping**

Analyst may propose affected project IDs, but Tech Lead confirms technical
impact. Planned FP registry is not represented as implemented.

- [ ] **Step 5: Update AI collaboration**

Add an Analyst permission row:

```markdown
| Analyst discovery | read `team-specs`; ask one question; prepare summary | write one non-authoritative draft only after permission for a named path | confirm facts/class/DoR or create the whole package |
```

- [ ] **Step 6: Run focused role checks**

```powershell
python -m pytest tests/test_product_faq_docs.py::test_multi_repository_workspace_and_role_routes_are_practical tests/test_product_faq_docs.py::test_ai_walkthrough_starts_with_plain_language_discovery -q
```

Expected: first test still fails only on Developer/QA tokens; discovery test
passes.

- [ ] **Step 7: Commit**

```powershell
git add -- docs/faq/roles/analyst.md docs/faq/ai-collaboration.md
git commit -m "docs: add analyst central workspace start"
```

---

### Task 6: Add complete Developer and QA two-repository routes

**Files:**

- Modify: `docs/faq/roles/developer.md`
- Modify: `docs/faq/roles/qa.md`
- Modify: `docs/faq/ai-collaboration.md`

**Interfaces:**

- Produces: final role tokens required by Task 2.

- [ ] **Step 1: Add Developer workspace setup**

Add:

```markdown
## Настройка двух репозиториев

```text
C:/work/product/
├── team-specs/       # team-specs: read-only в implementation session
└── client-profile/   # project/src и project/tests: bounded write
```

1. Обновите оба checkout и сохраните их commit IDs.
2. Откройте parent folder или IDE multi-root workspace.
3. Проверьте `.sdd-project.yaml` specialist validator-ом.
4. Убедитесь, что AI tool действительно видит оба workspace roots.
5. Укажите exact change path, project ID и разрешённые write paths.
6. Если sibling root недоступен, запросите specialist bounded read pack.
```

- [ ] **Step 2: Add Developer impact-first flow**

Require the exact plan shape:

```text
requirement/scenario -> current code -> proposed files -> required tests
```

Add the synthetic example `CLIENT-142-add-region-filter`, a table mapping
`REQ-CLIENT-014/SCEN-02` to `src/profile/query.py` and unit/integration tests,
and a blocked row for an undefined scenario.

- [ ] **Step 3: Add Developer AI prompt and write boundary**

Use:

```text
Работай как Developer над CLIENT-142-add-region-filter.
Читай C:/work/product/team-specs/openspec/changes/CLIENT-142-add-region-filter.
Изменять разрешено только C:/work/product/client-profile/src и tests.
Сначала подготовь requirement/scenario -> current code -> proposed files ->
required tests и остановись для review.
Не меняй team-specs, classification, lifecycle или approval.
Каждую command class выполняй только после отдельного разрешения.
```

Add separate permission wording for central PR/test evidence.

- [ ] **Step 4: Add QA workspace setup**

Add:

```markdown
## Настройка двух репозиториев

- `team-specs`: read-only;
- `project/src`: read-only by default;
- `project/tests`: write;
- central evidence update: отдельное разрешение.
```

Include update/revision checks and exact change/scenario source paths.

- [ ] **Step 5: Add QA scenario-to-test route**

Require a `scenario-to-test matrix` with columns:

```markdown
| Scenario ID | Expected behavior | Existing test | Needed test | Actual result | Evidence |
```

Explain positive, negative, regression and unavailable cases, failed-run
retention, and classification of defect/ambiguity/missing test/unavailable
evidence.

- [ ] **Step 6: Add QA AI prompt**

Use:

```text
Работай как QA assistant для CLIENT-142-add-region-filter.
Requirements читай только из C:/work/product/team-specs.
Код C:/work/product/client-profile/src только читай.
Писать разрешено только в C:/work/product/client-profile/tests.
Сначала составь scenario-to-test matrix и остановись для review.
Не выводи expected behavior из текущей реализации.
Не отмечай QA gate, DoD, risk или release принятыми.
```

- [ ] **Step 7: Expand the general AI permission matrix**

Add rows for Developer and QA and a section:

```markdown
## Работа AI с двумя repository roots
```

Explain direct multi-root, code-only sandbox blocker, specialist read-pack
fallback, separate central update and cross-project session isolation.

- [ ] **Step 8: Run FAQ GREEN**

```powershell
python scripts/validate_product_faq.py --json
python -m pytest tests/test_product_faq_docs.py -q
```

Expected: validator `valid`, all FAQ tests pass.

- [ ] **Step 9: Commit**

```powershell
git add -- docs/faq/roles/developer.md docs/faq/roles/qa.md docs/faq/ai-collaboration.md
git commit -m "docs: add developer qa multi repository ai routes"
```

---

### Task 7: Reconcile evidence and run final gates

**Files:**

- Modify: `openspec/changes/add-product-faq-and-role-runbook/tasks.md`
- Modify: `docs/audits/PRODUCT_FAQ_AND_ROLE_RUNBOOK_ACCEPTANCE_AUDIT_2026-07-24.md`
- Modify: `docs/CURRENT_PROJECT_AUDIT.md`

**Interfaces:**

- Consumes: all passing documentation checks.
- Produces: task 5.7 evidence; tasks 4.4 and AI discovery 5.3 remain open.

- [ ] **Step 1: Perform the reviewer-style human readability check**

Answer from FAQ alone:

1. Why is `team-specs` not a main project?
2. What does one repository normally map to?
3. What is current versus planned for FP mappings?
4. How does Developer AI see specs and code?
5. Where may Developer and QA AI write?
6. How is central evidence updated?
7. What happens for a three-project change?
8. Which specialist tools exist but are absent from public `sdd op list`?

Expected answers must match the reality audit.

- [ ] **Step 2: Mark task 5.7 complete**

Change only task 5.7 to `[x]` and add:

```markdown
  Evidence (2026-07-24): reality audit, governed shared-page/role contract,
  FAQ validator and tests, strict OpenSpec and roadmap/OpenSpec validation
  passed. FAQ task 4.4 and AI discovery task 5.3 remain independent first-time
  human walkthrough gates.
```

- [ ] **Step 3: Add acceptance-audit finding**

Add `FAQ-ACC-007` describing the original topology/role practical gap,
remediation files, current/planned boundary and exact verification table.

- [ ] **Step 4: Update Current Project Audit**

Record:

- central multi-repository page exists;
- role zero-start routes exist;
- AI read/write/evidence boundary is explicit;
- specialist/public command boundary is honest;
- FP storage remains planned `0/70`;
- FAQ is `19/20` after task 5.7, with only 4.4 open;
- AI discovery remains `12/13`, with only its human walkthrough open.

- [ ] **Step 5: Run focused and governance verification**

```powershell
python scripts/validate_product_faq.py --json
python -m pytest tests/test_product_faq_docs.py tests/test_validate_process_config.py tests/test_weak_model_kit.py -q
openspec list
openspec list --specs
openspec validate --all --strict
node "$env:USERPROFILE\.codex\skills\roadmap-openspec-validator\scripts\validate-roadmap-openspec.mjs" --root "C:\Users\danoc\Documents\projects\teamSsdCli"
git diff --check
```

Expected:

- FAQ validator valid;
- focused suites pass;
- OpenSpec strict zero failures;
- roadmap validator zero errors and the same unrelated lifecycle warnings;
- FAQ `19/20`, only 4.4 open;
- AI discovery `12/13`, only 5.3 open;
- publication model `0/70`;
- no claim that the full repository suite is green.

- [ ] **Step 6: Run final doc/reality scan**

```powershell
rg -n "sdd context|sdd config|автоматически клонирует|автоматически обновляет" docs/faq
rg -n "define-fp-analytics-publication-model|0/70|add-ai-analyst-discovery|12/13" docs/faq docs/CURRENT_PROJECT_AUDIT.md
```

Expected: first command returns no unsupported positive command claims; second
shows current/planned status in the shared page and audit.

- [ ] **Step 7: Commit**

```powershell
git add -- openspec/changes/add-product-faq-and-role-runbook/tasks.md docs/audits/PRODUCT_FAQ_AND_ROLE_RUNBOOK_ACCEPTANCE_AUDIT_2026-07-24.md docs/CURRENT_PROJECT_AUDIT.md
git commit -m "docs: record central specs faq evidence"
```

- [ ] **Step 8: Push after successful verification**

```powershell
git push origin main
```

Expected: `main` is synchronized with `origin/main`; the untracked
`.pytest-tmp-faq-20260724/` remains untouched.

---

## Completion State

After execution:

- a first-time reader can distinguish repository, technical project and ФП;
- `team-specs` is understood as a thin central catalogue, not a main project;
- installation/setup show a real sibling/registry route;
- Analyst, Developer and QA can start from zero with AI or without AI;
- AI context and write permissions are explicit and role-specific;
- cross-project work is decomposed into separate tasks/PRs;
- specialist versus public command boundaries match package `0.3.7`;
- planned FP storage/publication is not represented as delivered;
- automated checks protect the new content;
- human walkthrough tasks remain open and visible.
