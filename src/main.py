import os
import telebot
import uuid
from loguru import logger

from messages import messages

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
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    filename = str(uuid.uuid4())

    with open(f"photos/{filename}.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)

    reply_message = bot.reply_to(message, messages["got_photo"])

    try:
        pass
        # demographies = get_person_description(f"photos/{filename}.jpg")
    except ValueError:
        bot.send_message(message.chat.id, messages["no_face"])
    else:
        """emotions = list(map(
            lambda key: round(demographies["emotion"][key], 2),
            ["angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"]
        ))

        reply_message = bot.edit_message_text(
            messages["extracted_emotions"].format(*emotions),
            message.chat.id, reply_message.message_id)

        user_message = structurize_for_gpt(demographies)
        gpt_answer = request_promt(GPT_PROMT, user_message)

        bot.edit_message_text(messages["gpt_answer"].format(gpt_answer),
                              message.chat.id, reply_message.message_id)"""


if __name__ == "__main__":
    logger.info("Bot started")

    bot.polling()
