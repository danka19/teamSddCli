# Работа с AI: практический и безопасный маршрут

Канонический источник: [guided dispatcher](../../openspec/specs/guided-operation-dispatcher/spec.md),
[role-aware workflow](../../openspec/specs/role-aware-guided-workflow/spec.md),
[guided runbook](../runbooks/GUIDED_OWNER_WORKFLOW.md) и
[bounded role instructions](../../process/roles/).

AI здесь — интерфейс к контексту и локальным инструментам, а не владелец
процесса. Сначала человек задаёт роль, задачу, sources, разрешённые действия и
stop point. Затем выбирает discovery либо guided режим.

Если нужен не отдельный prompt, а полный реальный пример, начните со
[сквозного первого `minor` change вместе с AI](first-change-with-ai.md), а
после него повторите [тот же маршрут без AI](first-change-without-ai.md).

<!-- faq-question: ai-analyst-discovery -->

## Режим `analyst-discovery`: от сырой идеи к черновику

Для нового требования не нужен длинный prompt. Начните простой фразой:

```text
Роль человека: Analyst.
Помоги разобраться и оформить новую идею.
Сначала покажи темы, которые нужно уточнить, а после моего разрешения задавай
по одному вопросу. До подтверждения итоговой сводки не создавай файлы.
```

AI сначала покажет темы интервью: проблему и пользу, пользователя, текущее и
ожидаемое поведение, сценарии, scope, ограничения и приёмку. После разрешения
он задаёт по одному вопросу и сверяет понимание после каждого смыслового блока.

В evidence-сводке утверждения разделяются:

| Статус | Что означает |
| --- | --- |
| `confirmed` | Человек подтвердил факт или он доказан canonical source |
| `proposed` | AI предлагает формулировку для review |
| `unknown` | Факта пока нет; указан владелец вопроса и влияние пробела |
| `conflict` | Ответы или sources противоречат друг другу |

После интервью AI показывает итоговую сводку. Только после её подтверждения он
может предложить черновики `proposal.md`, Delta Spec, optional `design.md`,
preliminary `tasks.md` и вопросы владельцам решений. Создание файлов требует
отдельного согласия. Переход к `guided-change` и просьба «показать первую команду»
— ещё одно отдельное решение; оно не подтверждает classification, DoR или
реализацию.

<!-- faq-question: ai-permissions -->

## Перед началом сессии

Передайте AI только bounded context:

- человеческая роль (`Analyst`, `Tech Lead`, `Developer` или `QA`);
- один change/task/stage;
- canonical source IDs и paths;
- разрешённые read/write paths;
- allowed command class: guidance, read-only либо prepare;
- expected evidence/output;
- human decisions и stop point;
- unavailable surfaces и privacy exclusions.

Не передавайте tokens, credentials, corporate exports, production data,
private chat dumps и неизвестные файлы «на всякий случай».

## Настроить AI-клиент

У разных AI-инструментов разные форматы permissions и project instructions,
поэтому одного универсального конфигурационного файла нет. Общая безопасная
настройка выглядит так:

1. Откройте AI в корне конкретного project/workspace, а не во всём домашнем
   каталоге.
2. Передайте ему `AGENTS.md` команды или package-managed role instruction,
   затем bounded read pack для одной задачи.
3. Разрешите чтение только нужных sources и запись только в declared scope.
4. Для shell включите human approval и allowlist для `sdd --version`,
   `sdd start`, `sdd next`, `sdd op`, `sdd check`, `sdd prepare` и
   `sdd request`. `sdd run` и external tools оставьте запрещёнными.
5. Попросите AI всегда использовать `--json`, показывать exact command и raw
   result, а `next_command` не запускать автоматически.
6. Проверьте сначала guidance-only пример, затем одну read-only command.
7. Если конкретный client использует packaged adapter, выберите только adapter,
   соответствующий этому client/model family; adapter не меняет policy.

Package содержит tool-agnostic role instructions и thin adapters. Реальные
permissions, executable path и корпоративные restrictions проверяются
владельцем среды, а не угадываются из FAQ.

## Режим 1: AI только объясняет

AI читает разрешённый контекст и объясняет следующий canonical route, но не
запускает команду и не представляет состояние изменённым.

Пример:

```text
Роль человека: Analyst.
Задача: понять следующий шаг для нового minor-кандидата.
Canonical sources: <paths/IDs>.
AI не запускает команды и ничего не изменяет.
Раздели known facts, assumptions и missing facts. Объясни подходящий sdd route,
expected evidence, human decision и stop point. Отметь результат как guidance.
```

Ожидаемый ответ содержит:

- какие sources прочитаны;
- применимую команду, но не fabricated result;
- недостающие факты;
- evidence;
- человеческое решение;
- явно написанное «команда не запускалась».

## Режим 2: AI запускает разрешённую команду

Человек разрешает одну конкретную локальную команду с `--json`. AI возвращает
raw structured result и отдельно объясняет его. Он не запускает
`next_command` автоматически.

Пример:

```text
Роль человека: Developer.
Разрешено выполнить только:
sdd next --change C:/work/team-specs/openspec/changes/sample-001 --role Developer --json

Верни exact command, exit/result и raw JSON. Затем объясни status,
missing_facts, next_command, expected_evidence и authority_boundary.
Не выполняй next_command. Не меняй lifecycle и не заявляй approval.
```

Schema-v2 хранит lifecycle в top-level `status`; `sdd next` читает именно это
поле и передаёт значение во внутренний guided fact. AI не должен добавлять
второе persisted-поле `lifecycle_state`, менять `status`, выполнять
`next_command` или заявлять approval.

Для нового requirement:

```text
sdd start new-requirement --role Analyst --fact classification=minor --json
```

`classification=minor` в команде — известный вход candidate route, а не
доказательство human confirmation.

## Как читать JSON

| Поле | Что означает | Чего не означает |
| --- | --- | --- |
| `status` | Результат конкретной команды | Business acceptance или общий успех change |
| `missing_facts` | Какие inputs нельзя угадать | Разрешение AI заполнить их |
| `next_command` | Каноническое продолжение для review | Автоматическое разрешение исполнить |
| `expected_evidence` | Что нужно подготовить/сохранить | Что evidence уже существует |
| `human_decision` | Кто должен решить и последствия | Что решение уже принято |
| `authority_boundary` | Где маршрут обязан остановиться | Необязательная рекомендация |
| `lifecycle_mutated` | Выполнила ли команда lifecycle mutation | Полный аудит всех внешних систем |
| `external_state_mutated` | Выполнила ли команда external mutation | Release/deployment/customer acceptance |

## Permission matrix

| Ситуация | Разрешено AI | Обязательно человеку |
| --- | --- | --- |
| Понять следующий шаг | Guidance либо явно разрешённый `sdd ... --json` | Проверить sources и выбрать действие |
| Подготовить локальный draft | Один bounded stage с source references | Проверить содержание и принять/отклонить |
| Запустить read-only check | Exact command и raw result | Интерпретировать влияние и решить follow-up |
| Подготовить operation | `sdd prepare ... --json` при явном разрешении | Review результата и дальнейшее решение |
| Настроить workspace | Подсказать `sdd setup` без подтверждения | Выбрать path и лично добавить `--confirm` |
| Неизвестный факт | Сообщить missing/blocked | Найти факт или назначить owner |

<!-- faq-question: ai-prohibitions -->

## Что AI запрещено

AI не должен:

- создавать себе полномочия или выбирать более сильную роль;
- подставлять `--confirm` вместо человека;
- подтверждать classification, DoR/DoD, waiver, risk, release или archive;
- выдумывать facts, paths, source IDs, approvals или test results;
- считать `request` авторизацией либо `prepare` выполненной mutation;
- выполнять `sdd run` в обход fail-closed boundary;
- мутировать Jira, Confluence, Bitbucket, Jenkins или production;
- скрывать failed-run после успешного retry;
- заявлять passed для непроведённой проверки.

## Готовые prompts по ролям

### Analyst

```text
Подготовь один requirement/Delta draft. Отдели facts от assumptions, покажи
open decisions и scenarios. Не подтверждай classification/DoR и остановись для
human review.
```

### Tech Lead

```text
Собери source-linked decision support по class, risk, scope, dependencies и
controls. Не принимай human decision, не resume hold и не заменяй QA/release.
```

### Developer

```text
Работай только в <write scope> по <REQ/SCEN/TASK IDs>. Выполни согласованные
checks и покажи actual results. Не расширяй scope и остановись для review/QA.
```

### QA

```text
Свяжи positive/negative/regression cases со scenario IDs. Раздели proposed,
executed и unavailable. Не выдумывай actual и не отмечай DoD/release/archive.
```

Подробные варианты находятся на [страницах ролей](roles/index.md).

## Если AI не уверен

Правильный результат — `blocked` или список missing facts. AI должен привести
source conflict/отсутствие инструмента, не выбирать silent default и направить
к accountable owner или manual fallback.

## Продолжение без AI

1. Запустите ту же документированную `sdd` команду вручную.
2. Сохраните human-readable output либо `--json`.
3. Прочитайте canonical runbook для returned operation.
4. Зафиксируйте unavailable surface и evidence.
5. Передайте результат human owner.

Отключение AI не отменяет ни один gate. Детали сбоев находятся в
[troubleshooting](troubleshooting-and-boundaries.md). Для прямого сравнения
пройдите [manual-версию первого change](first-change-without-ai.md).
