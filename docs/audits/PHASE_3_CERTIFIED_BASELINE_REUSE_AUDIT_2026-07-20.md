# Аудит повторного использования certified baseline — 2026-07-20

## Цель и граница

Пакет `0.3.1` добавляет проверяемый режим `baseline-reuse`: он может сослаться
на неизменяемую полную matrix `0.3.0`, но только при совпадении модельного
контракта и свежем preflight. Это не меняет accepted `phase-2-14-rc6`, не
создаёт автоматического acceptance и не запускает корпоративную адаптацию.

## Критерии

1. Reuse указан явно и не может быть выведен из одной только версии package.
2. Все зарегистрированные AI-contract hashes совпадают с текущим payload.
3. Историческая matrix и её raw root остаются неизменяемыми и доступны для
   candidate-bound проверки.
4. Qwen и DeepSeek имеют отдельные свежие passed preflight текущей версии.
5. При любой неполноте acceptance отказывает, а не понижает проверку.

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
| Исторические raw-артефакты | найдены в `C:\Users\danoc\Documents\certifications`; все 48 файлов, объявленных rc6 manifest, совпали по SHA-256 |
| Новый чистый raw bundle | создан вне Git как `guided-owner-v0.3.1-candidate-raw-2026-07-20`; два лишних top-level runtime probe из исходных каталогов не включены |
| rc3 bytecode regression | обнаружена при валидации: CLI записывал `.pyc` в собственный payload; rc3 оставлен как rejected diagnostic history |
| Windows full-clean rehearsal rc4 | passed; manifest валиден до и после репетиции, payload SHA-256 `055451d125eec3055c45aee27725fd1cfc69fd542aa1159ad112936514e9e7e4` |

## Findings

### BR-001: Historical raw bundle найден и корректно закрыт

- Классификация: закрыто.
- Исправление поиска: первоначальная проверка ограничилась каталогом
  `teamSsdCli-release-artifacts`, хотя исторические исходные артефакты находились
  в `C:\Users\danoc\Documents\certifications`. Это была ошибка рабочего поиска,
  а не отсутствие evidence.
- Подтверждение: для Qwen и DeepSeek сверены все 48 файлов, перечисленных в
  immutable rc6 manifest. Не обнаружено ни пропусков, ни расхождений SHA-256.
- Защита от повторения rc5: два лишних top-level `*-runtime-probe.json` не
  перенесены в новый bundle, так как manifest их не объявляет. Новый bundle
  содержит только exact closure плюс отдельно зарегистрированные fresh preflight
  current package.

### BR-002: Linux/WSL2 host evidence ещё не получен

- Классификация: verified environment blocker, medium severity.
- Влияние: `rc3` не может получить `evidence-complete`, потому что acceptance
  требует ровно два host-файла: Windows full-clean rehearsal и Linux/WSL2
  portability smoke. Windows уже passed; macOS остаётся явно `not-certified`.
- Подтверждение: `wsl --list --quiet` сообщает, что на машине нет установленного
  Linux-дистрибутива. Поэтому нельзя честно создавать `linux-wsl2.yaml` из
  Windows-сеанса.
- Рекомендованное действие: выполнить Linux/WSL2 rehearsal на доступном Linux
  или после установки дистрибутива WSL, затем запустить `accept` для rc3. Полная
  Qwen/DeepSeek matrix при этом не требуется: условия baseline-reuse уже
  проверены и текущие preflight прошли.

### BR-003: Управляющий CLI изменял payload кандидата bytecode-файлами

- Классификация: закрыто до выпуска rc4.
- Причина: `manage_release_candidate.py` импортировал Python-модули из payload,
  а интерпретатор по умолчанию создавал рядом с ними `__pycache__/*.pyc`.
  Последующая проверка справедливо отклоняла уже изменённый кандидат с кодом
  `release.bytecode-forbidden`.
- Исправление: управляющий CLI отключает запись bytecode до импортов. Добавлен
  регрессионный тест, который запускает `validate` как отдельный процесс и
  проверяет, что SHA-256 payload остаётся неизменным.
- Подтверждение: rc4 прошёл manifest validation до и после Windows rehearsal.

## Следующий шаг

Владелец должен предоставить среду Linux/WSL2 для portability smoke или
разрешить установку WSL-дистрибутива на этой машине. После этого агент выполнит
строго предусмотренную репетицию и `accept` для уже созданного rc3. Human
acceptance остаётся отдельным решением после `evidence-complete`.
