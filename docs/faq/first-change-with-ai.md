# Первый `minor` change вместе с AI

Канонический источник: [guided workflow](../runbooks/GUIDED_OWNER_WORKFLOW.md),
[packaged governed flow](../runbooks/PACKAGED_GOVERNED_FLOW.md),
[classification runbook](../runbooks/CLASSIFICATION_AND_MIGRATION.md),
[versioned classification policy](../../process/policies/classification.yaml),
[AI authority contract](../../openspec/specs/role-aware-guided-workflow/spec.md)
и [accepted dispatcher contract](../../openspec/specs/guided-operation-dispatcher/spec.md).

Это первый проход [парного учебного маршрута](first-change.md). AI ведёт один
реальный bounded пример, но не становится Analyst, Tech Lead, Developer или QA.
Он читает разрешённые sources, собирает source-linked evidence, предлагает
candidate class, показывает exact command и запускает её только после отдельного
«выполняй». Человек принимает решения и подтверждает каждое изменение состояния
или файлов.

## Учебная задача и точный scope

Этот проход выполняется только в clean disposable checkout
`C:/work/teamSddCli-ai` от исходного revision и в отдельном пустом workspace
`C:/work/faq-walkthrough-ai`. В функции `_render_human` файла
`process/operation_dispatcher.py` переименовать
только локальный список `lines` в `output_lines`. Runtime-поведение,
human-readable output и public contract не меняются.

Focused regression test уже существует:

```text
python -m pytest tests/test_self_service_onboarding.py::test_start_human_renderer_uses_the_same_next_command -q
```

Ожидаемый результат до и после edit: `1 passed`.

## Перед началом: staged permissions

Откройте AI-клиент в checkout `teamSddCli` и дайте ему один bounded task.
Не выдавайте постоянное разрешение на shell или весь repository.

На этапе анализа разрешены только:

```text
rg ... process/operation_dispatcher.py tests/test_self_service_onboarding.py process/policies/classification.yaml
python -m pytest tests/test_self_service_onboarding.py::test_start_human_renderer_uses_the_same_next_command -q
sdd --version --json
sdd start ... --json
sdd request ... --json
sdd check ... --json
sdd next ... --json
sdd prepare ... --json
git diff -- process/operation_dispatcher.py
```

На этапе implementation отдельно разрешается изменить только локальное имя
`lines` внутри `_render_human`. Каждый edit, test и `sdd` вызов подтверждается
отдельно. `git add`, `commit`, `push`, merge, external tools, `sdd run`, прямые
mutation scripts и `sdd setup ... --confirm` AI не выполняет.

Если workspace ещё не создан, AI показывает
`sdd setup C:/work/faq-walkthrough-ai --confirm --json`, а человек проверяет пустой
path, лично выполняет команду и возвращает AI raw JSON.

## Сначала простая фраза: аналитическое интервью

Если packaged companion установлен, не копируйте длинный prompt. Начните так:

```text
Роль человека: Analyst.
Помоги оформить небольшое изменение. Сначала помоги разобраться.
```

Для более общей идеи можно сказать: «Помоги разобраться и оформить новую идею».

AI не должен сразу читать repository, запускать команду или создавать change.
Сначала он показывает план тем:

```text
Предлагаю уточнить:
1. какую проблему и для кого решает изменение;
2. как всё работает сейчас и что должно измениться;
3. основной, альтернативный и ошибочный сценарии;
4. scope, ограничения и зависимости;
5. критерии приёмки и открытые решения.

Можно пройти по этим темам? После разрешения я буду задавать по одному вопросу.
```

После ответа «да» пример продолжается одним вопросом:

```text
Какую проблему должен перестать испытывать пользователь?
```

Если человек отвечает «не знаю», AI сохраняет `unknown`, объясняет влияние и
назначает вопрос владельцу. Если ответы расходятся, AI сохраняет `conflict`, а
не выбирает удобную версию. Предложения AI остаются `proposed`; только слова
человека и проверенные sources становятся `confirmed`.

После смысловых блоков AI сверяет понимание. Формат результата — итоговая сводка:
проблема и польза, пользователь, текущее и ожидаемое поведение,
сценарии, scope/out of scope, ограничения, зависимости, критерии приёмки,
неизвестные факты и решения.

После подтверждения сводки AI предлагает черновики, но ничего не записывает без
отдельного согласия. После review черновиков он задаёт новый вопрос:

```text
Черновики готовы как рабочая версия. Показать первую команду для создания
change package?
```

Ответ на этот вопрос разрешает только показать первую команду. Для её
выполнения всё равно требуется отдельное «выполняй».

## Стартовый prompt

Ниже находится прозрачный fallback для AI-клиента без установленного packaged
companion. Замените `<repo>` на checkout `teamSddCli`, затем скопируйте:

```text
Мы проводим первый synthetic minor-change walkthrough.

Роль человека в начале: Analyst.
Requested change: в <repo>/process/operation_dispatcher.py, только внутри
_render_human, переименовать локальный список lines в output_lines без изменения
runtime и текста вывода.

Сначала собери evidence сам. Прочитай только:
- <repo>/process/operation_dispatcher.py
- <repo>/tests/test_self_service_onboarding.py
- <repo>/process/policies/classification.yaml
- <repo>/docs/runbooks/CLASSIFICATION_AND_MIGRATION.md
- <repo>/docs/runbooks/GUIDED_OWNER_WORKFLOW.md

Найди exact symbol и focused regression test. Выполни baseline test только
после моего отдельного «выполняй». Сопоставь все 17 minor-condition IDs с
конкретным source path и фактом. То, что source не доказывает, пометь unknown и
запроси у Tech Lead; не превращай assumption в true.

Сам предложи candidate class и покажи основания, unknown facts и major/hotfix
triggers. Это не human confirmation.

Перед каждой командой или edit покажи exact action, ожидаемый результат,
что изменится и что не изменится; дождись отдельного «выполняй». После команды
верни exit/result и raw output, затем объясни его отдельно.

Не выполняй next_command автоматически. Не подставляй --confirm. Не подтверждай
classification, DoR/DoD, risk, release или archive. Не выдумывай facts,
approvals и test results. Не выполняй Git publish/merge или external mutation.
```

## Шаг 1. AI собирает evidence из repository

AI сначала предлагает две read-only команды:

```text
rg -n "def _render_human|lines =|lines\.append|join\(lines\)" process/operation_dispatcher.py
rg -n "test_start_human_renderer_uses_the_same_next_command" tests/test_self_service_onboarding.py
```

После отдельного разрешения на каждую команду AI должен найти:

- `_render_human` и все использования локального `lines` только в одной функции;
- focused test, который проверяет неизменный human-readable `next_command`;
- 17 canonical IDs в `classification.minor-conditions`.

Затем AI показывает baseline command:

```text
python -m pytest tests/test_self_service_onboarding.py::test_start_human_renderer_uses_the_same_next_command -q
```

Человек отвечает: `Выполняй только baseline test.` AI запускает его и сохраняет
actual output. Если test не прошёл, route останавливается: нельзя использовать
красный baseline как evidence безопасного refactor.

## Шаг 2. AI предлагает `minor`, не подтверждая его

AI строит таблицу `condition ID → source → fact/unknown`. Для exact local rename
code и test подтверждают local/small scope, отсутствие output/public API и
простой regression check. Impact-факты, которые нельзя доказать только чтением
двух файлов, остаются `unknown` до ответа Tech Lead.

Ожидаемый вывод:

```text
Recommendation: candidate minor.
Evidence: exact local symbol, one-function write scope, passing focused baseline,
no observed behavior/output/public-contract change.
Unknowns for Tech Lead: скрытые component, data, security, integration,
reliability, performance, SLA, operations, governed-doc/test и architecture
impacts.
Authority: recommendation only; classification remains pending.
```

После проверки unknowns человек отвечает:

```text
Tech Lead проверил перечисленные impacts: дополнительных impacts нет.
Разрешаю использовать minor только как candidate input для sdd start.
Покажи команду; это ещё не canonical classification decision.
```

## Шаг 3. AI запускает guided start

AI показывает:

```text
sdd start new-requirement --role Analyst --fact classification=minor --json
```

После `Выполняй только эту команду.` AI запускает её и возвращает raw JSON.
Вместе проверьте:

- `status: guided`;
- `missing_facts` пуст;
- human owner — `Tech Lead`;
- `authority_boundary` говорит, что classification pending;
- `next_command` предлагает
  `sdd request create-change --role Analyst --json`;
- lifecycle/external mutation не выполнены.

AI не выполняет `next_command` автоматически.

## Шаг 4. AI создаёт только неавторитетный request

AI спрашивает:

```text
Разрешаете выполнить только следующую команду?
```

```text
sdd request create-change --role Analyst --json
```

После отдельного `Выполняй.` AI запускает команду. Ожидаются
`status: confirmation-requested`, `authority_granted: false`,
`review_required: true`, `trusted_event_metadata_required: true` и отсутствие
lifecycle/external mutation.

Это evidence подготовки, а не созданный change и не approval.

## Шаг 5. Человек создаёт change package

Public `sdd run` пока возвращает `confirmation-contract-pending`, поэтому AI
останавливается. После review request ответственный оператор лично выполняет
documented compatibility command:

```text
python scripts/create_change.py sample-minor-ai-001 --title "Rename internal renderer list variable" --classification minor --type refactor --changes-root C:/work/faq-walkthrough-ai/team-specs/openspec/changes --package-root C:/work/faq-walkthrough-ai/process --json
```

AI не запускает эту mutation. Человек передаёт ему raw result и path:

```text
C:/work/faq-walkthrough-ai/team-specs/openspec/changes/sample-minor-ai-001/
```

## Шаг 6. AI готовит classification evidence

Созданный `change.yaml` содержит только `local-change: unknown` и pending
decision. AI читает 17 IDs из
`C:/work/faq-walkthrough-ai/process/policies/classification.yaml` и форму rows из
`C:/work/faq-walkthrough-ai/process/templates/change-v2/change.yaml`.

Сначала AI предлагает отдельный factual artifact diff:

- `proposal.md`: точный intent `lines → output_lines`, один affected function,
  явные non-goals и acceptance `output unchanged`;
- `design.md`: before/after scope, отсутствие interface/runtime changes,
  regression command и rollback через обратный rename;
- `tasks.md`: baseline, exact edit, focused regression, diff review и QA handoff;
- `evidence/baseline-test.txt`: exact command, revision, exit и actual output;
- `decisions/impact-review.md`: только проверенный человеком ответ по скрытым
  impacts; AI может подготовить вопросы, но не подписывает ответ за Tech Lead;
- `change.yaml`: `spec_change.required: false` и `delta_paths: []`, потому что
  поведение не меняется.

Generated placeholder `specs/sample/spec.md` не используется как evidence:
после human review его удаляют из этого draft package, чтобы sample-текст не
выглядел каноническим Delta Spec.

Человек отдельно проверяет и разрешает этот artifact diff. Только после этого
AI предлагает второй diff, который добавляет ровно 17 source-linked
`classification_evidence` rows. Разрешённые source kinds указывают на
фактически заполненные `proposal.md`, `design.md`, human-owned impact decision
и retained baseline evidence. Rationale описывает именно этот refactor.
`unknown` не заменяется `true` без проверенного source. Блок `decision`
остаётся `state: pending`.

Человек проверяет diff и отдельно отвечает:

```text
Разрешаю применить показанный factual artifact diff и classification_evidence
только внутри этого synthetic change. Decision block не менять.
```

После edit AI показывает read-only classifier:

```text
sdd check classify-change --role "Tech Lead" -- C:/work/faq-walkthrough-ai/team-specs/openspec/changes/sample-minor-ai-001/change.yaml --config C:/work/faq-walkthrough-ai/team-specs/sdd.config.yaml --json
```

После отдельного `Выполняй.` ожидается:

- `classification.minor-evidence-incomplete`, если остался хотя бы один unknown;
- `classification.human-confirmation-required`, когда все 17 conditions
  подтверждены, но human decision ещё pending.

AI не исправляет эти blockers догадкой.

`status: valid` проверяет структуру rows, policy consistency и наличие
human decision. Классификатор не доказывает истинность prose сам по себе:
содержимое proposal/design/evidence и соответствие реальному diff проверяют
Tech Lead и QA.

## Шаг 7. Tech Lead подтверждает class

Tech Lead лично проверяет classifier report, source evidence и отсутствие
major/hotfix triggers. Затем через принятый human review route фиксирует
class, owner, reviewed evidence, outcome и дату в
`decisions/classification.md`, после чего сам обновляет `change.yaml.decision`
до `confirmed` или `corrected`. AI не пишет решение за него и не превращает
ответ чата в trusted event metadata.

После этого AI снова показывает ту же `sdd check classify-change ... --json`
command и ждёт отдельное разрешение. Только свежие exit `0`, `status: valid` и
`selected_class: minor` подтверждают согласованность declared route с policy и
human decision.

## Шаг 8. Developer выполняет один exact edit

AI показывает планируемый diff:

```diff
-    lines = [f"{payload['operation']}: {payload['status']}"]
+    output_lines = [f"{payload['operation']}: {payload['status']}"]
```

И отдельно перечисляет замены `lines.append(...) → output_lines.append(...)`
и `join(lines) → join(output_lines)` только внутри `_render_human`.

Developer отвечает:

```text
Разрешаю только показанный rename внутри _render_human.
Не меняй другие функции, output strings или tests.
```

После edit AI показывает:

```text
git diff -- process/operation_dispatcher.py
```

Человек отдельно разрешает read-only diff, проверяет отсутствие иных изменений,
затем отдельно разрешает regression command:

```text
python -m pytest tests/test_self_service_onboarding.py::test_start_human_renderer_uses_the_same_next_command -q
```

Ожидается `1 passed`. AI возвращает actual output; непроведённый или failed test
не записывается как passed.

## Шаг 9. AI продолжает change и передаёт QA

AI показывает:

```text
sdd next --change C:/work/faq-walkthrough-ai/team-specs/openspec/changes/sample-minor-ai-001 --role Developer --json
```

После отдельного разрешения AI запускает read-only continuation и возвращает
raw JSON. Developer передаёт QA exact change path, code diff, baseline result,
post-edit result и residual limitations.

QA отдельно разрешает:

```text
sdd next --change C:/work/faq-walkthrough-ai/team-specs/openspec/changes/sample-minor-ai-001 --role QA --json
```

QA лично повторяет focused test либо проверяет independently captured output и
решает достаточность evidence. AI не подтверждает DoD, release или archive.

## Шаг 10. AI подготавливает review, но не публикует

AI показывает:

```text
sdd prepare prepare-spec-pr --role Developer -- C:/work/faq-walkthrough-ai/team-specs/openspec/changes/sample-minor-ai-001 --package-root C:/work/faq-walkthrough-ai/process --json
```

После отдельного разрешения AI может запустить preparation и вернуть raw result.
Команда не создаёт commit/PR, не меняет lifecycle, не выполняет merge и не
подтверждает release/archive.

## Что именно подтверждает человек

Человек отдельно подтверждает:

1. bounded read scope и каждую read-only command;
2. baseline test;
3. использование `minor` как candidate input;
4. каждый `sdd` вызов;
5. human-owned создание package;
6. draft classification evidence без изменения decision;
7. final classification decision Tech Lead;
8. exact code edit, затем diff и focused test;
9. достаточность QA evidence и последующие gate/release/archive decisions.

Ответ `Выполняй` относится только к показанной команде или edit и не переносится
на следующий шаг.

## Если AI или инструмент недоступен

Сохраните последний raw result и перейдите к
[тому же маршруту без AI](first-change-without-ai.md). Manual route использует
тот же symbol, package title, commands, test и human gates. Отключение AI не
ослабляет classification, evidence или mutation boundary.
