# Аудит роли, acceptance и операционной готовности GigaCode

Дата: 2026-07-21

Проверяемая песочница: `C:\Users\danoc\Documents\projects\sdd-workflow-playground`

Канонический репозиторий процесса: `C:\Users\danoc\Documents\projects\teamSsdCli`

Режим проверки: read-only; файлы песочницы, OpenSpec, roadmap, шаблоны и код не изменялись.

## 1. Краткий вердикт

**Некорректно.**

Текстовые правила задают безопасное намерение: запросить роль, идти по этапам,
не начинать реализацию до человеческого решения, показывать сводку, пути,
ledger, проверки и один следующий шаг. Фактический машиночитаемый контур не
обеспечивает эти правила сквозным образом:

- неизвестная роль не является блокирующим состоянием validator или guided
  response contract;
- роль `Analyst` есть в AI role package, но отсутствует в корневом списке ролей
  человека;
- один role-neutral результат `begin-approved-implementation` может быть
  возвращён без проверки полномочий пользователя;
- acceptance-файл подтверждает только наличие заранее заданной строки в YAML,
  но не проверяет, что строку действительно написал уполномоченный человек;
- readiness спецификации проверяется слабее, чем требует `PROCESS_MAP.md`;
- наличие обязательной сводки проверяется только по маркерам в `status.md`, а не
  по фактическому ответу или UI payload.

Следовательно, наблюдавшийся prompt `Спека принята, реализуй` с вариантами
`Да / Нет` создаёт реальный путь к преждевременному acceptance или предложению
реализации пользователю с неизвестной либо несовместимой ролью.

## 2. Findings

| ID | Серьёзность | Наблюдение | Доказательство с точным путём | Нарушенное правило | Риск |
|---|---|---|---|---|---|
| GIG-ROLE-01 | critical | Корневое правило требует определить роль в начале нового рабочего чата, но guided catalog, summary payload и validator не имеют обязательного `unknown_role` stop. | `sdd-workflow-playground/AGENTS.md:78-89`; `sdd-workflow-playground/process/catalogs/guided-owner-workflow.yaml:35-50`; `sdd-workflow-playground/process/guided_process_integrity.py:68-101` | Сначала установить или запросить роль; не додумывать неизвестный факт. | Агент может показать role-sensitive действие до установления полномочий человека. |
| GIG-ROLE-02 | critical | Словари ролей не совпадают: для человека перечислены `Change Owner`, `Tech Lead`, `Developer`, `QA`, `Release Owner`, а reusable AI package использует `analyst`, `developer`, `qa`, `tech_lead`. Роль Analyst не имеет явного отображения в human-role contract. | `sdd-workflow-playground/AGENTS.md:80-83`; `sdd-workflow-playground/process/roles/analyst.md:1-17`; `sdd-workflow-playground/process/schemas/task-launch.schema.json` | Роль должна однозначно ограничивать допустимые действия и human decision gates. | Analyst может быть ошибочно принят за Change Owner или получить действие, которого его роль не разрешает. |
| GIG-ROLE-03 | critical | Analyst обязан подготовить ровно один draft и остановиться, но итог `begin-approved-implementation` не зависит от роли человека или AI. | `sdd-workflow-playground/process/roles/analyst.md:3-17,37-39`; `sdd-workflow-playground/process/guided_process_integrity.py:91-101` | Analyst не начинает реализацию и не владеет её запуском; AI не продвигает lifecycle. | Role-neutral UI может предложить реализацию Analyst или другому неподходящему пользователю. |
| GIG-UI-01 | high, `unverified` для фактического payload | По сообщению владельца, UI показал вопрос `Спека принята, реализуй` с `Да / Нет` без предварительной сводки и ссылки на spec. Журнал нового чата и фактический UI payload в доступных файлах не найдены. | Нормативные требования: `sdd-workflow-playground/AGENTS.md:19-31,57-61`; сообщение владельца от 2026-07-21. Фактический payload: `unverified`. | Перед acceptance CTA требуется краткое резюме, пути к артефактам, ledger, проверки и один допустимый следующий шаг. | Человек принимает неизвестную ревизию или неполный набор требований. |
| GIG-EVID-01 | critical | UI-ответ `Да` не равен буквальному сообщению `Спека принята, реализуй`. Текущий schema contract допускает только literal phrase. | `sdd-workflow-playground/process/schemas/spec-acceptance.schema.json:7-12`; `sdd-workflow-playground/PROCESS_MAP.md:14-15,31-32`; `sdd-workflow-playground/team-specs/openspec/changes/_template/decisions/spec-acceptance.yaml:1-5` | Implementation разрешена только после точного human evidence. | UI может интерпретировать общий ответ как более сильное решение, чем фактически сделал человек. |
| GIG-EVID-02 | critical | Validator проверяет, что YAML содержит константу, но не проверяет источник сообщения, actor type, human role, timestamp, chat/message reference, digest принятой spec revision или доверенную запись UI. Тест сам создаёт YAML и получает `begin-approved-implementation`. | `sdd-workflow-playground/process/schemas/spec-acceptance.schema.json:7-12`; `sdd-workflow-playground/process/guided_process_integrity.py:130-154`; `sdd-workflow-playground/tests/test_guided_process_integrity.py:83-106` | AI не создаёт и не выводит человеческое approval; validator не заменяет human evidence. | Агент либо любой writer change package может сфабриковать формально валидное acceptance evidence. |
| GIG-STAGE-01 | high | Карта требует на `spec_preparation` четыре документа и проверяемые сценарии, критерии и связи, но validator требует только `spec.md`. Он не отклоняет placeholders, открытые блокирующие вопросы и неподтверждённые допущения перед acceptance. | `sdd-workflow-playground/PROCESS_MAP.md:27-35`; `sdd-workflow-playground/AGENTS.md:73-76`; `sdd-workflow-playground/process/guided_process_integrity.py:41-51,177-179` | Этапы нельзя перескакивать; spec не готова при неполных документах или unresolved content. | Неполная spec может получить acceptance и открыть реализацию. |
| GIG-SUM-01 | high | Проверка сводки ищет строки-маркеры в `status.md`; generated summary не содержит роль, spec revision и признак допустимости CTA для этой роли. Связь с фактическим UI-ответом не проверяется. | `sdd-workflow-playground/process/guided_process_integrity.py:12-19,68-83,124-127` | Значимый ответ обязан отражать текущую роль, этап, артефакты, ledger, проверки и один следующий шаг. | Валидный файл не доказывает, что человек увидел необходимую сводку до решения. |
| GIG-SYNC-01 | medium | GigaCode skill формулирует `После подготовки спецификации создайте decisions/spec-acceptance.yaml`, а template говорит создавать файл только после literal acceptance. Вторая половина skill ограничивает отметку acceptance, но последовательность остаётся двусмысленной для слабой модели. | `sdd-workflow-playground/.gigacode/skills/sdd-process-companion.md:21-25`; `sdd-workflow-playground/team-specs/openspec/changes/_template/README.md:3-6` | Инструкции, шаблоны и validator должны задавать один порядок без неоднозначного промежуточного файла. | AI может создать acceptance-shaped artifact до человеческого решения. |
| GIG-STATE-01 | high | В корне песочницы нет текущего change package нового чата и нет каталога `openspec/changes`; tracked package `enforce-guided-process-integrity` отмечен удалённым, тогда как отдельный worktree его сохраняет. Желаемая судьба этого OpenSpec change по локальным данным не подтверждена. | `git -c safe.directory=C:/Users/danoc/Documents/projects/sdd-workflow-playground -C C:/Users/danoc/Documents/projects/sdd-workflow-playground status --short --branch`; `.worktrees/codex-enforce-guided-process-integrity/team-specs/openspec/changes/enforce-guided-process-integrity/` | Изменение process contract должно иметь однозначный канонический OpenSpec lifecycle и не зависеть от скрытого worktree. | Реализация существует без устойчивого change record; последующее исправление может потерять requirement/acceptance traceability. |
| GIG-CHAT-01 | medium, `unverified` | Полный журнал нового GigaCode-чата, raw model output и UI event/payload недоступны. Нельзя доказать, какой компонент сформировал `Да / Нет`, была ли скрытая role metadata и был ли записан literal phrase. | В доступном дереве песочницы таких журналов нет; исторический аудит расположен в `sdd-workflow-playground/docs/audits/GIGACODE_CHANGE_001_INTAKE_RESPONSE_AUDIT_2026-07-21.md`. | Аудит не должен выдумывать runtime evidence. | Нельзя приписывать конкретный дефект GigaCode UI, адаптеру или prompt renderer без event evidence. |

### Ответы на проверяемые вопросы

- **Обязан ли агент сначала установить или запросить роль?** Да. Это прямо
  закреплено в `AGENTS.md:80-83`. Текущая реализация это не гарантирует.
- **Как роль должна ограничивать действия и UI?** До определения роли допустимы
  только ориентация, чтение, один вопрос о роли и безопасный stop. Analyst может
  готовить draft и запросить review, но не должен видеть CTA начала реализации.
  Acceptance CTA допустим только роли, которой отдельный authority contract
  разрешает принять именно эту spec revision.
- **Допустим ли prompt без сводки и ссылки на spec?** Нет.
- **Совместимо ли `Да` с literal human evidence?** Нет. Это другой payload и
  более слабое, контекстно-зависимое сообщение.
- **Есть ли путь к преждевременному acceptance?** Да: writer может создать
  acceptance YAML, validator проверит константу, а summary вернёт
  `begin-approved-implementation` без provenance и role check.
- **Совпадают ли правила, шаблоны, validator и GigaCode-инструкции?** Частично.
  Намерение совпадает; роли, readiness, provenance и response/UI contract — нет.

## 3. Что агент сделал правильно

- Не начал продуктовую реализацию и не показал доказательств запуска сервера.
- Задавал вопросы вместо немедленного создания продукта.
- Остановился на человеческом выборе, а не объявил, что человек уже принял
  решение.
- Текущие текстовые правила ограничивают intake пятью содержательными вопросами
  и запрещают будущие артефакты на этапе `intake`.
- Validator является read-only и имеет отрицательные тесты для очевидного
  преждевременного acceptance на `intake`.
- Template однозначно говорит не создавать acceptance record до literal human
  acceptance.

Эти положительные признаки не устраняют критические пробелы role enforcement и
provenance.

## 4. Предложения доработок по приоритету

### P0. Единый role-and-authority gate

**Изменение правила.** Ввести один канонический словарь human roles и AI roles с
явным отображением. Неизвестная роль — отдельное блокирующее состояние. Для
каждой роли определить разрешённые draft/review/decision/implementation CTA.

**Изменение UI/диалога.** Первый рабочий вопрос при отсутствии допустимого
локального role record: `В какой роли вы работаете в этом изменении?`. До ответа
не показывать acceptance или implementation CTA. Analyst получает только
`продолжить анализ`, `показать сводку`, `передать на review`, `отложить`.

**Изменение validator/тестов.** Добавить role schema, `unknown-role` diagnostic,
role-scoped next actions и negative tests: Analyst/QA/Developer/Release Owner не
получают чужие решения; явная смена роли не переносит approvals.

**Критерии приёмки.** Новый чат без роли fail-closed; локальная роль используется
только из допустимого ignored record; сообщение текущего чата имеет приоритет;
каждый CTA разрешён authority matrix; Analyst никогда не получает
`begin-approved-implementation`.

- Новый OpenSpec change: **да**; рекомендуется отдельный P3 change поверх
  принятого `guided-owner-workflow`.
- Предположительно затронет:
  `openspec/changes/<new-role-aware-guided-workflow>/`, `docs/ROADMAP.md`,
  `process/catalogs/`, `process/read-packs/`, `process/roles/`, role/session
  schemas, `AGENTS.md`, `.gigacode/`, templates и focused tests.
- Human decision: **принято владельцем 2026-07-21** — обязательный role gate и
  запрет implementation CTA для Analyst. Осталось утвердить точную mapping table
  в новом OpenSpec design.

### P0. Trusted human acceptance вместо самодекларации YAML

**Изменение правила.** Literal phrase остаётся обязательной, но evidence должно
ссылаться на доверенный human-authored event или быть внесено отдельной
детерминированной процедурой, которая не доступна AI как обычная запись файла.

**Изменение UI/диалога.** Не использовать общий `Да`. Рекомендуемый безопасный
вариант: человек сам вводит `Спека принята, реализуй` после показа сводки и exact
spec revision. Если UI позже получает formal approval action, это должен быть
отдельный типизированный event, а не преобразование `Да` в literal phrase.

**Изменение validator/тестов.** Evidence contract должен включать actor type,
role, source kind, source/event reference, timestamp, change ID, spec digest или
commit, summary digest и запрет `created_by: ai`. Нужны negative tests для
agent-written YAML, `Да`, скопированной фразы из prompt, другой spec revision и
неподходящей роли.

**Критерии приёмки.** Ручное создание текущего YAML больше не открывает
implementation; `Да` отклоняется; принятая фраза связана с показанной revision;
повторное использование evidence после изменения spec блокируется.

- Новый OpenSpec change: **да**, можно объединить с P0 role change.
- Предположительно затронет: spec-acceptance schema/template, validator, summary
  contract, trusted-event adapter contract и tests/fixtures.
- Human decision: **принято владельцем 2026-07-21** — generic UI `Да` не является
  literal evidence; рекомендуемый ввод literal phrase принят.

### P0. Full spec-readiness и обязательная pre-acceptance summary

**Изменение правила.** Acceptance CTA разрешается только после валидного полного
набора этапа `spec_preparation`, отсутствия blockers/placeholders/unconfirmed
assumptions и формирования revision-bound summary.

**Изменение UI/диалога.** Перед решением показать: роль и authority; change ID;
spec path и revision; краткий scope/exclusions; применимые экраны, схемы и
интеграции; acceptance criteria; открытые вопросы; результаты validator;
последствие принятия. Затем — комментарии на доработку либо literal phrase.

**Изменение validator/тестов.** На `spec_preparation` требовать `spec.md`,
`tasks.md`, `traceability.md`, `status.md`; проверять реальные scenario/criteria
links, placeholders, blockers и spec digest. Summary contract должен проверять
role, пути, ledger, checks, next action и revision.

**Критерии приёмки.** Неполный либо изменённый после summary пакет не может
получить acceptance; UI не показывает CTA до valid readiness; сохранённое
evidence указывает exact revision.

- Новый OpenSpec change: **да**, тот же P3 remediation change.
- Предположительно затронет: `PROCESS_MAP.md`, guided catalog/schema, change
  template, integrity validator, summary payload и tests.
- Human decision: **принято владельцем 2026-07-21**.

### P1. Синхронизировать GigaCode-инструкции и сертифицировать реальный диалог

**Изменение правила.** GigaCode files только ссылаются на канонический contract;
последовательность `summary -> human event -> acceptance record -> next action`
описывается одинаково во всех поверхностях.

**Изменение UI/диалога.** Добавить transcript fixtures для первого сообщения,
неизвестной роли, Analyst, spec review, literal acceptance и post-acceptance.

**Изменение validator/тестов.** Contract drift test для root rules, catalog,
read-pack, schema, template и GigaCode skill; actual GigaCode walkthrough должен
сохранять prompt/response/event evidence без приватных данных.

**Критерии приёмки.** Ни один сертификационный сценарий не создаёт approval из
AI output; реальный GigaCode-сеанс воспроизводит role gate и literal acceptance;
AI-disabled маршрут остаётся эквивалентным.

- Новый OpenSpec change: **да**, как verification section того же change.
- Предположительно затронет: `.gigacode/`, certification cases/evidence,
  package manifest, validators и tests.
- Human decision: **принято владельцем 2026-07-21**; raw UI payload всё ещё
  требуется как новое evidence, его нельзя ретроспективно выдумать.

### P1. Восстановить однозначный OpenSpec lifecycle исправления

**Изменение правила.** Исправление не должно жить только в sandbox commits или
worktree. Канонический teamSsdCli OpenSpec change обязан владеть требованиями,
design, задачами, сценариями и verification evidence.

**Изменение UI/диалога.** Не требуется.

**Изменение validator/тестов.** Roadmap/OpenSpec validator должен видеть change,
его P3 metadata и inverse row.

**Критерии приёмки.** Есть ровно один active canonical change; удалённый sandbox
package не считается текущим источником; roadmap metadata валидна.

- Новый OpenSpec change: **да**.
- Предположительно затронет: `openspec/changes/<new-change>/`,
  `docs/ROADMAP.md`, `docs/CURRENT_PROJECT_AUDIT.md`.
- Human decision: владелец принял необходимость нового change; рекомендуется
  создать новый canonical change в `teamSsdCli`, а не восстанавливать скрытый
  sandbox worktree как источник истины.

## 5. Сохранность требований об аналитике, интеграциях и UI

### Что найдено и не потеряно

- Полный обезличенный разбор корпоративного аналитического шаблона и план
  миграции: `teamSsdCli/docs/planning/ANALYTIC_TEMPLATE_STRUCTURE_AND_MIGRATION_PLAN_2026-07-06.md`.
- 38 локальных фотографий шаблона в git-ignored
  `teamSsdCli/arch-screenshots/analytic-template/`; они содержат внутренние
  сведения и не должны коммититься.
- Принятые решения `D-009` и `D-010`: Git-managed source/source+export со
  stable IDs, существующий Confluence corpus read-only, generated view set
  определялся позже.
- Архитектурные границы Jira/Confluence/Bitbucket/Jenkins и определения
  `journey.yaml` / `screens.yaml` записаны в `docs/CONTEXT.md`, `docs/README.md`,
  `docs/IMPLEMENTATION_STRATEGY.md` и `docs/ROADMAP.md`.
- `AUDIT-011` и `AUDIT-018` уже честно отмечают эти контракты как
  не реализованные.

### Что фактически отсутствует

- В `process/schemas/` нет схем `status-model`, `channel-support`, `data-model`,
  `platform-services`, `journey` и `screens`.
- В `process/templates/` нет шаблонов этих analytics artifacts.
- `templates/team-specs/analytics/` содержит только `.gitkeep`.
- Нет validator checks для conditional analytics sections, stable asset IDs,
  source/export pairs, requirement/scenario references и integration descriptors.
- Нет готового screen gallery/generated view и нет live corporate wiring.
- Фактические параметры Jira/Confluence/Bitbucket/Jenkins, MCP policy и GigaCode
  runtime остаются `unverified` до Phase 4 environment inventory.

### Что недоступно и считается потерянным для текущего аудита

Полный transcript нового чата, raw UI payload и сам change package про экраны
оплаты в текущем root песочницы не найдены. История Git по пути
`team-specs/openspec/changes/change-001` также не вернула package content.
Поэтому точные бизнес-требования к платёжным экранам, которые были переданы в
том чате, сейчас **недоступны**. Их нельзя восстанавливать по памяти или
подменять содержанием фотографий корпоративного аналитического шаблона.

## 6. Предложение по границе `framework ready`

Рекомендуемый путь — один внешний P3 vertical slice до corporate adaptation:

1. role-aware guided workflow с trusted human evidence;
2. typed analytics artifact contract и conditional matrix;
3. schemas, templates, examples и deterministic validators для status/channel/
   data/platform-services/journey/screens/integration references;
4. один обезличенный worked example от business requirement до spec review;
5. AI-disabled и GigaCode walkthrough evidence.

Live Jira/Confluence/Bitbucket/Jenkins wiring, реальные credentials и mutation
в корпоративных системах остаются P4. Generated Confluence publication и
полноценная screen gallery могут оставаться P5, но их source contracts и sample
rendering должны быть определены в P3, иначе пакет нельзя честно назвать готовым
для аналитика.

Это расширяет ранее узкий Phase 3 и требует отдельного OpenSpec change либо
двух связанных changes: (1) role/acceptance remediation; (2) analytics artifact
framework. До принятия их design и acceptance scenarios продуктовую реализацию
начинать нельзя.

## 7. Проверки и ограничения аудита

- Прочитаны корневые правила, process map/sources, GigaCode instructions,
  catalogs, read-packs, schemas, templates, validator и focused tests.
- Проверено фактическое состояние root и отдельного worktree через read-only Git
  commands с локальным `safe.directory` параметром; глобальная Git config не
  изменялась.
- Файлы и тесты песочницы не изменялись и не запускались повторно, чтобы не
  создавать cache/temp artifacts в read-only объекте аудита.
- Прохождение текущих focused tests не опровергло бы findings: один из них
  демонстрирует именно возможность самостоятельно собрать acceptance YAML и
  получить implementation action.
- Chat log, UI event payload и hidden GigaCode runtime metadata недоступны;
  соответствующие выводы помечены `unverified`.
