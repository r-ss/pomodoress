# pylint: disable=C0116,W0613

# from datetime import datetime

from log import log
from config import config

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler

# from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ProcessPoolExecutor

from dispatcher import Dispatcher

# jobstores = {
#     'mongo': {'type': 'mongodb'},
#     'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
# }
executors = {
    "default": {"type": "threadpool", "max_workers": 5},
    "processpool": ProcessPoolExecutor(max_workers=1),
}
job_defaults = {"coalesce": False, "max_instances": 1}
scheduler = BackgroundScheduler()

# .. do something else here, maybe add jobs etc.

scheduler.configure(executors=executors, job_defaults=job_defaults, timezone=config.TZ)


# job_defaults = {"coalesce": False, "max_instances": 1}

# scheduler = BlockingScheduler()
# scheduler.configure(job_defaults=job_defaults, timezone=config.TZ)


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
    update.message.reply_text("started")


def pause(update: Update, context: CallbackContext) -> None:
    config.PAUSED = True
    update.message.reply_text("paused")


def sheduler_tick_event():
    if not config.PAUSED:
        dispatcher.tick()


def reset_day_event():
    global dispatcher
    dispatcher = None
    dispatcher = Dispatcher()
    config.PAUSED = False


# def test():
#     log('test func')
#     log(config.SCHEDULE_FILE_PATH)


def print_current_pomodoro(update: Update, context: CallbackContext):
    p = dispatcher.current_pomodoro()
    update.message.reply_text(p.description)


def print_next_pomodoro(update: Update, context: CallbackContext):
    p = dispatcher.current_pomodoro()
    update.message.reply_text(p.next.description)


def print_shedule(update: Update, context: CallbackContext):
    s = dispatcher.get_schedule(united=True)
    update.message.reply_text(s)


def print_full_shedule(update: Update, context: CallbackContext):
    s = dispatcher.get_schedule(united=False)
    update.message.reply_text(s)


# class TelegramCommand:
#     dbfield = None
#     question = None
#     answer = None

#     def __init__(self, name, func, aliases=[], description=''):
#         self.name = name
#         self.name = name
#         self.aliases = aliases
#         self.emoji = emoji


def main() -> None:
    """Run bot."""
    # Create the Updater and pass it your bot's token.
    # updater = Updater("TOKEN")

    # bot = Bot(token=config.TELEGRAM_TOKEN)
    # config.TELEGRAM_READY_BOT = bot

    # Get the dispatcher to register handlers
    bot_dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    bot_dispatcher.add_handler(CommandHandler("start", start))
    bot_dispatcher.add_handler(CommandHandler("pause", pause))

    bot_dispatcher.add_handler(CommandHandler("current", print_current_pomodoro))
    bot_dispatcher.add_handler(CommandHandler("next", print_next_pomodoro))
    bot_dispatcher.add_handler(CommandHandler("shedule", print_shedule))
    bot_dispatcher.add_handler(CommandHandler("fullshedule", print_full_shedule))

    # job = scheduler.add_job(sheduler_tick_event, 'interval', seconds=10)
    scheduler.add_job(sheduler_tick_event, "cron", minute="*", second=0)
    scheduler.add_job(reset_day_event, "cron", minute=15, hour=4)

    scheduler.start()

    log("app started, bot idling...")

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
