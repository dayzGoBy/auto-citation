import os
import telebot
import uuid
from loguru import logger
from messages import messages
from model import do_query, classify_face

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
        
        for entry in results:
            bot.send_message(message.chat.id, f"{entry['text']}\n\n - {entry['author']}, «{entry['piece']}»")


if __name__ == "__main__":
    logger.info("Bot started")

    bot.polling()
