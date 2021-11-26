import telebot
import os
# from config import Config






def send_telegram_message(message: str) -> None:
    # bot = telegram.Bot(TGBOT_HTTP_TOKEN)

    TGBOT_HTTP_TOKEN = os.environ.get('TGBOT_HTTP_TOKEN')
    TG_USERID = os.environ.get('TG_USERID')

    # bot.send_message(TG_USERID, message)
    # pass
    # bot = telebot.TeleBot(Config.TELEGRAM_TOKEN) # Regular version
    # bot = telebot.AsyncTeleBot()  # Async version   
    bot = telebot.TeleBot('pomodoress_bot')
    bot.config['api_key'] = TGBOT_HTTP_TOKEN

    # print(TG_USERID)
    bot.send_message(TG_USERID, message)
    # print(bot.get_me())
