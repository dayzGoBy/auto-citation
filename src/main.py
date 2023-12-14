import os
import telebot
from telebot import types
import uuid
from loguru import logger
from messages import messages, emoji
from model import do_query, classify_face, add_quote

bot = telebot.TeleBot(os.environ["BOT_TOKEN"])


@bot.message_handler(commands=["start"])
def start_command(message):
    bot.send_message(message.chat.id, messages["start"])


@bot.message_handler(commands=["help"])
def help_command(message):
    bot.send_message(message.chat.id, messages["help"])


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
        markup.add(*[
            types.InlineKeyboardButton(e, callback_data=str(i)) 
            for i, e in enumerate(emoji)
        ])

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


def save_author(message, quote):
    author = message.text
    bot.send_message(message.from_user.id, "Откуда цитата:")
    bot.register_next_step_handler(message, save_work, quote, author)


def save_work(message, quote, author):
    piece = message.text
    try:
        add_quote(quote, author, piece)
    except Exception:
        bot.send_message(message.from_user.id, "При добавлении цитаты произошла ошибка, попробуйте ещё раз")
    else:
        bot.send_message(message.from_user.id, "Цитата успешно добавлена")


# @bot.message_handler(commands=['view'])
# def view_quotes(message):
#     user_id = message.from_user.id
#     user_quotes = get_user_quotes(user_id)
#     if "quotes" in user_quotes and user_quotes["quotes"]:
#         quotes_text = "\n\n".join(
#             [f"\"{quote['quote']}\" - {quote['author']}, {quote['work']}" for quote in user_quotes["quotes"]])
#         bot.send_message(user_id, f"Ваши цитаты:\n{quotes_text}")
#     else:
#         bot.send_message(user_id, "Вы ещё не добавили никаких цитат.")


if __name__ == "__main__":
    logger.info("Bot started")

    bot.polling()
