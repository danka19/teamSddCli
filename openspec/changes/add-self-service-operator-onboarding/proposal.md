## Why

Текущий P3 dispatcher уже умеет объяснять маршрут, но обычному участнику команды всё ещё нужно знать путь к исходному репозиторию и имена Python-скриптов. Это не соответствует цели self-service: новый человек должен начать работу через один установленный интерфейс, увидеть следующий разрешённый шаг и не получить неявных полномочий.

## What Changes

- Добавить установленную команду `sdd` как единственную рекомендуемую точку входа; прямые `scripts/*.py` остаются совместимыми внутренними entrypoints.
- Добавить `sdd setup` для подтверждённого локального bootstrap центрального `team-specs`.
- Добавить `sdd start` для выбора рабочей ситуации и `sdd next` для объяснения единственного следующего действия по change.
- Сделать ответы CLI пригодными и для человека, и для AI: статус, недостающие факты, роль-владелец, human-decision boundary, fallback и точная следующая команда.
- Добавить e2e проверку чистого sandbox: setup, первый `minor` change, подготовка Spec PR и archive preparation.
- Сохранить P3 boundary: внешние интеграции и release-операции не выполняются автоматически; `mutate_external` остаётся запрещённым, а непокрытые mutation paths fail-closed.

## Capabilities

### New Capabilities

- `self-service-operator-onboarding`: установленный situation-first CLI, подтверждённый bootstrap и пошаговое продолжение работы без знания внутренних script paths.

### Modified Capabilities

- `guided-operation-dispatcher`: dispatcher получает стабильный установленный entrypoint, `start` и human-readable `next`, сохраняя безопасные классы операций и fail-closed mutation boundary.
- `repo-topology-config`: supported central `team-specs` topology получает воспроизводимый self-service bootstrap и project-facing entrypoint.

## Roadmap

- Execution phase: P3
- Related phases: P4
- Lifecycle status: in_progress

## Impact

Затрагиваются package distribution, `scripts/sdd.py` и dispatcher modules, bootstrap flow, CLI tests, controlled local evidence, topology/setup runbooks и Phase 3 acceptance evidence. Новые сетевые зависимости, credentials, Jira, Confluence, Bitbucket, Jenkins и release execution не входят в change.
