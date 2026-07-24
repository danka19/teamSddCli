## ADDED Requirements

### Requirement: Релизный инкремент трассирует изменения нескольких ФП

Release traceability SHALL связывать `release_id` с owning/affected FP, included change IDs, capability IDs, requirement/scenario IDs, source revisions, verification evidence, waivers и delivery state без копирования нормативного текста.

#### Scenario: Изменение принадлежит другой ФП
- **WHEN** release owner FP включает change, принадлежащий другой ФП
- **THEN** release record сохраняет owning FP change, affected FP relation и canonical requirement/scenario references, а ownership требований не переносится к release owner

#### Scenario: Requirement reference отсутствует
- **WHEN** included change указывает несуществующий или неоднозначный requirement/scenario ID
- **THEN** release validation и final publication блокируются с точным dangling reference

#### Scenario: Evidence заменено waiver
- **WHEN** обязательное verification evidence отсутствует, но применимая политика разрешает waiver
- **THEN** release traceability показывает approved waiver, owner, reason, scope и follow-up вместо fabricated passed status

### Requirement: Доставленный релиз трассирует reconciliation актуальных страниц

Delivered release SHALL хранить для каждой affected FP состояние reconciliation, current page document ID, source revision и content digest либо явный unresolved gap.

#### Scenario: Reconciliation завершён
- **WHEN** current page каждой affected FP отражает доставленный release baseline
- **THEN** release traceability содержит evidence-linked reconciled records для всех affected FP

#### Scenario: Reconciliation неполон
- **WHEN** хотя бы одна affected FP current page не обновлена или её digest не соответствует delivered source
- **THEN** release traceability показывает gap и не заявляет полную актуальность документации
