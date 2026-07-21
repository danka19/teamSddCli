# Ролевая политика P3 для GigaCode

Интерактивные роли в этом проекте: `Analyst`, `Tech Lead`, `Developer`, `QA`.

`Analyst` ведёт intake и аналитические артефакты, а также может быть доверенным человеком для literal, revision-bound acceptance спецификации. Это acceptance не отменяет DoR и не даёт CTA на реализацию.

`Tech Lead` получает единственный CTA `begin-approved-implementation`, и только после valid readiness/DoR и trusted acceptance. `Developer` и `QA` не получают право на acceptance или начало реализации.

Роли, не перечисленные выше, не являются интерактивными ролями P3. Release в этом локальном vertical slice не применяется.