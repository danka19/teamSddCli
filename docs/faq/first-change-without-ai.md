# Тот же первый `minor` change без AI

Канонический источник: [guided workflow](../runbooks/GUIDED_OWNER_WORKFLOW.md),
[packaged governed flow](../runbooks/PACKAGED_GOVERNED_FLOW.md),
[classification runbook](../runbooks/CLASSIFICATION_AND_MIGRATION.md),
[versioned classification policy](../../process/policies/classification.yaml)
и [accepted dispatcher contract](../../openspec/specs/guided-operation-dispatcher/spec.md).

Это второй проход [парного учебного маршрута](first-change.md). Сначала пройдите
[тот же change вместе с AI](first-change-with-ai.md), затем повторите эти шаги
вручную. Symbol, package title, commands, expected results, test и human gates
в обоих проходах одинаковы.

## Учебная задача и точный scope

Этот проход выполняется в отдельном clean disposable checkout
`C:/work/teamSddCli-manual` того же исходного revision и в пустом workspace
`C:/work/faq-walkthrough-manual`. Не продолжайте в AI-копии: там symbol и
change package уже изменены.

В функции `_render_human` файла `process/operation_dispatcher.py` переименовать
только локальный список `lines` в `output_lines`. Runtime-поведение,
human-readable output и public contract не меняются.

Используйте synthetic change ID `sample-minor-manual-001`. Оба checkout должны
начинаться с одного revision и не содержать unrelated changes.

## Шаг 1. Проверить source и baseline

Найдите exact symbol и focused test:

```text
rg -n "def _render_human|lines =|lines\.append|join\(lines\)" process/operation_dispatcher.py
rg -n "test_start_human_renderer_uses_the_same_next_command" tests/test_self_service_onboarding.py
```

Запустите baseline:

```text
python -m pytest tests/test_self_service_onboarding.py::test_start_human_renderer_uses_the_same_next_command -q
```

Ожидается `1 passed`. Сохраните actual output. Если baseline красный,
остановитесь и разберите исходный failure до создания refactor change.

## Шаг 2. Собрать признаки candidate `minor`

Откройте `process/policies/classification.yaml` и сопоставьте все 17 IDs из
`classification.minor-conditions` с source evidence.

Code и focused test подтверждают exact local symbol, one-function scope,
неизменность output/public contract и regression check. Tech Lead отдельно
проверяет component, data, security, integration, reliability, performance,
SLA, operations, governed-doc/test, architecture и другие скрытые impacts.
Неизвестный факт остаётся `unknown`; он не становится `true` по умолчанию.

Результат этого шага — recommendation `candidate minor`, список sources и
unknowns. Это ещё не human confirmation.

## Шаг 3. Подготовить workspace

Если workspace отсутствует, сначала убедитесь, что destination пуст, затем
человек лично выполняет:

```text
sdd setup C:/work/faq-walkthrough-manual --confirm --json
```

Ожидаются `status: created`, paths `process/` и `team-specs/`,
`next_command: sdd start new-requirement --role Analyst --json` и отсутствие
external/lifecycle mutation.

## Шаг 4. Analyst запускает guided route

После проверки candidate facts:

```text
sdd start new-requirement --role Analyst --fact classification=minor --json
```

Проверьте:

- `status: guided`;
- `missing_facts` пуст;
- human owner — `Tech Lead`;
- `authority_boundary` сообщает, что classification pending;
- `next_command` равен
  `sdd request create-change --role Analyst --json`;
- lifecycle/external mutation не выполнены.

`classification=minor` здесь только candidate input.

## Шаг 5. Analyst создаёт неавторитетный request

```text
sdd request create-change --role Analyst --json
```

Ожидаются `status: confirmation-requested`, `authority_granted: false`,
`review_required: true`, `trusted_event_metadata_required: true` и отсутствие
mutation. Передайте raw result и candidate evidence Tech Lead.

## Шаг 6. Человек создаёт change package

Public `sdd run` пока остаётся fail-closed. После human review ответственный
оператор выполняет specialist compatibility command:

```text
python scripts/create_change.py sample-minor-manual-001 --title "Rename internal renderer list variable" --classification minor --type refactor --changes-root C:/work/faq-walkthrough-manual/team-specs/openspec/changes --package-root C:/work/faq-walkthrough-manual/process --json
```

Ожидаются `status: created`, `decision_state: pending-human-confirmation` и path:

```text
C:/work/faq-walkthrough-manual/team-specs/openspec/changes/sample-minor-manual-001/
```

## Шаг 7. Заполнить и проверить classification evidence

Созданный `change.yaml` содержит `local-change: unknown` и pending decision.
Возьмите 17 IDs из
`C:/work/faq-walkthrough-manual/process/policies/classification.yaml`, а форму rows —
из `C:/work/faq-walkthrough-manual/process/templates/change-v2/change.yaml`.

До rows заполните factual artifacts:

- `proposal.md`: exact rename, one-function scope, non-goals и output unchanged;
- `design.md`: before/after, отсутствие interface/runtime changes, focused test
  и revert rollback;
- `tasks.md`: baseline, edit, focused test, diff review и QA handoff;
- `evidence/baseline-test.txt`: command, revision, exit и actual output;
- `decisions/impact-review.md`: подписанный человеком результат проверки
  скрытых impacts;
- в `change.yaml` установите `spec_change.required: false` и `delta_paths: []`.

Удалите generated placeholder `specs/sample/spec.md`: для non-behavior refactor
Delta Spec не требуется, а generic sample не является evidence.

Затем добавьте ровно 17 source-linked `classification_evidence` rows со
ссылками на фактически заполненные proposal/design/human-decision/external
evidence и точным rationale. Не меняйте `decision` и не подставляйте `true`
вместо unknown без evidence.

Запустите:

```text
sdd check classify-change --role "Tech Lead" -- C:/work/faq-walkthrough-manual/team-specs/openspec/changes/sample-minor-manual-001/change.yaml --config C:/work/faq-walkthrough-manual/team-specs/sdd.config.yaml --json
```

Если evidence неполно, ожидается
`classification.minor-evidence-incomplete`. Когда все 17 conditions
подтверждены, но decision pending, ожидается
`classification.human-confirmation-required`.

Tech Lead лично проверяет sources и фиксирует `confirmed` или `corrected` через
принятый human review route: записывает class, owner, reviewed evidence,
outcome и дату в `decisions/classification.md`, затем обновляет
`change.yaml.decision`. Повторите ту же classifier command. Только exit `0`,
`status: valid` и `selected_class: minor` подтверждают согласованность declared
route с policy и human decision.

Классификатор не доказывает истинность prose: он проверяет структуру и policy
consistency. Tech Lead и QA отдельно сверяют artifacts с реальным code diff и
test output.

## Шаг 8. Developer выполняет один exact edit

В `process/operation_dispatcher.py::_render_human` сделайте только:

```diff
-    lines = [f"{payload['operation']}: {payload['status']}"]
+    output_lines = [f"{payload['operation']}: {payload['status']}"]
```

Замените в этой же функции `lines.append(...)` на
`output_lines.append(...)`, а `join(lines)` — на `join(output_lines)`.
Другие functions, output strings и tests не меняйте.

Проверьте scope:

```text
git diff -- process/operation_dispatcher.py
```

Затем запустите тот же test:

```text
python -m pytest tests/test_self_service_onboarding.py::test_start_human_renderer_uses_the_same_next_command -q
```

Ожидается `1 passed`. Evidence: exact diff, baseline output, post-edit output и
отсутствие unrelated paths.

## Шаг 9. Developer и QA получают continuation

Developer:

```text
sdd next --change C:/work/faq-walkthrough-manual/team-specs/openspec/changes/sample-minor-manual-001 --role Developer --json
```

QA:

```text
sdd next --change C:/work/faq-walkthrough-manual/team-specs/openspec/changes/sample-minor-manual-001 --role QA --json
```

Обе команды read-only: `lifecycle_mutated` и `external_state_mutated` остаются
`false`. Developer передаёт QA exact change path, diff, baseline/post-edit
results и limitations. QA лично повторяет focused test либо проверяет
independently captured output и решает достаточность evidence.

## Шаг 10. Подготовить review без публикации

Используйте ту же command, что и в AI-route:

```text
sdd prepare prepare-spec-pr --role Developer -- C:/work/faq-walkthrough-manual/team-specs/openspec/changes/sample-minor-manual-001 --package-root C:/work/faq-walkthrough-manual/process --json
```

Preparation не создаёт commit/PR, не меняет lifecycle, не выполняет merge и не
подтверждает DoD, release или archive.

## Где текущая автоматизация останавливается

Текущий public CLI останавливается перед mutation через `sdd run`, external
operations и human-owned decisions. Package creation остаётся specialist
compatibility route; lifecycle, DoR/DoD, release и archive не подтверждаются
успешным `start`, `request`, `next`, `check` или `prepare`.

## Что считать успешным walkthrough

- один и тот же symbol и package title использованы во всех шагах;
- baseline и post-edit focused test реально выполнены и сохранены;
- все 17 minor conditions имеют source-linked evidence;
- final class подтверждён Tech Lead, а не inferred из `sdd start`;
- diff содержит только механический rename внутри `_render_human`;
- manual commands совпадают с [AI-route](first-change-with-ai.md);
- ни одна local/external mutation не выдана за approval или release.

Дальше откройте [runbook своей роли](roles/index.md),
[ежедневный lifecycle](daily-workflow.md) или
[troubleshooting](troubleshooting-and-boundaries.md).
