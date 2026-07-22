# Утверждённый дизайн: operation catalog и тонкий dispatcher `sdd`

Дата: 2026-07-22  
Статус: одобрен владельцем; до реализации требуется review этого документа и OpenSpec change `add-operation-catalog-and-dispatcher`.

## Проблема и граница

В пакете есть 30 локальных скриптов, однако их реестр фрагментирован между release allowlist, guided routes, hardcoded whitelist и справочными документами. Человек должен знать имя файла, а AI не имеет единого машиночитаемого источника допустимых действий. Это соответствует trigger T1/T6 из `docs/IMPLEMENTATION_STRATEGY.md`: ручное склеивание и сценарий onboarding уже не исправляются безопасно одними разрозненными скриптами.

Решение не создаёт автономного агента, не добавляет MCP, сеть или внешние интеграции и не переписывает бизнес-логику скриптов. Оно добавляет локальный каталог и тонкий диспетчер поверх существующих entrypoint'ов.

## Принятые решения владельца

- `D-CAT-1`: `process/catalogs/operations.yaml` — единый реестр операций. README, release allowlist и guided routes являются производными/проверяемыми поверх него; hardcoded whitelist удаляется.
- `D-CAT-2`: прямой запуск `python scripts/create_change.py` сохраняется поддерживаемым контрактом. `sdd` является удобной надстройкой, а не заменой.
- `D-CAT-3`: операции с `mutate_*` не исполняются, пока change `harden-role-aware-guided-workflow` не завершит revision-bound confirmation-event. До этого `sdd run` обязан fail closed.
- `D-CAT-4`: weak-model и certification scripts получают `visibility: internal`; `preview_analytics` — `public`; `run_actual_certification` и `normalize_actual_certification` имеют высокий риск и мутацию evidence. Полный список рисков проверяется при заполнении каталога.

## Архитектура

Один каталог определяет стабильный `operation id`, entrypoint, visibility, роли, ситуации, входы/выходы, mutation/risk level, требуемое человеческое решение, confirmation requirements, evidence, fallback, документацию, тестовое покрытие, lifecycle и automation class. Схема и строгий loader отказывают при некорректной или неполной записи.

`guided-owner-workflow.yaml` остаётся routing-слоем: ситуация указывает на operation ID, а не на путь скрипта. AI read-pack читает те же machine-readable ограничения. README содержит сгенерированную и закоммиченную таблицу; валидатор сравнивает её с каталогом и проверяет, что каждый `scripts/*.py` зарегистрирован ровно один раз, ссылки существуют, а производные allowlist/routes не расходятся.

Тонкий CLI имеет только `guide`, `next`, `op list`, `op show`, `check`, `prepare`, `request`, `run`. Он делегирует существующим скриптам, не переносит в себя бизнес-логику и сохраняет JSON/exit-code контракт. `check` допускает только read-only, `prepare` — только сбор evidence, `request` — только черновик подтверждения. `run` для local/release mutation валидирует роль, operation ID, digest нормализованных входов, revision digest и expiry; до готовности existing confirmation contract он всегда блокируется без побочного эффекта. `mutate_external` вне P3.

## Проверяемые результаты

- Все 30 скриптов представлены в каталоге; новый неучтённый скрипт делает validator/CI красным.
- README-таблица байт-в-байт соответствует генерации из каталога.
- `sdd guide/next/op list/op show/check/prepare/request` дают человеку ситуацию, допустимые действия, evidence и accountable human decision без знания файловой структуры.
- Прямые script entrypoint'ы остаются рабочими.
- Любой `sdd run` с отсутствующим, просроченным или несоответствующим confirmation блокируется без мутации; до завершения P3 confirmation contract так блокируется каждый mutate case.

## Не входит в scope

Нет MCP, credentials, сети, внешних mutations, полного набора CLI-подкоманд, автоматического human approval, waiver/DoR/DoD/release/archive/merge/deploy решения, а также исправления известных 18 падений полного owned-suite. Эти падения остаются интеграционной предпосылкой финальной приёмки и не должны маскироваться данным change.

## Канонический proposed contract

Детальные требования, сценарии, задачи и зависимости содержатся в `openspec/changes/add-operation-catalog-and-dispatcher/`. После реализации принятие и синхронизация в living specs остаются отдельным решением человека.
