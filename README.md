
# ДЗ #2
- Расширить тестовое покрытие smoke тестами на доступность микросервиса
  - добавить сервисный эндпоинт `/status` для проверки доступности микросервиса
- Использовать библиотеку fastapi-pagination для базовой пагинации в эндпоинтах, которые возвращают список объектов
- Добавить тесты на пагинацию. Тестовых данных должно быть достаточно для проверки пагинации (не менее 10)
- Проверяем:
    - ожидаемое количество объектов в ответе
    - правильное количество страниц при разных значениях size
    - возвращаются разные данные при разных значениях page
