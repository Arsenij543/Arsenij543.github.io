import random
import telebot
from password import gen_pass
from random import choice
import os
import requests


# Замени 'TOKEN' на токен твоего бота
# Этот токен ты получаешь от BotFather, чтобы бот мог работать
bot = telebot.TeleBot("7695916873:AAH6uAfMtDug_STKaO3Xx975RrYPGanMqcE")
memes = os.listdir('./img')

TRASH_DATA = {
    "бумага": ("♻ Перерабатывается", "🟦 Контейнер для бумаги"),
    "картон": ("♻ Перерабатывается", "🟦 Контейнер для бумаги"),
    "газета": ("♻ Перерабатывается", "🟦 Бумага"),

    "пластик": ("♻ Частично перерабатывается", "🟨 Контейнер для пластика"),
    "плёнка": ("❌ Не перерабатывается", "🗑 Общий мусор"),
    "пакет": ("❌ Обычно не перерабатывается", "🗑 Общий мусор"),
    "бутылка": ("♻ Перерабатывается (если пластиковая)", "🟨 Пластик"),

    "стекло": ("♻ Перерабатывается", "🟩 Контейнер для стекла"),
    "банка": ("♻ Если стеклянная — да", "🟩 Стекло"),

    "металл": ("♻ Перерабатывается", "🔵 Металл"),
    "жесть": ("♻ Перерабатывается", "🔵 Металл"),

    "органика": ("♻ Перерабатывается", "🟫 Органика"),
    "еда": ("♻ Перерабатывается", "🟫 Органика"),
    "яблоко": ("♻ Перерабатывается", "🟫 Органика"),

    "батарейка": ("⚠️ Опасный отход", "🟥 Пункт приёма опасных отходов"),
    "лампочка": ("⚠️ Опасный отход", "🟥 Специальный пункт"),
    "аккумулятор": ("⚠️ Опасный отход", "🟥 Сдать в спец. пункт"),

    "текстиль": ("♻ Перерабатывается частично", "🗑 Либо спец. сбор одежды"),
}

waiting_for_trash = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я твой Telegram бот. Напиши что-нибудь!")

#/help/ info
@bot.message_handler(commands=['help', 'info'])
def send_help(message):
    help_text = (
        "Вот что я умею:\n"
        "/hello - Приветствие\n"
        "/bye - Прощание\n"
        "/password <length> - Генерация пароля заданной длины (от 8 до 50)\n"
        "/coin <n> - Подбросить монетку n раз (по умолчанию 1)\n"
        "/calc <num1> <operator> <num2> - Калькулятор для простых операций (+, -, *, /)\n"
        "/heh <n> - Повторить 'he' n раз (по умолчанию 5)"
        "/mem - Отправить мем\n"
        "/anime <название> - Поиск информации об аниме\n"
        "/recommend - Посоветовать аниме\n"
        "/trash - Помощь с сортировкой мусора\n"
    )
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['hello'])
def send_hello(message):
    bot.reply_to(message, "Привет! Как дела?")

@bot.message_handler(commands=['bye'])
def send_bye(message):
    bot.reply_to(message, "Пока! Удачи!")

@bot.message_handler(commands=['password'])
def send_password(message):
    words = message.text.split()
    if len(words) == 2:
        p = gen_pass(int(words[1]))
        bot.reply_to(message, p)
    elif len(words) == 1:
        bot.reply_to(message, "Пожалуйста, укажи длину пароля. Например: /password 12 /password 12 25 59")
    else:
        numbers = words[1:]
        for num in numbers:
            p = gen_pass(int(num))
            bot.reply_to(message, p)

# /coin или /flip
@bot.message_handler(commands=['coin', 'flip'])
def coin_flip(message):
    parts = message.text.strip().split()
    n = 1
    if len(parts) > 1:
        try:
            n = int(parts[1])
        except ValueError:
            bot.reply_to(message, "Ошибка: укажите целое число бросков, например: /coin 3")
            return
    if n < 1:
        bot.reply_to(message, "Ошибка: количество бросков должно быть >= 1.")
        return
    if n > 100:
        bot.reply_to(message, "Ошибка: максимум 100 бросков.")
        return

    results = [choice(["Орёл", "Решка"]) for _ in range(n)]
    reply = "Результаты: " + ', '.join(results) + f"\nОрёл: {results.count('Орёл')}, Решка: {results.count('Решка')}"
    bot.reply_to(message, reply)


# Calculator
@bot.message_handler(commands=['calc'])
def calculate(message):
    words = message.text.split()
    if len(words) > 1:
        num1 = int(words[1])
        num2 = int(words[3])
        symbols = words[2]
        if num2 == 0 and symbols == '/':
            bot.reply_to(message, "Ошибка: Деление на ноль!")
        else:
            bot.reply_to(message, eval(f"{num1} {symbols} {num2}"))
    else:
        bot.reply_to(message, "Пожалуйста, введите выражение в формате: /calc 5 + 3")




# '/heh'
@bot.message_handler(commands=['heh'])
def send_heh(message):
    count_heh = int(message.text.split()[1]) if len(message.text.split()) > 1 else 5
    bot.reply_to(message, "he" * count_heh)

#  '/mem' 
@bot.message_handler(commands=['mem'])
def send_mem(message):
    words = message.text.split()
    if len(words) == 2:
        num = int(words[1])
        if 0 < num < len(memes):
            with open(f'./img/{memes[num -1]}', 'rb') as f:
                bot.send_photo(message.chat.id, f)
            return
    with open(f'./img/{memes[random.randint(0, len(memes) -1)]}', 'rb') as f:
        bot.send_photo(message.chat.id, f)

#  '/anime'
@bot.message_handler(commands=['anime'])
def get_anime(message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.reply_to(message, "Напиши название аниме. Пример: /anime tokyo ghoul")
        return

    query = parts[1]
    url = f"https://kitsu.io/api/edge/anime?filter[text]={query}"

    try:
        response = requests.get(url)
        data = response.json()

        if not data["data"]:
            bot.reply_to(message, "❌ Ничего не найдено.")
            return

        # Отправляем информацию о каждом аниме
        for anime in data["data"]:
            attr = anime["attributes"]
            title = attr.get("canonicalTitle", "Без названия")
            rating = attr.get("averageRating", "Нет рейтинга")
            episodes = attr.get("episodeCount", "Неизвестно")
            
            # Постер
            poster = attr["posterImage"]["large"] if attr.get("posterImage") else None

            caption = (
                f"🎬 *{title}*\n"
                f"⭐ Рейтинг: {rating}\n"
                f"📺 Эпизодов: {episodes}"
            )

            if poster:
                bot.send_photo(
                    message.chat.id,
                    poster,
                    caption=caption,
                    parse_mode="Markdown"
                )
            else:
                bot.send_message(message.chat.id, caption, parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, f"Ошибка при запросе: {e}")

#посоветовать аниме с высоким рейтингом
@bot.message_handler(commands=['recommend'])
def recommend_anime(message):
    url = "https://kitsu.io/api/edge/anime?sort=-averageRating&page[limit]=5"

    try:
        response = requests.get(url)
        data = response.json()

        recommendations = []
        for anime in data["data"]:
            attr = anime["attributes"]
            title = attr.get("canonicalTitle", "Без названия")
            rating = attr.get("averageRating", "Нет рейтинга")
            recommendations.append(f"🎬 *{title}* - ⭐ Рейтинг: {rating}")

        reply = "Вот несколько аниме с высоким рейтингом:\n\n" + "\n".join(recommendations)
        bot.reply_to(message, reply, parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, f"Ошибка при запросе: {e}")



# сортировка  /trash (предмет)(предмет).. через список 
@bot.message_handler(commands=['trash'])
def trash_multiple(message):
    parts = message.text.split(maxsplit=1)

    if len(parts) == 1:
        bot.reply_to(message, "Пожалуйста, укажи хотя бы один предмет. Например: /trash бумага пакет стекло")
        return

    items = parts[1].lower().split()
    reply = ""

    for item in items:
        if item in TRASH_DATA:
            status, container = TRASH_DATA[item]
            reply += f"♻ {item.capitalize()}\n{status}\n{container}\n\n"
        else:
            reply += f"❓ Не знаю, куда сортировать '{item}'.\n\n"

    bot.reply_to(message, reply.strip())

    






@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.polling()