## 1. Общий GigaCode workflow

- [x] 1.1 Зафиксировать RED pressure evidence для старого companion-only набора.
- [x] 1.2 Добавить отдельный `.gigacode/skills/superpowers.md` с branch/scope,
  fact/assumption, plan, human-authority и verification правилами.
- [x] 1.3 Задать в `.gigacode/AGENTS.md` порядок Superpowers → SDD companion и
  связать companion с общим workflow.

## 2. Process package

- [x] 2.1 Добавить новый skill в package manifest и schema exact inventory.
- [x] 2.2 Проверить fresh bootstrap, порядок активации и managed-file conflict.
- [x] 2.3 После merge с независимо выпущенным в `main` package `0.3.7`
  присвоить объединённому payload `0.3.8` без изменения immutable
  release/certification evidence.
- [x] 2.4 При rollback удалять новый managed-файл только при совпадении с
  current package bytes; блокировать локальное изменение и сохранять
  undeclared пользовательские `.gigacode`-файлы.

## 3. Документация и evidence

- [x] 3.1 Обновить setup runbook и карту файлов.
- [x] 3.2 Записать RED/GREEN/REFACTOR pressure-аудит с остаточными границами.
- [x] 3.3 Запустить focused package, bootstrap, update и validator regressions.

## 4. Acceptance

- [ ] 4.1 Получить human review результата и остаточных ограничений.
- [ ] 4.2 После отдельного решения синхронизировать Delta Specs и архивировать
  change; реализация сама по себе не означает acceptance.
