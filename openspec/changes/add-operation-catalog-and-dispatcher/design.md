## Контекст

P3 уже предоставляет situation-based guided workflow, однако его команды ссылаются на raw script paths, release allowlist покрывает только часть entrypoint'ов, а `guided_workflow.py` удерживает второй hardcoded whitelist. В README есть временная ручная таблица, но она не может выступать policy source. Владелец принял D-CAT-1…4: единый каталог, совместимость прямых скриптов, fail-closed mutations до существующего confirmation-event и определённая видимость девяти service entrypoint'ов.

Это реализует ограниченный usability trigger T1/T6 из `docs/IMPLEMENTATION_STRATEGY.md`: человеку и слабой модели нужен детерминированный вход по ситуации, но не отдельная CLI-платформа. П3 остаётся локальной и MCP-free.

## Goals / Non-Goals

**Goals:**

- Один versioned operation catalog покрывает все 30 локальных script entrypoint'ов и определяет их policy metadata.
- Каталог является canonical source для guided routes, AI read-pack, release allowlist и закоммиченной README-таблицы.
- Тонкий `sdd` dispatcher объясняет и выполняет только catalog-defined read-only/prepare операции, сохраняя direct script compatibility.
- Любая local/release mutation остаётся привязанной к существующему role-aware confirmation-event и блокируется до готовности этого контракта.

**Non-Goals:**

- Не переписывать существующие domain operations, не создавать background agent и не переносить human decisions в AI/CLI.
- Не добавлять MCP, credentials, сеть, external mutation или P4 corporate configuration.
- Не исправлять 18 известных падений полного owned-suite в рамках этого functional change.
- Не открывать `sdd run` для мутаций до завершения `harden-role-aware-guided-workflow`.

## Decisions

### Каталог вместо нескольких вручную синхронизируемых списков

`process/catalogs/operations.yaml`, его schema и loader становятся единым реестром. Каждая запись имеет stable ID, entrypoint, visibility, роли, situations, inputs/outputs, mutation/risk level, decision/confirmation, evidence, fallback, документацию, tests и lifecycle. `guided-owner-workflow.yaml` содержит operation IDs, release allowlist валидируется как derived view, README генерируется и проверяется. Это D-CAT-1; альтернатива с четырьмя списками отклонена из-за тихого drift.

### Тонкий dispatcher поверх поддерживаемых скриптов

`python -m process.operation_cli` и упаковочная команда `sdd` маршрутизируют к уже существующим entrypoint'ам. Они не получают domain logic. `sdd guide`, `next`, `op list`, `op show`, `check`, `prepare`, `request`, `run` имеют stable JSON/exit contract. Прямой `python scripts/create_change.py` не удаляется и остаётся тестируемым совместимым интерфейсом (D-CAT-2).

### Mutation boundary и один confirmation mechanism

`read_only` разрешён для `check`, `prepare` — для `prepare`; оба не получают lifecycle/release/external side effect. `request` создаёт только non-authoritative draft, привязанный к normalised input digest. `run` проверяет operation ID, allowed role, input digest, revision digest и expiry через existing `harden-role-aware-guided-workflow` confirmation event. Пока его contract не завершён, любой `run` для `mutate_local`, `mutate_release` или `mutate_external` блокируется до запуска entrypoint (D-CAT-3). `mutate_external` всегда запрещён в P3.

### Visibility service operations

Weak-model kit и certification tools видны как `internal`, `preview_analytics` — как `public`; raw evidence writers имеют high risk и mutation metadata. Internal не означает неучтённый: каждая операция остаётся в каталоге, validator и package distribution (D-CAT-4).

### Drift detection as a delivery gate

Validator проверяет: ровно одну запись для каждого scripts/*.py; существование entrypoint/test/runbook paths; schema/invariant correctness; derived allowlist/routes; byte-exact README block. Новый скрипт без записи или hand-edited generated table — blocking error in local check and CI/pre-commit.

## Risks / Trade-offs

- [Зависимость от незавершённого confirmation-event] → `run` реализуется fail-closed, а enablement остаётся отдельной задачей после зависимости.
- [Слишком широкий CLI] → ограниченный набор восьми команд, без domain logic и внешних integrations.
- [Разрыв между каталогом и legacy scripts] → direct entrypoint smoke/compatibility scenarios и validator coverage.
- [Неверно назначенный risk/visibility] → D-CAT-4 задаёт service-class defaults; каждую из 30 records review'ит owner через schema/test fixture.
- [Красный полный suite] → фиксируется как integration prerequisite, не как скрытая часть данного scope.

## Migration Plan

1. Добавить schema/loader и complete catalog без удаления действующих scripts.
2. Добавить validator и generated README block; CI/pre-commit сначала проверяют новый source-of-truth.
3. Добавить dispatcher для discovery/read-only/prepare/request и сохранить direct scripts.
4. Перевести guided routes и allowlist на operation IDs/derived validation, затем удалить hardcoded whitelist.
5. После отдельного завершения confirmation-event включить `run` только через новый OpenSpec task/review; rollback — вернуть route/allowlist compatibility, не удаляя evidence или confirmation artifacts.

## Open Questions

Нет блокирующих product decisions: D-CAT-1…4 приняты. До implementation review требуется подтвердить точные risk metadata остальных public operations как часть catalog fixture review; это task-level verification, а не новая policy choice.
