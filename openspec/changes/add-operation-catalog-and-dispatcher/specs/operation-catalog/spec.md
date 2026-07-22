## ADDED Requirements

### Requirement: Версионируемый единый каталог операций
Процессный пакет SHALL содержать versioned canonical operation catalog, который определяет каждую локальную script-based операцию через стабильный operation ID, entrypoint, visibility, owner/allowed roles, situations, inputs/outputs, mutation level, risk level, human decision, confirmation requirements, evidence, fallback, documentation, test coverage и lifecycle status.

#### Scenario: Все локальные скрипты учтены
- **WHEN** validator проверяет process package
- **THEN** каждый файл `scripts/*.py` представлен ровно одной active/deprecated/internal/forbidden catalog записью с существующим entrypoint, а незарегистрированный или дублированный script является blocking error

#### Scenario: Служебная операция остаётся видимой для контроля
- **WHEN** каталог описывает weak-model или certification entrypoint
- **THEN** запись имеет `visibility: internal`, участвует в package/validator coverage и не предлагается обычным guided route без явного разрешения

#### Scenario: Локальный analytics preview доступен человеку
- **WHEN** каталог описывает `preview_analytics.py`
- **THEN** его запись имеет `visibility: public`, `mutation_level: read_only` и указывает локальный результат без внешнего вызова

### Requirement: Каталог валидирует полномочия и побочные эффекты
Каталог SHALL разрешать только `public|internal|deprecated|forbidden` visibility, `read_only|prepare|mutate_local|mutate_release|mutate_external` mutation level, `none|low|medium|high` risk level и `ai_auto|ai_prepare|ai_request|human_only` automation class; loader SHALL reject inconsistent combinations.

#### Scenario: Мутация требует явного человеческого основания
- **WHEN** catalog record имеет `mutation_level` равный `mutate_local`, `mutate_release` или `mutate_external`
- **THEN** record содержит non-null human decision и confirmation requirements, а `automation_class` не предоставляет AI самостоятельное исполнение

#### Scenario: Внешняя мутация запрещена в P3
- **WHEN** P3 validator встречает catalog record с `mutation_level: mutate_external`
- **THEN** он блокирует package validation и сообщает, что external mutation находится вне P3 scope

#### Scenario: Устаревшая операция не предлагается как новый маршрут
- **WHEN** record имеет `lifecycle_status: deprecated`
- **THEN** `sdd op list` помечает его как legacy, а guided routing не предлагает его для нового workflow

### Requirement: Производные реестры не расходятся с каталогом
Процесс SHALL детерминированно проверять, что guided workflow ссылается на operation IDs, release allowlist согласован с catalog-defined distributable operations, AI read-pack указывает на catalog authority, а hardcoded command whitelist не является отдельным нормативным источником.

#### Scenario: Guided route ссылается на operation ID
- **WHEN** пользователь выбирает поддержанную business situation
- **THEN** route возвращает только существующие operation IDs и их human-decision/fallback metadata, а не raw script path как policy contract

#### Scenario: Производный список устарел
- **WHEN** release allowlist, guided route или read-pack не соответствует catalog record
- **THEN** validator завершается blocking error до package release и называет divergent derived artifact

### Requirement: Сгенерированная справка операций защищена от дрейфа
Процесс SHALL строить закоммиченную Markdown-таблицу операций в README из canonical catalog и byte-validate её перед package release.

#### Scenario: Ручное изменение generated table обнаружено
- **WHEN** README operation table отличается от результата generation из текущего catalog
- **THEN** validator блокирует проверку и объясняет, как regenerate canonical derived view

#### Scenario: Человек видит назначение без знания Python-файла
- **WHEN** человек открывает README без запуска команд
- **THEN** он видит для каждой public/deprecated операции её title, роль, ситуацию, mutation/risk boundary, confirmation requirement и ссылку на runbook
