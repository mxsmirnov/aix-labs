# Проверка вручную (без Cursor)

Все команды надо запускать из каталога примера

```powershell
# В одной консоли запустите сервер:
python simple_file_server.py

# В другой консоли отправьте тестовые запросы:
# 1. Инициализация
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' | python simple_file_server.py

# 2. Запрос списка инструментов
echo '{"jsonrpc":"2.0","id":2,"method":"tools/list"}' | python simple_file_server.py

# 3. Чтение файла
echo '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"read_notes","arguments":{}}}' | python simple_file_server.py
```