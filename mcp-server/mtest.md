# Проверка вручную (без Cursor)

Все команды запускайте из каталога примера.

## Вариант 1: быстрый тест в одной консоли

Для этих команд отдельная консоль не нужна: каждый запрос поднимает одноразовый процесс, получает ответ и завершается.

```powershell
# 1. Инициализация
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' | python simple_file_server.py

# 2. Запрос списка инструментов
echo '{"jsonrpc":"2.0","id":2,"method":"tools/list"}' | python simple_file_server.py

# 3. Чтение файла
echo '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"read_notes","arguments":{}}}' | python simple_file_server.py
```

## Вариант 2: сервер в отдельной консоли (если нужен long-running режим)

Используйте этот вариант, когда сервер должен работать постоянно, а клиент отправляет несколько запросов отдельно.

```powershell
# Консоль 1: запустить сервер
python simple_file_server.py

# Консоль 2: отправлять запросы (пример)
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' | python simple_file_server.py
```