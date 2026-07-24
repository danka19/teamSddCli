## Why

`sdd next` не продолжает работу с реальным schema-v2 change package: канонический
writer записывает lifecycle в поле `status`, а dispatcher читает неканоническое
`lifecycle_state`. Из-за этого поддержанный маршрут первого change блокируется
сразу после его создания, хотя synthetic tests проходят на вручную собранном
несовместимом fixture.

## What Changes

- Читать lifecycle для `sdd next` только из обязательного верхнеуровневого поля
  `status` в `change.yaml`.
- Передавать прочитанное значение во внутренний situation-first route без
  изменения внутреннего имени факта и без добавления второго lifecycle field в
  change package.
- Fail closed при отсутствующем, пустом или неподдерживаемом `status`; не
  использовать `lifecycle_state` как fallback.
- Сохранить read-only характер `sdd next`, role boundary, стабильный continuation
  envelope и отсутствие lifecycle/external mutations.
- Добавить regression evidence на реальном пакете
  `create_change -> sdd next`, а не только на handcrafted YAML.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `guided-operation-dispatcher`: `sdd next` использует канонический lifecycle
  field schema-v2 change package и fail closed на отсутствующем или
  неподдерживаемом `status`.

## Roadmap

- Execution phase: P3
- Related phases: P4
- Lifecycle status: in_progress

## Impact

Изменение затрагивает только локальный parser/dispatcher, focused CLI tests,
self-service walkthrough и производную FAQ-документацию. Оно не меняет
change schema, guided catalog, роли, полномочия, mutation boundary, внешние
интеграции или release execution.
