## Why

Повтор полной Qwen/DeepSeek matrix не даёт новых знаний, если AI-контракт
пакета не менялся. Текущий release contract, однако, запрещает даже
проверяемое переиспользование сертифицированной matrix после изменения версии
пакета, поэтому вынуждает либо выполнять лишние model runs, либо не выпускать
безопасный successor candidate.

## What Changes

- Добавить version-aware baseline reuse для model certification evidence.
- Разрешить новый candidate ссылаться на полную baseline matrix только при
  точном совпадении AI-контракта по SHA-256 и свежем bounded preflight для
  затронутого слоя.
- Требовать явную baseline ссылку, обоснование и fail-closed диагностику при
  любом расхождении.
- Сохранить обязательный полный matrix run при изменении адаптера, role prompt,
  response schema, model catalog или launcher/read-pack семантики.

## Capabilities

### New Capabilities

- `certified-baseline-reuse`: проверяемое переиспользование модельной matrix
  между версиями process package.

### Modified Capabilities

None.

## Impact

Затрагиваются release-certification selection/schema, candidate acceptance
validation, normalized evidence и их тесты. Не затрагиваются human authority,
raw evidence retention, AI-disabled fallback или immutable rc6.

## Roadmap

- Execution phase: P3
- Related phases: P4
- Lifecycle status: accepted
