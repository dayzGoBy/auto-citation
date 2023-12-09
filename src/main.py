import os
import telebot
from telebot import types
import uuid
from loguru import logger
from messages import messages, emoji
from model import do_query, classify_face
from pathlib import Path
import json

bot = telebot.TeleBot(os.environ["BOT_TOKEN"])


@bot.message_handler(commands=["start"])
def start_command(message):
    bot.send_message(message.chat.id, messages["start"])


@bot.message_handler(commands=["help"])
def help_command(message):
    bot.send_message(message.chat.id, messages["help"])


FEATURE_ORDER = ["angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"]


@bot.message_handler(content_types=['photo'])
def photo(message):
    logger.info("Got photo")

    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    filename = str(uuid.uuid4())

    with open(f"photos/{filename}.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.reply_to(message, messages["got_photo"])

    try:
        vector = classify_face(f"photos/{filename}.jpg")
    except ValueError:
        bot.send_message(message.chat.id, messages["no_face"])
    else:
        results = do_query(vector)
        bot.send_message(message.chat.id, messages['model_answer'])

        markup = types.InlineKeyboardMarkup(row_width=5)
        markup.add(*[types.InlineKeyboardButton(e, callback_data=str(i)) for i, e in enumerate(emoji)])

        for entry in results:
            bot.send_message(
                message.chat.id,
                f"{entry['text']}\n\n - {entry['author']}, «{entry['piece']}»",
                reply_markup=markup
            )


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    # process answer
    bot.answer_callback_query(call.id, "Ваша оценка сохранена")


json_file_path = "./user_quotes.json"


@bot.message_handler(commands=['add'])
def add_quote_handler(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Введите цитату:")
    bot.register_next_step_handler(message, save_quote_step)


def save_quote_step(message):
    user_id = message.from_user.id
    quote_text = message.text
    bot.send_message(user_id, "Теперь автора цитаты:")
    bot.register_next_step_handler(message, save_author, quote_text)


def save_author(message, quote_text):
    user_id = message.from_user.id

    author_text = message.text
    bot.send_message(user_id, "Откуда цитата:")
    bot.register_next_step_handler(message, save_work, quote_text, author_text)


def get_user_quotes(user_id):
    if Path(json_file_path).is_file():
        with open(json_file_path, "r") as file:
            all_quotes = json.load(file)
    if str(user_id) not in all_quotes:
        user_quotes = {"quotes": []}
    else:
        user_quotes = all_quotes[str(user_id)]
    return user_quotes


def set_user_quotes(user_quotes, user_id):
    with open(json_file_path, "rwx") as file:
        all_quotes = json.load(file)
    all_quotes[str(user_id)] = user_quotes
    with open(json_file_path, "w") as file:
        json.dump(all_quotes, file, indent=4)


def save_quote(user_id, quote_text, author_text, work_text):
    user_quotes = get_user_quotes(user_id)

    user_quotes["quotes"].append({
        "quote": quote_text,
        "author": author_text,
        "work": work_text
    })

    set_user_quotes(user_quotes, user_id)


def save_work(message, quote_text, author_text):
    user_id = message.from_user.id
    work_text = message.text
    save_quote(user_id, quote_text, author_text, work_text)
    bot.send_message(user_id, "Цитата успешно добавлена")


@bot.message_handler(commands=['view'])
def view_quotes(message):
    user_id = message.from_user.id
    user_quotes = get_user_quotes(user_id)
    if "quotes" in user_quotes and user_quotes["quotes"]:
        quotes_text = "\n\n".join(
            [f"\"{quote['quote']}\" - {quote['author']}, {quote['work']}" for quote in user_quotes["quotes"]])
        bot.send_message(user_id, f"Ваши цитаты:\n{quotes_text}")
    else:
        bot.send_message(user_id, "Вы ещё не добавили никаких цитат.")


if __name__ == "__main__":
    logger.info("Bot started")

    bot.polling()
