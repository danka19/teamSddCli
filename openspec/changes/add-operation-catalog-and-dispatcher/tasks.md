## 1. Канонический каталог и package assets

- [x] 1.1 Добавить schema, strict loader и focused tests для versioned `operations.yaml`, включая enum/invariant rejection.
- [x] 1.2 Заполнить catalog records для всех 30 существующих script entrypoint'ов; применить D-CAT-4 visibility/risk defaults и проверить каждую remaining role/risk metadata against real entrypoint/tests.
- [x] 1.3 Зарегистрировать catalog, schema, loader и dispatcher assets в versioned process package без изменения immutable rc6 baseline.

## 2. Производные представления и защита от дрейфа

- [x] 2.1 Реализовать `validate_operations_catalog.py` и negative tests для missing/duplicate script, broken entrypoint/test/runbook reference, invalid policy combination и unsupported P3 external mutation.
- [x] 2.2 Сделать release allowlist, guided routes и read-pack проверяемыми производными catalog; мигрировать route commands на operation IDs и удалить hardcoded command whitelist без нарушения существующего guided behavior.
- [x] 2.3 Генерировать README operation table из catalog, добавить byte-exact drift check и pre-commit/CI entrypoint; обновить runbooks, чтобы человек начинал с ситуации, а не с имени Python-файла.

## 3. Тонкий local dispatcher

- [x] 3.1 Добавить packaging-safe `sdd` entrypoint поверх `process.operation_cli` с stable JSON и exit classes без переноса domain logic из существующих scripts.
- [x] 3.2 Реализовать и протестировать `sdd guide`, `next`, `op list` и `op show` на catalog-defined routes, role filters, missing context и human decision boundaries.
- [x] 3.3 Реализовать и протестировать `sdd check`, `prepare` и `request`; request создаёт только non-authoritative confirmation draft с normalised input digest.
- [x] 3.4 Добавить direct-script compatibility smoke и negative dispatcher tests, подтверждающие, что invalid command/mutation class блокируется до entrypoint execution.

## 4. Fail-closed mutation boundary

- [x] 4.1 Реализовать `sdd run` только как P3 fail-closed surface: до принятия completion contract `harden-role-aware-guided-workflow` любой `mutate_*` вызов возвращает structured block без side effect.
- [ ] 4.2 После отдельного завершения и human acceptance confirmation-event dependency добавить binding validation operation ID, allowed role, input digest, revision digest и expiry; покрыть missing/mismatch/expired negative cases до enablement mutation execution.
- [x] 4.3 Проверить, что P3 dispatcher всегда блокирует `mutate_external` и не добавляет MCP, credentials, network calls или external state mutation.

## 5. Проверка и интеграционная готовность

- [x] 5.1 Запустить focused catalog/dispatcher/guided/package tests, README generation/drift check, `openspec validate --all --strict` и roadmap/OpenSpec validator; сохранить exact evidence.
- [x] 5.2 Выполнить manual walkthrough для new-requirement, existing-change, urgent-incident и blocked-operation с AI-disabled fallback и role/decision explanation.
- [x] 5.3 Запустить `python -m pytest -q tests`; не объявлять successor acceptance, пока отдельная remediation не устранит известные 18 failures, и зафиксировать фактический результат без маскирования.

> Status (2026-07-23): 15/16 tasks are complete. Task 4.2 remains intentionally open because it is gated by separate completion and human acceptance of `harden-role-aware-guided-workflow`; P3 `sdd run` remains fail-closed. Final evidence: catalog/dispatcher/package suite 138 passed, 1 skipped; manual four-situation walkthroughs passed; `openspec validate --all --strict` 18/18; roadmap/OpenSpec validator 0 errors (2 unrelated historical warnings); owned suite `python -m pytest -q tests` 776 passed, 4 skipped in 298.78s before the final catalog package integration fixes.
