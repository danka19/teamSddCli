# Первый `minor` change: сквозной учебный маршрут

Канонический источник: [guided workflow](../runbooks/GUIDED_OWNER_WORKFLOW.md),
[packaged governed flow](../runbooks/PACKAGED_GOVERNED_FLOW.md),
[classification runbook](../runbooks/CLASSIFICATION_AND_MIGRATION.md),
[AI authority contract](../../openspec/specs/role-aware-guided-workflow/spec.md)
и [accepted dispatcher contract](../../openspec/specs/guided-operation-dispatcher/spec.md).

Если вы ещё не устанавливали CLI и не создавали workspace, сначала откройте
[self-service entrypoint](self-service-entrypoint.md).

Здесь один и тот же synthetic change пройден двумя способами. Сначала человек
работает в паре с AI: AI собирает признаки, предлагает candidate class,
показывает и запускает разрешённые команды, объясняет JSON и останавливается за
человеческим подтверждением. Затем человек повторяет маршрут без AI.

Такой порядок показывает не два разных процесса, а два интерфейса к одним
правилам, evidence и stop points.

## До двух проходов

Человек готовит две отдельные disposable practice-копии одного и того же
revision:

- clean checkout `C:/work/teamSddCli-ai` и пустой workspace
  `C:/work/faq-walkthrough-ai`;
- clean checkout `C:/work/teamSddCli-manual` и пустой workspace
  `C:/work/faq-walkthrough-manual`.

Не выполняйте оба прохода в одном checkout или workspace: после первого rename
исходного `lines` уже не будет, а повторное создание того же change ID
завершится `destination-exists`. Две копии позволяют действительно повторить
один и тот же change от одинакового baseline.

## Учебная задача

В `process/operation_dispatcher.py::_render_human` переименовать только
локальный список `lines` в `output_lines` без изменения runtime-поведения,
текста вывода или public contract.

В обоих проходах нужно подтвердить evidence:

- изменение затрагивает одну функцию и одно локальное имя;
- public API, данные, безопасность, compliance и внешние интеграции не меняются;
- user scenario, governed documentation/tests, component interaction,
  cross-repository, архитектурного и широкого regression impact нет;
- существующий test
  `test_start_human_renderer_uses_the_same_next_command` подтверждает
  неизменность human-readable continuation;
- rollback — обычный revert локального изменения.

После проверки эти facts позволяют AI или человеку предложить `minor` как
candidate class. Они не подтверждают класс автоматически: окончательное
решение принимает и фиксирует Tech Lead.

## Проход 1 — вместе с AI

Откройте [пошаговый маршрут с AI](first-change-with-ai.md). В нём есть готовый
стартовый prompt, пример диалога, точные команды, ожидаемые JSON-поля и все
моменты, когда AI обязан запросить действие или решение человека.

AI выполняет только явно разрешённые локальные команды. Он не подставляет
`--confirm`, не выполняет `next_command` автоматически, не создаёт себе роль и
не выдаёт candidate `minor` за подтверждённую классификацию.

## Проход 2 — без AI

После AI-маршрута повторите [тот же change вручную](first-change-without-ai.md).
Команды, evidence, роли и границы те же; вместо объяснения AI человек сам
читает structured result и выбирает следующий шаг.

## Что сравнить после двух проходов

| Контрольная точка | Вместе с AI | Без AI |
| --- | --- | --- |
| Предложение класса | AI связывает факты с candidate `minor` | Analyst/Tech Lead делают это сами |
| Запуск команды | AI показывает exact command и ждёт разрешение | Человек запускает exact command |
| Чтение результата | AI объясняет raw JSON отдельно от выводов | Человек проверяет те же поля |
| Подтверждение | AI формулирует вопрос и останавливается | Человек сверяется с runbook и решает |
| Неизвестный факт | AI показывает blocker и не угадывает | Человек фиксирует blocker и owner |
| Mutation/external action | AI останавливается у запретной границы | Человек переходит в specialist route |

## Где заканчивается текущий публичный CLI

Маршрут честно останавливается перед выполнением mutation через `sdd run`,
external operations и human-owned decisions. `sdd request` создаёт только
неавторитетный запрос, а `sdd prepare` — локальную подготовку. Полностью
автоматический путь от требования до созданного, одобренного и архивированного
change пока недоступен; актуальный статус есть в [roadmap](roadmap.md).

Дальше откройте [runbook своей роли](roles/index.md),
[ежедневный lifecycle](daily-workflow.md) или
[troubleshooting](troubleshooting-and-boundaries.md).
