# Self-service: начать работу через `sdd`

Канонический источник:
[self-service operator onboarding](../../openspec/changes/add-self-service-operator-onboarding/specs/self-service-operator-onboarding/spec.md),
[guided dispatcher](../../openspec/specs/guided-operation-dispatcher/spec.md) и
[operation catalog](../../openspec/specs/operation-catalog/spec.md).

Эта страница — короткая точка входа. Она помогает установить `sdd`, понять
первую команду и заранее увидеть, где public CLI передаёт работу specialist
инструменту, другой роли или внешней системе.

## Что такое public `sdd`

Public `sdd` — установленная локальная команда поверх versioned process
package. Человеку не нужно искать имя Python-скрипта, чтобы проверить пакет,
создать пустое рабочее пространство, начать новую ситуацию или получить один
следующий разрешённый шаг для существующего change.

Команда не является автономным руководителем процесса. Она показывает факты,
missing context, ответственную роль, ожидаемое evidence, human boundary,
fallback и следующий вызов, но не принимает решения за команду.

## Быстрый старт

1. Установите пакет из доверенного checkout или утверждённого package source:

   ```text
   python -m pip install .
   ```

2. Проверьте фактически установленную версию:

   ```text
   sdd --version --json
   ```

3. Для новой команды сначала выполните setup без подтверждения и изучите
   preflight. После проверки пустого destination человек повторяет команду с
   `--confirm`:

   ```text
   sdd setup C:/work/my-team
   sdd setup C:/work/my-team --confirm --json
   ```

4. Начните новую рабочую ситуацию:

   ```text
   sdd start new-requirement --role Analyst --json
   ```

5. Для существующего change запросите ровно один следующий шаг:

   ```text
   sdd next --change C:/work/my-team/team-specs/openspec/changes/example --role Developer --json
   ```

Подробности установки находятся в [инструкции по установке](installation.md),
а структура workspace — в [setup и topology](setup-and-topology.md).

## Что public `sdd` делает сам

| Команда | Результат | Чего она не делает |
| --- | --- | --- |
| `sdd --version` | Показывает identity установленного package | Не доказывает совместимость конкретного workspace |
| `sdd setup` | Проверяет destination; с `--confirm` создаёт только локальный workspace | Не подключает корпоративные системы |
| `sdd start` | Выбирает маршрут по ситуации и фактам | Не создаёт change неявно |
| `sdd next` | Возвращает один следующий разрешённый шаг | Не меняет lifecycle |
| `sdd op` | Показывает каталог и границу операции | Не выдаёт полномочия роли |
| `sdd check` | Запускает разрешённую read-only проверку | Не подтверждает classification, DoR или DoD |
| `sdd prepare` | Готовит локальный результат для review | Не публикует, не делает commit или merge |
| `sdd request` | Создаёт non-authoritative запрос операции | Не является trusted human confirmation |

JSON и human-readable выводы строятся из одного continuation result. Успешный
exit означает только успешное выполнение названной операции, а не автоматическое
принятие следующего решения.

## Из каких частей состоит полный цикл

Полный управляемый маршрут пройти можно. Но текущий public `sdd` не выполняет
его автоматически от требования до внешней поставки.

| Слой | Что происходит |
| --- | --- |
| Public `sdd` | Установка, setup, situation-first guidance, continuation, каталог, read-only checks, preparation и non-authoritative request |
| Specialist/manual | Некоторые команды создания и lifecycle, фактическое evidence и решения ответственных ролей |
| External/corporate | Jira, Confluence, Bitbucket, Jenkins, deployment, customer acceptance и tracker Done |

На практике это означает:

- public CLI помогает не потерять следующий шаг и не перескочить границу;
- specialist runbook выполняет операцию, которой ещё нет в public mutation
  surface;
- Analyst, Tech Lead, Developer, QA, release owner и другие ответственные роли
  принимают только свои решения;
- внешняя система меняется отдельным разрешённым механизмом и только после
  настройки корпоративной среды.

Поэтому фраза «через `sdd` нельзя пройти полный цикл» неточна. Нельзя
автоматически выполнить весь цикл только public-командами `sdd`; пройти
управляемый цикл с явными specialist/manual шагами и решениями людей можно.

## Почему `sdd run` закрыт

`sdd run` остаётся fail-closed даже при подготовленном request. Это защищает от
ситуации, когда локальная строка, флаг, UI-ответ или AI-текст ошибочно
принимаются за полномочие человека.

Текущая граница намеренно не позволяет CLI или AI:

- подтвердить classification, acceptance, DoR/DoD, waiver или residual risk;
- выполнить merge, release, archive, deployment или tracker Done;
- изменить Jira, Confluence, Bitbucket или Jenkins;
- скрыть отсутствующее evidence или превратить assumption в факт.

Детальная расшифровка команд и состояний находится в
[границах и troubleshooting](troubleshooting-and-boundaries.md).

## Куда перейти дальше

- Поставить команду: [установка `sdd`](installation.md).
- Создать workspace: [setup и topology](setup-and-topology.md).
- Пройти реальный учебный маршрут:
  [первый synthetic `minor` change](first-change.md).
- Начать по ответственности: [runbooks ролей](roles/index.md).
- Работать в паре с помощником:
  [правила и примеры AI](ai-collaboration.md).
- Разобрать блокировку:
  [сбои, приватность и границы](troubleshooting-and-boundaries.md).
