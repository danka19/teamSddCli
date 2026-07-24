# Владелец процесса: установить и подготовить команду

Канонический источник: [process package setup](../../runbooks/PROCESS_PACKAGE_SETUP.md),
[transfer runbook](../../runbooks/TRANSFER_RELEASE_CANDIDATE.md) и
[self-service onboarding](../../../openspec/changes/add-self-service-operator-onboarding/specs/self-service-operator-onboarding/spec.md).

## Когда использовать

Runbook нужен человеку, который выбирает принятую package version, создаёт
central workspace, назначает owner’ов, подключает project adapters, организует
первый walkthrough и удерживает FAQ/config от drift.

## Что нужно до начала

- утверждённый package source и expected version/hash;
- Python 3.11+ и разрешённый installation channel;
- новый пустой destination;
- решение о central `team-specs` location;
- проверенные non-secret project/owner IDs;
- понимание, где хранятся local secrets вне Git;
- plan rollback/support при несовместимости.

Не используйте примеры из template как реальные corporate values.

## Пошаговый маршрут

1. Установите package по [installation guide](../installation.md).
2. Проверьте:

   ```text
   sdd --version --json
   sdd --help
   ```

3. До подтверждения выполните:

   ```text
   sdd setup <empty-workspace> --json
   ```

   Ожидается `confirmation-required` и отсутствие созданной папки.

4. Человек проверяет destination и запускает:

   ```text
   sdd setup <empty-workspace> --confirm --json
   ```

5. Проверьте созданные `process/` и `team-specs/`, package/config identity и
   `next_command`.
6. Заполните только non-secret `owners.yaml`, `projects.yaml` и documented
   config values. Прогоните deterministic config validation.
7. Подключите optional `.sdd-project.yaml` только к проверенным project paths.
8. Организуйте [первый synthetic minor walkthrough](../first-change.md) с
   Analyst, Tech Lead, Developer и QA.
9. Запишите непонятные шаги и обновите FAQ через reviewed change.

## Ожидаемый результат

- установлен ожидаемый `sdd-process`;
- central workspace создан только в выбранном пустом path;
- package/config identity совместимы;
- versioned files не содержат secrets/private exports;
- owner/project registries проверены людьми;
- project adapter указывает на один central source;
- команда прошла synthetic route и понимает stop/authority boundaries.

## Доказательства

Сохраните package version/hash, installation/version output, setup blocked и
created results, config validation, tree/inventory, owner review, adapter
validation, walkthrough notes и failed attempts. Не коммитьте raw secrets,
private model prompts или реальные credentials.

## Решения и границы

Владелец процесса выбирает package/config rollout и организует support, но не
принимает business requirement, QA, security, release или archive за
соответствующих владельцев.

`--confirm` — человеческое разрешение создать локальные файлы. Оно не
разрешает external mutation и не является универсальным approval.

## Передача работы

Analyst получает working workspace и starting route. Tech Lead получает owner,
policy/package identities и escalation route. Developer/QA получают project
mapping и evidence locations. Corporate configuration/pilot передаются только
после принятого successor package и отдельного Phase 4 gate.

## Сбои, fallback и эскалация

- destination не пуст — не очищать автоматически; выбрать новый path;
- package/config mismatch — hold, сохранить output, использовать controlled
  update/rollback;
- placeholder остался — не начинать реальную работу;
- secret найден в versioned file — удалить из Git surface и перевыпустить
  безопасный config; если secret уже был shared/committed, немедленно
  revoke/rotate его, уведомить security/owner и следовать incident/history
  policy;
- adapter указывает в другой central repo — остановить drift и исправить source;
- новый участник не понимает маршрут — FAQ не принимается как готовый и
  исправляется до повторного walkthrough.

## Работа с AI

AI может проверить checklist, объяснить output и подготовить command. Для setup:

```text
Проверь prerequisites и подготовь команду sdd setup для пути <path>.
Не добавляй --confirm. Покажи, какие локальные файлы должны появиться,
какие secrets запрещены и где человек должен остановиться.
```

Человек сам проверяет путь и добавляет `--confirm`. AI не заполняет реальные
owner/project values догадками.

## Чек-лист завершения

- [ ] Package source/version/hash проверены.
- [ ] Installation/version smoke пройден.
- [ ] Setup без confirm заблокирован без side effects.
- [ ] Confirmed setup создал только declared workspace.
- [ ] Config/owners/projects validated и без secrets.
- [ ] Project adapters указывают на central source.
- [ ] Synthetic walkthrough выполнен всеми ролями.
- [ ] Непонятные шаги и failed-runs записаны.
- [ ] Human content acceptance ещё не подменено automated test.
