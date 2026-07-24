# Product FAQ and role runbook acceptance audit

Date: 2026-07-24.

Status: technical verification complete; OpenSpec acceptance pending the required first-time user walkthrough.

## Scope and criteria

This audit reviews `add-product-faq-and-role-runbook` on branch
`phase-3/add-product-faq-and-role-runbook` for human-readable navigation,
canonical-source links, safe AI and release boundaries, documentation-map
coverage, deterministic validation, and completion of the agreed OpenSpec
tasks.

Acceptance criteria:

- the FAQ is readable in UTF-8 and reachable from `docs/README.md`;
- the FAQ contract, internal links, required questions and canonical sources
  pass deterministic validation;
- existing catalog/dispatcher behavior remains covered by its focused suite;
- OpenSpec and roadmap consistency checks pass;
- all agreed tasks remain represented, including a recorded first-time user
  walkthrough.

## Evidence

| Check | Result | Classification |
| --- | --- | --- |
| `pytest tests/test_product_faq_docs.py tests/test_operation_catalog_dispatcher.py -q` | `28 passed` | pass |
| `python scripts/validate_product_faq.py --json` | `status: valid`, no errors | pass |
| `openspec validate --all --strict` | `21 passed, 0 failed` | pass |
| Roadmap/OpenSpec validator | `0 errors`, 2 unrelated historical lifecycle warnings | pass with known warnings |
| `git diff --check` | passed | pass |
| `openspec list` | change has `12/13 tasks` | verified limitation |

## Findings

### FAQ-ACC-001 — `docs/README.md` was written with damaged UTF-8 text

Classification: verified documentation defect, high severity for the product
entrypoint.

Affected behavior: the README contained literal `` `r`n `` tokens and mojibake
in the Russian content, so the intended FAQ entrypoint was not reliably
human-readable.

Evidence and root cause: comparison with the immediate known-good parent
revision showed that the FAQ implementation commit rewrote existing Russian
README content with the wrong encoding. The newly created FAQ pages were
readable; the defect was limited to the rewritten README.

Remediation: restore the known-good UTF-8 README content, add the intended FAQ
entrypoint, add the repository-map entry for `docs/faq/`, and add a regression
test that rejects both literal `` `r`n `` and the observed mojibake marker.
Committed in `2150bfd`.

### FAQ-ACC-002 — mandatory first-time user walkthrough is not recorded

Classification: verified acceptance limitation, high severity for final
acceptance.

Affected behavior: task 4.4 from the agreed change required recording a user
walkthrough and the FAQ maintenance process. The implementation commit removed
the task instead of producing the evidence. The FAQ mentions a synthetic local
check, which is useful but is not evidence of a first-time human operator
following the documentation.

Remediation decision: restore task 4.4 as unchecked. Do not set the proposal
or roadmap status to `accepted` until a human records the walkthrough outcome.

### FAQ-ACC-003 — исходный FAQ прошёл structural checks, но не прошёл content acceptance

Классификация: подтверждённый дефект документации, высокая критичность для
onboarding.

Затронутое поведение: исходный FAQ из 13 страниц содержал около 1 230
разделённых пробелами слов, а каждая ролевая страница — только 48-62. Страницы
называли темы и первую команду, но не давали исполнимый installation route,
first-change tutorial, role prerequisites/inputs, ожидаемые результаты, полные
evidence/handoff/fallback инструкции, практическую AI-настройку и конкретное
сравнение продукта. Human owner 2026-07-24 явно отклонил результат как
существенно не соответствующий исходному запросу на полный FAQ и
полноформатные role runbooks.

Подтверждённая причина: `validate_product_faq.py` проверял наличие
question-markers, links, canonical-source labels и двух safety strings, но не
task-oriented content. Поэтому `valid` и пять documentation tests доказывали
целостность навигации, а не возможность выполнить пользовательскую задачу.

Исправление: направить feedback как `adopt_now` в active change; расширить FAQ
до 16 связанных страниц и примерно 8 951 разделённого пробелами слова; дать
каждой role page одинаковую рабочую структуру из десяти разделов; добавить
installation, setup/topology, first-change и glossary; расширить product
comparison, AI, roadmap и troubleshooting; заставить validator отклонять
отсутствующие обязательные страницы или role sections.

Доказательства исправления:

| Проверка | Результат | Классификация |
| --- | --- | --- |
| `python -m pytest -q -o addopts='' --basetemp <fresh-temp> tests/test_product_faq_docs.py tests/test_self_service_onboarding.py tests/test_operation_catalog_dispatcher.py` | `47 passed` | pass |
| `python scripts/validate_product_faq.py --json` | `status: valid`, no errors | pass |
| Clean venv `pip install --no-deps .` plus `sdd --version/setup/start/request` walkthrough | package `0.3.6`; setup blocked without confirmation, created with confirmation; request non-authoritative | pass, synthetic only |
| `openspec validate --all --strict` | `21 passed, 0 failed` | pass |
| Roadmap/OpenSpec validator | `0 errors`, 2 unrelated historical lifecycle warnings | pass with known warnings |

Остаточная неопределённость: проверки доказывают внутреннюю согласованность
расширенного content и документированных local commands. Они не доказывают,
что first-time human пройдёт страницы без помощи. Task 4.4 остаётся
неотмеченной, а change — `in_progress`.

### FAQ-ACC-004 — canonical `status` для real schema-v2 `sdd next`

Классификация: закрытый product/documentation blocker. Отдельный OpenSpec
change `fix-sdd-next-canonical-status` устранил несовместимость storage adapter
без изменения schema, guided catalog, ролей или mutation boundary.

Подтверждённая причина: schema-v2 `create_change` записывает lifecycle в
обязательное top-level поле `status`, а прежний dispatcher читал
`lifecycle_state`; handcrafted fixture маскировал mismatch. Теперь dispatcher
читает только `status`, передаёт его во внутренний guided fact
`lifecycle_state`, а missing/empty/non-string status блокирует с
`missing-change-status`. Неподдерживаемое непустое значение продолжает
проверяться canonical guided catalog и возвращает `invalid-context`. Второе
persisted-поле `lifecycle_state` не является fallback.

Реальное smoke evidence (2026-07-24):

```text
python scripts/create_change.py sample-minor-001 --title "Sample minor change" --classification minor --type config_ops --changes-root <fresh-temp>/changes --json
python scripts/sdd.py next --change <fresh-temp>/changes/sample-minor-001 --role Developer --json
```

Первый вызов вернул `status: created`; второй — `status: guided`,
`next_command: sdd prepare prepare-spec-pr --role Developer --json`,
`lifecycle_mutated: false` и `external_state_mutated: false`. Поэтому FAQ
теперь требует использовать только `status`, запрещает ручное добавление
`lifecycle_state` и сохраняет все human authority/mutation warnings.

## Residual risk and next action

Расширенная документация и real-package continuation готовы к содержательному
review, но не к финальному first-time walkthrough. Новый operator должен пройти
`docs/faq/index.md`, выполнить
безопасный локальный маршрут своей роли и записать, хватило ли инструкции и
какая команда или формулировка осталась непонятной. Только эта запись завершает
task 4.4 и позволяет принять отдельное human acceptance decision; sync/archive
остаются отдельными действиями.
