## ADDED Requirements

### Requirement: Одна полная актуальная страница на ФП

Система публикации SHALL поддерживать для каждой зарегистрированной самостоятельной ФП ровно одну логическую актуальную страницу аналитики со стабильной identity, которая объединяет человекочитаемый контекст, нормативные требования, типизированные модели, assets, evidence-backed состояния и навигацию.

#### Scenario: Новый читатель открывает ФП
- **WHEN** человек открывает актуальную страницу зарегистрированной ФП
- **THEN** он видит назначение и границы ФП, владельцев, бизнес-контекст, функциональность, архитектуру, безопасность, эксплуатационные требования, проверки, последнее доставленное состояние, изменения в работе, риски и ссылки на канонические источники

#### Scenario: Репозиторий не определяет границу ФП
- **WHEN** одна ФП использует несколько кодовых репозиториев или один репозиторий участвует в нескольких ФП
- **THEN** система сохраняет одну страницу на `fp_id` и использует project/repository mappings только как технические ссылки

#### Scenario: Одна страница не превращается в страницу портфеля
- **WHEN** central `team-specs` содержит несколько самостоятельных ФП
- **THEN** каждая ФП имеет отдельную актуальную страницу, а portfolio index содержит ссылки вместо объединения всей аналитики в один документ

### Requirement: Доставленное состояние отделено от изменений в работе

Основное тело актуальной страницы ФП SHALL показывать последнее подтверждённое доставленное состояние, а approved-not-delivered и active changes SHALL отображаться отдельными evidence-backed блоками и не смешиваться с текущими фактами.

#### Scenario: Изменение одобрено, но не доставлено
- **WHEN** change прошёл требуемые approval gates, но не имеет подтверждённого `delivered` release evidence
- **THEN** актуальная страница показывает его в блоке «одобрено, но не доставлено» и не включает новое поведение в основное доставленное описание

#### Scenario: Draft change находится в работе
- **WHEN** change ещё находится в draft/review/implementation state
- **THEN** актуальная страница может показать ссылку и evidence-backed state в блоке «изменения в работе», но не публикует draft как принятое текущее поведение

#### Scenario: Доставленный инкремент обновляет текущую аналитику
- **WHEN** release increment получает подтверждённый `delivered` state и reconciliation для ФП
- **THEN** living analytics и generated current page обновляются из канонических источников, а страница ссылается на доставленный инкремент

### Requirement: Отдельная страница каждого релизного инкремента

Система SHALL создавать отдельный publication document для каждого `release_id`, показывающий цель, пользовательский эффект, состав changes/FP, аналитическую дельту, cross-FP зависимости, evidence, risks, approvals, delivery и source provenance конкретного инкремента.

#### Scenario: Автономный релиз одной ФП
- **WHEN** релиз содержит changes только одной owning FP
- **THEN** release page показывает эту ФП, включённые changes, затронутые требования/сценарии и evidence без создания отдельной обязательной change page

#### Scenario: Релиз содержит changes нескольких ФП
- **WHEN** release manifest включает changes, принадлежащие разным ФП
- **THEN** одна release page показывает owning и affected FP для каждого change и связывает их current pages и canonical requirement/scenario IDs без копирования нормативного текста

#### Scenario: Релиз отменён
- **WHEN** release increment отменён после создания draft/candidate page
- **THEN** страница сохраняется со статусом `cancelled`, причиной и source evidence вместо удаления или представления как доставленного

### Requirement: Финализированный релиз не переписывается молча

После публикации release increment система SHALL связывать страницу с frozen manifest, source revisions и content digest и SHALL требовать явную correction chain для изменения финализированного содержания.

#### Scenario: Состав меняется до candidate
- **WHEN** release page находится в `draft`
- **THEN** состав может изменяться с обычной Git history и новый preview отражает актуальный manifest

#### Scenario: Published manifest изменён без correction
- **WHEN** source composition или нормативная дельта опубликованного release изменена без `correction_reason`, предыдущего digest и source change reference
- **THEN** validation и final publication SHALL fail closed

#### Scenario: Исправляется ошибка представления
- **WHEN** после publication обнаружена ошибка generated content, не меняющая продуктовую дельту
- **THEN** новый page revision содержит correction reason, previous digest и ссылку на исправляющий source change

### Requirement: Полный смысловой каркас страниц

Publication profile SHALL определять упорядоченный полный каркас `fp-current` и `release-increment`, источник, renderer, применимость и evidence rule каждой секции.

#### Scenario: Актуальная страница собирается полностью
- **WHEN** генерируется `fp-current`
- **THEN** composition включает карточку, обзор, контакты, бизнес-контекст, функциональную аналитику, архитектуру, безопасность, NFR/operations, проверки, текущие изменения, release history и source metadata либо явное валидное `not_applicable`

#### Scenario: Release page собирается полностью
- **WHEN** генерируется `release-increment`
- **THEN** composition включает карточку, цель/эффект, состав, аналитическую дельту, cross-FP зависимости, проверки/risks/approvals, delivery/reconciliation и source metadata

#### Scenario: Обязательная секция отсутствует
- **WHEN** required section не имеет разрешённого source content и не допускает `not_applicable`
- **THEN** final publication блокируется с диагностикой section ID, ожидаемого источника и accountable owner

### Requirement: Условная применимость является проверяемым решением

Каждая conditional section SHALL хранить applicability state, основание, accountable owner, explanation для `not_applicable` и требуемое approval/evidence.

#### Scenario: Раздел обоснованно неприменим
- **WHEN** ответственный человек фиксирует `not_applicable` с разрешённым основанием и evidence
- **THEN** validation принимает решение, а generated page явно показывает неприменимость без пустой таблицы

#### Scenario: AI предлагает неприменимость
- **WHEN** AI предлагает `not_applicable`, но accountable human ещё не подтвердил решение
- **THEN** состояние остаётся proposed/unresolved и final publication блокируется

#### Scenario: Условие делает раздел обязательным
- **WHEN** semantic input удовлетворяет applicability predicate обязательного раздела
- **THEN** отсутствие section content/evidence считается ошибкой, даже если автор удалил строку из manifest

### Requirement: Typed sources не зависят от внешнего вида Confluence

Сложные повторяемые модели SHALL храниться как versioned typed records, а вручную поддерживаемые nested Markdown/HTML tables SHALL NOT быть каноническим источником.

#### Scenario: Статусы имеют условные переходы
- **WHEN** status model содержит descriptions, entry actions, conditional transitions и system statuses
- **THEN** schema сохраняет все семантические поля, а renderer строит вложенное представление без потери строк

#### Scenario: Платформенные сервисы имеют разные конфигурации
- **WHEN** analytics использует audit, monitoring, authorization и parameter-store services
- **THEN** `service_kind` выбирает соответствующие discriminated records и renderer вместо произвольного общего списка строк

#### Scenario: Простая таблица остаётся читаемой
- **WHEN** небольшой плоский список не требует типизированной вложенности
- **THEN** человекочитаемая плоская Markdown-таблица допускается, если она не дублирует отдельный нормативный typed source

### Requirement: Renderer сохраняет вложенность и полноту

Каждый section renderer SHALL объявлять поддерживаемый source/schema version, output block, nesting, anchors, ordering, empty behavior, wide-table fallback и unsupported-macro behavior.

#### Scenario: Вложенные атрибуты аудита
- **WHEN** audit event содержит список attributes
- **THEN** local preview и Confluence renderer показывают все attributes в детерминированном nested/expand представлении с stable event anchor

#### Scenario: Macro недоступен
- **WHEN** corporate renderer не поддерживает macro, необходимый обязательной секции
- **THEN** он использует заранее разрешённый lossless fallback либо останавливает publication вместо удаления внутреннего содержания

#### Scenario: Очень широкая таблица
- **WHEN** data/API table превышает разрешённую ширину profile
- **THEN** renderer применяет объявленный deterministic fallback и сохраняет все поля и stable references

### Requirement: Publication profile отделён от экземпляра документа

Система SHALL разделять versioned publication profile, который описывает типы страниц и секции, и publication document manifest, который связывает конкретную ФП/релиз, source revisions, target mapping, state и digest.

#### Scenario: Корпоративный шаблон обновился
- **WHEN** corporate template меняет порядок или renderer sections без изменения semantic source
- **THEN** создаётся новая profile version, а source analytics не переписывается под Confluence layout

#### Scenario: Создаётся current page
- **WHEN** publication manifest имеет `page_type: fp-current`
- **THEN** он содержит `fp_id`, profile identity, source revisions, stable document ID, target mapping reference и digest без `release_id`

#### Scenario: Создаётся release page
- **WHEN** publication manifest имеет `page_type: release-increment`
- **THEN** он содержит `fp_id`, `release_id`, frozen sources, profile identity, distinct document ID и correction metadata policy

### Requirement: Local preview эквивалентен semantic publication model

Local preview и future Confluence adapter SHALL потреблять одну и ту же normalized publication model, при этом preview SHALL быть read-only, offline-capable и не требовать credentials.

#### Scenario: Multi-FP preview без AI
- **WHEN** synthetic release с changes двух ФП проходит validation и preview при отключённом AI
- **THEN** output показывает полный current/release composition, cross-FP links, nested sections и source metadata без network action

#### Scenario: Preview не гарантирует publication
- **WHEN** local preview проходит, но corporate profile/capability probe не подтверждён
- **THEN** система сообщает preview-ready, но не заявляет Confluence-published или corporate-compatible state

#### Scenario: Golden rendering drift
- **WHEN** renderer change меняет approved nested output
- **THEN** golden snapshot check сообщает явный diff и требует review вместо молчаливого изменения страницы

### Requirement: Release reconciliation проверяет все затронутые ФП

После delivered release система SHALL отслеживать reconciliation каждой affected FP current page и SHALL показывать незавершённый reconciliation как gap.

#### Scenario: Все страницы обновлены
- **WHEN** delivered release затронул две ФП и обе current pages собраны из соответствующего delivered source state
- **THEN** release получает reconciliation-complete evidence со ссылками и digests обеих страниц

#### Scenario: Одна ФП не обновлена
- **WHEN** delivered release затронул две ФП, но current page второй ФП осталась на предыдущем baseline
- **THEN** release и portfolio/current navigation показывают unresolved reconciliation gap и не заявляют полную синхронизацию

### Requirement: Generated content сохраняет provenance и human authority

Каждая generated page SHALL показывать source commit, change/release IDs, timestamp, profile/renderer versions, content digest, source warning и ссылки назад; AI SHALL оставаться advisory-only.

#### Scenario: Читатель проверяет источник
- **WHEN** человек видит requirement, status или approval на generated page
- **THEN** он может перейти к canonical source и evidence/waiver, на котором основано отображение

#### Scenario: AI подготовил draft
- **WHEN** AI создал или преобразовал analytics source
- **THEN** provenance и draft state сохраняются до human review, а AI не может финализировать applicability, approval, release composition или delivered state

#### Scenario: Confluence недоступен
- **WHEN** publication adapter не может обратиться к Confluence
- **THEN** validation, publication model и local preview сохраняются, canonical Git state не изменяется, а external publication state остаётся unknown/failed с evidence

### Requirement: Legacy analytics мигрируется постепенно

Система SHALL поддерживать read-only inventory и поэтапное преобразование legacy analytics в FP sources с provenance и явными gaps без требования одномоментной полной миграции.

#### Scenario: Legacy поле неясно
- **WHEN** старый документ содержит неоднозначное или неподтверждённое значение
- **THEN** migration record сохраняет source reference и gap/open question вместо AI-догадки

#### Scenario: Pilot FP готовится к публикации
- **WHEN** одна выбранная ФП прошла inventory, source conversion, validation и human review
- **THEN** её current page и один release increment могут перейти к corporate preview независимо от состояния остальных ФП

### Requirement: Analyst discovery входит в публикацию только через reviewed canonical sources

Publication flow SHALL принимать результат AI Analyst Discovery Skill только
после human-confirmed summary и преобразования в reviewed canonical
Markdown/YAML/OpenSpec artifacts; interview summary, partial draft и assertion
evidence SHALL NOT становиться delivered truth самостоятельно.

#### Scenario: Подтверждённая сводка ещё не прошла review
- **WHEN** analyst-discovery завершён, человек подтвердил summary и AI подготовил draft change package, но canonical review/approval/delivery ещё не выполнены
- **THEN** current page может показать source-linked change в work-in-progress, но delivered body и release composition не изменяются

#### Scenario: Утверждение имеет proposed или unknown
- **WHEN** discovery assertion имеет status `proposed` или `unknown`
- **THEN** publication показывает его только как draft/gap с impact и owner либо не показывает, но SHALL NOT представлять его как подтверждённый факт

#### Scenario: Источники конфликтуют
- **WHEN** discovery assertion имеет status `conflict`
- **THEN** AI и publication model сохраняют competing source references и human decision route и SHALL NOT выбирать версию автоматически

#### Scenario: Discovery выявляет другую ФП
- **WHEN** интервью показывает возможное влияние на другую ФП
- **THEN** AI создаёт proposed cross-FP dependency и вопросы владельцам, а owning/affected FP и release inclusion остаются unresolved до human-owned canonical records

#### Scenario: Пользователь не разрешил создание файлов
- **WHEN** человек завершил или остановил interview, но не дал отдельное согласие на file creation или переход в `guided-change`
- **THEN** skill может вернуть summary/partial draft в разговоре, но canonical files, publication model и external state не изменяются

#### Scenario: Discovery map завершена
- **WHEN** interaction discovery map не содержит открытых тем
- **THEN** это не считается автоматическим подтверждением truth status каждого assertion и не заменяет human review canonical artifacts
