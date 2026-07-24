## ADDED Requirements

### Requirement: Bootstrap устанавливает полный GigaCode workflow

Версионированный process package SHALL объявлять и устанавливать как managed
files точный GigaCode-набор: `.gigacode/AGENTS.md`,
`.gigacode/skills/superpowers.md` и
`.gigacode/skills/sdd-process-companion.md`. Update SHALL fail closed с точным
путём, если любой declared managed file локально изменён, и SHALL NOT
перезаписывать остальные пользовательские `.gigacode`-файлы. Rollback SHALL
удалять managed-файл, отсутствующий в target manifest, только если его bytes
совпадают с текущей установленной package-версией; иначе rollback SHALL fail
closed до package/config mutations. Bootstrap, update и rollback SHALL также
fail closed, если существующий ancestor declared target под `.gigacode`
является symlink/reparse point или не-directory, и SHALL NOT читать, писать или
удалять данные через такой redirected path.

#### Scenario: Fresh bootstrap устанавливает оба skill

- **WHEN** оператор выполняет подтверждённый bootstrap из валидного process package
- **THEN** workspace получает exact declared GigaCode inventory, а AGENTS задаёт порядок Superpowers → SDD companion

#### Scenario: Локально изменённый Superpowers не перезаписывается

- **WHEN** `.gigacode/skills/superpowers.md` отличается от установленной package-версии перед update
- **THEN** update блокируется с `gigacode-managed-file-conflict`, называет этот путь и не меняет workspace

#### Scenario: Rollback удаляет только неизменённый новый managed-файл

- **WHEN** rollback возвращает package к версии, где `skills/superpowers.md` ещё не объявлен
- **THEN** неизменённый package-файл удаляется, произвольные пользовательские `.gigacode`-файлы сохраняются, а локально изменённый Superpowers вместо удаления блокирует rollback с `gigacode-managed-file-conflict`

#### Scenario: Вложенный junction не перенаправляет managed operation

- **WHEN** `.gigacode/skills` является symlink или Windows reparse point во внешний каталог
- **THEN** bootstrap, update или rollback блокируется с filesystem-safe diagnostic до package/config и внешних file mutations
