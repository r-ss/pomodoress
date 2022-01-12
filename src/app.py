# from datetime import datetime

from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Updater

from config import config
from dispatcher import Dispatcher
from log import log

# from apscheduler.schedulers.blocking import BlockingScheduler


executors = {
    "default": {"type": "threadpool", "max_workers": 5},
    "processpool": ProcessPoolExecutor(max_workers=1),
}
job_defaults = {"coalesce": False, "max_instances": 1}
scheduler = BackgroundScheduler()
# scheduler = BlockingScheduler()

scheduler.configure(executors=executors, job_defaults=job_defaults, timezone=config.TZ)


dispatcher = Dispatcher()
updater = Updater(config.TELEGRAM_TOKEN)


def start(update: Update, context: CallbackContext) -> None:
    config.PAUSED = False
    update.message.reply_text("started")
    log("Command /start fired", level="info")


def pause(update: Update, context: CallbackContext) -> None:
    config.PAUSED = True
    update.message.reply_text("paused")
    log("Command /pause fired", level="info")


def scheduler_tick_event():
    if not config.PAUSED:
        dispatcher.tick()


def reset_day_event():
    global dispatcher
    del dispatcher
    dispatcher = Dispatcher()
    config.PAUSED = False
    log("reset_day_event()", level="info")


def reload_schedule(update: Update = None, context: CallbackContext = None):
    if update:
        log("Command /reload fired", level="info")
    else:
        log("reload_schedule event", level="warning")
    dispatcher.reload_schedule()


def print_current_pomodoro(update: Update, context: CallbackContext):
    log("print_current_pomodoro()", level="info")
    p = dispatcher.current_pomodoro()
    update.message.reply_text(p.description)


def print_next_pomodoro(update: Update, context: CallbackContext):
    log("print_next_pomodoro()", level="info")
    p = dispatcher.current_pomodoro()
    update.message.reply_text(p.next.description)


def print_schedule(update: Update, context: CallbackContext):
    log("print_schedule()", level="info")
    s = dispatcher.get_schedule(united=True)
    update.message.reply_text(s)


def print_full_schedule(update: Update, context: CallbackContext):
    log("print_full_schedule()", level="info")
    s = dispatcher.get_schedule(united=False)
    update.message.reply_text(s)


def debug_command(update: Update = None, context: CallbackContext = None):

    log("debug_command()", level="debug")

    for item in dispatcher.pomodoros:
        log(item, level="debug")

    update.message.reply_text("ok, look in the logs")


class TelegramCommand:
    def __init__(self, name, handler, aliases=[], description=""):
        self.name = name
        self.handler = handler
        self.aliases = aliases
        self.description = description


class TelegramCommandsBin:
    def __init__(self):
        self.commands = []

    def add(self, cmd: TelegramCommand):
        self.commands.append(cmd)

    def setup_handlers(self, bot_dispatcher):
        def add_handler_to_bot_dispatcher(command_name, function):
            bot_dispatcher.add_handler(CommandHandler(command_name, function))

        for cmd in self.commands:
            add_handler_to_bot_dispatcher(cmd.name, cmd.handler)
            for a in cmd.aliases:
                add_handler_to_bot_dispatcher(a, cmd.handler)

    def show_commands_list(self, update: Update, context: CallbackContext):

        text = ["Available commands:"]
        for cmd in self.commands:
            text.append(f"{cmd.name} - {cmd.description}")
        final = "\n".join(text)
        update.message.reply_text(final)

    def __iter__(self):
        return iter(self.commands)

    def __getitem__(self, item):
        return self.commands[item]


commands = TelegramCommandsBin()

commands.add(TelegramCommand("start", start, description="start or resume paused bot"))
commands.add(TelegramCommand("pause", pause, description="pause bot until tomorrow"))
commands.add(TelegramCommand("current", print_current_pomodoro, aliases=["now"], description="show current pomodoro"))
commands.add(TelegramCommand("next", print_next_pomodoro, description="show next pomodoro"))
commands.add(TelegramCommand("schedule", print_schedule, aliases=["day", "today"], description="show today's schedule"))
commands.add(TelegramCommand("fullschedule", print_full_schedule, aliases=["fullday", "full"], description="show extended today's schedule"))
commands.add(TelegramCommand("reload", reload_schedule, description="reload schedule and calendar"))
commands.add(TelegramCommand("debug", debug_command, description="debug action"))


def show_commands_list(update: Update, context: CallbackContext) -> None:
    commands.show_commands_list(update, context)


def main() -> None:
    """Run bot."""
    # Create the Updater and pass it your bot's token.
    # updater = Updater("TOKEN")

    # bot = Bot(token=config.TELEGRAM_TOKEN)
    # config.TELEGRAM_READY_BOT = bot

    # Get the dispatcher to register handlers
    bot_dispatcher = updater.dispatcher

    commands.setup_handlers(bot_dispatcher)

    bot_dispatcher.add_handler(CommandHandler("help", show_commands_list))

    # job = scheduler.add_job(scheduler_tick_event, 'interval', seconds=10)
    scheduler.add_job(scheduler_tick_event, "cron", minute="*", second=0)
    scheduler.add_job(reset_day_event, "cron", minute=15, hour=4)
    scheduler.add_job(reload_schedule, "cron", hour="*", minute=40, second=0)

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
