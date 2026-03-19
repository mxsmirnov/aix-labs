import os
import subprocess
import requests
import json
import re
from datetime import datetime

# ========== НАСТРОЙКИ ==========
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")
if not DEEPSEEK_API_KEY:
    print("ОШИБКА: Не найдена переменная окружения DEEPSEEK_API_KEY")
    print("Установи: export DEEPSEEK_API_KEY='sk-...' (Linux/Mac) или")
    print("          $env:DEEPSEEK_API_KEY='sk-...' (Windows PowerShell)")
    exit(1)

API_URL = "https://api.deepseek.com/v1/chat/completions"
MODEL = "deepseek-chat"

# Счетчики токенов
total_prompt_tokens = 0
total_completion_tokens = 0
total_tokens = 0
request_count = 0

def print_token_usage(response_json, request_desc):
    """Выводит информацию об использовании токенов из ответа API"""
    global total_prompt_tokens, total_completion_tokens, total_tokens, request_count
    
    if "usage" in response_json:
        usage = response_json["usage"]
        prompt_tokens = usage.get("prompt_tokens", 0)
        completion_tokens = usage.get("completion_tokens", 0)
        tokens = usage.get("total_tokens", 0)
        
        total_prompt_tokens += prompt_tokens
        total_completion_tokens += completion_tokens
        total_tokens += tokens
        request_count += 1
        
        print(f"  [Токены {request_desc}]:")
        print(f"    Prompt: {prompt_tokens:>6} | Completion: {completion_tokens:>6} | Всего: {tokens:>6}")
    else:
        print(f"  [ВНИМАНИЕ] Нет информации о токенах в ответе {request_desc}")

def call_deepseek(messages, temperature=0.1, desc=""):
    """Универсальная функция для вызова API с подсчетом токенов"""
    response = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": MODEL,
            "messages": messages,
            "temperature": temperature
        }
    )
    
    response_json = response.json()
    print_token_usage(response_json, desc)
    return response_json

# ========== СТАРТ ==========
print("=" * 60)
print("CLI-ПОДХОД: ПОЛУЧЕНИЕ ПОГОДЫ ЧЕРЕЗ КОМАНДУ curl")
print("=" * 60)
start_time = datetime.now()

# ========== 1. ПРОСИМ МОДЕЛЬ НАПИСАТЬ КОМАНДУ ==========
messages_1 = [
    {
        "role": "system",
        "content": """Ты - помощник, который может выполнять команды в Windows.
Если нужно получить данные из внешнего источника - напиши команду curl.exe.
Отвечай ТОЛЬКО командой, без пояснений, если тебя просят выполнить действие."""
    },
    {
        "role": "user",
        "content": "Напиши команду для получения погоды в Москве через wttr.in в формате: температура, ветер, влажность"
    }
]

print("\n[1/4] Просим Deepseek написать команду curl...")
response_1 = call_deepseek(messages_1, temperature=0.1, desc="запрос команды")

# Извлекаем команду
command = response_1["choices"][0]["message"]["content"].strip()
command = command.replace("`", "").strip()

# Если модель вернула пояснения, пытаемся извлечь curl
if not command.startswith("curl"):
    curl_match = re.search(r'curl[^\n]+', command)
    if curl_match:
        command = curl_match.group(0)
    else:
        print("Модель не вернула команду curl. Ответ:")
        print(command)
        exit(1)

print(f"[2/4] Команда от модели: {command}")

# ========== 2. ВЫПОЛНЯЕМ КОМАНДУ ==========
print("[3/4] Выполняем команду...")
exec_start = datetime.now()

result = subprocess.run(command, shell=True, capture_output=True, text=True)
exec_time = (datetime.now() - exec_start).total_seconds()

if result.returncode != 0:
    print(f"Ошибка выполнения: {result.stderr}")
    exit(1)

weather_data = result.stdout.strip()
print(f"  Результат: {weather_data}")
print(f"  Время выполнения: {exec_time:.2f} сек")

# ========== 3. ПРОСИМ ИНТЕРПРЕТИРОВАТЬ РЕЗУЛЬТАТ ==========
messages_2 = [
    {
        "role": "system",
        "content": "Ты - полезный помощник. Отвечай на русском языке кратко и по делу."
    },
    {
        "role": "user",
        "content": f"Вот данные о погоде в Москве: {weather_data}\n\nЧто означают эти цифры? "
    }
]

print("\n[4/4] Просим Deepseek интерпретировать результат...")
response_2 = call_deepseek(messages_2, temperature=0.3, desc="интерпретация")

answer = response_2["choices"][0]["message"]["content"]

# ========== ИТОГИ ==========
print("\n" + "=" * 60)
print("РЕЗУЛЬТАТ")
print("=" * 60)
print(f"Погода (сырые данные): {weather_data}")
print(f"Ответ модели: {answer}")

print("\n" + "=" * 60)
print("СТАТИСТИКА ТОКЕНОВ")
print("=" * 60)
print(f"Запросов к API:           {request_count}")
print(f"Prompt токенов (всего):   {total_prompt_tokens:>8}")
print(f"Completion токенов (всего):{total_completion_tokens:>8}")
print(f"ИТОГО токенов:            {total_tokens:>8}")

print("\n" + "=" * 60)
print(f"Время выполнения: {(datetime.now() - start_time).total_seconds():.1f} сек")
print("=" * 60)