# Итоговая архитектура локальной SDD-автоматизации команды

**Версия:** 1.0
**Назначение:** рабочая архитектура для внедрения процесса SDD на базе OpenSpec/Markdown, Git, Bitbucket, Jenkins, Confluence, Jira/трекера задач, локальных CLI и локальных AI-инструментов.
**Цель:** автоматизировать сквозной процесс от аналитики до разработки, тест-кейсов и автотестов без централизованного автономного агента.

---

## 1. Короткое описание решения

Основной источник требований и инженерной документации хранится в Git в виде структурированных OpenSpec/Markdown-артефактов. Confluence используется как опубликованная витрина для чтения, обсуждений и согласований, но не как первичный редактируемый источник.

Целевой поток:

```text
OpenSpec/Markdown в Git
  -> Spec PR в Bitbucket
  -> Jenkins-валидация
  -> Confluence preview/publication
  -> approval/merge Spec PR
  -> автосоздание задач разработки, QA и AT
  -> локальная работа разработчика/QA/AT через sdd CLI
  -> code PR / QA PR / AT PR
  -> тестирование
  -> archive change
  -> обновление living specs и финальной Confluence-страницы
```

Ключевая идея: **автоматизируется не один большой агент, а переходы состояния между артефактами**. AI используется локально как помощник роли, а процесс контролируется Git, PR, CI, схемами и traceability.

---

## 2. Основные принципы

| Принцип | Решение | Короткое обоснование |
|---|---|---|
| Единый источник инженерной правды | `team-specs` repo с OpenSpec/Markdown | Git даёт diff, PR, историю, CI и удобный контекст для CLI/AI. |
| Confluence как витрина | Generated pages из Markdown/OpenSpec | Confluence громоздкий и плохо подходит как машинный первоисточник. |
| Нет двусторонней синхронизации | Только `Git -> Confluence` | Иначе появятся две расходящиеся версии требований. |
| Маленькие change packages | Каждый инкремент оформляется как отдельный OpenSpec change | Проще ревьюить, валидировать, связывать с задачами и тестами. |
| Автоматизация через CLI/CI | `sdd CLI` + Jenkins pipelines | Безопаснее и дешевле централизованного автономного агента. |
| AI не владеет процессом | AI только предлагает черновики, проверки, skeletons | Решения, approve и merge остаются за людьми. |
| Traceability обязательно | Requirement -> scenario -> dev task -> test case -> AT | Позволяет понять, что реализовано и чем проверено. |
| Ревью по владельцам | Reviewer'ы назначаются по affected systems и owners registry | Не нужно отправлять каждый PR всей команде. |

---

## 3. Состав системы

### 3.1. Репозитории

```text
team-specs/
  openspec/
    config.yaml
    specs/
    changes/
  sdd/
    registry/
    templates/
    publishing/
    schemas/

backend-service-a/
  src/
  tests/
  openspec/config.yaml

backend-service-b/
  src/
  tests/
  openspec/config.yaml

mobile-app/
  app/
  tests/
  openspec/config.yaml

api-at/
  tests/
  openspec/config.yaml

mobile-at/
  tests/
  openspec/config.yaml
```

### 3.2. Назначение репозиториев

| Репозиторий | Что хранит | Кто работает |
|---|---|---|
| `team-specs` | Требования, OpenSpec changes, living specs, QA/AT-планы, traceability, registry | Аналитики, разработчики, QA, AT, техлиды |
| Code repos | Реализация, unit/integration tests, локальные технические notes | Разработчики |
| `api-at` | API автотесты, fixtures, test data setup, Allure/TestOps mapping | Автотестеры backend/API |
| `mobile-at` | Mobile UI/E2E автотесты, device/cloud configs, test data | Мобильные автотестеры |
| Confluence | Публикуемые страницы для чтения, комментариев и согласований | Все роли, бизнес, менеджмент |
| Jira/трекер | Workflow задач и статусов | Все роли |

---

## 4. Почему архитектура Markdown/OpenSpec-first

### 4.1. Что выбираем

Выбирается поток:

```text
OpenSpec/Markdown -> Git PR -> Confluence publication
```

а не:

```text
Confluence -> parser -> Markdown/OpenSpec
```

### 4.2. Короткое обоснование

Confluence удобен для чтения и согласований, но неудобен как машинный источник: страницы содержат внутренний формат, макросы, вложения, таблицы и нестабильное оформление. Это плохо парсится в чистый Markdown и создаёт риск постоянной борьбы с форматированием.

Markdown/OpenSpec в Git удобен для SDD: его можно валидировать, ревьюить, версионировать, связывать с задачами, тестами и автотестами.

### 4.3. Правило владения данными

```text
Git/OpenSpec = canonical source
Confluence = generated view
Jira/Tracker = workflow/status
Bitbucket PR = review/audit
Jenkins = validation/automation
```

### 4.4. Работа с ручными правками в Confluence

Generated-блоки в Confluence не редактируются вручную. Комментарии допустимы, но изменение требований делается через Git PR.

```text
Комментарий в Confluence
  -> аналитик переносит изменение в OpenSpec change
  -> Spec PR обновляется
  -> Confluence preview публикуется заново
```

---

## 5. Центральный объект процесса: Change Package

Каждое изменение оформляется как отдельный package в `team-specs/openspec/changes/<change-id>/`.

```text
openspec/changes/AUTH-2026-071-add-remember-me/
  change.yaml
  proposal.md
  design.md
  tasks.md
  specs/
    auth-session/
      spec.md
  qa/
    test-plan.md
    test-cases/
      auth-remember-me.feature
    automation-plan.md
  traceability.yaml
```

### 5.1. Назначение файлов

| Файл | Назначение |
|---|---|
| `change.yaml` | Метаданные изменения: тип, статус, затронутые проекты, владельцы, quality requirements. |
| `proposal.md` | Что меняется, зачем, scope, out of scope, acceptance criteria. |
| `design.md` | Техническое решение, affected systems, API/contracts, миграции, риски. |
| `tasks.md` | Черновая декомпозиция dev/QA/AT задач. |
| `specs/*/spec.md` | OpenSpec delta: добавленные/изменённые/удалённые требования. |
| `qa/test-plan.md` | Стратегия проверки изменения. |
| `qa/test-cases/*.feature` | Тест-кейсы в Gherkin/BDD-подобном формате. |
| `qa/automation-plan.md` | Что автоматизировать, где, приоритет, ограничения. |
| `traceability.yaml` | Связи requirement -> scenario -> task -> test case -> automated test. |

---

## 6. Типы изменений и требования к артефактам

| Тип | Когда использовать | Обязательные артефакты |
|---|---|---|
| `new_feature` | Новая пользовательская или системная возможность | `proposal`, `spec delta`, `design`, `test-plan`, test cases, automation-plan |
| `behavior_change` | Меняется существующее поведение | `proposal`, `spec delta`, impact analysis, обновлённые test cases |
| `bugfix` | Исправление дефекта | bug scenario, regression test, краткое описание причины |
| `refactor` | Нет изменения поведения | design note или waiver, proof через существующие тесты |
| `removal` | Удаление/депрекация поведения | spec removal, deprecation notes, обновление тестов |
| `config_ops` | Конфигурация, инфраструктура, операционные изменения | validation/rollback plan, smoke checks |

---

## 7. Жизненный цикл change

```text
draft
  -> spec_review
  -> approved
  -> tasks_created
  -> in_dev
  -> ready_for_qa
  -> implemented
  -> archived
```

### 7.1. Состояния

| Состояние | Что означает | Кто двигает |
|---|---|---|
| `draft` | Change создаётся и наполняется | Аналитик / техлид |
| `spec_review` | Открыт Spec PR | Аналитик / автор PR |
| `approved` | Spec PR approved и merged | Bitbucket/Jenkins |
| `tasks_created` | Созданы dev/QA/AT задачи | Jenkins / `sdd tasks create` |
| `in_dev` | Реализация в работе | Разработчики |
| `ready_for_qa` | Реализация доступна для проверки | Разработчики / CI/CD |
| `implemented` | Проверки пройдены | QA/AT |
| `archived` | Change закрыт, specs обновлены | Jenkins / release owner |

---

## 8. Роли и ответственность

| Роль | Основная ответственность |
|---|---|
| Аналитик | Формирует `proposal.md`, acceptance criteria, scope, бизнес-смысл, уточняет комментарии. |
| Разработчик | Проверяет реализуемость, пишет/ревьюит `design.md`, реализует code tasks. |
| Техлид | Следит за архитектурными решениями, cross-repo impact, API/contracts, owners. |
| QA | Проверяет testability, пишет/ревьюит test-plan и test cases. |
| AT | Оценивает автоматизацию, создаёт/ревьюит skeleton PR в AT repo. |
| DevOps/CI owner | Поддерживает Jenkins pipelines, доступы, публикацию, validation gates. |
| Product/Business stakeholder | Читает Confluence view, оставляет комментарии, участвует в согласовании. |

---

## 9. Review-модель без перегруза команды

Ревью назначается автоматически по `change.yaml`, `owners.yaml` и affected systems.

### 9.1. Матрица ревью

| Тип изменения | Кто ревьюит |
|---|---|
| Малый bugfix без изменения поведения | Dev owner, QA optional |
| Bugfix с пользовательским сценарием | Dev owner + QA |
| Behavior change | Analyst + Dev owner + QA |
| New feature | Analyst + Dev owner + QA + AT optional/required по impact |
| Cross-repo/API/mobile | Analyst + owners affected repos + QA + AT |
| Refactor | Tech owner, QA optional при наличии риска |
| Removal/deprecation | Analyst + owners + QA |

### 9.2. Как избежать задержек

- Не все изменения требуют полного Spec PR.
- Reviewer'ы назначаются только по affected systems.
- AI-review advisory, не заменяет людей.
- Blocking checks только формальные: schema, traceability, required artifacts, policy.
- Малые изменения могут идти через упрощённый spec patch в code PR.

---

## 10. Registry в `team-specs`

Registry нужен, чтобы автоматизация понимала проекты, владельцев, правила качества и места публикации.

```text
team-specs/sdd/registry/
  projects.yaml
  owners.yaml
  systems.yaml
  quality-policy.yaml
  confluence-map.yaml
  issue-types.yaml
```

### 10.1. `projects.yaml`

```yaml
projects:
  backend-auth:
    type: backend
    repo: ssh://bitbucket/scm/auth/backend-auth.git
    default_branch: main
    jira_project: AUTH
    test_layers: [unit, integration, api_contract]

  mobile-app:
    type: mobile
    repo: ssh://bitbucket/scm/mob/mobile-app.git
    default_branch: main
    jira_project: MOB
    test_layers: [unit, ui, e2e]

  api-at:
    type: api_at
    repo: ssh://bitbucket/scm/at/api-at.git
    default_branch: main
    framework: pytest

  mobile-at:
    type: mobile_at
    repo: ssh://bitbucket/scm/at/mobile-at.git
    default_branch: main
    framework: appium
```

### 10.2. `owners.yaml`

```yaml
domains:
  auth-session:
    analyst: auth-ba
    qa: auth-qa
    dev:
      - backend-auth-dev
      - mobile-auth-dev
    at:
      - api-at-team
      - mobile-at-team

repos:
  backend-auth:
    owners: [backend-auth-dev]
  mobile-app:
    owners: [mobile-auth-dev]
  api-at:
    owners: [api-at-team]
  mobile-at:
    owners: [mobile-at-team]
```

### 10.3. `quality-policy.yaml`

```yaml
rules:
  new_feature:
    requires:
      - proposal
      - spec_delta
      - design
      - test_plan
      - test_cases
      - automation_plan

  behavior_change:
    requires:
      - proposal
      - spec_delta
      - impact_analysis
      - updated_test_cases

  bugfix:
    requires:
      - bug_scenario
      - regression_test_or_waiver

  refactor:
    requires:
      - no_behavior_change_statement
      - test_evidence
```

---

## 11. `sdd CLI`: назначение и команды

`sdd CLI` - собственный командный инструмент команды. Он не заменяет OpenSpec CLI, а оборачивает OpenSpec, Git, Bitbucket, Jenkins, Jira, Confluence и локальные AI-инструменты в единый процесс.

### 11.1. Задачи `sdd CLI`

- Создавать change package по шаблонам.
- Валидировать структуру и policy.
- Генерировать context pack для локального AI.
- Создавать PR в Bitbucket.
- Назначать reviewer'ов по owners registry.
- Публиковать preview/final страницы в Confluence.
- Создавать задачи в Jira/трекере после merge Spec PR.
- Создавать QA/AT skeleton artifacts.
- Собирать inbox для ролей.
- Поддерживать traceability.
- Архивировать change и обновлять living specs.

### 11.2. Базовые команды

```bash
sdd init
sdd doctor
sdd sync
sdd inbox --role analyst
sdd inbox --role developer
sdd inbox --role qa
sdd inbox --role api-at
sdd inbox --role mobile-at
```

### 11.3. Команды для change

```bash
sdd change new <change-id>
sdd change validate <change-id>
sdd change pr <change-id>
sdd change status <change-id>
sdd change archive <change-id>
```

### 11.4. Команды для Confluence

```bash
sdd publish confluence --change <change-id> --preview
sdd publish confluence --change <change-id> --final
sdd confluence comments pull --change <change-id>
sdd confluence check-drift --change <change-id>
```

### 11.5. Команды для задач

```bash
sdd tasks plan --change <change-id>
sdd tasks create --change <change-id>
sdd tasks sync --change <change-id>
```

### 11.6. Команды разработчика

```bash
sdd dev start <task-id>
sdd dev context <task-id>
sdd dev pr <task-id>
sdd dev check <task-id>
```

### 11.7. Команды QA

```bash
sdd qa inbox
sdd qa propose --change <change-id>
sdd qa validate --change <change-id>
sdd qa export --target api-at
sdd qa export --target mobile-at
```

### 11.8. Команды AT

```bash
sdd at inbox --target api-at
sdd at inbox --target mobile-at
sdd at propose --change <change-id> --target api-at
sdd at propose --change <change-id> --target mobile-at
sdd at validate --change <change-id>
```

### 11.9. Команды AI-контекста

```bash
sdd ai context --change <change-id> --role analyst
sdd ai context --change <change-id> --role developer --task <task-id>
sdd ai context --change <change-id> --role qa
sdd ai context --change <change-id> --role api-at
```

Команда создаёт локальный context pack, который можно передать в Codex/Claude Code/Cursor/другой CLI-инструмент.

---

## 12. OpenSpec CLI и собственные расширения

### 12.1. Роль OpenSpec CLI

OpenSpec CLI используется для:

- структуры `openspec/changes` и `openspec/specs`;
- валидации spec deltas;
- поддержки SDD-подхода;
- работы с living specs;
- совместимости с локальными coding agents/AI tools.

### 12.2. Роль собственного `sdd CLI`

OpenSpec не должен отвечать за весь корпоративный процесс. Собственный `sdd CLI` добавляет:

- интеграции с Bitbucket/Jenkins/Jira/Confluence;
- corporate quality policy;
- owners registry;
- role inbox;
- publication pipeline;
- task generation;
- AT skeleton generation;
- traceability rules;
- local workspace setup.

### 12.3. Возможная структура CLI-проекта

```text
company-sdd-cli/
  src/
    core/
      config.ts
      validation.ts
      schemas.ts
      traceability.ts
    git/
      branches.ts
      pullRequests.ts
      diff.ts
    bitbucket/
      client.ts
      reviewers.ts
      codeInsights.ts
    jira/
      client.ts
      issueFactory.ts
    confluence/
      publisher.ts
      comments.ts
      drift.ts
    qa/
      testPlan.ts
      gherkin.ts
      coverage.ts
    at/
      skeleton.ts
      fixtures.ts
    ai/
      contextPack.ts
      prompts.ts
    commands/
      change.ts
      dev.ts
      qa.ts
      at.ts
      publish.ts
  templates/
  schemas/
  README.md
```

---

## 13. Интеграции

### 13.1. Bitbucket

Используется для:

- Spec PR;
- code PR;
- QA/AT PR;
- reviewer assignment;
- branch policies;
- PR comments;
- Code Insights reports от Jenkins/AI-review.

### 13.2. Jenkins

Используется для:

- validation pipelines;
- публикации Confluence preview/final;
- создания задач после merge;
- обновления traceability;
- запуска тестов;
- публикации отчётов в Bitbucket Code Insights;
- archive flow.

### 13.3. Jira/трекер задач

Используется для:

- dev tasks;
- QA tasks;
- AT tasks;
- workflow/status;
- связи задач с change-id и requirement-id.

Задачи создаются после approved/merged Spec PR, а не при первом черновике.

### 13.4. Confluence

Используется для:

- generated preview;
- финальной опубликованной документации;
- комментариев stakeholder'ов;
- согласований, если они требуются процессом;
- release/capability summaries.

### 13.5. Локальные AI-инструменты

Используются для:

- черновиков acceptance criteria;
- поиска неоднозначностей;
- ревью testability;
- генерации Gherkin drafts;
- подготовки skeleton автотестов;
- помощи разработчику в реализации;
- кратких PR summaries.

AI не должен иметь право автоматически approve/merge/publish без явного действия человека или CI-policy.

### 13.6. MCP

MCP можно подключать постепенно:

```text
Этап 1: без MCP, только CLI + API.
Этап 2: read-only MCP для поиска контекста в Confluence/Jira/Bitbucket.
Этап 3: ограниченные write-tools только для draft comments/descriptions.
```

Write-действия через MCP должны быть ограничены правами пользователя и требовать подтверждения.

---

## 14. CI/CD validation gates

### 14.1. Spec PR gate

```text
- change.yaml валиден по schema;
- change-id уникален;
- type/status указаны;
- affected systems существуют в registry;
- owners найдены;
- proposal.md заполнен;
- spec delta валиден;
- у каждого requirement есть scenario;
- у каждого scenario есть requirement-id;
- для new_feature/behavior_change есть test-plan;
- для API/mobile impact есть automation-plan или waiver;
- traceability.yaml валиден;
- Confluence preview собирается;
- запрещены ручные изменения generated markers.
```

### 14.2. Code PR gate

```text
- PR связан с approved change-id;
- task-id указан;
- touched requirements указаны;
- тесты добавлены или есть waiver;
- public API change требует docs update;
- contract change требует QA/AT visibility;
- build/tests проходят.
```

### 14.3. QA PR gate

```text
- test cases имеют requirement-id;
- test layer указан;
- tags валидны;
- coverage matrix заполнена;
- changed behavior покрыт тестами или waiver.
```

### 14.4. AT PR gate

```text
- automated tests имеют stable test-id;
- есть ссылка на requirement-id и test case;
- fixtures/test data описаны;
- flaky/blocked markers допустимы только с причиной;
- результаты тестов публикуются в отчётность.
```

---

## 15. Работа аналитика

### 15.1. Создание изменения

```bash
sdd sync
sdd change new AUTH-2026-071-add-remember-me
```

CLI создаёт package по шаблону.

Аналитик заполняет:

```text
proposal.md
specs/<capability>/spec.md
change.yaml
```

### 15.2. AI-помощь

```bash
sdd ai context --change AUTH-2026-071-add-remember-me --role analyst
```

AI можно попросить:

```text
- найти неоднозначные acceptance criteria;
- предложить edge cases;
- проверить scope/out of scope;
- превратить rough notes в структурированный proposal;
- предложить scenarios.
```

### 15.3. Публикация preview

```bash
sdd publish confluence --change AUTH-2026-071-add-remember-me --preview
sdd change pr AUTH-2026-071-add-remember-me
```

---

## 16. Работа разработчика

### 16.1. Получение задач

```bash
sdd sync
sdd inbox --role developer
```

CLI показывает задачи, связанные с approved changes.

### 16.2. Старт работы

```bash
sdd dev start AUTH-101
```

CLI делает:

```text
- проверяет актуальность team-specs;
- находит change-id;
- создаёт/переключает branch;
- собирает context pack;
- открывает связанные файлы proposal/spec/design/tasks;
- подготавливает PR template.
```

### 16.3. AI-контекст

```bash
sdd dev context AUTH-101
```

Context pack включает только нужное:

```text
- approved spec delta;
- related design section;
- assigned task;
- affected requirements;
- existing code map, если доступен;
- test expectations;
- ограничения scope.
```

---

## 17. Работа QA

### 17.1. QA inbox

```bash
sdd qa inbox
```

Показывает изменения, где требуется QA review, test-plan или проверка готовности.

### 17.2. Создание тестовых артефактов

```bash
sdd qa propose --change AUTH-2026-071-add-remember-me
```

CLI создаёт или обновляет:

```text
qa/test-plan.md
qa/test-cases/*.feature
qa/automation-plan.md
traceability.yaml
```

### 17.3. Что проверяет QA

```text
- все acceptance criteria тестируемы;
- есть позитивные/негативные сценарии;
- учтены edge cases;
- понятно, что проверяется вручную;
- понятно, что отдаётся в AT;
- есть тестовые данные/предусловия;
- есть regression impact.
```

---

## 18. Работа автотестеров

### 18.1. AT inbox

```bash
sdd at inbox --target api-at
sdd at inbox --target mobile-at
```

CLI показывает изменения, где нужна или возможна автоматизация.

### 18.2. Генерация skeleton PR

```bash
sdd at propose --change AUTH-2026-071-add-remember-me --target api-at
```

CLI создаёт draft branch/PR в `api-at` или `mobile-at`.

Skeleton содержит:

```text
- test file;
- requirement-id;
- test case id;
- TODO по fixtures;
- TODO по test data;
- предполагаемые assertions;
- ссылки на spec/change/task.
```

### 18.3. Принцип работы AT

ИИ может подготовить черновик автотеста, но автотестер отвечает за корректность, стабильность, данные, интеграцию с framework и отчётность.

---

## 19. Traceability model

Traceability хранится в `traceability.yaml` и/или синхронизируется с Jira/Allure/TestRail/Xray.

Пример:

```yaml
requirements:
  - id: REQ-AUTH-001
    title: Remember Me login option
    change: AUTH-2026-071-add-remember-me
    scenarios:
      - SCN-AUTH-001
    dev_tasks:
      - AUTH-101
    qa_tasks:
      - AUTH-120
    test_cases:
      - TC-AUTH-001
    automation:
      api:
        repo: api-at
        path: tests/auth/test_remember_me.py
        status: planned
      mobile:
        repo: mobile-at
        status: impacted
```

### 19.1. Минимальное правило

Нельзя закрыть change, если:

```text
- есть requirement без scenario;
- есть scenario без test case или waiver;
- есть required automation без AT status;
- есть dev task без связи с requirement;
- есть QA blocker.
```

---

## 20. Waiver-механизм

Waiver нужен для случаев, когда формальное требование можно не выполнять, но решение должно быть прозрачным.

```yaml
waiver:
  id: WVR-AUTH-001
  type: no_new_tests
  reason: Refactor only; no behavior change
  evidence:
    - Existing regression suite passed
    - No public API contract changed
  approved_by:
    - auth-qa-lead
```

Waiver не должен быть свободным текстом без владельца и evidence.

---

## 21. Role inbox и локальная работа без фонового агента

Локальный AI работает в формате request-response, поэтому мониторинг изменений делает не AI, а `sdd CLI`.

### 21.1. Команды

```bash
sdd sync
sdd inbox --role developer
sdd inbox --role qa
sdd inbox --role api-at
```

### 21.2. Что хранится локально

```text
~/.sdd/config.yaml
~/.sdd/state.json
~/.sdd/index.sqlite
```

Пример state:

```yaml
active_change: AUTH-2026-071-add-remember-me
active_task: AUTH-101
last_seen:
  spec_prs: 2026-07-01T10:00:00
  tasks: 2026-07-01T10:00:00
registered_repos:
  team-specs: ~/work/team-specs
  backend-auth: ~/work/backend-auth
  api-at: ~/work/api-at
```

### 21.3. Как не смешивать контексты

Правило:

```text
Один task/change = один AI context pack.
```

Для новостей используется `sdd inbox`, а не текущий AI-диалог.

---

## 22. Настройка рабочего места

### 22.1. Общее

```bash
git clone ssh://bitbucket/scm/sdd/team-specs.git ~/work/team-specs
sdd init
sdd config set team_specs_path ~/work/team-specs
sdd doctor
```

### 22.2. Для разработчика

```bash
git clone ssh://bitbucket/scm/auth/backend-auth.git ~/work/backend-auth
sdd register repo backend-auth ~/work/backend-auth
sdd doctor --role developer
```

### 22.3. Для QA

```bash
sdd doctor --role qa
sdd qa inbox
```

QA не обязан клонировать все code repos. Достаточно `team-specs`, а нужные репозитории CLI подсказывает по роли и задаче.

### 22.4. Для автотестера

```bash
git clone ssh://bitbucket/scm/at/api-at.git ~/work/api-at
sdd register repo api-at ~/work/api-at
sdd doctor --role api-at
```

---

## 23. Публикация в Confluence

### 23.1. Типы страниц

```text
/Changes/<change-id>
/Capabilities/<capability>
/Releases/<release>
/QA/<target>/<domain>
```

### 23.2. Generated page содержит

```text
- title;
- status;
- source commit;
- source PR;
- affected systems;
- requirements;
- scenarios;
- tasks;
- QA/AT status;
- links;
- generated timestamp;
- warning: generated content, edit source in Git.
```

### 23.3. Drift detection

Перед публикацией CLI проверяет, не меняли ли generated-блок вручную.

```bash
sdd confluence check-drift --change <change-id>
```

Если drift найден:

```text
- publication fails;
- author получает diff;
- можно перенести изменения в Git или выполнить force publish по правам.
```

---

## 24. Архивация change

После реализации и прохождения проверок:

```bash
sdd change archive <change-id>
```

Архивация делает:

```text
- применяет spec delta к openspec/specs;
- переносит change в archive;
- проверяет traceability completion;
- публикует final Confluence page;
- обновляет capability page;
- обновляет release summary, если нужно;
- закрывает/линкует связанные задачи.
```

---

## 25. Минимальная схема данных

### 25.1. `change.yaml`

```yaml
id: AUTH-2026-071-add-remember-me
title: Add Remember Me option to login
type: new_feature
status: spec_review

capability: auth-session

systems:
  code_repos:
    - backend-auth
    - mobile-app
  at_repos:
    - api-at
    - mobile-at

review:
  analyst_owner_group: auth-ba
  dev_owner_groups:
    - backend-auth-dev
    - mobile-auth-dev
  qa_owner_group: auth-qa
  at_owner_groups:
    - api-at-team
    - mobile-at-team

quality:
  manual_cases: required
  api_at: required
  mobile_at: impacted
  security_review: required

publication:
  confluence_space: AUTH
  page_id: null
  mode: generated
```

### 25.2. `proposal.md`

```markdown
# Proposal

## Problem

...

## Goal

...

## Scope

### In
- ...

### Out
- ...

## Acceptance criteria

- REQ-AUTH-001: ...
- REQ-AUTH-002: ...
```

### 25.3. `spec.md`

```markdown
## ADDED Requirements

### Requirement: Remember Me session

The system SHALL support an optional Remember Me mode during login.

#### Scenario: Login with Remember Me enabled
Given a user has valid credentials
When the user logs in with Remember Me enabled
Then the system creates an extended session
```

### 25.4. `qa/test-cases/*.feature`

```gherkin
@REQ-AUTH-001 @layer=api @target=api-at
Feature: Remember Me session

  Scenario: User enables Remember Me during login
    Given the user has valid credentials
    When the user logs in with Remember Me enabled
    Then the API returns an extended session token
```

---

## 26. Полная схема

```text
┌──────────────────────────────────────────────────────────────┐
│                         team-specs                           │
│  OpenSpec changes, living specs, QA/AT docs, traceability    │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               │ Spec PR
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                         Bitbucket                            │
│  Review by owners: analyst, dev, QA, AT by affected systems  │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               │ Jenkins validation
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                          Jenkins                             │
│  validate, AI advisory review, Confluence preview, gates     │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               │ generated preview
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                        Confluence                            │
│  Readable generated view, comments, approval if required     │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               │ approved + merged Spec PR
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                    Deterministic automation                   │
│  create dev tasks, QA tasks, AT tasks, links, traceability   │
└───────────────┬───────────────────────┬──────────────────────┘
                │                       │
                ▼                       ▼
┌────────────────────────────┐   ┌─────────────────────────────┐
│        Code repositories    │   │          QA / AT repos       │
│  backend, mobile, services  │   │  test cases, AT skeletons    │
└───────────────┬────────────┘   └──────────────┬──────────────┘
                │                               │
                │ code PR / tests               │ QA PR / AT PR
                ▼                               ▼
┌──────────────────────────────────────────────────────────────┐
│                    Verification and reporting                 │
│  CI tests, QA status, AT results, traceability completion     │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               │ done
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                           Archive                            │
│  update living specs, publish final Confluence, close change │
└──────────────────────────────────────────────────────────────┘
```

---

## 27. Рекомендуемый план внедрения

### Этап 1. Минимальный пилот

```text
- создать team-specs repo;
- добавить базовую OpenSpec-структуру;
- добавить шаблоны change.yaml/proposal/design/tasks;
- настроить Spec PR и Jenkins validation;
- публиковать Confluence preview;
- один пилотный проект, один QA-поток.
```

### Этап 2. Task automation

```text
- добавить registry проектов и владельцев;
- автоматически назначать reviewer'ов;
- создавать Jira/dev/QA задачи после merge Spec PR;
- обновлять links и traceability.
```

### Этап 3. QA/AT automation

```text
- добавить qa/test-plan.md и Gherkin test cases;
- добавить sdd qa inbox/propose;
- добавить sdd at inbox/propose;
- создавать draft PR в api-at/mobile-at.
```

### Этап 4. Укрепление процесса

```text
- добавить waiver policy;
- добавить role inbox;
- добавить drift detection в Confluence;
- добавить Code Insights reports;
- добавить read-only MCP при необходимости.
```

---

## 28. Минимальный набор для старта

Для первого рабочего прототипа достаточно:

```text
1. team-specs repo.
2. OpenSpec CLI.
3. company sdd CLI с командами:
   - sdd change new
   - sdd change validate
   - sdd change pr
   - sdd publish confluence
   - sdd tasks create
   - sdd qa propose
   - sdd at propose
   - sdd inbox
4. Jenkins pipeline для Spec PR.
5. Bitbucket reviewer assignment.
6. Confluence generated preview.
7. Jira task creation после merge.
8. traceability.yaml.
```

---

## 29. Итоговое решение

Итоговая архитектура:

```text
OpenSpec/Markdown-first
+ центральный team-specs repo
+ Confluence как generated publication layer
+ Bitbucket PR как review/audit layer
+ Jenkins как validation/automation layer
+ Jira/трекер как workflow layer
+ отдельные code и AT repos
+ собственный sdd CLI как единый процессный интерфейс
+ локальные AI-инструменты как помощники, не владельцы процесса
```

Это решение сохраняет привычные корпоративные инструменты, убирает ручную склейку между аналитикой, разработкой и тестированием и не требует дорогого централизованного автономного агента.
