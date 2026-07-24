## 1. Контракт

- [x] 1.1 Зафиксировать proposal, design, Delta Spec и связь с P3.
- [x] 1.2 Провалидировать change и roadmap/OpenSpec inverse mapping.

## 2. Packaged companion

- [x] 2.1 Добавить RED tests для режима discovery и границы перед действиями.
- [x] 2.2 Добавить `analyst-discovery` и `guided-change` в существующий
  `sdd-process-companion`.
- [x] 2.3 Подтвердить focused tests установки и human-authority boundaries.

## 3. FAQ

- [x] 3.1 Добавить RED tests для человекочитаемого discovery route.
- [x] 3.2 Дополнить AI, Analyst и first-change pages.
- [x] 3.3 Усилить FAQ validator и подтвердить навигацию.

## 4. Пакет и документация

- [x] 4.1 Синхронизировать process package version и mutable pins.
- [x] 4.2 Обновить roadmap, file map и статусы без изменения исторических
  evidence.

## 5. Проверка

- [x] 5.1 Выполнить focused tests, FAQ validation, full pytest и strict
  OpenSpec validation.
  Evidence (2026-07-24): fresh focused set `24 passed`; FAQ validator `valid`;
  OpenSpec strict `24/24`; full pytest `801 passed, 11 skipped, 20 failed`.
  Representative certification/guide/allowlist failures воспроизводятся на
  `main`; release rehearsal проходит из короткого `main` path, а deep worktree
  вызывает Windows path-length failures. Полный suite не объявляется зелёным.
- [ ] 5.2 Провести независимое review ветки и устранить findings.
- [ ] 5.3 Провести реальный first-time human walkthrough; до него change не
  считать human-accepted.
