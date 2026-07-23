# Руководство: начать с рабочей ситуации

<!-- guided-catalog-sha256: b0c39b4161324aa449d6e52809eb4b1e9f52fccf9eee5e1984c64a794d3207fb -->

Этот документ — производное руководство. Канонический маршрут находится в
`process/catalogs/guided-owner-workflow.yaml`, а операции и их границы — в
`process/catalogs/operations.yaml`. Никакая команда не заменяет решение человека.

## Выберите ситуацию

| Ситуация | Что подготовить | Следующий безопасный шаг | Решение человека |
| --- | --- | --- | --- |
| Новое требование | Класс `minor`, `major` или `hotfix` | `sdd guide new-requirement --role <role> --fact classification=<class>` | Tech Lead подтверждает классификацию. |
| Уже есть change | ID change и lifecycle state | `sdd guide existing-change --role <role> --fact change_id=<id> --fact lifecycle_state=<state>` | Analyst выбирает применимый gate. |
| Срочный инцидент | Ссылка на incident evidence | `sdd guide urgent-incident --role "Tech Lead" --fact incident_ref=<path>` | Tech Lead подтверждает право на hotfix; срочность не отменяет safety gates. |
| Операция заблокирована | Ссылка на failed-run evidence | `sdd guide blocked-operation --role "Tech Lead" --fact failed_run_ref=<path>` | Tech Lead фиксирует hold или resume. |

## Границы

`sdd check`, `sdd prepare` и `sdd request` требуют явно переданную разрешённую роль.
`sdd run` остаётся fail-closed в P3: локальные, release и внешние мутации не
исполняются. Для недоступного AI или интеграции используйте `manual-fallback`.

Проверка производного руководства: `python scripts/validate_guided_owner_workflow.py --json`.
