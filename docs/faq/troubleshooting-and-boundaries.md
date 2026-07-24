# Сбои, приватность, поддержка и границы релиза

Канонический источник: [corporate controls](../runbooks/CORPORATE_FLOW_CONTROLS.md),
[process setup](../runbooks/PROCESS_PACKAGE_SETUP.md) и
[implementation strategy](../IMPLEMENTATION_STRATEGY.md).

Общая карта public, specialist/manual и external/corporate слоёв находится в
[self-service entrypoint](self-service-entrypoint.md).

<!-- faq-question: failure-escalation -->

## Быстрый troubleshooting

| Симптом | Что это обычно означает | Что делать |
| --- | --- | --- |
| `sdd` не найден | Не активировано окружение или package не установлен туда, откуда запускается shell | Проверить `python -m pip show sdd-process`, активировать venv, повторить [installation](installation.md) |
| `confirmation-required` | Setup получил path, но человек ещё не подтвердил локальное создание | Проверить path и только человеку повторить с `--confirm` |
| `destination-not-empty` | Setup защищает существующие файлы | Не очищать автоматически; выбрать новый пустой destination |
| `input-invalid` | Package/template/path не существует или невалиден | Сохранить JSON, проверить approved source и точный path |
| `missing-context` | Route не имеет обязательного факта | Найти fact у accountable owner либо оставить blocked |
| `invalid-role` / `unknown-role` | Роль не указана или не поддерживается | Проверить human role/registry; не выбирать другую роль ради CTA |
| `sdd next` не находит change | Неверный path либо отсутствует `change.yaml`/state | Получить exact change path у владельца процесса |
| `missing-change-status` на real schema-v2 change | Отсутствует, пусто или некорректно прочитано обязательное top-level поле `status` | Не добавлять `lifecycle_state` вручную; сохранить failed-run и восстановить/эскалировать канонический status по specialist lifecycle runbook |
| Candidate `minor` блокируется | Не доказано low impact либо есть material/unknown trigger | Передать classification evidence Tech Lead; не ослаблять criteria |
| `confirmation-contract-pending` | Mutation намеренно не включена в текущую версию | Использовать documented specialist/manual route либо остановиться |
| Test/validator failed | Реальный failed-run | Сохранить input/output, исправить в scope, повтор записать отдельно |
| AI/model недоступен | Convenience layer отсутствует | Использовать тот же deterministic/manual route |
| Integration недоступна | External state нельзя подтвердить | Оставить external state unknown, записать unavailable surface |
| `gigacode-managed-file-conflict` | Локально изменённый managed-файл расходится с установленной package-версией | Не перезаписывать и не удалять файл; сохранить diagnostic и решить, нужно ли перенести локальную правку в канонический package |
| GigaCode setup/update сообщает о небезопасном пути | Один из каталогов `.gigacode` оказался symlink/junction, reparse point или не-directory | Остановиться, проверить реальный target с владельцем workspace и не разрешать write/delete через перенаправленный путь |

## Как сохранить и эскалировать failure

1. Не повторяйте команду до сохранения первого output.
2. Запишите exact command, package/change/revision identity и безопасный result.
3. Поместите evidence в разрешённый change/evidence location.
4. Запустите:

   ```text
   sdd start blocked-operation --role <role> --fact failed_run_ref=<safe-evidence-path> --json
   ```

5. Передайте owner’у `status`, blocker code, missing facts, failed-run path и
   уже выполненные проверки.
6. Повторный success храните рядом, не вместо failure.

Tech Lead может записать hold/resume decision в своей зоне. Эскалация не
разрешает обойти gate.

<!-- faq-question: privacy -->

## Приватность

Не добавляйте в Git, command arguments или AI request:

- passwords, tokens, private keys и production credentials;
- реальные corporate exports и tracker/Confluence dumps;
- private chat/model raw output без разрешённого evidence process;
- персональные данные и внутренние URL, если они не нужны и не разрешены;
- реальные owner/project values в synthetic walkthrough.

Используйте placeholders и safe synthetic paths. Secrets хранятся только в
локальном игнорируемом storage, принятом командой. Перед отправкой support
проверьте output на secret/private content.

Если credential уже попал в commit, PR, log или shared artifact, простого
удаления из текущего файла недостаточно. Немедленно остановите распространение,
сообщите security/credential owner, отзовите или ротируйте credential и
следуйте принятой incident/history policy. Не переписывайте shared Git history
самостоятельно без согласованного remediation plan.

<!-- faq-question: release-boundary -->

## Почему successful command не означает release

`sdd check` проверяет contract. `sdd prepare` создаёт локальный preparation
result. `sdd request` создаёт неавторитетный intent. Сейчас `sdd run` остаётся
fail-closed.

Отдельными человеческими/системными фактами остаются:

- implementation complete;
- DoD;
- release/transfer readiness;
- merge;
- OpenSpec archive;
- deployment;
- customer acceptance;
- tracker Done.

Ни один из них не выводится автоматически из другого.

<!-- faq-question: corporate-pilot -->

## Корпоративный pilot

Pilot ещё не является текущей функцией FAQ или local walkthrough. Реальные
Jira/Confluence/Bitbucket/Jenkins values, credentials, wiring и mutation
принадлежат последующей контролируемой адаптации. Текущий внешний этап использует только local,
synthetic и MCP-free evidence.

<!-- faq-question: updates-support -->

## Обновление package

Не заменяйте `process/` копированием поверх установленной версии. Controlled
update обязан проверить from/to version, compatibility evidence, backup и
rollback proof. Используйте
[packaged governed flow](../runbooks/PACKAGED_GOVERNED_FLOW.md) и
[transfer runbook](../runbooks/TRANSFER_RELEASE_CANDIDATE.md).

Для package-managed GigaCode-набора действуют дополнительные гарантии:

- update блокируется, если локально изменённый managed-файл нельзя безопасно
  сопоставить с установленной версией;
- rollback удаляет новый managed-файл только при точном совпадении его
  содержимого с текущим package;
- произвольные пользовательские файлы внутри `.gigacode` сохраняются;
- bootstrap, update и rollback не читают, не записывают и не удаляют данные
  через symlink/junction или другой redirected ancestor.

При блокировке не удаляйте `.gigacode` целиком. Сохраните exact path и
diagnostic, сравните локальную правку с каноническим package и выберите
осознанно: перенести правку в package, вернуть managed-файл к package-версии
или оставить workspace на текущей версии.

## Что приложить к запросу поддержки

- роль и безопасный change ID/path;
- `sdd --version --json`;
- exact command без secrets;
- JSON/human output и exit class;
- expected versus actual;
- failed-run evidence path;
- какие sources/checks уже просмотрены;
- какие факты неизвестны;
- требуется ли hold, owner decision или package/config support.

Не пишите просто «не работает»: без identity и output нельзя отличить missing
context от package mismatch или intentional fail-closed boundary.
