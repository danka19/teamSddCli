# QA: проверить сценарии, регрессию и evidence

Канонический источник: [artifact/lifecycle gates](../../runbooks/ARTIFACT_AND_LIFECYCLE_GATES.md),
[corporate flow controls](../../runbooks/CORPORATE_FLOW_CONTROLS.md) и
[bounded QA instruction](../../../process/roles/qa.md).

## Когда использовать

Используйте runbook для подготовки или выполнения одного QA stage: test plan,
test cases, regression check либо проверки implementation evidence. QA делает
quality findings видимыми, но не присваивает change release/archive status.

## Что нужно до начала

- роль подтверждена как `QA`;
- указан exact change path и revision;
- доступны source requirements/scenarios и class/risk evidence;
- expected behavior и environment известны;
- implementation evidence передано Developer;
- определено, какие checks будут executed, proposed или unavailable;
- есть разрешённое место для test/failed-run evidence.

Если expected result отсутствует, QA не должен изобретать его из реализации.

## Пошаговый маршрут

1. Получите продолжение:

   ```text
   sdd next --change <path-to-change> --role QA --json
   ```

   На real schema-v2 change текущая версия возвращает известный
   `missing-lifecycle-state`. Не меняйте metadata вручную; сохраните blocker и
   следуйте specialist QA/lifecycle runbooks до product fix.
2. После исправления проверьте returned evidence/decision boundary; не считайте route QA approval.
3. Свяжите positive, negative и regression cases со stable scenario IDs.
4. Проверьте class-specific risk areas и обязательные evidence types по
   canonical matrix.
5. Выполните разрешённые checks в заявленном environment.
6. Для каждого case запишите input, expected, actual, result и evidence path.
7. Сохраните failed attempts даже после исправления/retest.
8. Отдельно перечислите defects, unavailable evidence, waivers и residual gaps.
9. Передайте findings ответственным людям и остановитесь перед чужим decision.

## Ожидаемый результат

- scenarios имеют test/evidence mapping;
- executed и proposed checks не смешаны;
- actual results воспроизводимы;
- blockers и residual gaps видимы;
- failed-run history сохранена;
- QA conclusion не выдаёт DoD/release/archive за автоматически принятые.

## Доказательства

Сохраните exact revision/environment, case IDs, commands, expected/actual,
timestamps при необходимости, logs/screenshots с stable references, defect
links, retest history, unavailable checks и approved waiver references.
Screenshot или AI-summary без source/evidence reference недостаточны.

## Решения и границы

QA отвечает за достоверность QA findings и применимые quality conclusions.
QA не меняет classification, не одобряет product/security/release за другие
роли, не скрывает failed case и не объявляет external delivery.

AI может подготовить cases или свести evidence, но не отмечает gate green и не
принимает waiver/residual risk.

## Передача работы

Developer получает defects с reproduction и affected scenario. Analyst
получает ambiguity в expected behavior. Tech Lead получает regression/risk
findings и blockers. Release/archive owner получает QA evidence и отдельную
human QA disposition, если она требуется contract.

## Сбои, fallback и эскалация

- source scenario отсутствует/противоречив — вернуть Analyst;
- environment неизвестен — отметить unavailable и запросить owner;
- implementation revision изменилась — остановить stale run и повторно связать;
- failed safety/regression case — block соответствующий conclusion;
- evidence нельзя сохранить безопасно — не вставлять private data в Git,
  запросить разрешённое хранилище;
- AI недоступен — выполнить test plan и evidence checklist вручную.

## Работа с AI

```text
Ты помогаешь QA для exact revision <digest>. Sources: <REQ/SCEN/risk IDs>.
Предложи positive/negative/regression cases и отдели proposed от executed.
Не выдумывай actual result, не отмечай DoD/release/archive и оставь gaps
видимыми. Остановись для human QA review.
```

Если AI запускает check, он должен привести exact command и raw result; человек
проверяет environment и связывает evidence.

## Чек-лист завершения

- [ ] Exact change/revision/environment зафиксированы.
- [ ] Scenarios и risks прочитаны из canonical source.
- [ ] Positive/negative/regression coverage определено.
- [ ] Executed/proposed/unavailable разделены.
- [ ] Actual evidence сохранено.
- [ ] Failed-run не удалён.
- [ ] Defects/gaps/waivers видимы.
- [ ] Выполнен handoff нужным owners.
- [ ] QA не присвоила чужое решение или lifecycle state.
