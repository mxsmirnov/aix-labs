# Внимание! Этот пример Leagcy и работать не будет
from openai import OpenAI

client = OpenAI(api_key="ваш-api-ключ")

# Самый простой вызов
response = client.completions.create(
    model="gpt-3.5-turbo-instruct",
    prompt="Кратко объясни, что такое Python",
    max_tokens=100
)

print(response.choices[0].text)