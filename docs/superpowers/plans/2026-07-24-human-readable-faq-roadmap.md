# Human-Readable FAQ Roadmap Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Перестроить FAQ-roadmap вокруг понятных пользовательских результатов и подробно зафиксировать будущую аналитику ФП с точным именем и ссылками открытой OpenSpec change.

**Architecture:** Одна страница `docs/faq/roadmap.md` остаётся главным пользовательским roadmap и получает status legend и capability-карточки. Нормативное поведение остаётся в OpenSpec; FAQ объясняет смысл, честный статус и ведёт на proposal/design/spec/tasks. Deterministic validator и tests закрепляют обязательную карточку `define-fp-analytics-publication-model`.

**Tech Stack:** Markdown, Python 3.11+, pytest, существующий `scripts/validate_product_faq.py`, OpenSpec CLI 1.4.1, roadmap/OpenSpec validator.

## Global Constraints

- Писать пользовательский текст по-русски; стабильные IDs, команды и пути сохранять на английском.
- Не обещать календарные даты.
- Не называть planned capability работающей по факту наличия design, template или OpenSpec change.
- Git/OpenSpec/Markdown/YAML остаются каноническими источниками; FAQ — человекочитаемое derived view.
- Для publication model использовать только решение `D-029` и active change `define-fp-analytics-publication-model`.
- Не изображать отдельную обязательную Confluence page на каждый change.
- Не изображать AI Analyst Discovery draft как delivered analytics.
- Не менять lifecycle status `define-fp-analytics-publication-model`; он остаётся `planned`, progress — `0/70`.
- Не закрывать FAQ task 4.4: first-time human walkthrough остаётся обязательным acceptance gate.
- Не менять `.pytest-tmp-faq-20260724/`.

---

## File Structure

**Modify:**

- `docs/faq/roadmap.md` — единая человекочитаемая roadmap-страница с status legend и capability-карточками.
- `docs/faq/index.md` — более понятная подпись ссылки на roadmap.
- `scripts/validate_product_faq.py` — обязательный вопрос и tokens карточки аналитики.
- `tests/test_product_faq_docs.py` — positive и negative contract tests roadmap.
- `openspec/changes/add-product-faq-and-role-runbook/specs/product-faq-and-role-runbook/spec.md` — acceptance scenario для понятной planned capability-карточки.
- `openspec/changes/add-product-faq-and-role-runbook/design.md` — принятое решение о формате roadmap-карточек.
- `openspec/changes/add-product-faq-and-role-runbook/tasks.md` — отдельная task 5.6 и evidence после выполнения.
- `openspec/changes/add-product-faq-and-role-runbook/proposal.md` — change-intake запись о remediation.
- `docs/audits/PRODUCT_FAQ_AND_ROLE_RUNBOOK_ACCEPTANCE_AUDIT_2026-07-24.md` — finding и verification evidence.
- `docs/CURRENT_PROJECT_AUDIT.md` — текущий статус FAQ remediation.

**Reference only:**

- `docs/superpowers/specs/2026-07-24-human-readable-faq-roadmap-design.md`.
- `openspec/changes/define-fp-analytics-publication-model/`.
- `docs/superpowers/specs/2026-07-24-ai-analyst-discovery-skill-design.md`.
- `docs/audits/ANALYTIC_TEMPLATE_AND_CONFLUENCE_PUBLICATION_GAP_AUDIT_2026-07-24.md`.

---

### Task 1: Зафиксировать FAQ-контракт и intake

**Files:**

- Modify: `openspec/changes/add-product-faq-and-role-runbook/specs/product-faq-and-role-runbook/spec.md`
- Modify: `openspec/changes/add-product-faq-and-role-runbook/design.md`
- Modify: `openspec/changes/add-product-faq-and-role-runbook/tasks.md`
- Modify: `openspec/changes/add-product-faq-and-role-runbook/proposal.md`

**Interfaces:**

- Consumes: решение `D-029`, design `2026-07-24-human-readable-faq-roadmap-design.md`, active publication change metadata.
- Produces: acceptance scenario и task 5.6, на которые опираются tests и итоговый audit.

- [ ] **Step 1: Добавить acceptance scenario в Plain-language roadmap requirement**

В `openspec/changes/add-product-faq-and-role-runbook/specs/product-faq-and-role-runbook/spec.md` после сценария `User distinguishes framework layers` добавить:

```markdown
#### Scenario: Planned capability объяснена и связана с открытой спекой

- **WHEN** roadmap FAQ описывает будущую аналитику ФП и релизных инкрементов
- **THEN** карточка простыми словами объясняет, что это, зачем нужно, что получит пользователь, что уже подготовлено и что ещё не реализовано, называет exact change `define-fp-analytics-publication-model`, показывает честный progress и ведёт на proposal, design, requirements и tasks
```

- [ ] **Step 2: Записать design decision активного FAQ change**

В `openspec/changes/add-product-faq-and-role-runbook/design.md` в `## Decisions` добавить:

```markdown
- Plain-language roadmap использует одну страницу и capability-карточки. Каждая
  planned карточка отвечает «что это / зачем / что получит человек / что уже
  готово / что ещё не работает», называет exact OpenSpec change и даёт прямые
  ссылки. Наличие открытой спеки не изображается как доступная функция.
```

- [ ] **Step 3: Добавить task 5.6**

В конец `## 5. Content acceptance remediation` добавить:

```markdown
- [ ] 5.6 Перестроить FAQ-roadmap вокруг status legend и человекочитаемых capability-карточек; подробно описать `define-fp-analytics-publication-model`, связь с AI Analyst Discovery и отличия planned design от работающей функции; закрепить карточку validator/tests.
```

- [ ] **Step 4: Добавить change-intake запись**

В конец `proposal.md` добавить:

````markdown
## Change Intake — human-readable roadmap capability cards

```text
Idea: Сделать FAQ-roadmap понятным людям и подробно назвать открытый contract будущей аналитики ФП/release increments.
Source: Human feedback 2026-07-24 after acceptance of D-029.
Type: scope_refinement, documentation_change, verification_change
Decision: adopt_now
Reason: Existing roadmap lists future layers in one technical bullet and does not explain the user outcome or exact active OpenSpec source.
Affected specs: product-faq-and-role-runbook; references define-fp-analytics-publication-model without duplicating its normative behavior.
Affected architecture: No product architecture change; FAQ becomes a checked human-readable view over roadmap/OpenSpec.
Data contract impact: None.
Verification impact: Required roadmap question, exact tokens/links and positive/negative documentation tests.
Status: Queued as task 5.6; task 4.4 remains the only final human walkthrough gate.
```
````

- [ ] **Step 5: Проверить OpenSpec RED/GREEN контракта**

Run:

```powershell
openspec validate add-product-faq-and-role-runbook --strict
```

Expected: change validation passes. Task progress temporarily becomes `17/19`: existing task 4.4 and new task 5.6 are unchecked.

- [ ] **Step 6: Commit**

```powershell
git add -- openspec/changes/add-product-faq-and-role-runbook
git commit -m "spec: require human-readable faq roadmap cards"
```

---

### Task 2: Закрепить roadmap-карточку тестами и validator-ом

**Files:**

- Modify: `tests/test_product_faq_docs.py`
- Modify: `scripts/validate_product_faq.py`

**Interfaces:**

- Consumes: exact FAQ tokens из Task 1 и design.
- Produces: `REQUIRED_ROADMAP_TOKENS: frozenset[str]` и deterministic diagnostics `roadmap capability detail is missing`.

- [ ] **Step 1: Написать failing positive test**

В `test_product_ai_roadmap_and_troubleshooting_are_practical` после проверки секций roadmap добавить:

```python
    for token in (
        "## Как читать roadmap",
        "## Работает сейчас",
        "## Следующее",
        "## Запланировано",
        "## Намеренно недоступно",
        "### Полная аналитика ФП и страницы релизных инкрементов",
        "`define-fp-analytics-publication-model`",
        "0/70",
        "одна полная актуальная страница",
        "отдельная страница каждого релизного инкремента",
        "AI Analyst Discovery",
        "proposal.md",
        "design.md",
        "spec.md",
        "tasks.md",
    ):
        assert token in roadmap
```

- [ ] **Step 2: Написать failing negative validator test**

Добавить:

```python
def test_validator_requires_detailed_analytics_roadmap_card(tmp_path: Path) -> None:
    from scripts.validate_product_faq import validate_product_faq

    faq = tmp_path / "docs" / "faq"
    faq.mkdir(parents=True)
    (faq / "roadmap.md").write_text(
        "# Roadmap\nКанонический источник: x\n"
        "<!-- faq-question: analytics-publication-roadmap -->\n"
        "Запланирована аналитика.\n",
        encoding="utf-8",
    )

    errors = validate_product_faq(tmp_path)
    assert any(
        "roadmap capability detail is missing" in error
        and "define-fp-analytics-publication-model" in error
        for error in errors
    )
```

- [ ] **Step 3: Запустить tests и подтвердить RED**

Run:

```powershell
python -m pytest tests/test_product_faq_docs.py::test_product_ai_roadmap_and_troubleshooting_are_practical tests/test_product_faq_docs.py::test_validator_requires_detailed_analytics_roadmap_card -q
```

Expected: FAIL, потому что roadmap ещё не содержит новой структуры, а validator не проверяет required tokens.

- [ ] **Step 4: Добавить required question и tokens**

В `REQUIRED_QUESTIONS` добавить:

```python
    "analytics-publication-roadmap",
```

После `WALKTHROUGH_INSTANCE_TOKENS` добавить:

```python
REQUIRED_ROADMAP_TOKENS = frozenset(
    {
        "## Как читать roadmap",
        "## Работает сейчас",
        "## Следующее",
        "## Запланировано",
        "## Намеренно недоступно",
        "### Полная аналитика ФП и страницы релизных инкрементов",
        "define-fp-analytics-publication-model",
        "0/70",
        "одна полная актуальная страница",
        "отдельная страница каждого релизного инкремента",
        "AI Analyst Discovery",
        "proposal.md",
        "design.md",
        "spec.md",
        "tasks.md",
    }
)
```

- [ ] **Step 5: Добавить roadmap diagnostics**

В цикле `for page in pages`, после walkthrough-проверок добавить:

```python
        if page.name == "roadmap.md":
            for token in sorted(REQUIRED_ROADMAP_TOKENS):
                if token not in text:
                    errors.append(
                        "roadmap capability detail is missing: "
                        f"{page.relative_to(root)} -> {token}"
                    )
```

- [ ] **Step 6: Запустить focused tests**

Run:

```powershell
python -m pytest tests/test_product_faq_docs.py::test_validator_requires_detailed_analytics_roadmap_card tests/test_product_faq_docs.py::test_validator_reports_missing_required_question -q
```

Expected: PASS для negative contract tests. Positive roadmap test всё ещё FAIL до Task 3.

- [ ] **Step 7: Commit RED/validator contract**

```powershell
git add -- scripts/validate_product_faq.py tests/test_product_faq_docs.py
git commit -m "test: require detailed faq roadmap capability card"
```

---

### Task 3: Переписать FAQ-roadmap человеческими карточками

**Files:**

- Modify: `docs/faq/roadmap.md`
- Modify: `docs/faq/index.md`

**Interfaces:**

- Consumes: `REQUIRED_ROADMAP_TOKENS`, `D-029`, publication change links.
- Produces: одна human-readable roadmap page; все ссылки являются relative Markdown links к реальным `.md` файлам.

- [ ] **Step 1: Заменить вводную и добавить marker**

Начало `docs/faq/roadmap.md` должно быть:

```markdown
# Что уже работает и что будет дальше

Канонический источник: [project roadmap](../ROADMAP.md),
[implementation strategy](../IMPLEMENTATION_STRATEGY.md),
[решение D-029](../DECISIONS.md)
и активные OpenSpec changes, ссылки на которые указаны в карточках ниже.

<!-- faq-question: analytics-publication-roadmap -->

Эта страница объясняет roadmap через результаты, которые получает человек.
Здесь нет календарных обещаний: возможность становится доступной только после
реализации, проверок и требуемого человеческого решения.

## Как читать roadmap

- **Работает сейчас** — реализовано в текущем package с указанными границами.
- **Следующее** — ближайший незакрытый пользовательский gate.
- **Запланировано** — design или OpenSpec change существует, но функция ещё не
  работает.
- **Намеренно недоступно** — действие блокируется ради безопасности или пока
  не имеет принятого контракта.

Открытая спека, заполненный `tasks.md` или готовый template сами по себе не
означают, что функция реализована.
```

- [ ] **Step 2: Написать `Работает сейчас` и `Следующее`**

Использовать карточки с подзаголовками `Что это`, `Для чего`, `Статус и граница`.
Обязательно сохранить фактические текущие возможности из старого
`## Что уже можно сделать`, включая fail-closed `sdd run`, AI-disabled fallback
и минимальный typed analytics preview.

Разделы должны называться точно:

```markdown
## Работает сейчас
## Следующее
```

В `Следующее` описать:

- first-time human walkthrough;
- FAQ task 4.4;
- Linux/WSL2 portability gate перед corporate adaptation.

- [ ] **Step 3: Добавить точную карточку publication model**

В `## Запланировано` добавить следующий блок без сокращения смысловых пунктов:

```markdown
### Полная аналитика ФП и страницы релизных инкрементов

**Что это.** Для каждой самостоятельной ФП будет одна полная актуальная
страница аналитики. Для каждого релиза будет создаваться отдельная страница
релизного инкремента. Отдельная обязательная Confluence-страница на каждый
change не нужна.

**Для чего.** Человек сможет найти целостное описание своей ФП, не просматривая
спеки десятков проектов. Релизная страница сохранит историю конкретного
инкремента. Один релиз сможет включать изменения нескольких ФП, но ownership
требований останется у owning FP, а нормативный текст не будет копироваться.

**Как определяется актуальность.** Основная часть current page показывает
подтверждённое доставленное состояние. Active и approved-not-delivered changes
показываются отдельно. После delivery выполняется reconciliation всех
затронутых ФП; незавершённое обновление остаётся видимым gap.

**Как будут собираться сложные таблицы.** Markdown объясняет смысл, OpenSpec
владеет требованиями и сценариями, typed YAML хранит повторяемые модели, а
renderer собирает вложенные таблицы и expand blocks. Confluence остаётся
generated read model, а не редактируемым источником.

**Связь с AI Analyst Discovery.** AI сможет провести аналитическое интервью и
подготовить draft. Статусы `confirmed`, `proposed`, `unknown` и `conflict` не
смешиваются. Interview summary и draft не становятся delivered truth:
публикация использует только reviewed canonical artifacts, а ownership,
release inclusion, approval и delivery остаются решениями людей.

**Честный статус.** Решение `D-029` принято, а proposal, design, requirements и
план реализации подготовлены. Реализация не начата: открытая спека содержит
`0/70` выполненных implementation tasks. Расширенные schemas, renderers,
publisher и corporate publication пока недоступны. Точные Confluence
space/parent mappings, macros и adapter требуют corporate capability probe.

**Как называется открытая спека.** `define-fp-analytics-publication-model`.

- [Зачем нужен change и что он меняет](../../openspec/changes/define-fp-analytics-publication-model/proposal.md)
- [Полный архитектурный design](../../openspec/changes/define-fp-analytics-publication-model/design.md)
- [Проверяемые requirements и scenarios](../../openspec/changes/define-fp-analytics-publication-model/specs/fp-analytics-publication/spec.md)
- [Implementation tasks](../../openspec/changes/define-fp-analytics-publication-model/tasks.md)
- [Аудит исходного корпоративного шаблона](../audits/ANALYTIC_TEMPLATE_AND_CONFLUENCE_PUBLICATION_GAP_AUDIT_2026-07-24.md)
- [Дизайн AI Analyst Discovery](../superpowers/specs/2026-07-24-ai-analyst-discovery-skill-design.md)
```

- [ ] **Step 4: Добавить остальные planned capability-карточки**

В том же формате, но короче, описать:

- corporate adaptation и monitored pilot;
- AI Analyst Discovery Skill;
- controlled Confluence publication как часть publication model;
- Jira task planning, QA/AT proposal layers и role inbox;
- bounded AI automation поверх deterministic control plane.

Для AI Analyst Discovery явно написать:

```markdown
Согласован design, но OpenSpec change и реализация ещё не созданы.
```

Не придумывать имя несуществующей OpenSpec change.

- [ ] **Step 5: Переименовать intentionally blocked section**

Заменить заголовок:

```markdown
## Что намеренно не автоматизировано
```

на:

```markdown
## Намеренно недоступно
```

Сохранить все существующие запреты и добавить пояснение, что это safety/status
boundary, а не список забытых функций.

- [ ] **Step 6: Обновить индекс**

В `docs/faq/index.md` заменить подпись:

```markdown
- [Что доступно и что запланировано](roadmap.md)
```

на:

```markdown
- [Понятный roadmap: что работает, что запланировано и где открытые спеки](roadmap.md)
```

- [ ] **Step 7: Запустить FAQ GREEN**

Run:

```powershell
python scripts/validate_product_faq.py --json
python -m pytest tests/test_product_faq_docs.py -q
```

Expected:

- validator returns `"status": "valid"` and `errors: []`;
- all FAQ documentation tests pass.

- [ ] **Step 8: Commit**

```powershell
git add -- docs/faq/roadmap.md docs/faq/index.md
git commit -m "docs: explain roadmap through user capabilities"
```

---

### Task 4: Reconcile evidence, finish task 5.6 and run final gates

**Files:**

- Modify: `openspec/changes/add-product-faq-and-role-runbook/tasks.md`
- Modify: `docs/audits/PRODUCT_FAQ_AND_ROLE_RUNBOOK_ACCEPTANCE_AUDIT_2026-07-24.md`
- Modify: `docs/CURRENT_PROJECT_AUDIT.md`

**Interfaces:**

- Consumes: passing FAQ validator/tests and committed roadmap content.
- Produces: task 5.6 evidence, durable audit finding and current-state summary; task 4.4 remains unchecked.

- [ ] **Step 1: Mark task 5.6 complete with evidence**

Заменить task 5.6 checkbox на `[x]` и сразу под ней добавить:

```markdown
  Evidence (2026-07-24): roadmap capability-card contract, exact
  `define-fp-analytics-publication-model` links, FAQ validator/tests, strict
  OpenSpec and roadmap/OpenSpec validation passed; task 4.4 remains the
  independent first-time human walkthrough gate.
```

- [ ] **Step 2: Добавить audit finding**

В FAQ acceptance audit добавить:

```markdown
### FAQ-ACC-006 — roadmap называл слои, но не объяснял будущий результат

Классификация: подтверждённый content gap, исправлен в FAQ и deterministic
checks.

Затронутое поведение: прежняя roadmap-страница перечисляла controlled
publication и другие later layers одной строкой. Человек не мог понять, что
такое будущая аналитика ФП, зачем нужны две страницы, как работает cross-FP
release и как называется открытая спека.

Исправление: roadmap перестроен через status legend и capability-карточки.
Карточка `define-fp-analytics-publication-model` объясняет current FP page,
release increment page, delivered/WIP separation, typed nested rendering,
cross-FP ownership, AI Analyst Discovery boundary, progress `0/70` и прямые
canonical links. Validator и tests требуют эти элементы.
```

После блока добавить фактическую таблицу команд и результатов из Step 4.

- [ ] **Step 3: Обновить Current Project Audit**

В верхний FAQ-раздел `docs/CURRENT_PROJECT_AUDIT.md` добавить:

```markdown
- FAQ roadmap теперь объясняет planned capabilities через человеческий
  результат и exact OpenSpec links. Publication model явно называется
  `define-fp-analytics-publication-model`, остаётся `planned` с `0/70` tasks и
  не изображается работающей. FAQ task 5.6 закрыта; task 4.4 остаётся открытым
  first-time human walkthrough gate.
```

- [ ] **Step 4: Run focused and governance verification**

Run:

```powershell
python scripts/validate_product_faq.py --json
python -m pytest tests/test_product_faq_docs.py -q
openspec list
openspec list --specs
openspec validate --all --strict
node "$env:USERPROFILE\.codex\skills\roadmap-openspec-validator\scripts\validate-roadmap-openspec.mjs" --root "C:\Users\danoc\Documents\projects\teamSsdCli"
git diff --check
```

Expected:

- FAQ validator valid with zero errors;
- FAQ tests all pass;
- OpenSpec strict validation has zero failures;
- roadmap/OpenSpec validation has zero errors; existing unrelated lifecycle
  warnings are reported, not silently fixed;
- `git diff --check` returns no errors;
- `add-product-faq-and-role-runbook` has only task 4.4 unchecked;
- `define-fp-analytics-publication-model` remains `planned`, `0/70`.

- [ ] **Step 5: Reviewer-style content check**

Ответить по тексту FAQ без открытия OpenSpec:

1. Какие четыре status category используются?
2. Какие две страницы появятся для аналитики?
3. Почему change page не является третьей обязательной страницей?
4. Как cross-FP release сохраняет ownership?
5. Почему AI discovery draft не является delivered fact?
6. Как называется open spec и сколько tasks выполнено?

Expected:

```text
Работает сейчас / Следующее / Запланировано / Намеренно недоступно.
Current FP analytics page и release increment page.
Change остаётся Git/OpenSpec working unit и входит в release delta.
Requirements остаются у owning FP; release агрегирует ссылки.
Только reviewed canonical artifacts после delivery входят в current truth.
define-fp-analytics-publication-model, 0/70.
```

- [ ] **Step 6: Commit**

```powershell
git add -- openspec/changes/add-product-faq-and-role-runbook/tasks.md docs/audits/PRODUCT_FAQ_AND_ROLE_RUNBOOK_ACCEPTANCE_AUDIT_2026-07-24.md docs/CURRENT_PROJECT_AUDIT.md
git commit -m "docs: record faq roadmap remediation evidence"
```

---

## Completion State

После выполнения плана:

- FAQ-roadmap понятен без знания внутренних phase/work-item терминов;
- `define-fp-analytics-publication-model` явно назван и подробно объяснён;
- наличие открытой спеки не выдаётся за реализованную функцию;
- AI Analyst Discovery связан с публикацией без превращения draft в canonical
  truth;
- validator/tests защищают обязательную карточку от удаления;
- FAQ task 5.6 закрыта;
- task 4.4 и first-time human walkthrough остаются открыты;
- никакая publication, Confluence mutation или product behavior не реализованы.
