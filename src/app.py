# pylint: disable=C0116,W0613

# from datetime import datetime

import logging
from config import config

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

from apscheduler.schedulers.background import BackgroundScheduler

from dispatcher import Dispatcher

job_defaults = {
    'coalesce': False,
    'max_instances': 1
}
scheduler = BackgroundScheduler()
scheduler.configure(job_defaults=job_defaults, timezone=config.TZ)


logging.basicConfig(format=config.LOGGING_FORMAT, level=config.LOGGING_LEVEL)
logger = logging.getLogger(__name__)

dispatcher = Dispatcher()

updater = Updater(config.TELEGRAM_TOKEN)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
# Best practice would be to replace context with an underscore,
# since context is an unused local variable.
# This being an example and not having context present confusing beginners,
# we decided to have it present as context.
def start(update: Update, context: CallbackContext) -> None:
    config.PAUSED = False
    update.message.reply_text('started')

def pause(update: Update, context: CallbackContext) -> None:
    config.PAUSED = True
    update.message.reply_text('paused')

def sheduler_tick_event():
    if not config.PAUSED:
        dispatcher.tick()

def reset_day_event():
    global dispatcher
    dispatcher = None
    dispatcher = Dispatcher()
    config.PAUSED = False

# def test():
#     print('test func')
#     print(config.SCHEDULE_FILE_PATH)

def print_current_pomodoro(update: Update, context: CallbackContext):
    p = dispatcher.current_pomodoro()
    update.message.reply_text(p.description)

def print_next_pomodoro(update: Update, context: CallbackContext):
    p = dispatcher.current_pomodoro()
    update.message.reply_text(p.next.description)

def print_shedule(update: Update, context: CallbackContext):
    s = dispatcher.get_schedule(united = True)
    update.message.reply_text(s)

def print_full_shedule(update: Update, context: CallbackContext):
    s = dispatcher.get_schedule(united = False)
    update.message.reply_text(s)

def main() -> None:
    """Run bot."""
    # Create the Updater and pass it your bot's token.
    # updater = Updater("TOKEN")

    # bot = Bot(token=config.TELEGRAM_TOKEN)
    # config.TELEGRAM_READY_BOT = bot
    

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("pause", pause))

    dispatcher.add_handler(CommandHandler("current", print_current_pomodoro))
    dispatcher.add_handler(CommandHandler("next", print_next_pomodoro))
    dispatcher.add_handler(CommandHandler("shedule", print_shedule))
    dispatcher.add_handler(CommandHandler("fullshedule", print_full_shedule))

    # Start the Bot
    updater.start_polling()

    # job = scheduler.add_job(sheduler_tick, 'interval', minutes=1, seconds=0)
    scheduler.add_job(sheduler_tick_event, 'cron', minute='*', second=0)
    scheduler.add_job(reset_day_event, 'cron', minute=15, hour=4)
    scheduler.start()


    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()

    

    


if __name__ == '__main__':
    main()
    # print_shedule()