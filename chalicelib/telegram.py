from chalicelib.config import config
import telebot
import os

from chalicelib.cw_log import CWLog

def send_telegram_message(message: str) -> None:
    if not config.TELEGRAM_ENABLED:
        print(message)
        return

    bot = telebot.TeleBot('pomodoress_bot')
    bot.config['api_key'] = os.environ.get('TGBOT_HTTP_TOKEN')


    CWLog.send_cw_log(f'sending telegram message: {message}')

    bot.send_message(os.environ.get('TG_USERID'), message)
