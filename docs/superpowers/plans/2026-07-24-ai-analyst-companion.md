# AI Analyst Companion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Расширить поставляемый `sdd-process-companion` человекочитаемым режимом аналитического интервью, который по разрешению уточняет сырую идею, формирует проверяемую сводку и черновики, а затем отдельно предлагает перейти к управляемым командам.

**Architecture:** Один существующий packaged skill остаётся входной точкой и маршрутизирует запрос в `analyst-discovery` либо `guided-change`. Поведение описывается в OpenSpec, проверяется контрактными тестами текста и установки пакета, объясняется в FAQ и не меняет детерминированные полномочия CLI. Состояние интервью хранится только в текущем диалоге; новый runtime, schema или автономный агент не добавляются.

**Tech Stack:** Markdown/OpenSpec, Python 3.11+, pytest, существующий FAQ validator, Git.

## Global Constraints

- Проектная документация и новое OpenSpec prose пишутся на русском; стабильные ID, пути и CLI tokens остаются на английском.
- AI не подтверждает classification, DoR/DoD, risk, release, archive, merge и другие human authority gates.
- До отдельного согласия AI не создаёт файлы, не запускает команды и не выполняет `next_command`.
- Перед каждой командой или edit AI показывает exact action, ожидаемый результат, что изменится и что не изменится, затем ждёт отдельное «выполняй».
- `analyst-discovery` сначала показывает короткий список тем, затем после разрешения задаёт по одному вопросу.
- `confirmed`, `proposed`, `unknown` и `conflict` различаются в evidence-сводке; догадки AI не становятся фактами.
- Ручной и AI-disabled маршруты сохраняются.
- Не добавлять автономный runtime, внешние публикации или новый конкурирующий companion skill.

---

### Task 1: Зафиксировать контракт аналитического интервью в OpenSpec

**Files:**
- Create: `openspec/changes/add-ai-analyst-discovery/proposal.md`
- Create: `openspec/changes/add-ai-analyst-discovery/design.md`
- Create: `openspec/changes/add-ai-analyst-discovery/tasks.md`
- Create: `openspec/changes/add-ai-analyst-discovery/specs/role-aware-guided-workflow/spec.md`

**Interfaces:**
- Consumes: принятый контракт `openspec/specs/role-aware-guided-workflow/spec.md` и дизайн `docs/superpowers/specs/2026-07-24-ai-analyst-discovery-skill-design.md`.
- Produces: requirements `Analyst discovery interview`, `Discovery evidence summary`, `Permission-bound draft creation` и `Explicit guided-change handoff`.

- [ ] **Step 1: Прочитать текущий accepted contract и проверить уникальность change ID**

Run:

```powershell
openspec list
openspec list --specs
Get-Content -Raw openspec/specs/role-aware-guided-workflow/spec.md
```

Expected: change `add-ai-analyst-discovery` отсутствует; accepted capability `role-aware-guided-workflow` доступна.

- [ ] **Step 2: Создать proposal и design с точной границей изменения**

В `proposal.md` записать:

```markdown
# Change: добавить аналитическое интервью в AI companion

## Зачем

Текущий учебный маршрут начинает работу с уже точной постановки и заставляет
пользователя копировать длинный prompt. Аналитику нужен простой вход, который
помогает уточнить сырую идею и подготовить source-aware черновик без передачи AI
человеческих полномочий.

## Что меняется

- существующий packaged `sdd-process-companion` получает режимы
  `analyst-discovery` и `guided-change`;
- перед интервью AI показывает темы и получает разрешение;
- вопросы задаются по одному, а понимание сверяется по смысловым блокам;
- черновики создаются только после подтверждения итоговой сводки;
- переход к файлам и командам требует отдельного согласия.

## Что не меняется

- детерминированные CLI contracts и human authority boundaries;
- ручной и AI-disabled маршруты;
- lifecycle, classification и gate semantics.
```

В `design.md` сослаться на утверждённый design doc и зафиксировать, что это
prompt/packaging change без нового runtime и persistence.

- [ ] **Step 3: Создать delta spec с проверяемыми сценариями**

Добавить четыре requirements со сценариями:

```markdown
## ADDED Requirements

### Requirement: Analyst discovery interview

При сыром новом требовании companion SHALL сначала показать короткий план тем и
запросить разрешение на интервью.

#### Scenario: Человек разрешает углубление

- **WHEN** Analyst просит помочь оформить общую идею
- **THEN** AI показывает темы интервью до первого подробного вопроса
- **AND** после разрешения задаёт только один вопрос за раз
- **AND** после каждого смыслового блока сверяет понимание

#### Scenario: Человек запрещает дальнейшие вопросы

- **WHEN** человек не разрешает или прекращает интервью
- **THEN** AI прекращает задавать вопросы
- **AND** предлагает частичный черновик, сводку либо завершение без файлов

### Requirement: Discovery evidence summary

Companion SHALL разделять `confirmed`, `proposed`, `unknown` и `conflict`.

#### Scenario: Ответ неизвестен или противоречив

- **WHEN** человек отвечает «не знаю» либо sources конфликтуют
- **THEN** AI не превращает пробел в факт
- **AND** объясняет влияние и назначает вопрос владельцу решения

### Requirement: Permission-bound draft creation

Companion SHALL создавать proposal, Delta Spec, optional design и preliminary
tasks только после подтверждения итоговой сводки.

#### Scenario: Сводка ещё не подтверждена

- **WHEN** интервью завершено, но человек не подтвердил понимание
- **THEN** AI не создаёт и не редактирует файлы

### Requirement: Explicit guided-change handoff

Companion SHALL отдельно предлагать переход из `analyst-discovery` в
`guided-change`.

#### Scenario: Переход к действию

- **WHEN** человек подтвердил сводку и черновики
- **THEN** AI спрашивает, показать ли первую команду
- **AND** не выполняет команду, `next_command` или `--confirm` автоматически
```

- [ ] **Step 4: Заполнить tasks checklist и проверить OpenSpec**

Run:

```powershell
openspec validate add-ai-analyst-discovery --strict
```

Expected: `add-ai-analyst-discovery` valid.

- [ ] **Step 5: Commit**

```powershell
git add openspec/changes/add-ai-analyst-discovery
git commit -m "docs: specify AI analyst discovery workflow"
```

---

### Task 2: Расширить packaged companion с TDD-контрактом

**Files:**
- Modify: `tests/test_packaged_flow.py`
- Modify: `tests/test_p3_vertical_slice.py`
- Modify: `process/gigacode/skills/sdd-process-companion.md`

**Interfaces:**
- Consumes: четыре requirements из Task 1.
- Produces: один packaged skill с mode routing, interview protocol, evidence summary и explicit handoff.

- [ ] **Step 1: Добавить failing contract test для установленного skill**

В `test_bootstrap_installs_managed_gigacode_role_gate` после существующей
проверки добавить:

```python
    companion = installed.read_text(encoding="utf-8")
    for token in (
        "## Режим `analyst-discovery`",
        "## Режим `guided-change`",
        "покажи короткий план тем",
        "задавай по одному вопросу",
        "`confirmed`",
        "`proposed`",
        "`unknown`",
        "`conflict`",
        "не создавай и не редактируй файлы",
        "показать первую команду",
    ):
        assert token in companion
```

Добавить отдельный тест:

```python
def test_companion_keeps_discovery_and_action_permissions_separate() -> None:
    companion = (
        PROCESS / "gigacode" / "skills" / "sdd-process-companion.md"
    ).read_text(encoding="utf-8")
    discovery = companion.split("## Режим `analyst-discovery`", 1)[1].split(
        "## Режим `guided-change`", 1
    )[0]
    assert "сначала покажи короткий план тем" in discovery
    assert "после явного разрешения" in discovery
    assert "только после подтверждения итоговой сводки" in discovery
    assert "не создавай и не редактируй файлы" in discovery
```

- [ ] **Step 2: Запустить тесты и подтвердить ожидаемый failure**

Run:

```powershell
python -m pytest tests/test_packaged_flow.py::test_bootstrap_installs_managed_gigacode_role_gate tests/test_packaged_flow.py::test_companion_keeps_discovery_and_action_permissions_separate -q
```

Expected: FAIL из-за отсутствующих sections/tokens в текущем companion.

- [ ] **Step 3: Добавить mode router и interview protocol в существующий skill**

В `process/gigacode/skills/sdd-process-companion.md` после role gate добавить:

```markdown
## Выбор режима простыми словами

- «Помоги разобраться и оформить новую идею» — используй
  `analyst-discovery`.
- «Проведи меня по уже описанному изменению» — используй `guided-change`.
- Если человек не знает, с чего начать, кратко уточни ситуацию и предложи один
  подходящий режим.

Не требуй от человека копировать технический prompt.

## Режим `analyst-discovery`

Сначала перескажи идею и раздели подтверждённые факты, предложения,
неизвестность и конфликты. Затем покажи короткий план тем и запроси разрешение
на интервью. После явного разрешения задавай по одному вопросу. После каждого
смыслового блока сверяй понимание.

Веди evidence-сводку со статусами `confirmed`, `proposed`, `unknown` и
`conflict`. Ответ «не знаю» не заменяй догадкой: объясни влияние пробела и
назначь вопрос владельцу решения.

Перед черновиками покажи итоговую сводку: проблема и польза, пользователь,
текущее и ожидаемое поведение, сценарии, scope/out of scope, ограничения,
зависимости, критерии приёмки и открытые решения. Только после подтверждения
итоговой сводки предложи подготовить `proposal.md`, Delta Spec, optional
`design.md`, preliminary `tasks.md` и список вопросов владельцам.

До отдельного согласия не создавай и не редактируй файлы. Если человек
прекращает вопросы, предложи частичный черновик с пробелами, только сводку либо
завершение без файлов.

## Режим `guided-change`

После подтверждённых черновиков отдельно спроси, хочет ли человек увидеть
первую команду. Перед каждой командой или edit покажи exact action, ожидаемый
результат, что изменится и что не изменится; дождись отдельного «выполняй».
Не выполняй `next_command`, не подставляй `--confirm` и не принимай human
authority decisions.
```

Сохранить существующие более строгие role, acceptance и operation-confirmation
правила ниже; новый раздел их не заменяет.

- [ ] **Step 4: Добавить negative authority assertions**

В `tests/test_p3_vertical_slice.py` добавить:

```python
def test_gigacode_companion_discovery_does_not_claim_human_authority() -> None:
    companion = (
        ROOT / "process" / "gigacode" / "skills" / "sdd-process-companion.md"
    ).read_text(encoding="utf-8")
    assert "не подтверждай classification" in companion
    assert "не подставляй `--confirm`" in companion
    assert "не выполняй `next_command`" in companion
    assert "AI подтверждает classification" not in companion
```

- [ ] **Step 5: Запустить focused tests**

Run:

```powershell
python -m pytest tests/test_packaged_flow.py::test_bootstrap_installs_managed_gigacode_role_gate tests/test_packaged_flow.py::test_companion_keeps_discovery_and_action_permissions_separate tests/test_p3_vertical_slice.py::test_gigacode_start_prompt_uses_only_project_interactive_roles tests/test_p3_vertical_slice.py::test_gigacode_companion_discovery_does_not_claim_human_authority -q
```

Expected: 4 passed.

- [ ] **Step 6: Commit**

```powershell
git add process/gigacode/skills/sdd-process-companion.md tests/test_packaged_flow.py tests/test_p3_vertical_slice.py
git commit -m "feat: add analyst discovery to packaged companion"
```

---

### Task 3: Заменить длинный prompt в FAQ простым входом и показать реальное интервью

**Files:**
- Modify: `docs/faq/ai-collaboration.md`
- Modify: `docs/faq/first-change-with-ai.md`
- Modify: `docs/faq/roles/analyst.md`
- Modify: `docs/faq/index.md`
- Modify: `scripts/validate_product_faq.py`
- Modify: `tests/test_product_faq_docs.py`

**Interfaces:**
- Consumes: mode names и permission boundaries из Task 2.
- Produces: понятный маршрут «простая фраза → темы → вопросы → сводка → черновики → guided change».

- [ ] **Step 1: Добавить failing FAQ contract test**

В `test_product_ai_roadmap_and_troubleshooting_are_practical` расширить tokens:

```python
        "## Режим `analyst-discovery`: от сырой идеи к черновику",
        "Помоги разобраться и оформить новую идею",
        "сначала покажет темы интервью",
        "по одному вопросу",
        "`confirmed`",
        "`proposed`",
        "`unknown`",
        "`conflict`",
```

Добавить отдельный тест:

```python
def test_ai_walkthrough_starts_with_plain_language_discovery() -> None:
    page = (ROOT / "docs" / "faq" / "first-change-with-ai.md").read_text(
        encoding="utf-8"
    )
    plain = "Помоги оформить небольшое изменение. Сначала помоги разобраться"
    assert plain in page
    assert page.index(plain) < page.index("## Стартовый prompt")
    for token in (
        "план тем",
        "Можно пройти по этим темам?",
        "по одному вопросу",
        "итоговая сводка",
        "показать первую команду",
    ):
        assert token in page
```

- [ ] **Step 2: Запустить test и подтвердить failure**

Run:

```powershell
python -m pytest tests/test_product_faq_docs.py::test_product_ai_roadmap_and_troubleshooting_are_practical tests/test_product_faq_docs.py::test_ai_walkthrough_starts_with_plain_language_discovery -q
```

Expected: FAIL из-за отсутствующего discovery route.

- [ ] **Step 3: Дополнить FAQ отдельным discovery route**

В `ai-collaboration.md` добавить:

- короткие пользовательские фразы для выбора режима;
- пример предварительного списка из пяти тем;
- правило «один вопрос за раз»;
- пример `unknown` и `conflict`;
- итоговую сводку;
- отдельное согласие на черновики и отдельное согласие на первую команду.

В `roles/analyst.md` добавить ссылку на режим и объяснить, что AI помогает
сформулировать, но Analyst подтверждает смысл и владельцев открытых решений.

В `first-change-with-ai.md` перед длинным fallback prompt вставить сквозной
диалог:

```text
Человек: Помоги оформить небольшое изменение. Сначала помоги разобраться.

AI: Предлагаю уточнить пять тем: проблему и пользу, пользователя, текущее и
ожидаемое поведение, сценарии, границы и приёмку. Можно пройти по этим темам?

Человек: Да.

AI: Какую проблему должен перестать испытывать пользователь?
```

Продолжить пример до подтверждённой итоговой сводки и вопроса:

```text
Черновики готовы как рабочая версия. Показать первую команду для создания
change package?
```

Длинный prompt сохранить ниже как прозрачный fallback для среды без
установленного skill.

- [ ] **Step 4: Усилить FAQ validator**

В `REQUIRED_QUESTIONS` добавить `"ai-analyst-discovery"`, а в
`WALKTHROUGH_SECTIONS["first-change-with-ai.md"]` — section
`"## Сначала простая фраза: аналитическое интервью"`.

Добавить `DISCOVERY_TOKENS` и проверять их только в `ai-collaboration.md` и
`first-change-with-ai.md`:

```python
DISCOVERY_TOKENS = {
    "Помоги разобраться и оформить новую идею",
    "по одному вопросу",
    "`confirmed`",
    "`proposed`",
    "`unknown`",
    "`conflict`",
    "показать первую команду",
}
```

- [ ] **Step 5: Запустить FAQ tests и validator**

Run:

```powershell
python -m pytest tests/test_product_faq_docs.py -q
python scripts/validate_product_faq.py --json
```

Expected: 19+ tests passed; JSON contains `"status": "valid"` and empty
`errors`.

- [ ] **Step 6: Commit**

```powershell
git add docs/faq scripts/validate_product_faq.py tests/test_product_faq_docs.py
git commit -m "docs: add analyst discovery walkthrough"
```

---

### Task 4: Версионировать пакет и проверить поставку

**Files:**
- Modify: `process/VERSION`
- Modify: `process/package.yaml`
- Modify: version-pinned fixtures found by the search command below
- Modify: `docs/00_FILE_STRUCTURE.md`
- Modify: `docs/ROADMAP.md`
- Modify: `openspec/changes/add-ai-analyst-discovery/tasks.md`

**Interfaces:**
- Consumes: finished packaged asset and FAQ from Tasks 2–3.
- Produces: internally consistent successor package version `0.3.7` and durable repository navigation/status.

- [ ] **Step 1: Найти все текущие version pins before edit**

Run:

```powershell
rg -n '0\.3\.6|version:\s*0\.3\.6' process templates tests docs openspec
```

Expected: exact inventory of package/config/fixture pins; historical immutable
evidence is identified and excluded from bulk replacement.

- [ ] **Step 2: Добавить failing version consistency assertion if absent**

Убедиться, что существующий
`test_synthetic_central_topology_is_coherent` сравнивает `process/VERSION`,
`process/package.yaml`, template config, adapter и release fixture. Если новое
место pin не покрыто, добавить его в этот test before changing versions.

- [ ] **Step 3: Bump mutable package pins to `0.3.7`**

Изменить:

```text
process/VERSION: 0.3.7
process/package.yaml: package.version: 0.3.7
```

Обновить только mutable current fixtures/configuration. Не переписывать
исторические release candidates, audits и accepted evidence, где `0.3.6`
является фактом прошлого состояния.

- [ ] **Step 4: Обновить карту и статус**

В `docs/00_FILE_STRUCTURE.md` добавить новый design, plan и active OpenSpec
change. В `docs/ROADMAP.md` описать человекочитаемо: companion умеет провести
аналитическое интервью и подготовить черновики, но реальный first-time human
walkthrough остаётся обязательным acceptance evidence.

В `tasks.md` отметить выполненные технические tasks; отдельный human walkthrough
оставить unchecked до фактического выполнения человеком.

- [ ] **Step 5: Запустить focused package regression**

Run:

```powershell
python -m pytest tests/test_process_package.py::test_synthetic_central_topology_is_coherent tests/test_packaged_flow.py::test_bootstrap_installs_managed_gigacode_role_gate tests/test_product_faq_docs.py tests/test_p3_vertical_slice.py::test_gigacode_start_prompt_uses_only_project_interactive_roles tests/test_p3_vertical_slice.py::test_gigacode_companion_discovery_does_not_claim_human_authority -q
python scripts/validate_product_faq.py --json
openspec validate add-ai-analyst-discovery --strict
```

Expected: all tests pass; FAQ valid; OpenSpec change valid.

- [ ] **Step 6: Запустить full verification с достаточным timeout**

Run:

```powershell
python -m pytest -q
openspec list
openspec list --specs
openspec validate --all --strict
```

Expected: full pytest passes; OpenSpec strict validation passes. Если full pytest
снова превышает локальный timeout, сохранить exact timeout и не объявлять full
suite зелёным.

- [ ] **Step 7: Commit**

```powershell
git add process/VERSION process/package.yaml templates tests docs/00_FILE_STRUCTURE.md docs/ROADMAP.md openspec/changes/add-ai-analyst-discovery/tasks.md
git commit -m "chore: prepare analyst companion package update"
```

---

### Task 5: Провести финальный review и оставить human walkthrough открытым

**Files:**
- Modify if findings require it: files changed in Tasks 1–4
- Modify: `openspec/changes/add-ai-analyst-discovery/tasks.md`

**Interfaces:**
- Consumes: complete branch diff and verification output.
- Produces: reviewed implementation ready for human walkthrough, without false completion claims.

- [ ] **Step 1: Review branch scope**

Run:

```powershell
git diff main...HEAD --stat
git diff main...HEAD --check
git status --short
```

Expected: only intended skill/OpenSpec/FAQ/version/docs/test changes; no
temporary files.

- [ ] **Step 2: Выполнить requirement-to-evidence review**

Для каждого requirement из Task 1 сопоставить:

- exact section в `sdd-process-companion.md`;
- automated test name;
- FAQ example;
- manual residual evidence.

Не закрывать requirement только ссылкой на prose без test или walkthrough.

- [ ] **Step 3: Провести реальный human walkthrough**

Человек начинает фразой:

```text
Помоги оформить небольшое изменение. Сначала помоги разобраться.
```

Проверить вручную:

1. AI показывает темы до подробных вопросов.
2. AI ждёт разрешение.
3. AI задаёт вопросы по одному.
4. «Не знаю» остаётся `unknown`.
5. AI показывает сводку до файлов.
6. AI ждёт подтверждение сводки.
7. AI отдельно спрашивает о первой команде.
8. AI не выполняет команду без «выполняй».

Если walkthrough не проведён, оставить соответствующий task unchecked и
сообщить residual risk.

- [ ] **Step 4: Финальная проверка и commit fixes**

Run:

```powershell
python -m pytest tests/test_packaged_flow.py tests/test_product_faq_docs.py tests/test_p3_vertical_slice.py -q
python scripts/validate_product_faq.py --json
openspec validate --all --strict
git diff --check
```

Expected: all focused checks pass; strict OpenSpec valid; no whitespace errors.

Если review потребовал исправления:

```powershell
git add <exact-reviewed-files>
git commit -m "fix: address analyst companion review"
```

- [ ] **Step 5: Подготовить merge handoff**

Сообщить branch name `feature/ai-analyst-companion`, commits, проверки,
незавершённый human walkthrough (если применимо) и предложить merge только после
human acceptance. Push/merge выполнять лишь по отдельному запросу пользователя.
