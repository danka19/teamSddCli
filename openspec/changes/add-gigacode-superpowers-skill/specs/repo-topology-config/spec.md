## ADDED Requirements

### Requirement: Bootstrap устанавливает полный GigaCode workflow

Версионированный process package SHALL объявлять и устанавливать как managed
files точный GigaCode-набор: `.gigacode/AGENTS.md`,
`.gigacode/skills/superpowers.md` и
`.gigacode/skills/sdd-process-companion.md`. Update SHALL fail closed с точным
путём, если любой declared managed file локально изменён, и SHALL NOT
перезаписывать остальные пользовательские `.gigacode`-файлы.

#### Scenario: Fresh bootstrap устанавливает оба skill

- **WHEN** оператор выполняет подтверждённый bootstrap из валидного process package
- **THEN** workspace получает exact declared GigaCode inventory, а AGENTS задаёт порядок Superpowers → SDD companion

#### Scenario: Локально изменённый Superpowers не перезаписывается

- **WHEN** `.gigacode/skills/superpowers.md` отличается от установленной package-версии перед update
- **THEN** update блокируется с `gigacode-managed-file-conflict`, называет этот путь и не меняет workspace
