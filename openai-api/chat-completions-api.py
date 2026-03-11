# Пример из документации OpenAI https://github.com/openai/openai-python
from openai import OpenAI

client = OpenAI()

# Можем пропустить указание api_key, если он установлен в окружении
# client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"),)

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "developer", "content": "Talk like a pirate."},
        {
            "role": "user",
            "content": "How do I check if a Python object is an instance of a class?",
        },
    ],
)

print(completion.choices[0].message.content)