# Tech Lead: подтвердить границы и остановку

Канонический источник: [classification runbook](../../runbooks/CLASSIFICATION_AND_MIGRATION.md).

Цель — подтвердить класс, риски и hold/resume. Начните с `sdd start urgent-incident --role "Tech Lead" --fact incident_ref=<path>` или `sdd next --change <путь> --role "Tech Lead"`. Результат — маршрут без внешней мутации; hotfix не отменяет safety gates. При неполных данных зафиксируйте hold.
