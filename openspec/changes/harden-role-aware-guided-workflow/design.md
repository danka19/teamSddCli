## Контекст

`D-024` фиксирует, что UI-ответ не является доказательством решения человека, а аудит выявил fail-open маршрутизацию. Контроль остаётся полностью локальным и детерминированным.

## Цели / Не-цели

**Цели:** fail-closed role gate; trusted human event; revision-bound summary; минимальный readiness/DoR validator; один role-scoped CTA.

**Не-цели:** UI-интеграция, выдача роли по эвристике, lifecycle mutation, MCP, внешние системы или замена human approval.

## Решения

- Входной `human_role` обязателен для всех каталоговых маршрутов. Неизвестная/неподдерживаемая роль возвращает structured block.
- `Analyst` может быть доверенным человеком для literal, revision-bound acceptance спецификации, но получает только draft/review CTA; после valid DoR и acceptance summary Analyst готовит PR для ролевого согласования; начало реализации не выдаётся ни одной роли этим validator.
- Acceptance record версии `2.0` хранит literal message, human actor/role, timestamp, trusted reference, spec path/digest и summary digest. `Да` отвергается.
- Readiness проверяет пять обязательных документов, Delta Spec/scenario/traceability, отсутствие placeholder/blocker и `DoR: passed`; acceptance не отменяет ни одну ошибку.
- MCP удаляется только из P3 catalog/runbook/read-pack. P4 inventory/release contracts не являются входом P3.

## Риски / Компромиссы

- Строгая evidence-проверка требует явного trusted reference → это намеренно fail-closed и не создаёт UI adapter.
- Полный анализ Markdown не заменяется парсером → validator проверяет минимальные наблюдаемые инварианты и оставляет содержательный review человеку.

## Канонический GigaCode package template

Два исполняемых контекстных файла (`AGENTS.md` и `skills/sdd-process-companion.md`) являются versioned
asset `process/gigacode/`, а не локальной копией sandbox. Bootstrap устанавливает их в `.gigacode/`.
`check` и `update` сравнивают только эти declared files: совпадающий файл остаётся без изменений,
файл, совпадающий со старым package, обновляется, а любое локальное отличие блокирует операцию с
точным путём. Неуправляемые `.gigacode`-файлы не сканируются и не перезаписываются.

## Двухшаговое chat-confirmation и proactive discovery

`decision_draft` — единственный объект, который AI может подготовить после естественной фразы решения. Он содержит идентификатор `DEC-…`, change id, тип решения, revision digest, предложенное единственное последствие и дословную цитату исходной реплики. До подтверждения draft не меняет этап, DoR, acceptance или implementation CTA.

Подтверждение принимается только от следующего сообщения человека после активной карточки: точное `Подтверждаю DEC-…` или нормализованное короткое `Подтверждаю`. Любая другая реплика, переход к другому сообщению, истёкшая карточка, несовпадающий code либо изменённый digest оставляют решение неподтверждённым. Финальный record хранит обе дословные реплики, code, digest, время и ссылку на trusted chat event. `status.md` является производным summary этого record и validator report, а не AI-owned authority source.

`обычно` — proactive discovery mode, а не разрешение завершать intake по собственному усмотрению. Агент строит change-specific карту релевантных областей и для каждого существенного неизвестного указывает `confirmed`, `proposed_default`, `deferred` или `blocking`. Перед созданием spec draft он обязан показать ранжированные возможности углубления и дождаться явного выбора `углубиться`, `принять defaults` или `подготовить draft с открытыми решениями`. Отсутствие ответа не меняет статус и не принимает default.

Локальная форма/команда в будущем создаёт тот же confirmation-event record. Она не создаёт альтернативный workflow и не является P3 dependency.

## Operation-confirmation extension (2026-07-23)

The existing v1 decision confirmation remains intact and can never be used as
operation authority. P3 adds a separate `operation_confirmation_request` and
`operation_confirmation_event` contract. Both bind `human_role`, catalog
`operation_id`, `input_digest`, `revision_digest`, `issued_at`, `expires_at`,
and the existing trusted human/assistant/human event chain.

`input_digest` is SHA-256 of canonical JSON containing the operation ID and the
ordered forwarded argv after removing only dispatcher `--json`; argument order,
duplication, and values otherwise remain significant. `revision_digest` is
SHA-256 of the exact canonical request-card bytes shown to the human. A changed
request therefore invalidates the event. Validation checks the catalog role,
all bindings, timestamp awareness, and expiry against injected current time.

The extension is contract-only. `sdd request` may emit a request with
`authority_granted: false`; every `sdd run` remains
`confirmation-contract-pending` before entrypoint spawn. `mutate_external`
remains rejected at catalog load and dispatch. Trusted ingress and replay-safe
one-time consumption are intentionally deferred to a later human-accepted
execution-enablement change.
