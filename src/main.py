import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
import json

TOKEN = "8110376772:AAHHMdldRzDwS6RH0MXfGtAvHy0wYWGNrNQ"
bot = telebot.TeleBot(TOKEN)

ENCYCLOPEDIA = {
    "Фрезерование": "Фрезерование — это процесс обработки металла резанием с помощью фрезы. Применяется для создания пазов, канавок, зубчатых колёс и других сложных поверхностей.",
    "Токарная обработка": "Токарная обработка — это процесс обработки металла на токарном станке, где заготовка вращается, а режущий инструмент перемещается. Используется для изготовления валов, втулок и других деталей вращения.",
    "Шлифование": "Шлифование — это процесс абразивной обработки, который позволяет получить высокую точность размеров и низкую шероховатость поверхности.",
    "Сварка": "Сварка — это процесс соединения металлов путем их местного нагрева до расплавленного или пластичного состояния. Основные виды: дуговая, газовая, контактная.",
}

def get_currency_rates():
    try:
        url = "https://www.cbr-xml-daily.ru/daily_json.js"
        response = requests.get(url)
        data = json.loads(response.text)
        usd = data["Valute"]["USD"]["Value"]
        eur = data["Valute"]["EUR"]["Value"]
        return f"💰 Курсы валют (ЦБ РФ):\n🇺🇸 Доллар: {usd} ₽\n🇪🇺 Евро: {eur} ₽"
    except Exception as e:
        return "❌ Не удалось получить курсы валют. Попробуйте позже."

def get_metal_prices():
    try:
        # Нербаочий парсинг
        url = "https://www.metallplace.ru/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        steel_price = "75 000 ₽/т"  # Пример
        aluminum_price = "150 000 ₽/т"  # Пример
        copper_price = "700 000 ₽/т"  # Пример
        
        return (
            f"🔩 Цены на металлы (пример):\n"
            f"🛠️ Сталь: {steel_price}\n"
            f"📦 Алюминий: {aluminum_price}\n"
            f"🔌 Медь: {copper_price}"
        )
    except Exception as e:
        return "❌ Не удалось получить цены на металлы. Попробуйте позже."

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("💰 Курсы валют")
    btn2 = types.KeyboardButton("🔩 Цены на металлы")
    btn3 = types.KeyboardButton("📚 Энциклопедия")
    btn4 = types.KeyboardButton("📩 Обратная связь")
    markup.add(btn1, btn2, btn3, btn4)
    
    bot.send_message(
        message.chat.id,
        "👋 Добро пожаловать в бот PRO Detali!\n\n"
        "Здесь вы можете узнать актуальные курсы валют, цены на металлы, "
        "почитать энциклопедию по металлообработке или связаться с разработчиками.",
        reply_markup=markup
    )

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == "💰 Курсы валют":
        bot.send_message(message.chat.id, get_currency_rates())
    
    elif message.text == "🔩 Цены на металлы":
        bot.send_message(message.chat.id, get_metal_prices())
    
    elif message.text == "📚 Энциклопедия":
        markup = types.InlineKeyboardMarkup()
        for key in ENCYCLOPEDIA.keys():
            markup.add(types.InlineKeyboardButton(key, callback_data=f"encyclopedia_{key}"))
        bot.send_message(message.chat.id, "📚 Выберите тему из энциклопедии:", reply_markup=markup)
    
    elif message.text == "📩 Обратная связь":
        msg = bot.send_message(message.chat.id, "✍️ Напишите ваше сообщение разработчикам PRO Detali:")
        bot.register_next_step_handler(msg, process_feedback)
    
    else:
        bot.send_message(message.chat.id, "❌ Неизвестная команда. Используйте кнопки ниже.")

# Обработчик энциклопедии
@bot.callback_query_handler(func=lambda call: call.data.startswith('encyclopedia_'))
def handle_encyclopedia(call):
    topic = call.data.split('_')[1]
    bot.send_message(call.message.chat.id, f"📖 {topic}:\n\n{ENCYCLOPEDIA.get(topic, 'Информация не найдена.')}")

# Обработчик обратной связи
def process_feedback(message):
    

    user = message.from_user
    feedback = message.text
    user_info = (
        f"👤 Пользователь:\n"
        f"├ ID: {user.id}\n"
        f"├ Имя: {user.first_name}\n"
        f"├ Фамилия: {user.last_name if user.last_name else '❌'}\n"
        f"└ Юзернейм: @{user.username if user.username else '❌'}\n\n"
        f"✉️ Сообщение:\n{feedback}"
    )


    bot.send_message(
        message.chat.id,
        "✅ Спасибо за ваше сообщение! Мы свяжемся с вами в ближайшее время.\n\n"
        f"Ваше сообщение: {feedback}"
    )

    if not user.username:
      bot.send_message(
        message.chat.id,
        "⚠️ У вас не указан username (@никнейм). "
        "Рекомендуем его добавить в настройках Telegram, "
        "чтобы мы могли с вами связаться."
    )
    ADMIN_CHAT_ID = 819873265;
    bot.send_message(ADMIN_CHAT_ID, f"📩 Новое сообщение от пользователя:\n\n {user_info}")

# Запуск бота
if __name__ == "__main__":
    print("Бот запущен!")
    bot.polling(none_stop=True)
