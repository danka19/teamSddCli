# Developer: начать реализацию безопасно

Канонический источник: [artifact and lifecycle gates](../../runbooks/ARTIFACT_AND_LIFECYCLE_GATES.md).

Цель — реализовать только одобренный bounded change и сохранить доказательства. Начните с `sdd next --change <путь> --role Developer`. До реализации убедитесь в DoR; приложите тесты и review evidence. Не меняйте lifecycle, не подтверждайте релиз и остановитесь, если маршрут требует Analyst или Tech Lead.
