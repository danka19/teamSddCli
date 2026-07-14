# Отчёт: Phase 2 work item 2.2 — schema effective-base fix

## Задача

Исправить единственное замечание финального review: local-only scanner package JSON Schemas игнорировал `$id` как effective base URI и поэтому мог принять относительный `$ref` или `$dynamicRef`, который семантически разрешался в remote URI. Границы работы: только schema-graph safety; статусы Phase 2/2.2 и OpenSpec task 1.3 не изменяются.

## Исходное состояние и причина

- Ветка: `codex/phase-2-transfer-readiness-plan`; исходный HEAD: `7469f74`.
- `collect_refs()` возвращал плоский список ссылок без контекста узла.
- `_validate_schema_resource()` разрешал каждую относительную ссылку от физического каталога текущего файла.
- Поэтому subschema с `$id: https://example.invalid/base/` и `$ref: auxiliary.schema.json` ошибочно принималась, если локальный `auxiliary.schema.json` существовал рядом.
- Visited-set по каноническим `Path` и containment относительно `process/schemas/` уже существовали и должны были сохраниться.

## Решение и суждения

Выбран минимальный стандартно-библиотечный вариант: рекурсивный обход схемы несёт текущий base URI, применяет `$id` текущего узла через `urljoin()` до обработки `$ref`/`$dynamicRef`, затем допускает только относительную authored reference, которая после разрешения становится `file:` URI внутри объявленного schema root.

Не выбраны broad refactor, внешний JSON Schema resolver/registry, network lookup, новая диагностика или изменение CLI. Существующий stable code `package.schema-invalid`, общий visited-set и проверка containment сохранены.

## TDD: RED → GREEN

- Добавлена точная remote-base regression для `$ref` и `$dynamicRef`: remote `$id` + relative reference + реально существующий локальный sibling.
- Добавлен валидный local control для обоих keywords: nested relative `$id: nested/` + `auxiliary.schema.json` внутри `nested/`.
- RED-команда: `python -m pytest -q tests/test_validate_process_config.py -k "relative_reference_under_remote_id or resolves_reference_from_local_relative_id"`.
- RED-результат: 4 failed. Remote-base случаи ошибочно вернули exit 0; local-relative-base случаи ошибочно вернули exit 1.
- После production fix та же команда: 4 passed, 35 deselected.
- Focused suite: `python -m pytest -q tests/test_validate_process_config.py` -> 39 passed.

## Изменения проекта

- `process/validators/config_discovery.py`: flat reference collection заменён контекстным base-aware traversal; используются `urljoin`, `urlsplit` и `url2pathname` из standard library.
- `tests/test_validate_process_config.py`: 4 параметризованных regression/control cases.
- `docs/phases/PHASE_2_EVIDENCE_INDEX.md`: расширена scenario mapping и записаны RED/GREEN/final counts.
- `docs/runbooks/PROCESS_PACKAGE_SETUP.md`: уточнена operator-facing local-only `$id`/reference гарантия.
- Статусы work item/phase и OpenSpec checkbox не менялись.

## Проверки

- Focused regression: 4 passed, 35 deselected.
- Full focused validator suite: 39 passed in 8.71s.
- Full repository suite: 88 passed in 10.69s.
- `python -m compileall -q process/validators scripts/validate_process_config.py` -> exit 0.
- `python scripts/validate_change.py --allow-placeholders templates/change` -> `OK`.
- Representative human CLI -> exit 0, `OK [config.valid] compatible central configuration`.
- Representative JSON CLI -> exit 0, exactly one valid central compatibility object with runtime OpenSpec `1.4.1`.
- `openspec list` -> `define-transfer-ready-process-package` remains 2/33; `adopt-nis-corporate-process-governance` remains 0/43.
- `openspec list --specs` -> 8 accepted specs.
- `openspec validate --all --strict` -> 10 passed, 0 failed.
- `git diff --check` is recorded after the final documentation/report diff.

## Self-review

- `$id` is inspected at every object/subschema depth before either reference keyword.
- `$ref` and `$dynamicRef` share exactly the same resolution path.
- Fragment-only references remain internal and do not cause filesystem or network access.
- Remote effective references fail before target loading.
- Local relative `$id` changes the filesystem target according to URI resolution semantics.
- Existing canonical-path visited-set still terminates cycles.
- Resolved targets still pass `relative_to(schema_root)` and `is_file()` checks.
- No unrelated presentation files, `.claude/`, or `.vite/` were inspected or changed.

## Phase/OpenSpec governance

Read-only phase status review confirmed Phase 2 is `in_progress`, item 2.2 remains active, and item 2.3 is sequentially dependent. No status repair was made. The global roadmap/OpenSpec validator reported 33 pre-existing metadata/inverse-table errors for the repository's current documentation format; they are outside this bounded fix and were not changed. Native OpenSpec strict validation passes 10/10.

## Риски и ограничения

Риск ограничен URI edge cases outside the approved bundled-relative schema contract. Explicit network, absolute, UNC, drive-rooted, missing, and schema-root-escaping targets remain rejected. Этот commit является implementation evidence, а не coordinator acceptance; independent review/verification всё ещё требуются до task 1.3/2.2 reconciliation.

## Skills и subagents

Использованы `receiving-code-review`, `systematic-debugging`, `test-driven-development`, `phase-change-intake`, `phase-step-runner`, `phase-status-audit`, `roadmap-openspec-validator`, `verification-before-completion`, `session-report`. Subagents не использовались по явному ограничению задания.

## Следующий шаг

Передать commit coordinator/reviewer для повторной проверки единственного schema-base finding; только coordinator после независимого approval может отметить OpenSpec task 1.3 и изменить статус work item 2.2.
