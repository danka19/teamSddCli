## ADDED Requirements

### Requirement: Центральная топология имеет пространство ФП

Центральный `team-specs` SHALL регистрировать самостоятельные ФП отдельно от технических проектов/репозиториев и SHALL предоставлять FP-scoped человекочитаемую аналитику, при этом canonical OpenSpec root остаётся совместимым с поддерживаемым OpenSpec CLI.

#### Scenario: Десятки ФП находятся в одном team-specs
- **WHEN** central repository обслуживает несколько самостоятельных ФП
- **THEN** `fp-catalog` и `fps/<fp-id>/` дают отдельные owner/navigation boundaries, а changes/specs разрешаются по stable FP/capability IDs

#### Scenario: Одна ФП использует несколько проектов
- **WHEN** capability ФП реализуется в нескольких кодовых проектах
- **THEN** FP registry ссылается на все участвующие project IDs без копирования implementation truth в `team-specs`

#### Scenario: Один проект участвует в нескольких ФП
- **WHEN** общий component/repository обслуживает несколько ФП
- **THEN** `projects.yaml` и FP mappings отражают many-to-many relation, а owner/traceability checks используют affected zones вместо назначения репозитория одной ФП

#### Scenario: OpenSpec не поддерживает вложенный capability path
- **WHEN** pinned OpenSpec CLI не поддерживает желаемую FP-вложенность
- **THEN** topology использует валидируемый flat compound capability ID и explicit `fp_id` metadata вместо unsupported layout или отдельного OpenSpec root на каждую ФП

### Requirement: Общие каталоги изменений, релизов и публикации не дублируют FP-источники

Центральная топология SHALL хранить changes, release manifests и publication manifests как композиционные записи, которые ссылаются на owning FP sources по stable IDs.

#### Scenario: Cross-FP release собирается централизованно
- **WHEN** release включает changes нескольких ФП
- **THEN** release manifest находится в общем release registry, а аналитика и normative specs остаются в owning FP namespaces

#### Scenario: Generated page строит FP-навигацию
- **WHEN** publication model собирает current или release page
- **THEN** он разрешает FP/project/change/release references через центральные registries и отклоняет dangling или ambiguous mapping
