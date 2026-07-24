# Self-service entrypoint и обязательный GigaCode Superpowers skill

Дата: 2026-07-24
Статус: согласовано владельцем продукта
Ветка: `feature/self-service-gigacode-superpowers`

## Задача

Сделать начало работы с `teamSddCli` заметным и понятным без чтения большого
`docs/README.md`, точно объяснить границу полного SDD-цикла и обязательно
поставлять общий Superpowers workflow skill в GigaCode workspace.

Повторённые пункты про self-service entrypoint считаются одним требованием.

## Текущее состояние

- Отдельной FAQ-страницы про public self-service entrypoint нет.
- Краткое описание `sdd` находится внутри большого `docs/README.md`.
- FAQ объясняет ограничения в нескольких местах, но формулировка
  «полный цикл недоступен» не разделяет public CLI, specialist/manual шаги,
  решения людей и внешние интеграции.
- Bootstrap устанавливает в `.gigacode/` только `AGENTS.md` и
  `skills/sdd-process-companion.md`.
- Общий способ работы GigaCode над проектом не отделён от SDD companion.

## Решение

### 1. Отдельный self-service entrypoint

Создать `docs/faq/self-service-entrypoint.md`. Страница должна отвечать на пять
вопросов:

1. Что такое public `sdd`.
2. Как установить пакет и проверить версию.
3. Как создать workspace и начать или продолжить работу.
4. Какие команды выполняют действие, а какие только проверяют, подготавливают
   или запрашивают подтверждение.
5. Где продолжить чтение: установка, topology, первый `minor` change, роли,
   AI и troubleshooting.

Сразу после заголовка `docs/README.md` появится ссылка на эту страницу. В FAQ
ссылка войдёт в маршрут первого знакомства и в связанные страницы установки и
настройки.

`docs/README.md` останется архитектурным обзором, но его первый экран будет
короче и понятнее: назначение продукта, текущий практический результат,
self-service ссылка и ссылки на канонические источники. Подробная инструкция
по командам будет удалена из README, чтобы не существовало двух копий.

### 2. Точное объяснение полного цикла

Пользовательская документация не должна говорить, что полный управляемый
SDD-процесс в принципе невозможен. Корректная модель состоит из трёх слоёв:

| Слой | Что доступно сейчас |
| --- | --- |
| Public `sdd` | Установка, `setup`, выбор ситуации, `start`, `next`, каталог, read-only checks, подготовка и non-authoritative request |
| Specialist/manual | Некоторые команды создания и lifecycle, фиксация evidence и явные решения ответственных ролей |
| External/corporate | Реальные Jira, Confluence, Bitbucket, Jenkins, deployment, customer acceptance и tracker Done |

Полный управляемый маршрут пройти можно, но public `sdd` пока не выполняет его
автоматически от требования до внешней поставки. `sdd run` остаётся
fail-closed; classification, acceptance, DoR/DoD, risk, waiver, merge, release
и archive не становятся решениями AI или CLI. Внешние mutations относятся к
контролируемой corporate adaptation.

Эта граница будет объяснена на self-service странице и связана ссылками с
`first-change.md` и `troubleshooting-and-boundaries.md`. Каноническое
поведение останется в OpenSpec; FAQ будет человекочитаемым представлением.

### 3. Отдельный обязательный GigaCode Superpowers skill

Создать `process/gigacode/skills/superpowers.md`. Это короткий
tool-agnostic workflow skill для GigaCode, а не копия runtime-specific
глобальных Codex skills.

Skill должен требовать:

1. До ответа или действия определить применимые skills и обязательные
   инструкции проекта.
2. Прочитать минимальный достаточный canonical context.
3. Отделить факты от предположений и назвать отсутствующее evidence.
4. Для изменения согласовать результат и короткий план.
5. Перед изменением определить проверку, затем работать небольшими
   проверяемыми шагами.
6. Не объявлять command, test, approval или lifecycle result без фактического
   evidence.
7. Остановиться перед решениями человека и запрещёнными внешними действиями.
8. После изменения выполнить проверки и дать понятный итог и следующий шаг.

`process/gigacode/AGENTS.md` будет требовать сначала применить
`.gigacode/skills/superpowers.md`, а для SDD-задачи затем
`.gigacode/skills/sdd-process-companion.md`. Companion получит короткую ссылку
на этот порядок, но не будет дублировать общий workflow.

### 4. Поставка и версия

Новый skill войдёт в:

- `process/package.yaml`;
- exact file-list contract в
  `process/schemas/process-package.schema.json`;
- bootstrap/update managed-file contract;
- package setup runbook.

Версия process package изменится с `0.3.6` на `0.3.7`. Все связанные version
pins и тестовые ожидания будут обновлены одним изменением.

Fresh-bootstrap тест должен доказать, что установленный `.gigacode` inventory
точно совпадает с manifest и содержит оба skills. Отдельный тест проверит
обязательный порядок `superpowers -> sdd-process-companion`.

## OpenSpec и phase intake

Типы обратной связи:

- `documentation_change`;
- `scope_refinement`;
- `new_feature` для поставляемого GigaCode skill;
- `verification_change` для exact inventory test.

Routing decision: `create_openspec_change`.

Причина: FAQ остаётся производной документацией, но новый обязательный
поставляемый skill изменяет process package contract и acceptance criteria.
По ранее разрешённому порядку сначала будет подготовлена рабочая реализация,
после чего в той же ветке появится отдельный OpenSpec change, описывающий
GigaCode Superpowers contract задним числом до итоговой верификации.

Primary roadmap owner — Phase 3, потому что skill относится к внешнему
self-service guided-operation слою до corporate adaptation. Roadmap inverse
tables должны получить одну primary ownership row для нового active change.

## Проверка

Минимальное доказательство результата:

- FAQ validator принимает новую страницу и ссылки;
- Markdown-ссылки на новую страницу существуют и разрешаются;
- package schema принимает новый exact GigaCode file list;
- fresh bootstrap устанавливает оба skills и только declared managed files;
- update сохраняет conflict protection для локально изменённых managed files;
- targeted self-service/package tests проходят;
- native OpenSpec strict validation проходит;
- roadmap/OpenSpec validator не возвращает ошибок;
- `git diff --check` проходит.

Полный suite будет повторно запущен с подходящим временем. Если среда снова
оборвёт его по таймауту, итоговый отчёт отделит targeted passing evidence от
неполного full-suite evidence.

## Не входит в изменение

- Включение `sdd run` mutations.
- Автоматические approvals, merge, release или archive.
- Реальные Jira/Confluence/Bitbucket/Jenkins операции.
- Установка глобального Codex Superpowers plugin в корпоративной среде.
- Изменение ролевых полномочий или lifecycle.
