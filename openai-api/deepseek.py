# deepseek_minimal.py
import os
from openai import OpenAI

def main():
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("❌ DEEPSEEK_API_KEY не найден")
        return
    
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    messages = []
    
    while True:
        user_input = input("\nВы: ").strip()
        if user_input.lower() in ["выход", "exit"]:
            break
        
        messages.append({"role": "user", "content": user_input})
        
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                stream=True
            )
            
            print("DeepSeek: ", end="")
            full_response = ""
            for chunk in response:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    print(content, end="", flush=True)
                    full_response += content
            
            messages.append({"role": "assistant", "content": full_response})
            print()
            
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            messages.pop()  # Удаляем последний запрос

if __name__ == "__main__":
    main()