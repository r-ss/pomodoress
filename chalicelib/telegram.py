import telebot
import os
# from config import Config

TGBOT_HTTP_TOKEN = os.environ.get('TGBOT_HTTP_TOKEN')
TG_USERID = os.environ.get('TG_USERID')

def sendTelegram(message: str) -> None:
    # bot = telebot.TeleBot(Config.TELEGRAM_TOKEN) # Regular version
    # bot = telebot.AsyncTeleBot()  # Async version   
    bot = telebot.TeleBot('pomodoress_bot')
    bot.config['api_key'] = TGBOT_HTTP_TOKEN
    bot.send_message(TG_USERID, message)
    # print(bot.get_me())
