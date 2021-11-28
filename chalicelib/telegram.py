from chalicelib.config import Config
import telebot
import os
from chalicelib.config import Config

TGBOT_HTTP_TOKEN = os.environ.get('TGBOT_HTTP_TOKEN')
TG_USERID = os.environ.get('TG_USERID')


def send_telegram_message(message: str) -> None:
    if not Config.TELEGRAM_ENABLED:
        print(message)
        return

    

    bot = telebot.TeleBot('pomodoress_bot')
    bot.config['api_key'] = TGBOT_HTTP_TOKEN

    bot.send_message(TG_USERID, message)