# Tech Lead: классификация, границы и остановка

Канонический источник: [classification runbook](../../runbooks/CLASSIFICATION_AND_MIGRATION.md),
[Tech Lead governance](../../runbooks/TECH_LEAD_GOVERNANCE.md) и
[bounded Tech Lead instruction](../../../process/roles/tech-lead.md).

## Когда использовать

Откройте runbook для classification, technical risk/scope review, проверки
owner/dependency, hold/escalate/resume, engineering completion или release
recommendation. Tech Lead получает deterministic decision support, но решение
фиксирует человек.

## Что нужно до начала

- роль подтверждена registry как `Tech Lead`;
- есть source requirement/change ID и актуальная revision;
- доступны proposed classification и её evidence;
- известны affected systems/paths, risks, dependencies и owners;
- для existing change есть current lifecycle/gate evidence;
- для incident существует безопасная ссылка на incident evidence.

Не оценивайте change по пересказу AI без source IDs/digests.

## Пошаговый маршрут

1. Для обычного existing change получите продолжение:

   ```text
   sdd next --change <path-to-change> --role "Tech Lead" --json
   ```

   На real schema-v2 change `sdd next` читает канонический top-level `status`.
   Не добавляйте compatibility field `lifecycle_state` вручную и не меняйте
   lifecycle: missing или unsupported status остаётся fail-closed blocker для
   specialist governance/lifecycle runbooks.
2. Сверьте class с canonical classification report. Не сохраняйте policy
   thresholds в этой странице как самостоятельное правило.
3. Проверьте scope, architecture disposition, dependencies, owner coverage,
   DoR/DoD evidence, waivers/deferrals и активные controls.
4. Для срочного incident начните отдельный маршрут:

   ```text
   sdd start urgent-incident --role "Tech Lead" --fact incident_ref=<safe-evidence-path> --json
   ```

5. Убедитесь, что urgency не скрыла regression, minimum verification,
   rollback/hold и reconciliation.
6. При блокере зафиксируйте human-authored `stop | hold | escalate` record.
7. `resume` рассматривайте только против всех active controls и после
   source-linked corrective evidence.
8. Передайте role-specific действия и остановитесь; не исполняйте решения
   других владельцев.

## Ожидаемый результат

- source-linked findings и рекомендации;
- подтверждённый человеком class либо явный hold;
- список blockers, owners и required evidence;
- snapshot/version/date согласованы;
- independent QA/product/security/release decisions остаются отдельными;
- ни lifecycle, ни external system не изменены output’ом review.

## Доказательства

Сохраните classification/gate reports, source IDs/hashes, affected scope,
dependency/owner resolution, control records, фактические commands/results,
waiver/deferral references, risks и human decision record. Не заменяйте
decision evidence строкой «Tech Lead согласен» без trusted source.

## Решения и границы

Tech Lead отвечает за техническую classification/governance и human control
decision в разрешённой зоне. Он не заменяет QA, product, security, release,
merge, archive или tracker authority.

AI не может за Tech Lead подтвердить class, DoR/DoD, waiver, residual risk,
release readiness или resume. Positive recommendation не равна approval.

## Передача работы

- Analyst получает classification decision, scope corrections и open questions.
- Developer получает bounded implementation scope только после DoR.
- QA получает class-specific risk/scenario/evidence expectations.
- Release/archive owners получают recommendation и evidence, но принимают
  собственные решения.

## Сбои, fallback и эскалация

- mixed/stale snapshot — hold и повторный сбор evidence;
- unknown material impact — не `minor`; остановиться до выяснения;
- owner отсутствует — escalation владельцу процесса;
- timestamp/source digest conflict — заблокировать decision support;
- failed control/check — сохранить failed-run, не маскировать повтором;
- AI unavailable — выполнить deterministic Tech Lead runbook вручную.

## Работа с AI

```text
Ты готовишь decision-support для человека Tech Lead. Используй только
перечисленные canonical IDs и actual reports. Покажи class/risk/scope gaps,
owners и stop conditions. Не подтверждай classification, DoR/DoD, waiver,
resume, release или archive. Заверши списком человеческих решений.
```

Если AI запускает `sdd ... --json`, он возвращает raw result и объяснение
отдельно. Он не исполняет `next_command` автоматически.

## Чек-лист завершения

- [ ] Role/owner authority подтверждены.
- [ ] Sources, revision и snapshot совпадают.
- [ ] Classification основана на evidence.
- [ ] Scope, risk, dependencies и owners проверены.
- [ ] Active blockers/controls не скрыты.
- [ ] Human decision записан отдельно от AI recommendation.
- [ ] Independent approvals сохранены.
- [ ] Handoff выполнен, lifecycle/external systems не изменены выводом.
