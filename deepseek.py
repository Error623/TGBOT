import requests

API_KEY = "sk-5ef32fdf90c840ef8b3724dde66f1570"
URL = "https://api.deepseek.com/chat/completions"


headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


data = {
    "model": "deepseek-chat",
    "messages": [
        {"role": "user", "content": "Привет! Объясни основы Python коротко и понятными словами"}
    ]
}


response = requests.post ( 
    URL,
    headers=headers,
    json=data, 
    timeout=30
)

print("Статус: ", response.status_code)


result = response.json()

if response.status_code != 200:
    print("Ошибка от API:")
    print(result)
    exit()

if "choices" not in result:
    print("Нет ответа модели:")
    print(result)
    exit()

answer = result["choices"][0]["message"]["content"]

print("Ответ ИИ: ")
print(answer)
print(response.text)