# Дизайн человекочитаемого roadmap в FAQ

Дата: 2026-07-24
Статус: утверждённое направление, реализация не начата

## Цель

Перестроить `docs/faq/roadmap.md` так, чтобы новый участник понимал развитие
продукта без знания фаз, внутренних work item, OpenSpec lifecycle и названий
технических артефактов.

Страница должна отвечать на пять вопросов:

1. Что уже работает?
2. Что появится следующим?
3. Что запланировано позже?
4. Что намеренно пока недоступно?
5. Где посмотреть точную открытую спецификацию конкретной будущей возможности?

## Выбранный вариант

Сохраняется одна основная FAQ-страница roadmap. Она не дробится на отдельную
страницу для каждой будущей функции.

Внутри используются подробные capability-карточки. Каждая карточка объясняет:

- название возможности человеческими словами;
- что это;
- зачем это нужно;
- что получит пользователь;
- что уже подготовлено;
- что ещё не реализовано;
- текущий понятный статус;
- точное имя OpenSpec change;
- ссылки на proposal, design, specs и tasks;
- условие, после которого возможна реализация или использование.

## Структура страницы

### 1. Как читать roadmap

В начале страницы располагается короткая легенда:

- **Работает сейчас** — функция реализована и подтверждена указанными
  проверками/ограничениями.
- **Следующее** — ближайший пользовательский результат с незакрытым gate.
- **Запланировано** — направление и открытая спека существуют, но функция ещё
  недоступна.
- **Намеренно недоступно** — действие заблокировано ради безопасности или пока
  не имеет принятого контракта.

Наличие design, template или OpenSpec change не означает, что функция уже
работает.

### 2. Что работает сейчас

Краткие карточки текущих пользовательских результатов:

- установка и проверка `sdd`;
- создание central workspace;
- situation-first старт и продолжение change;
- role-aware guidance;
- deterministic checks и AI-disabled fallback;
- class-aware changes, evidence и failed-run history;
- минимальные typed analytics и локальный read-only preview.

Карточки не перечисляют внутренние номера задач. Они честно называют известные
границы, особенно fail-closed mutation и отсутствие внешних изменений.

### 3. Что появится следующим

Показываются не фазы, а практические результаты:

- независимый first-time walkthrough;
- завершение onboarding acceptance;
- обязательная Linux/WSL2 portability-проверка перед корпоративным этапом.

Для каждого результата указывается, что именно остаётся сделать и почему без
этого нельзя считать следующий этап доступным.

### 4. Что запланировано позже

Каждая крупная возможность получает отдельную capability-карточку.

Минимальный набор:

1. Corporate adaptation и monitored pilot.
2. AI Analyst Discovery Skill.
3. Полная аналитика ФП и страницы релизных инкрементов.
4. Controlled Confluence publication.
5. Jira task planning, QA/AT layers и role inbox.
6. Дальнейшая bounded AI automation.

### 5. Что намеренно недоступно

Сохраняется отдельный список действий, которые нельзя считать доступными:

- `sdd run` mutations;
- AI approval/risk/waiver/release/archive;
- автоматическое изменение Jira, Confluence, Bitbucket и Jenkins;
- deploy/customer acceptance;
- silent defaults;
- удаление failed-run evidence.

### 6. Как проверить статус

Порядок проверки:

1. прочитать capability-карточку;
2. проверить установленный CLI;
3. открыть linked OpenSpec change;
4. различать `planned`, task progress, human acceptance и реально доступное
   поведение.

## Обязательная карточка аналитики ФП

Человекочитаемое название:

> Полная аналитика ФП и страницы релизных инкрементов

Точное имя открытой спеки:

> `define-fp-analytics-publication-model`

Карточка объясняет:

### Что это

- одна полная актуальная generated page на каждую самостоятельную ФП;
- отдельная зафиксированная page на каждый релизный инкремент;
- отдельная обязательная Confluence page на каждый change не создаётся.

### Для чего

- человеку не нужно искать аналитику ФП среди specs десятков проектов;
- текущая страница показывает целостное состояние ФП;
- релизные страницы сохраняют историю изменений;
- один релиз может включать функциональность разных ФП;
- ownership требований не переносится и нормативный текст не копируется.

### Как выглядит актуальность

- основное тело current page показывает подтверждённое доставленное состояние;
- active и approved-not-delivered changes отображаются отдельно;
- после доставки выполняется reconciliation всех затронутых ФП;
- незавершённое обновление остаётся видимым gap.

### Как хранятся сложные таблицы

- Markdown используется для человекочитаемого объяснения;
- OpenSpec владеет нормативным поведением и сценариями;
- typed YAML хранит статусы, данные, API, platform services и другие
  повторяемые модели;
- renderer собирает вложенные таблицы и expand blocks;
- Confluence остаётся generated read model.

### Как участвует AI

- AI Analyst Discovery Skill помогает пройти интервью и создать черновик;
- `confirmed | proposed | unknown | conflict` не смешиваются;
- интервью и draft не становятся delivered truth;
- публикация использует только reviewed canonical artifacts;
- ownership, release inclusion, approval и delivery остаются решениями людей.

### Честный статус

- решение `D-029` принято;
- proposal/design/specs/tasks подготовлены;
- change имеет `0/70` implementation tasks;
- publisher, расширенные schemas, renderers и corporate publication ещё не
  реализованы;
- точные Confluence mappings/macros/adapter требуют corporate capability probe.

### Ссылки

Карточка должна вести непосредственно на:

- `openspec/changes/define-fp-analytics-publication-model/proposal.md`;
- `openspec/changes/define-fp-analytics-publication-model/design.md`;
- `openspec/changes/define-fp-analytics-publication-model/specs/`;
- `openspec/changes/define-fp-analytics-publication-model/tasks.md`;
- `docs/audits/ANALYTIC_TEMPLATE_AND_CONFLUENCE_PUBLICATION_GAP_AUDIT_2026-07-24.md`;
- `docs/superpowers/specs/2026-07-24-ai-analyst-discovery-skill-design.md`.

## Другие planned capability-карточки

Остальные карточки используют тот же формат, но могут быть короче:

- corporate adaptation/pilot — реальная конфигурация и один monitored change;
- AI Analyst Discovery — интервью из простой фразы, truth statuses, human
  summary, drafts и остановки перед файлами/командами;
- controlled Confluence publication — только после profile/capability probe;
- Jira/QA/AT/inbox — отдельные последующие contracts;
- bounded AI automation — только поверх deterministic control plane и без
  передачи human authority.

## OpenSpec и documentation changes

Реализация должна:

1. обновить `docs/faq/roadmap.md`;
2. при необходимости уточнить подпись ссылки в `docs/faq/index.md`;
3. дополнить активный change `add-product-faq-and-role-runbook` требованием или
   сценарием о capability-карточках и явных OpenSpec links;
4. добавить отдельную task/evidence запись для remediation;
5. расширить FAQ validation/tests, чтобы карточка аналитики не могла потерять:
   понятное название, status, точное change ID и ссылки;
6. не дублировать нормативные требования из publication change.

## Проверка

Автоматически:

- FAQ validator;
- FAQ documentation tests;
- broken-link and required-content negative tests;
- `openspec validate --all --strict`;
- roadmap/OpenSpec validator;
- `git diff --check`.

Вручную:

- новый человек может объяснить разницу между «есть открытая спека» и
  «функция работает»;
- человек может назвать два planned publication views;
- человек может найти `define-fp-analytics-publication-model`;
- человек понимает, почему AI discovery draft не является опубликованным
  фактом.

## Не входит

- реализация analytics publication;
- изменение lifecycle или phase status publication change;
- создание Confluence pages;
- реализация AI Analyst Discovery Skill;
- обещания календарных дат;
- копирование полного publication design в FAQ.
