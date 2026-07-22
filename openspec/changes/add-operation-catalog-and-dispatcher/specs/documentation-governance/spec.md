## ADDED Requirements

### Requirement: Operation table is a validated derived documentation view
Документация SHALL хранить operation table в README как закоммиченное производное представление canonical operation catalog, а не как independently maintained policy list.

#### Scenario: Generated operation view identifies its source
- **WHEN** README отображает operation table
- **THEN** он указывает canonical catalog/change source и объясняет, что таблица описывает назначение и границы операции, но не заменяет human decision или authorization

#### Scenario: Canonical catalog changes
- **WHEN** operation catalog record добавляется, удаляется или меняет public human-facing metadata
- **THEN** generation обновляет README table, а deterministic validation отклоняет несинхронизированный committed view
