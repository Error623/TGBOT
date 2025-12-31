import telebot
from config import BOT_TOKEN, ADMIN_IDS
from users import get_user, can_use, users
from models import ask_model
from keyboards import model_keyboard
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    get_user(message.from_user.id)
    bot.send_message(
        message.chat.id,
        "Выбрать модель",
        reply_markup=model_keyboard()
    )


@bot.message_handler(commands=["id"])
def show_id(message):
    bot.send_message(message.chat.id, f"твой ID: {message.from_user.id}")

@bot.message_handler(commands=["admin"])
def admin_panel(message):
    if message.from_user.id not in ADMIN_IDS:
        return
    
    text = {
        f"Админ-панель\n\n"
        f"Всего пользователей: {len(users)}"
    }
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["give"])
def give_subscription(message):
    if message.from_user.id not in ADMIN_IDS:
        return

    parts = message.text.split()
    if len(parts) != 3:
        bot.send_message(
            message.chat.id,
            "Формат: /give user_id limit\nПример: /give 123456789 15"
        )
        return

    try:
        target_user_id = int(parts[1])
        limit = int(parts[2])
    except ValueError:
        bot.send_message(message.chat.id, "user_id и limit должны быть числами")
        return

    # получаем или создаём пользователя
    user = get_user(target_user_id)

    # ЗАЩИТА ОТ БИТЫХ ДАННЫХ 
    if "requests_left" not in user:
        user["requests_left"] = 0
    if "plan" not in user:
        user["plan"] = "free"
    if "model" not in user:
        user["model"] = "yandex"

    user["requests_left"] += limit
    user["plan"] = "pro"

    bot.send_message(
        message.chat.id,
        f"✅ Подписка выдана\n"
        f"ID: {target_user_id}\n"
        f"Добавлено запросов: {limit}\n"
        f"Всего осталось: {user['requests_left']}"
    )



@bot.callback_query_handler(func=lambda c: c.data.startswith("model:"))
def select_model(call):
    model = call.data.split(":")[1]
    user = get_user(call.from_user.id)
    user["model"] = model

    bot.answer_callback_query(call.id, f"Модель выбрана: {model}")
    bot.send_message(call.message.chat.id, "Напишите запрос")



@bot.message_handler(content_types=["text"])
def text_handler(message):
    user_id = message.from_user.id
    user = get_user(user_id)

    if not can_use(user_id):
        bot.send_message(message.chat.id, "Лимит исчерпан")
        return
    
    answer = ask_model(message.text, user["model"])
    bot.send_message(message.chat.id, answer)


bot.polling(none_stop=True, skip_pending=True)
    