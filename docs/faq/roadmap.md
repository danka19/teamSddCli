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

## Работает сейчас

### Локальный маршрут через одну команду `sdd`

**Что это.** Установленный versioned package даёт команды `sdd setup`,
`sdd start`, `sdd next`, `sdd op`, `sdd check`, `sdd prepare` и
`sdd request`. Они создают central `process/` + `team-specs/` workspace только
после человеческого `--confirm`, выбирают role-aware маршрут и возвращают
human-readable или structured `--json` результат.

**Для чего.** Новый участник начинает с понятной ситуации и видит следующий
шаг, необходимые факты, evidence и authority boundary, не разыскивая внутренние
Python-скрипты.

**Статус и граница.** Guided, read-only и preparation routes работают локально.
`sdd next` читает канонический schema-v2 `status`. Команда `sdd run` остаётся
fail-closed и не выполняет mutation или внешнее действие.

### Управляемые changes, evidence и локальная аналитика

**Что это.** В Git можно хранить class-aware changes `minor | major | hotfix`,
requirements, human decisions, evidence, traceability и failed-run history.
Typed analytics artifacts уже имеют минимальный локальный read-only preview.

**Для чего.** Команда видит, почему выбран класс изменения, какие проверки
выполнены, кто принял решение и где работа остановилась.

**Статус и граница.** Это рабочая OpenSpec/Markdown-first основа. Текущий
analytics preview не является полной аналитической базой ФП и пока не
публикуется автоматически в Confluence.

### Работа с AI и без AI

**Что это.** AI может объяснять маршрут, готовить draft и запускать отдельно
разрешённые локальные команды с `--json`. Тот же обязательный процесс можно
пройти без AI.

**Для чего.** AI ускоряет поиск контекста и подготовку материалов, но процесс не
останавливается, если модель или интеграция недоступны.

**Статус и граница.** Deterministic checks и AI-disabled fallback уже
доступны. AI не получает authority: не подтверждает классификацию, риск,
waiver, merge, release или archive и не подставляет `--confirm` вместо человека.

### AI Analyst Discovery

**Что это.** Установленный companion принимает обычную фразу аналитика,
показывает план тем, после разрешения задаёт по одному вопросу и разделяет
`confirmed`, `proposed`, `unknown` и `conflict`. После подтверждённой сводки он
предлагает только один разрешённый текущим stage черновик и отдельно спрашивает
о переходе к командам.

**Для чего.** Аналитик может превратить сырую идею в проверяемый draft без
копирования длинного технического prompt и без выдачи догадки AI за требование.

**Статус и граница.** Реализация уже входит в process package `0.3.7`;
OpenSpec change `add-ai-analyst-discovery` выполнен на `12/13`. Capability
работает сейчас, но остаётся `pending_acceptance`: first-time human walkthrough
ещё не записан. AI не создаёт весь пакет одним действием и не принимает
classification, approval, merge, release или archive за человека.

- [Первый minor change вместе с AI](first-change-with-ai.md)
- [Правила работы с AI](ai-collaboration.md)
- [OpenSpec change](../../openspec/changes/add-ai-analyst-discovery/proposal.md)

## Следующее

### Проверка FAQ человеком, который впервые видит продукт

**Что это.** Независимый участник должен по FAQ установить package, пройти
real-package route, объяснить границы полномочий и указать, куда передавать
работу.

**Для чего.** Автоматические тесты доказывают наличие разделов, ссылок и
команд, но не доказывают, что инструкция действительно понятна новичку.

**Статус и граница.** Это незакрытая задача 4.4 change
`add-product-faq-and-role-runbook`. До человеческого walkthrough FAQ не получает
финальную content acceptance.

### Проверка AI-интервью аналитиком

**Что это.** Человек, который впервые использует companion, должен начать
простой фразой и проверить план тем, вопросы по одному, обработку «не знаю»,
подтверждение сводки, один разрешённый draft и остановку перед первой командой.

**Для чего.** Контрактные тесты подтверждают инструкции и границы полномочий,
но не доказывают, что живой диалог удобен аналитику без знания внутренних
команд.

**Статус и граница.** Это открытая task 5.3 change
`add-ai-analyst-discovery`. Она блокирует human acceptance и archive, но не
отменяет факт, что capability уже установлена и работает в package `0.3.7`.

### Portability перед корпоративной адаптацией

**Что это.** Принятый reusable package должен пройти Linux/WSL2 portability
gate до переноса в ограниченную корпоративную среду.

**Для чего.** Проверка отделяет переносимый процесс от случайной зависимости
на текущий Windows workspace.

**Статус и граница.** Gate ещё не закрыт. Corporate adaptation и pilot не
считаются начатыми до его прохождения и отдельного человеческого решения.

## Запланировано

### Полная аналитика ФП и страницы релизных инкрементов

**Что это.** Для каждой самостоятельной ФП будет одна полная актуальная
страница аналитики. Для каждого релиза будет создаваться отдельная страница
релизного инкремента.

Коротко: одна полная актуальная страница для ФП и отдельная страница каждого релизного инкремента.

Отдельная обязательная Confluence-страница на каждый change не нужна: change
остаётся рабочей единицей в Git/OpenSpec, а его delta входит в страницу
релизного инкремента.

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

### Контролируемая публикация в Confluence

**Что это.** Publisher будет собирать current FP page и release increment page
из reviewed canonical artifacts, публиковать их по явным space/parent mappings
и сохранять traceability до исходных changes.

**Для чего.** Люди получат удобные страницы и вложенные таблицы в Confluence,
не превращая Confluence во второй редактируемый источник требований.

**Статус и граница.** Это часть открытой спеки
`define-fp-analytics-publication-model`, а не отдельная уже работающая функция.
Локальные contracts проектируются заранее, но реальная публикация зависит от
corporate capability probe и человеческого разрешения внешней mutation.

### Corporate adaptation и monitored pilot

**Что это.** После переносимости package в корпоративной среде будут заполнены
только реальные non-secret project/owner/config values, подключены доступные
standard tools и thin adapter, затем проведён один наблюдаемый governed-change
pilot.

**Для чего.** Pilot проверит процесс на настоящих ограничениях и даст evidence
для точечных usability/reliability исправлений без перепроектирования процесса
по догадкам.

**Статус и граница.** Это будущий этап после portability и human acceptance.
Корпоративные credentials, production data и неподтверждённые integration
возможности не закладываются в reusable package.

### Планирование задач, QA/AT proposals и role inbox

**Что это.** Поздние слои смогут готовить Jira task plan, предложения по QA/AT
и role-specific очередь следующей работы из принятого change package.

**Для чего.** Командам не придётся вручную переносить одну и ту же структуру
из требований в рабочие представления для ролей.

**Статус и граница.** Для этих слоёв ещё нужны отдельные принятые contracts.
Их наличие в roadmap не означает Jira mutation, создание тест-кейсов или
готовый role inbox.

### Ограниченная AI-автоматизация поверх deterministic control plane

**Что это.** AI сможет помогать с decomposition, evidence assembly, routing,
monitoring и подготовкой разрешённых state transitions.

**Для чего.** Повторяемая подготовительная работа станет быстрее, а человек
будет получать более полный пакет для решения.

**Статус и граница.** Автоматизация будет добавляться отдельными принятыми
changes. Deterministic policy checks остаются control plane, а approvals,
waivers, risk acceptance, merge, release и archive остаются у людей.

## Намеренно недоступно

Это safety/status boundary, а не список забытых функций. Пока действие
находится здесь, документация и инструменты не должны изображать его
выполненным:

- `sdd run` mutations в текущей версии;
- AI approval, risk acceptance, waiver, merge, release или archive;
- автоматическое изменение Jira, Confluence, Bitbucket и Jenkins;
- deploy и customer acceptance;
- Jira tasks, Confluence publication, QA/AT generation и role inbox в первом
  MVP;
- silent defaults при неизвестном факте;
- удаление failed-run после успешного retry.

## Как проверить статус конкретной функции

1. Найдите карточку на этой странице и прочитайте её `Статус и граница`.
2. Проверьте `sdd --help` и `sdd op list --json` для установленной версии.
3. Если карточка называет OpenSpec change, откройте его `proposal.md`,
   `design.md`, `spec.md` и `tasks.md`.
4. Не считайте planned capability доступной только потому, что о ней есть
   template, design, draft или заполненный план.
