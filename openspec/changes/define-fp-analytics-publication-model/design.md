## Context

### Проблема

Команда работает с десятками самостоятельных функциональных платформ (ФП). У каждой ФП могут быть:

- собственные владельцы и команда;
- независимый жизненный цикл;
- собственные изменения и релизы;
- функциональность, не связанная с другими ФП;
- функциональность, зависимая от других ФП;
- релиз, включающий изменения, принадлежащие другим ФП.

Принятая центральная топология `team-specs` удобна как единая точка контроля, но без FP namespace превращает `openspec/specs/` и аналитику в общий неориентируемый список. Сырой OpenSpec хорошо подходит для нормативных требований, сценариев и AI-контекста, но недостаточен как ежедневная человекочитаемая аналитическая документация.

Повторная проверка 38 изображений корпоративного шаблона показала, что будущая публикация должна уметь собирать:

- карточку решения;
- контакты и ответственность;
- бизнес- и функциональные требования;
- пользовательские, технические, альтернативные, ошибочные и degraded-сценарии;
- формы, экраны и диаграммы;
- статусные модели и поддержку каналов;
- модели данных;
- компоненты, размещение и API;
- безопасность и маскирование;
- платформенные сервисы с разными типами вложенной конфигурации;
- нагрузку, раскатку, переключатели и исключения;
- чек-листы, согласования и историю.

Текущий P3 typed analytics framework сознательно является компактным локальным каркасом. Его manifest и семь предметных схем не являются полной моделью корпоративной аналитики и не реализуют Confluence publication.

### Принятое решение владельца

Целевая модель содержит два основных вида страниц:

1. **Одна полная актуальная страница аналитики для каждой ФП.**
2. **Отдельная страница для каждого релиза/инкремента.**

Страница отдельного изменения не является самостоятельным обязательным типом публикации. Change package остаётся канонической рабочей единицей в Git/OpenSpec и входит в релизную страницу как источник релизной дельты.

### Stakeholders

- аналитик и системный аналитик — авторы и владельцы смысла аналитики;
- product/business owner — владелец цели, области и бизнес-решений;
- Tech Lead/архитектор — владелец технических границ и решений в своей зоне;
- разработчики, QA и AT — потребители требований, сценариев и evidence;
- владельцы ФП — владельцы FP namespace и cross-FP зависимостей;
- release owner — владелец состава и финализации релизного инкремента;
- security/architecture/operations reviewers — владельцы специализированных согласований;
- AI assistants — локальные помощники по подготовке и проверке, но не владельцы решений;
- Confluence readers — потребители generated read model.

### Архитектурные ограничения

- Git/OpenSpec/Markdown/YAML — канонический источник.
- Confluence — generated read model, а не место ручного ведения требований.
- Jira/tracker — workflow/status, а не источник смысла требований.
- Bitbucket/PR/recorded human decision — источник review/approval evidence.
- AI не утверждает применимость, полноту, согласование, релизный состав или доставленность.
- Процесс должен работать и проверяться при отключённом AI.
- Реальные space IDs, parent page IDs, credentials, API/MCP capabilities и разрешённые Confluence macros проверяются только в корпоративной среде.
- Корпоративные материалы, изображения и секреты не переносятся в публичный/внешний reusable package.

## Goals / Non-Goals

**Goals:**

- дать человеку одну понятную точку входа в текущее состояние каждой ФП;
- сохранять историю каждого релизного инкремента отдельной страницей;
- поддержать самостоятельные и связанные ФП без копирования требований;
- сделать структуру Git предсказуемой для человека, валидатора и AI;
- детерминированно собирать сложные и вложенные таблицы из typed sources;
- отделить доставленное состояние от изменений в работе;
- обеспечить трассировку от страницы до FP/change/release/requirement/scenario/evidence;
- обеспечить одинаковую semantic publication model для local preview и Confluence;
- предусмотреть проверяемую миграцию существующей аналитики;
- сохранить возможность ручной работы без AI и без Confluence.

**Non-Goals:**

- реализация Confluence publisher в рамках этого proposal;
- выбор конкретного Confluence REST/MCP/standard-tool adapter до корпоративной проверки;
- автоматическая публикация или изменение внешнего состояния без отдельного разрешения;
- bidirectional sync между Confluence и Git;
- сохранение Confluence как редактируемого master document;
- одна огромная страница на весь портфель из десятков ФП;
- обязательная отдельная Confluence-страница на каждый change package;
- перенос реальных корпоративных credentials, space IDs, данных или внутренних изображений;
- массовая миграция всех исторических документов до пилота;
- автоматическое признание страницы полной на основании AI-оценки;
- изменение human approval, release, risk acceptance или waiver authority.

## Decisions

### D1. Единица текущей документации — самостоятельная ФП

Для каждой ФП существует ровно одна логическая **актуальная страница аналитики**. Она имеет стабильный `fp_id`, стабильный publication identity и постоянный URL/Confluence page ID после первого связывания.

Страница не создаётся на репозиторий и не подразумевает `1 repository = 1 FP`. Один central `team-specs` содержит много FP namespaces; одна ФП может быть реализована несколькими кодовыми репозиториями.

**Почему:** ФП является устойчивой единицей ответственности и навигации, тогда как репозитории являются техническими контейнерами, а релизы и изменения меняются во времени.

**Отклонено:**

- одна страница на весь портфель — слишком велика и смешивает владельцев;
- одна страница на capability — дробит контекст и усложняет поиск;
- одна страница на репозиторий — не соответствует бизнес- и release-границам;
- одна страница на change — не даёт актуального целостного состояния.

### D2. Актуальная страница различает доставленное состояние и работу в процессе

Основное тело актуальной страницы показывает **последнее подтверждённое доставленное состояние** ФП.

Страница дополнительно содержит блоки:

- `Изменения в работе` — ссылки на active change packages и их evidence-backed state;
- `Одобрено, но не доставлено` — изменения, прошедшие требуемые gates, но ещё не вошедшие в доставленный релиз;
- `Открытые вопросы и риски` — unresolved items с владельцем и ссылкой на каноническую запись;
- `Последний доставленный инкремент` — ссылка на соответствующую release page.

Недоставленное поведение не смешивается с текущими фактами. После подтверждения `delivered` release reconciliation обновляет living analytics и основное тело страницы.

**Почему:** «актуальная» должна означать реальное известное состояние продукта, а не смесь deployed, approved и draft.

### D3. Единица истории — релизный инкремент

Каждый релиз/инкремент имеет отдельный стабильный `release_id` и отдельную страницу.

Release increment — именованный состав изменений, доставляемый и сверяемый как одна единица. Он не равен автоматически Git tag, Jira version или pipeline run, но может хранить ссылки на них.

Страница проходит состояния:

```text
draft -> candidate -> published -> delivered
                   \-> cancelled
```

- `draft`: состав меняется;
- `candidate`: состав зафиксирован для release review;
- `published`: страница создана из конкретных source revisions;
- `delivered`: имеется human/evidence-backed подтверждение доставки;
- `cancelled`: инкремент отменён с причиной.

После `published` состав и нормативное описание не переписываются молча. Исправление требует:

- нового page revision с `correction_reason`, предыдущим `content_digest` и ссылкой на исправляющий change; либо
- отдельного correction increment, если исправление относится к продукту, а не к опечатке публикации.

Git manifest сохраняет историю и digest независимо от Confluence version history.

### D4. Релиз может включать несколько ФП, но владение не переносится

Release manifest содержит:

- `release_id`;
- `title`;
- `owner_fp_id`;
- `release_owner`;
- `affected_fp_ids`;
- `included_changes`;
- `source_revisions`;
- `candidate_at`, `published_at`, `delivered_at`;
- release/evidence references;
- content digest и publication state.

Каждый `included_change` содержит:

- `change_id`;
- `owning_fp_id`;
- `affected_fp_ids`;
- `capability_ids`;
- requirement/scenario ID references;
- inclusion status;
- source commit/PR;
- verification/waiver references;
- optional dependency links.

Функция другой ФП остаётся в analytics/OpenSpec своей owning FP. Релизная страница агрегирует ссылки и объясняет вклад, но не копирует нормативный текст.

После доставки обновляется актуальная страница каждой затронутой ФП только в пределах принадлежащего ей содержания. Consumer FP может показать зависимость и пользовательский эффект ссылкой на owning FP.

### D5. Центральная структура разделяется по смыслу, а не по репозиториям

Целевая логическая структура:

```text
team-specs/
├── sdd.config.yaml
├── owners.yaml
├── projects.yaml
├── fp-catalog.yaml
├── fps/
│   └── <fp-id>/
│       ├── fp.yaml
│       ├── README.md
│       └── analytics/
│           ├── README.md
│           ├── overview.md
│           ├── business/
│           ├── functional/
│           ├── architecture/
│           ├── operations/
│           ├── decisions/
│           ├── artifacts/
│           ├── diagrams/
│           └── assets/
├── openspec/
│   ├── changes/
│   └── specs/
├── releases/
│   └── <release-id>/
│       └── release.yaml
└── publication/
    ├── profiles/
    ├── documents/
    └── state/
```

Физическое имя OpenSpec capability должно оставаться совместимым с поддерживаемым OpenSpec CLI. Если CLI не поддерживает желаемую вложенность, используется flat compound ID, например `<fp-id>--<capability-id>`, а `fp_id` хранится также в валидируемых metadata.

`projects.yaml` регистрирует технические проекты/репозитории. `fp-catalog.yaml` регистрирует продуктовые/функциональные пространства. Один проект может участвовать в нескольких ФП, одна ФП — использовать несколько проектов.

### D6. Человекочитаемая аналитика и OpenSpec имеют разные обязанности

| Информация | Канонический владелец | Представление |
|---|---|---|
| Назначение ФП, границы, терминология, контекст | Markdown analytics | Актуальная страница ФП |
| Нормативное поведение и acceptance scenarios | OpenSpec Master/Delta Specs | Секции требований и сценариев |
| Повторяемые модели и таблицы | Typed YAML | Таблицы, диаграммы, матрицы |
| Визуальные материалы | Git source/source+export + stable asset ID | Встроенные изображения/диаграммы |
| Change intent и design | Change package | Блоки изменений в работе и release delta |
| Release composition | `release.yaml` | Страница инкремента |
| Approval/review/test status | PR/CI/tracker/evidence/waiver references | Evidence-backed status |
| Обсуждение в Confluence | Comment + disposition record | Feedback, не requirement source |

Markdown не дублирует полные нормативные требования. Он объясняет смысл и ссылается на стабильные requirement/scenario IDs.

### D7. Актуальная страница ФП имеет фиксированный смысловой каркас

Одна логическая страница содержит следующие секции:

1. **Карточка ФП**
   - название, `fp_id`, назначение;
   - владелец и контакт;
   - уровень зрелости/состояние с evidence;
   - дата и источник генерации;
   - последний доставленный release;
   - предупреждение о generated source.
2. **Кратко для нового читателя**
   - что делает ФП;
   - для кого;
   - какую ценность даёт;
   - границы ответственности;
   - что не входит.
3. **Контакты и ответственность**
   - product/business owner;
   - аналитики;
   - Tech Lead/архитектор;
   - QA/AT;
   - security/operations contacts;
   - owner zones и escalation route.
4. **Бизнес-контекст**
   - бизнес-требования;
   - цели и ограничения;
   - термины;
   - допущения;
   - открытые вопросы.
5. **Функциональная аналитика**
   - capability map;
   - пользовательские journey/use cases;
   - функциональные требования и сценарии;
   - alternative/error/degraded flows;
   - формы, экраны и channel support;
   - status models.
6. **Архитектура решения**
   - system/context boundaries;
   - компоненты и размещение;
   - data models;
   - provided/consumed APIs;
   - async jobs/events;
   - внешние и платформенные интеграции.
7. **Безопасность**
   - классификация данных;
   - маскирование;
   - secrets references;
   - роли/privileges;
   - обязательные согласования и evidence.
8. **Нефункциональные и эксплуатационные требования**
   - platform services;
   - logging/audit/monitoring;
   - performance/load/TPS;
   - availability/degraded behavior;
   - rollout/toggles/channels;
   - rollback/technical breaks;
   - exceptions/waivers.
9. **Проверки и согласования**
   - применимые checklist IDs;
   - evidence-backed completion;
   - unresolved blockers;
   - approved waivers.
10. **Текущее состояние изменений**
    - последний доставленный инкремент;
    - approved not delivered;
    - changes in progress;
    - открытые cross-FP зависимости;
    - известные gaps/risks.
11. **История релизных инкрементов**
    - упорядоченный список release pages;
    - дата, состояние, краткий эффект;
    - correction/supersession links.
12. **Источник и трассировка**
    - source commit;
    - generation timestamp;
    - publication profile/version;
    - source file links;
    - content digest.

Секции могут использовать Confluence expand blocks, anchors и оглавление, но остаются одной логической страницей. Renderer не делит актуальную аналитику на произвольные child pages без отдельного corporate profile decision.

### D8. Страница релизного инкремента имеет отдельный каркас

1. **Карточка релиза**
   - `release_id`, название, owner FP;
   - состояние, planned/delivered даты;
   - release owner;
   - source commit/digest;
   - ссылки на release evidence.
2. **Цель и пользовательский эффект**
   - зачем выпускался инкремент;
   - что изменилось для пользователей/операторов;
   - ограничения и exclusions.
3. **Состав**
   - included changes;
   - owning/affected FP;
   - capabilities;
   - inclusion/cancellation status.
4. **Дельта аналитики**
   - добавленные/изменённые/удалённые требования;
   - затронутые сценарии;
   - status/channel/data/API/UI/architecture delta;
   - migration/compatibility impact.
5. **Cross-FP зависимости**
   - dependency direction/type;
   - owner;
   - expected/verified state;
   - unresolved blockers.
6. **Проверки, риски и согласования**
   - QA/AT/CI/manual evidence;
   - security/architecture/operations approvals;
   - waivers;
   - rollback/hold conditions.
7. **Доставка и reconciliation**
   - delivery evidence;
   - project/repository/PR/build references;
   - какие FP current pages обновлены;
   - reconciliation status.
8. **Источник**
   - frozen release manifest;
   - source revisions;
   - generation/publish timestamps;
   - publication profile;
   - digest/correction chain.

### D9. Typed sources моделируют предметную область, а не внешний вид таблицы

Набор typed artifacts расширяется поэтапно. Минимальный целевой каталог:

| Artifact | Назначение |
|---|---|
| `analytics-manifest.yaml` | FP/capability identity и перечень источников |
| `contacts.yaml` | роли, владельцы, escalation и зоны ответственности |
| `business-context.yaml` или Markdown metadata | цели, ограничения, assumptions/open questions |
| `journeys.yaml` | journeys, шаги и связи requirements/scenarios/screens |
| `screens.yaml` | stable screen IDs, assets и состояния |
| `status-model.yaml` | статусы, descriptions, entry actions, transitions и conditions |
| `channel-support.yaml` | channel/capability/operation matrix |
| `data-model.yaml` | entities, attributes, master/storage/cache/masking/export |
| `components.yaml` | components, deployment, repository/runtime metadata |
| `api-catalog.yaml` | provided/consumed, type, provider/consumer, purpose, contract, auth |
| `platform-services.yaml` | discriminated service configurations |
| `security.yaml` | data classification, masking, secrets refs, roles и approvals |
| `performance.yaml` | load/TPS/latency/capacity assumptions и evidence |
| `rollout.yaml` | toggles, channels, phases, rollback и technical-break behavior |
| `checklists.yaml` | applicable checklists, evidence и waiver refs |
| `release.yaml` | frozen increment composition и source identities |
| `publication.yaml` | page type, source selection, profile, target и digest |

Схемы закрываются `additionalProperties: false` там, где контракт стабилен. Расширение выполняется версионировано.

### D10. Platform services используют discriminated records

`platform-services.yaml` не является списком произвольных строк. Каждая запись имеет `service_kind`, который выбирает конкретную конфигурацию, например:

- `parameter-store`;
- `logging`;
- `audit`;
- `monitoring`;
- `authorization`;
- `toggler`;
- `profile`;
- `confirmation`;
- `content`;
- `scheduler`;
- `secret-store`;
- `other-approved`.

Общая оболочка содержит ID, purpose, owner, applicability, dependency, degraded behavior и evidence links. Внутренняя схема зависит от `service_kind`.

Примеры:

- audit event содержит event code, condition и attributes;
- monitoring metric содержит name, meaning, measurement point и event value;
- authorization содержит role, description, privilege/action и channels;
- parameter store содержит key, description, type, default/list и role.

Renderer выбирается по семантическому типу и может построить вложенную таблицу или expand block.

### D11. Вложенность является renderer contract

Канонический источник не содержит вручную поддерживаемые вложенные Markdown/HTML-таблицы.

Допустимо:

- простая плоская Markdown-таблица для небольшого человекочитаемого списка;
- typed YAML для сложных повторяемых структур;
- generated local HTML/Markdown preview;
- generated Confluence nested table/expand content.

Каждый section renderer объявляет:

- поддерживаемый source type/schema version;
- output block type;
- nesting strategy;
- anchor/ID strategy;
- empty/not-applicable behavior;
- wide-table fallback;
- unsupported-macro fallback;
- deterministic ordering;
- rendering version.

При отсутствии поддерживаемого способа показать обязательную секцию publisher останавливается. Он не теряет внутренние строки и не заменяет таблицу неполным summary.

### D12. Publication profile отделён от экземпляра страницы

`publication profile` — версионированный reusable контракт представления:

```yaml
profile_id: corporate-analytics-v4
profile_version: "1.0"
page_types:
  fp-current:
    sections: [...]
  release-increment:
    sections: [...]
```

Для каждой секции profile задаёт:

- `section_id`;
- title;
- source selector;
- `required | conditional | optional`;
- applicability expression;
- renderer ID/version;
- order;
- empty behavior;
- allowed fallback;
- approval/evidence rule.

`publication document manifest` — экземпляр:

- `document_id`;
- `page_type: fp-current | release-increment`;
- `fp_id`;
- optional `release_id`;
- source revisions;
- profile ID/version;
- target mapping reference;
- publication state;
- generated/published timestamps;
- content digest;
- correction/supersession refs.

Конкретные Confluence space/parent/page IDs хранятся в local/corporate configuration, а не в reusable package.

### D13. Применимость является данными и проверяется

Каждая условная секция имеет:

- applicability status;
- правило/основание;
- accountable owner;
- explanation при `not_applicable`;
- required evidence/approval;
- source references.

Validator различает:

- раздел заполнен;
- раздел обоснованно неприменим;
- раздел условно обязателен, но решение не принято;
- обязательный раздел отсутствует.

AI может предложить applicability, но результат остаётся `proposed` до решения ответственного человека.

### D14. Навигация строится по смыслу

В Git:

- root README объясняет портфель и ведёт в FP catalog;
- FP catalog позволяет искать по ID, названию, владельцу, статусу, проектам и связанным ФП;
- `fps/<fp-id>/README.md` объясняет, где находится аналитика, OpenSpec capability IDs, релизы и проекты;
- analytics README содержит карту смысловых разделов;
- release index перечисляет increments.

В Confluence:

- portfolio index ведёт на current pages ФП;
- current page ФП ведёт на release history и связанные ФП;
- release page ведёт на owning/affected FP current pages;
- anchors ведут к конкретным разделам, requirement/scenario IDs и assets;
- raw file layout не копируется 1:1.

### D15. Local preview и Confluence используют одну промежуточную модель

Pipeline:

```text
Git sources
  -> schema validation
  -> semantic/reference validation
  -> publication model
  -> local preview renderer
  -> human review
  -> permitted Confluence adapter
```

Publication model содержит уже разрешённые sections/rows/anchors/source refs, но не Confluence-specific credentials.

Local preview проверяет:

- полный состав страницы;
- вложенность;
- таблицы и expand blocks;
- anchors/links;
- warnings;
- source metadata;
- not-applicable presentation;
- release/current reconciliation;
- отсутствие external mutation.

Golden snapshots фиксируют сложные варианты исходного шаблона.

### D16. Generated page всегда показывает происхождение

Верхний и/или нижний блок страницы содержит:

- source repository/path;
- source commit;
- change/release IDs;
- generation timestamp;
- publication profile/version;
- renderer version;
- content digest;
- предупреждение «изменять источник в Git/OpenSpec»;
- ссылку для открытия source change/PR.

Статусы approval/testing/release показываются только с evidence или waiver.

### D17. Feedback возвращается в канонический источник

Комментарий Confluence не изменяет requirement автоматически.

Disposition:

- accepted — Git/OpenSpec update или follow-up change;
- rejected — причина;
- deferred — follow-up owner/record;
- duplicate — ссылка на исходное решение.

До следующей final publication blocker feedback должен иметь disposition или waiver по принятому `confluence-feedback-loop`.

### D18. AI работает как ограниченный соавтор и проверяющий

AI разрешено:

- объяснять структуру;
- создавать черновики Markdown/YAML;
- извлекать предлагаемые structured records из одобренных источников;
- искать gaps, dangling IDs и противоречия;
- предлагать diagrams и summaries;
- собирать bounded read pack;
- генерировать preview после deterministic validation;
- помогать подготовить feedback disposition.

AI запрещено:

- назначать owning FP или release owner без человека;
- объявлять раздел неприменимым как окончательное решение;
- придумывать approvals/evidence/delivery;
- включать change в release;
- финализировать/публиковать release;
- принимать waiver/risk;
- переносить секреты;
- считать ручную правку Confluence каноном.

Каждый AI-authored artifact сохраняет draft/provenance до human review.

### D19. Миграция выполняется постепенно

Не требуется немедленно переписывать весь legacy corpus.

Порядок:

1. утвердить schemas и publication profile на sanitized example;
2. выбрать одну pilot FP;
3. зарегистрировать FP и проекты;
4. инвентаризировать существующую аналитику read-only;
5. перенести актуальный смысл в Markdown/YAML/OpenSpec с provenance;
6. отметить unknown/gap вместо догадки;
7. собрать local current-page preview;
8. собрать один synthetic или реальный разрешённый release increment;
9. проверить corporate renderer constraints;
10. связать/создать Confluence pages только после человеческого решения;
11. расширять на следующие ФП по validated template.

Legacy page остаётся read-only reference. Миграция не переписывает её автоматически.

### D20. Publication failure не повреждает канон

Preview и validation read-only.

Publisher должен быть:

- dry-run capable;
- idempotent по document ID/source digest;
- fail-closed при неполной обязательной секции;
- безопасен к retry;
- с redacted action log;
- без хранения credentials в Git;
- способен оставить Git state неизменным при Confluence failure;
- способен показать план create/update/no-op до mutation.

Rollback публикации восстанавливает предыдущий generated page version или прекращает обновление; он не откатывает канонический Git автоматически.

### D21. AI Analyst Discovery Skill является upstream authoring flow, а не источником публикации

Согласованный дизайн
`docs/superpowers/specs/2026-07-24-ai-analyst-discovery-skill-design.md`
включается в общий путь:

```text
сырая идея
  -> analyst-discovery interview
  -> human-confirmed summary
  -> draft proposal/spec/design/tasks
  -> separate consent to guided-change
  -> reviewed canonical change package
  -> approval/implementation/delivery
  -> FP current page + release increment page
```

Discovery skill владеет:

- человекочитаемым входом из сырой идеи;
- разрешением на интервью и вопросами по одному;
- разделением фактов, предположений, неизвестности и конфликтов;
- сверкой смысловых блоков;
- human-confirmed final summary;
- подготовкой partial/full drafts;
- отдельной остановкой перед созданием файлов;
- отдельной остановкой перед переходом в `guided-change`;
- остановкой перед каждой командой или правкой.

Publication change владеет:

- допуском только reviewed canonical artifacts;
- запретом leakage proposed/unknown/conflict в delivered body;
- отображением unresolved items как work-in-progress gap/risk с владельцем;
- source/provenance ссылками;
- release/current reconciliation.

#### Две модели состояния не объединяются

Существующая `discovery_map` описывает состояние **тем интервью и выбора
глубины**: что уже рассмотрено, где нужно углубиться, принять default или
сохранить открытое решение.

Новая evidence-модель описывает достоверность **конкретных утверждений**:

- `confirmed`;
- `proposed`;
- `unknown`;
- `conflict`.

Это разные контракты. Нельзя заменять один enum другим или считать завершённую
тему доказательством истинности всех утверждений внутри неё.

#### Правила попадания в страницы

| Источник discovery | Current delivered body | Current work-in-progress | Release page |
|---|---|---|---|
| `confirmed`, но только в interview summary | Нет, пока нет reviewed canonical artifact | Можно как draft/source-linked summary | Нет, пока change не включён в release |
| `proposed` | Запрещено | Можно с явной меткой и owner | Только как unresolved proposal/risk |
| `unknown` | Запрещено | Gap с owner/impact | Gap/risk, если относится к release |
| `conflict` | Запрещено | Conflict с competing source refs | Blocker/waiver path, не выбранная AI версия |
| Reviewed requirement/scenario/typed source | После delivered reconciliation | Да, по evidence-backed state | Да, если входит в frozen release |

Если интервью выявляет cross-FP влияние, AI создаёт только proposed dependency
с предполагаемыми source/target FP и вопросом владельцам. Owning/affected FP и
release inclusion утверждаются людьми через canonical records.

Этот change не реализует внутреннюю логику skill повторно. Он потребляет
версионированный discovery output contract или human-reviewed change artifacts
и сохраняет AI-disabled/manual authoring fallback.

## Data Boundaries

### Stable identities

Минимальные ID:

- `FP-<ID>` или утверждённый kebab-case `fp_id`;
- `CAP-...`;
- `CHANGE-...`;
- `REL-...`;
- `REQ-...`;
- `SCEN-...`;
- `SCR-...`;
- `JOURNEY-...`;
- `API-...`;
- `DATA-...`;
- `COMP-...`;
- `PUB-...`.

ID не переиспользуются после удаления. Display names могут меняться.

### Cross-reference rules

- каждый capability принадлежит одной owning FP;
- change имеет одну accountable owning FP и может затрагивать несколько FP;
- release имеет one release owner/owner FP и несколько affected FP;
- cross-FP dependency указывает source/target, type, owner и state;
- ссылка на requirement/scenario разрешается в canonical OpenSpec;
- отсутствующий owner или dangling reference блокирует final publication;
- дублирование requirement text между FP запрещено; используется ссылка и краткое derived explanation.

### Content security

- секретные значения запрещены;
- credentials только в ignored/local secret storage;
- data classification обязательна для чувствительных атрибутов;
- corporate assets проходят разрешённый storage/export flow;
- внешняя reusable fixture полностью synthetic;
- logs и diagnostics редактируют sensitive values;
- AI read pack ограничивается нужной ФП/change/release областью.

## Verification Strategy

### Schema checks

- закрытые schemas для FP, release и publication manifests;
- version compatibility;
- discriminated service records;
- conditional applicability;
- forbidden secret patterns;
- stable ID grammar.

### Semantic checks

- FP/project mappings разрешаются;
- owner/affected FP существуют;
- capability owner уникален;
- release change refs существуют;
- requirement/scenario refs существуют;
- current page source соответствует last delivered release;
- approved-not-delivered не попадает в delivered body;
- published release composition не меняется без correction metadata;
- duplicate release/document identities отклоняются;
- mandatory section missing и unresolved applicability блокируют final output;
- evidence-backed statuses имеют ссылки.

### Rendering checks

- deterministic ordering;
- snapshot текущей страницы;
- snapshot release page;
- nested status transitions;
- nested audit attributes;
- platform-service variants;
- wide data/API tables;
- expand/anchor links;
- missing macro fallback;
- `not_applicable` rendering;
- source metadata/digest;
- no hidden row loss.

### End-to-end scenarios

1. Одна автономная ФП, один релиз.
2. Релиз owner FP включает изменения второй ФП.
3. Изменение approved, но не delivered.
4. Release delivered и обе affected FP current pages reconciled.
5. Missing owning FP.
6. Dangling requirement ID.
7. Обязательный раздел отсутствует.
8. AI предложил `not_applicable`, человек не подтвердил.
9. Published release manifest изменён без correction.
10. Confluence adapter unavailable: preview/evidence сохраняются, канон не меняется.
11. Legacy page imported as reference with gaps.
12. Sensitive value rejected/redacted.
13. Расплывчатая идея проходит analyst-discovery, подтверждённую сводку и draft package, но не попадает в delivered current body.
14. `proposed`, `unknown` и `conflict` assertions отображаются только как draft/gap/risk и не превращаются в факты публикации.
15. Discovery выявляет cross-FP влияние, но AI не назначает owning FP и не включает change в release.
16. Пользователь останавливает интервью или не разрешает file creation/guided-change; publication sources и external state не меняются.

### Manual corporate verification

- поддержка nested tables/expand в разрешённом Confluence способе;
- максимальный размер страницы и wide-table behavior;
- create/update/idempotency;
- page permissions;
- comment extraction/disposition;
- version history/rollback;
- asset upload/embed;
- MCP/API policy;
- no secret leakage;
- current/release page navigation.

## Risks / Trade-offs

- **[Одна актуальная страница может стать большой]** → оглавление, anchors, expand blocks, детерминированные секции и wide-table fallback; не делить автоматически без решения profile owner.
- **[Living page и release history могут разойтись]** → release reconciliation report и source digest; delivered increment не считается reconciled, пока affected FP pages не обновлены или gap не записан.
- **[Cross-FP release размывает ответственность]** → one owner per artifact, affected FP approvals и ссылки вместо копирования.
- **[Слишком много YAML ухудшит авторский опыт]** → YAML только для повторяемых/валидируемых структур; narrative остаётся Markdown; templates и role guidance по ситуации.
- **[Универсальная схема platform services станет бесконтрольной]** → discriminated records и versioned extension points.
- **[Confluence не поддержит ожидаемую вложенность]** → common publication model, corporate renderer profile и fail-closed fallback; semantic source не зависит от macro.
- **[Релизную страницу потребуется исправить]** → correction chain и digest вместо молчаливой перезаписи.
- **[Смешение accepted и delivered]** → отдельные блоки и release evidence.
- **[AI создаст убедительную, но ложную полноту]** → deterministic completeness, provenance и human applicability/approval gates.
- **[Discovery skill станет параллельным источником аналитики]** → публикация потребляет только reviewed canonical artifacts; interview summary/evidence остаются provenance и WIP input.
- **[Discovery map и truth status будут ошибочно объединены]** → отдельные schemas/owners и explicit adapter; завершение темы не подтверждает утверждения.
- **[Legacy migration станет бесконечной]** → pilot FP, incremental baseline и visible gaps.
- **[Центральный repo станет шумным]** → FP catalog, namespace, indexes и bounded read packs.
- **[Схемы будут преждевременно привязаны к одному корпоративному шаблону]** → publication profile отделён от semantic sources.

## Migration Plan

### Stage 0. Contract acceptance

- human review proposal/design/specs/tasks;
- resolve open questions;
- accept change for implementation;
- do not publish externally.

### Stage 1. Semantic foundation

- define FP catalog and manifests;
- extend typed analytics schemas;
- add cross-reference validators;
- create synthetic multi-FP fixture.

### Stage 2. Publication model

- define profile/document schemas;
- build normalized publication model;
- implement current/release composition;
- implement reconciliation/digest rules.

### Stage 3. Local renderers

- human-readable local preview;
- nested renderer registry;
- golden snapshots;
- negative/fail-closed tests.

### Stage 4. Corporate capability probe

- verify real Confluence constraints without publishing canonical content;
- select permitted adapter;
- fill non-secret mapping;
- record unsupported macros/limits.

### Stage 5. Pilot FP

- migrate one bounded FP;
- generate current page preview;
- generate one release page preview;
- perform human review;
- publish only after explicit approval;
- verify navigation, feedback and rollback.

### Stage 6. Controlled rollout

- update runbooks/templates;
- migrate FP-by-FP;
- retain gaps and provenance;
- monitor drift and reconciliation.

### Rollback

- source artifacts remain in Git;
- disable publication adapter without disabling validation/preview;
- restore previous Confluence generated version if supported;
- retain failed-run evidence;
- never roll back or delete canonical source automatically;
- hold rollout and open a follow-up OpenSpec change when semantic contract is wrong.

## Open Questions

These questions do not invalidate the approved two-page semantic model:

1. Which exact corporate template version/profile is first supported?
2. Which Confluence macros/storage representation are permitted for nested tables and expand blocks?
3. What maximum page size or performance limit requires a human-approved fallback?
4. What exact event is authoritative for `delivered` in the corporate release process?
5. Which owner approves current-page reconciliation for every affected FP?
6. Are publication targets mapped per FP, per portfolio space, or through a shared parent hierarchy?
7. Which legacy page becomes the first pilot and what privacy constraints apply?
8. Does the corporate environment permit automatic update after preview approval, or require a manual publication step?
9. Which future OpenSpec change owns the versioned assertion-evidence artifact emitted by the AI Analyst Discovery Skill?
10. Is a confirmed interview summary persisted as a separate typed evidence file or only as revision-bound metadata of the generated draft package?

## Durable Source References

- `docs/audits/ANALYTIC_TEMPLATE_AND_CONFLUENCE_PUBLICATION_GAP_AUDIT_2026-07-24.md`
- `docs/planning/ANALYTIC_TEMPLATE_STRUCTURE_AND_MIGRATION_PLAN_2026-07-06.md`
- `openspec/specs/repo-topology-config/spec.md`
- `openspec/specs/confluence-feedback-loop/spec.md`
- `openspec/specs/documentation-governance/spec.md`
- `openspec/specs/traceability-contract/spec.md`
- `openspec/changes/add-typed-analytics-artifact-framework/`
- `docs/superpowers/specs/2026-07-24-ai-analyst-discovery-skill-design.md`
