## ADDED Requirements

### Requirement: Situation-first dispatcher discovery
Локальный `sdd` dispatcher SHALL предоставлять `guide`, `next`, `op list` и `op show` поверх canonical operation catalog без переноса domain logic из существующих scripts.

#### Scenario: Пользователь начинает с ситуации
- **WHEN** человек или AI вызывает `sdd guide <situation>` с требуемыми facts
- **THEN** dispatcher возвращает catalog-defined следующий безопасный operation, required inputs/evidence, fallback и accountable human decision без требования знать путь скрипта

#### Scenario: Недостающий контекст блокирует маршрут
- **WHEN** situation или required fact отсутствует либо недействителен
- **THEN** dispatcher возвращает structured `blocked` result с missing context и human route, не угадывая command или decision

#### Scenario: Операция раскрывается до запуска
- **WHEN** пользователь вызывает `sdd op show <operation-id>`
- **THEN** он получает title, permitted roles, inputs/outputs, mutation/risk boundary, evidence, fallback и confirmation requirement этой catalog record

### Requirement: Безопасная dispatch-классификация
Dispatcher SHALL позволять `check` только для `read_only` operation, `prepare` только для `prepare` operation и `request` только как non-authoritative preparation confirmation draft; каждая команда SHALL выдавать machine-readable result и stable success/blocked/operational exit class.

#### Scenario: Read-only check получает evidence
- **WHEN** пользователь запускает `sdd check <operation-id>` для разрешённой read-only операции
- **THEN** dispatcher делегирует существующему entrypoint, возвращает его evidence и не изменяет lifecycle, release, human decision или external state

#### Scenario: Неподходящая команда блокируется до entrypoint
- **WHEN** пользователь пытается передать prepare/mutate operation в `sdd check` либо read-only operation в `sdd prepare`
- **THEN** dispatcher возвращает blocked result без запуска entrypoint и объясняет допустимый command class

#### Scenario: Request не создаёт authority
- **WHEN** пользователь вызывает `sdd request <mutating-operation>`
- **THEN** dispatcher создаёт только review-required draft с operation ID и digest нормализованных входов, не создавая acceptance, DoR, lifecycle, release или mutation authority

### Requirement: Мутации fail closed до доверенного confirmation event
Dispatcher SHALL не исполнять `mutate_local`, `mutate_release` или `mutate_external` operation через `sdd run`, пока отсутствует действующий completion contract `harden-role-aware-guided-workflow`; после его отдельного принятия dispatcher SHALL требовать валидный confirmation artifact, привязанный к operation ID, allowed role, input digest, reviewed revision digest и expiry.

#### Scenario: P3 run блокируется до completion dependency
- **WHEN** пользователь вызывает `sdd run <mutating-operation>` в P3 до принятия required confirmation-event contract
- **THEN** dispatcher возвращает blocked result с dependency explanation и не запускает mutation entrypoint

#### Scenario: Неверное confirmation не создаёт побочного эффекта
- **WHEN** confirmation artifact отсутствует, истёк, имеет другую роль, operation ID, input digest или revision digest
- **THEN** dispatcher возвращает blocked result и не изменяет package, evidence, lifecycle, release или external state

#### Scenario: Внешняя мутация остаётся вне P3
- **WHEN** пользователь пытается выполнить external operation через dispatcher в P3
- **THEN** dispatcher блокирует её независимо от supplied confirmation и ссылается на P4 boundary

### Requirement: Direct script compatibility
Добавление `sdd` SHALL NOT удалить или изменить поддерживаемый прямой вызов поддерживаемого direct script entrypoint'а для каждой catalog record.

#### Scenario: Existing direct entrypoint remains usable
- **WHEN** regression smoke запускает `python scripts/create_change.py` как representative existing documented entrypoint с его прежними valid arguments
- **THEN** entrypoint сохраняет documented JSON/exit-code contract, а `sdd` выступает только дополнительным UX layer
