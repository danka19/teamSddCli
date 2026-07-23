## Why

В пакете уже есть 30 локальных скриптов, но их назначение, допустимость и связь с рабочими ситуациями разнесены по нескольким неполным спискам. Человек вынужден искать имя Python-файла, а AI не имеет единого проверяемого источника разрешённых действий. Это зафиксированный usability trigger для узкой CLI-надстройки, а не основание строить автономный или полный CLI-продукт.

## What Changes

- Добавить версионируемый `operations.yaml` как единственный машиночитаемый реестр всех локальных операций, их ролей, рисков, мутаций, входов, evidence, fallback и человеческих решений.
- Добавить строгую схему, loader и validator дрейфа: каталог покрывает все скрипты, entrypoint/test/runbook ссылки существуют, release allowlist и guided routes согласованы, а README-таблица является сгенерированным закоммиченным представлением.
- Добавить тонкий локальный `sdd` dispatcher поверх существующих entrypoint'ов: `guide`, `next`, `op list`, `op show`, `check`, `prepare`, `request`, `run`.
- Мигрировать guided routes с путей скриптов на stable operation IDs и убрать hardcoded command whitelist как второй источник правды.
- Сохранить прямой `python scripts/create_change.py` как поддерживаемый совместимый интерфейс.
- Сделать `sdd run` для `mutate_*` fail-closed до готовности revision-bound confirmation-event из `harden-role-aware-guided-workflow`; P3 не добавляет external mutation, MCP, сеть или AI-approval.

## Capabilities

### New Capabilities

- `operation-catalog`: Единый каталог операций, его схема, классификация visibility/risk/mutation, производные представления и проверка дрейфа.
- `guided-operation-dispatcher`: Тонкий локальный `sdd` интерфейс, который показывает и запускает только разрешённые catalog-defined операции с сохранением human authority.

### Modified Capabilities

- `documentation-governance`: Закоммиченная README-таблица операций становится производным, детерминированно проверяемым представлением canonical operation catalog.
- `repo-topology-config`: Версионируемый process package объявляет operation catalog, его schema/validator и dispatcher как общие package assets.

## Roadmap

- Execution phase: P3
- Related phases: P4, P5
- Lifecycle status: accepted

## Принятые решения владельца

- `D-CAT-1`: единый `operations.yaml`; release allowlist, guided routes и README производны, hardcoded whitelist удаляется.
- `D-CAT-2`: прямые script entrypoint'ы остаются поддерживаемыми.
- `D-CAT-3`: `mutate_*` через `sdd run` до готовности confirmation-event всегда fail closed; готовятся только read-only/prepare/request возможности.
- `D-CAT-4`: weak-model/certification операции internal, `preview_analytics` public, raw certification writers high-risk mutating; остальные значения фиксируются и тестируются в каталоге.

## Impact

Затрагиваются `process/catalogs/`, `process/schemas/`, package registry, guided routing/read-pack, release allowlist, существующий `process.operation_cli`, обёртка `sdd`, validators, pre-commit, README/runbooks и тесты. Данный change координируется с активным `harden-role-aware-guided-workflow`, но не создаёт второй механизм human confirmation. Известные 18 падений полного owned-suite остаются отдельным remediation risk и не входят в функциональный scope.
