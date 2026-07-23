# Сбои, приватность и границы релиза

Канонический источник: [корпоративные контроли](../runbooks/CORPORATE_FLOW_CONTROLS.md) и [стратегия реализации](../IMPLEMENTATION_STRATEGY.md).

<!-- faq-question: failure-escalation -->

При блокировке сохраните вывод команды как failed-run evidence, не угадывайте недостающий факт и используйте `sdd start blocked-operation` либо manual fallback. Tech Lead фиксирует hold или resume; эскалация не разрешает обходить гейты.

<!-- faq-question: privacy -->

Не добавляйте секреты, корпоративные выгрузки, production credentials или частные контексты в репозиторий и запрос AI. Секреты остаются в локальных игнорируемых файлах. Синтетические walkthrough не являются доказательством внешней операции.

<!-- faq-question: release-boundary -->

`sdd run` в P3 остаётся fail-closed: локальные, release и внешние мутации не включаются одной командой или подтверждением. Релиз, merge, archive и принятие риска остаются за ответственным человеком и отдельными контрактами.

<!-- faq-question: corporate-pilot --><!-- faq-question: updates-support -->

Корпоративный pilot — будущая контролируемая фаза; FAQ не обещает существующую интеграцию с Jira, Confluence, Bitbucket или Jenkins. Обновление процесса проходит через OpenSpec change, проверки и human acceptance. Для помощи приложите безопасный вывод команды, роль, change ID и путь к failed-run evidence.
