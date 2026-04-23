# simple_file_server.py
import json
import sys

def main():
    """Простейший MCP сервер для чтения одного файла через stdio"""
    FILE_PATH = r"C:\Users\mxsmi\AIX-04\aix-labs\mcp-server\notes.txt"

    def send(obj):
        print(json.dumps(obj, ensure_ascii=False), flush=True)

    while True:
        line = sys.stdin.readline()
        if not line:
            break

        raw = line.strip()
        if not raw:
            continue

        try:
            message = json.loads(raw)
        except json.JSONDecodeError:
            continue

        if not isinstance(message, dict) or "method" not in message:
            continue

        method = message["method"]

        # Уведомления JSON-RPC 2.0 не содержат "id" — ответа не отправляют
        # (в т.ч. notifications/initialized после initialize)
        if "id" not in message:
            continue

        msg_id = message["id"]
        params = message.get("params") or {}

        if method == "initialize":
            protocol_version = params.get("protocolVersion", "2024-11-05")
            response = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "protocolVersion": protocol_version,
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "simple-file-reader", "version": "1.0.0"},
                },
            }
        elif method == "ping":
            response = {"jsonrpc": "2.0", "id": msg_id, "result": {}}
        elif method == "tools/list":
            response = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "tools": [
                        {
                            "name": "read_notes",
                            "description": "Прочитать файл notes.txt",
                            "inputSchema": {
                                "type": "object",
                                "properties": {},
                                "required": [],
                            },
                        }
                    ]
                },
            }
        elif method == "tools/call":
            tool_name = params.get("name", "")
            if tool_name == "read_notes":
                try:
                    with open(FILE_PATH, "r", encoding="utf-8") as f:
                        content = f.read()
                    text = f"Содержимое файла:\n\n{content}"
                except FileNotFoundError:
                    text = f"Файл не найден: {FILE_PATH}"
                except OSError as e:
                    text = f"Ошибка чтения: {str(e)}"

                response = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"content": [{"type": "text", "text": text}]},
                }
            else:
                response = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "error": {"code": -32602, "message": f"Неизвестный инструмент: {tool_name}"},
                }
        elif method in ("resources/list", "prompts/list"):
            key = "resources" if method == "resources/list" else "prompts"
            response = {"jsonrpc": "2.0", "id": msg_id, "result": {key: []}}
        else:
            response = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32601, "message": f"Method not found: {method}"},
            }

        send(response)

if __name__ == "__main__":
    main()
