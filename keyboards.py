from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def model_keyboard():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("DeepSeek", callback_data="model:deepseek"),
        InlineKeyboardButton("Yandex", callback_data="model:yandex")
    )
    return kb