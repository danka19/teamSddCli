## 1. Контракт и отрицательные случаи

- [x] 1.1 Добавить RED tests для совместимого reuse, hash mismatch, отсутствующего/failed preflight и неявного reuse.
- [x] 1.2 Расширить selection/evidence schema явным baseline-reuse record и allowlisted contract hashes.

## 2. Deterministic validator

- [x] 2.1 Реализовать fail-closed baseline reuse validation в release candidate acceptance.
- [x] 2.2 Обновить selection/evidence fixtures и release documentation с причинами, критериями и ограничениями.

## 3. Проверка successor candidate

- [x] 3.1 Запустить focused release/actual-certification tests и зафиксировать свежий Qwen/DeepSeek preflight evidence.
- [x] 3.2 Подготовить versioned successor package и candidate-bound transfer evidence без повторной полной matrix. Immutable `guided-owner-v0.3.1-rc4` принят владельцем по `D-023`; Linux/WSL2 portability smoke остаётся отложенной обязательной проверкой перед Phase 4.
