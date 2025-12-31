def ask_model(prompt, model):
    if model == "yandex":
        return f"[YandexGPT] Ответ на: {prompt}"
    
    if model == "deepseek":
        return f"[DeepSeek] Ответ на: {prompt}"
    
    return "Неизвестная модель"