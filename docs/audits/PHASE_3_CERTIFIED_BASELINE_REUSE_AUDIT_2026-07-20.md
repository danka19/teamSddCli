# Аудит повторного использования certified baseline — 2026-07-20

## Цель и граница

Пакет `0.3.1` добавляет проверяемый режим `baseline-reuse`: он может сослаться
на неизменяемую полную matrix `0.3.0`, но только при совпадении модельного
контракта и свежем preflight. Это не меняет accepted `phase-2-14-rc6`, не
создаёт автоматического acceptance и не запускает корпоративную адаптацию.

## Что сделано

- В selection schema добавлены явные режимы `full-matrix` и `baseline-reuse`.
  Неявная ссылка на старое evidence не проходит schema validation.
- Для Qwen и DeepSeek зарегистрированы SHA-256 девяти AI-contract источников:
  adapter, catalog, model adapter, operation plan, четыре role instruction и
  response schema.
- Acceptance fail-closed проверяет hashes, hash и passed-статус baseline,
  наличие exact external raw root и свежий preflight текущего package.
- Role-output certification теперь хеширует UTF-8 policy text после
  межплатформенной newline-нормализации: Git baseline хранит LF, а Windows
  checkout с `core.autocrlf=true` выдаёт CRLF. Это исправляет ложный отказ,
  не ослабляя проверку содержания.
- Запущены настоящие локальные preflight: Qwen 5/5 и DeepSeek 5/5; оба
  результата содержат `process_package_version: 0.3.1`, actual model identity
  и пустые diagnostics при `validate_phase_gate`.

## Почему полная matrix не запускалась

Изменение добавляет guided owner workflow и корректирует Windows CRLF
нормализацию read-pack. Оно не меняет зарегистрированные adapter, model catalog,
roles, response schema, `model_adapter.py` или `operation_plan.py`. CRLF слой
не замалчивается: он заново исполнен свежими preflight на текущей версии.

Полная matrix обязана быть запущена, если изменится любой из девяти hashes,
preflight исчезнет или завершится ошибкой, либо владелец не сможет предоставить
исторический raw bundle.

## Проверки

| Проверка | Результат |
| --- | --- |
| RED: compatible reuse, hash mismatch, missing/failed preflight | добавлена и затем проходит |
| 17 целевых release/certification/actual-certification regression tests | `17 passed in 10.01s` в bundled Python |
| Qwen actual preflight | 5/5, `qwen3.5:9b`, local family proxy |
| DeepSeek actual preflight | 5/5, `deepseek-r1:8b`, local family proxy |
| `validate_phase_gate` обоих fresh result | `[]` |

## Блокер candidate-bound acceptance

В доступном внешнем хранилище отсутствуют два historical raw roots,
зарегистрированные baseline evidence `0.3.0`. Поэтому невозможно честно
собрать raw bundle и получить `evidence-complete` для successor candidate без
повторного полного matrix или восстановления именно этих архивных артефактов.
Созданная пустая временная папка `guided-owner-v0.3.1-candidate-raw-2026-07-20`
не является evidence и не используется как результат.

## Следующий шаг

Владелец должен выбрать одно из двух действий: восстановить оба exact
historical raw-artifact roots из release archive (рекомендуется — сохранит
прошлую matrix) либо явно разрешить новую полную Qwen/DeepSeek matrix. После
этого можно собрать versioned candidate, выполнить host rehearsal и оставить
human acceptance отдельным решением.
