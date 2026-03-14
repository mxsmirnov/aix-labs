# simple_file_server.py
import json
import sys

def main():
    """Простейший MCP сервер для чтения одного файла через stdio"""
    # Жестко заданный путь к файлу (Обязательно измените на свой!)
    FILE_PATH = r"C:\Users\mxsmi\AIX\aix-labs\mcp-server\notes.txt"
    
    while True:
        # Читаем ввод (JSON-RPC сообщение)
        line = sys.stdin.readline()
        if not line:
            break
            
        try:
            message = json.loads(line.strip())
            msg_id = message.get("id")
            method = message.get("method")
            
            # Ответ на инициализацию
            if method == "initialize":
                response = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "serverInfo": {"name": "simple-file-reader"},
                        "capabilities": {"tools": {}}
                    }
                }
            
            # Список инструментов
            elif method == "tools/list":
                response = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "tools": [{
                            "name": "read_notes",
                            "description": "Прочитать файл notes.txt",
                            "inputSchema": {
                                "type": "object",
                                "properties": {},
                                "required": []
                            }
                        }]
                    }
                }
            
            # Вызов инструмента
            elif method == "tools/call":
                tool_name = message.get("params", {}).get("name", "")
                
                if tool_name == "read_notes":
                    try:
                        with open(FILE_PATH, 'r', encoding='utf-8') as f:
                            content = f.read()
                        text = f"Содержимое файла:\n\n{content}"
                    except FileNotFoundError:
                        text = f"Файл не найден: {FILE_PATH}"
                    except Exception as e:
                        text = f"Ошибка чтения: {str(e)}"
                    
                    response = {
                        "jsonrpc": "2.0",
                        "id": msg_id,
                        "result": {
                            "content": [{
                                "type": "text",
                                "text": text
                            }]
                        }
                    }
                else:
                    response = {
                        "jsonrpc": "2.0",
                        "id": msg_id,
                        "error": {"message": f"Неизвестный инструмент: {tool_name}"}
                    }
            
            else:
                response = {"jsonrpc": "2.0", "id": msg_id, "result": {}}
            
            # Отправляем ответ
            print(json.dumps(response, ensure_ascii=False), flush=True)
            
        except json.JSONDecodeError:
            continue

if __name__ == "__main__":
    main()