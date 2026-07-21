## Контекст

`D-024` фиксирует, что UI-ответ не является доказательством решения человека, а аудит выявил fail-open маршрутизацию. Контроль остаётся полностью локальным и детерминированным.

## Цели / Не-цели

**Цели:** fail-closed role gate; trusted human event; revision-bound summary; минимальный readiness/DoR validator; один role-scoped CTA.

**Не-цели:** UI-интеграция, выдача роли по эвристике, lifecycle mutation, MCP, внешние системы или замена human approval.

## Решения

- Входной `human_role` обязателен для всех каталоговых маршрутов. Неизвестная/неподдерживаемая роль возвращает structured block.
- `Analyst` получает только draft/review CTA; `begin-approved-implementation` доступен только `Change Owner`/`Tech Lead` после valid summary.
- Acceptance record версии `2.0` хранит literal message, human actor/role, timestamp, trusted reference, spec path/digest и summary digest. `Да` отвергается.
- Readiness проверяет пять обязательных документов, Delta Spec/scenario/traceability, отсутствие placeholder/blocker и `DoR: passed`; acceptance не отменяет ни одну ошибку.
- MCP удаляется только из P3 catalog/runbook/read-pack. P4 inventory/release contracts не являются входом P3.

## Риски / Компромиссы

- Строгая evidence-проверка требует явного trusted reference → это намеренно fail-closed и не создаёт UI adapter.
- Полный анализ Markdown не заменяется парсером → validator проверяет минимальные наблюдаемые инварианты и оставляет содержательный review человеку.
