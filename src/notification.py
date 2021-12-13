from telegram import Bot

from config import config

bot = Bot(token=config.TELEGRAM_TOKEN)

def send_telegram(txt: str) -> None:
    if config.TELEGRAM_ENABLE_SENDING:
        bot.send_message(config.TELEGRAM_USER, text = txt)