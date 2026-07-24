## ADDED Requirements

### Requirement: Семантический набор generated views состоит из current FP и release increment pages

Confluence publication SHALL поддерживать одну полную актуальную страницу для каждой ФП и отдельную страницу для каждого релизного инкремента; отдельная обязательная page на каждый change package SHALL NOT требоваться.

#### Scenario: Корпоративная среда выбирает технический mapping
- **WHEN** Confluence-enabled workflow настраивается в корпоративной среде
- **THEN** human owner выбирает разрешённые space/parent IDs, macros и adapter, но не заменяет принятую семантику current FP и release increment pages произвольным raw OpenSpec mirror

#### Scenario: Change отображается без отдельной страницы
- **WHEN** active change должен быть виден читателю до релиза
- **THEN** current FP page показывает source-linked status в блоке изменений в работе, а release page позже включает его дельту без требования отдельного generated change document

#### Scenario: Релизная история доступна из текущей страницы
- **WHEN** ФП имеет один или несколько release increments
- **THEN** current page содержит упорядоченные ссылки на release pages, а каждая release page ссылается на owning/affected FP current pages

### Requirement: Stable generated documents обновляются идемпотентно

Publisher SHALL связывать current FP page со stable document identity, а каждый release increment — с отдельной immutable-by-default identity и SHALL показывать create/update/no-op plan до внешней мутации.

#### Scenario: Повторная публикация без source changes
- **WHEN** document ID, profile version и source content digest не изменились
- **THEN** publication plan возвращает `no-op` и не создаёт duplicate page

#### Scenario: Обновляется актуальная страница ФП
- **WHEN** validated delivered source state или evidence-backed work-in-progress blocks изменились
- **THEN** publisher планирует update той же current page identity с новым digest и source metadata

#### Scenario: Повторно используется release ID
- **WHEN** новый document пытается использовать `release_id`, уже связанный с другим frozen digest
- **THEN** publication блокируется, если нет валидной correction chain

### Requirement: Corporate capability probe предшествует final publication

До final publication система SHALL проверить разрешённый adapter, page permissions, nested/expand behavior, asset handling, size limits, version/rollback и feedback access в реальной корпоративной среде.

#### Scenario: Local preview готов, probe не завершён
- **WHEN** semantic validation и local preview проходят, но corporate capability probe отсутствует
- **THEN** состояние остаётся preview-ready и система не утверждает Confluence compatibility или publication success

#### Scenario: Nested macro не разрешён
- **WHEN** capability probe показывает, что выбранный nested/expand macro запрещён
- **THEN** corporate profile выбирает проверенный lossless fallback или publication остаётся blocked

## MODIFIED Requirements

### Requirement: Unresolved feedback and publication blockers
The SDD process SHALL define how unresolved Confluence comments affect future publication and archive gates.

#### Scenario: Feedback SLA is configurable
- **WHEN** a Confluence-enabled workflow defines feedback triage rules
- **THEN** blocker and non-blocker triage SLA values are read from editable team/process configuration and may be disabled explicitly when corporate workflow tooling owns timing control

#### Scenario: Default triage SLA is used when enabled
- **WHEN** feedback SLA is enabled and no stricter team override exists
- **THEN** blocker comments are triaged within 1 working day and non-blocker comments are triaged within 3 working days

#### Scenario: Blocker comment prevents final publication
- **WHEN** a Confluence-enabled flow has an unresolved blocker comment
- **THEN** final publication or archive readiness is blocked until the comment has an accepted, rejected, deferred, duplicate, or approved-waiver disposition

#### Scenario: Non-blocking comment still needs disposition
- **WHEN** a Confluence-enabled flow has a non-blocking comment
- **THEN** the flow may continue only when the comment has an explicit disposition and any accepted/deferred follow-up is recorded

#### Scenario: Thin MVP does not require Confluence evidence
- **WHEN** a first-MVP thin change has no Confluence publication, preview, or feedback evidence
- **THEN** the absence of Confluence evidence does not block review or archive readiness because Confluence publication is outside the first MVP

#### Scenario: Existing Confluence corpus is read-only archive
- **WHEN** an existing Confluence analytics page is used as input for new SDD work
- **THEN** the page is treated as read-only reference material and any accepted requirement or analytics content is rewritten or linked through a Git/OpenSpec change instead of editing the legacy page as canonical source

#### Scenario: Technical publication mapping is selected in corporate environment
- **WHEN** the first Confluence-enabled workflow is planned after `D-029`
- **THEN** the semantic view set remains one current analytics page per FP plus release-increment pages, while real corporate templates and tool constraints determine the permitted space/parent mappings, macros, adapter, permissions and lossless renderer fallbacks
