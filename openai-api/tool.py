import json
from openai import OpenAI

client = OpenAI()

# 1. Имитация функции (API погоды)
def get_weather(location):
    return {"location": location, "temperature": "22", "unit": "celsius"}

# 2. Описание инструментов
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string"}
            },
            "required": ["location"]
        }
    }
}]

messages = [{"role": "user", "content": "Какая погода в Сочи?"}]

# ШАГ 1: Запрос к модели
response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools
)

assistant_message = response.choices[0].message

# ШАГ 2: Если модель хочет вызвать функцию, выполняем её
if assistant_message.tool_calls:
    messages.append(assistant_message) # Добавляем ответ ассистента в историю
    
    for tool_call in assistant_message.tool_calls:
        # Извлекаем аргументы
        args = json.loads(tool_call.function.arguments)
        # Вызываем нашу локальную функцию
        result = get_weather(args['location'])
        
        # Добавляем результат выполнения в историю
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result)
        })

# ШАГ 3: Финальный ответ модели на основе данных функции
final_response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages
)

print(final_response.choices[0].message.content)