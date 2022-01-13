import os
import socket
from pathlib import Path

import pytz
from dotenv import load_dotenv

SECRETS_ENV_PATH = f"{Path.cwd()}/.env.secrets"
load_dotenv(dotenv_path=SECRETS_ENV_PATH)


class config:

    APP_NAME = "pomodoress"
    APP_SERVER = "ress@bass"
    BASE_DIR: str = Path.cwd()
    ENTRYPOINT = Path("src/app.py")

    # mode switch
    PRODUCTION: bool = True
    if socket.gethostname() == "ress-mpb.local":
        PRODUCTION = False

    DEBUG: bool = not PRODUCTION
    TESTING_MODE: bool = False  # Must be set to True only in autotests

    # secrets
    SECRET_KEY = str(os.environ.get("SECRET_KEY"))

    # server and deploy config
    HOST = "0.0.0.0"
    PORT = 9004
    SERVER_WATCH_FILES = not PRODUCTION  # auto reload on source files change

    # logging setup, more in log.py
    LOG_FILE_PATH = f"{Path.cwd()}/logs/log.log"
    LOG_LEVEL = "INFO"

    # notifications
    TELEGRAM_ENABLE_SENDING = True
    TELEGRAM_TOKEN = str(os.environ.get("TELEGRAM_HTTP_TOKEN"))
    TELEGRAM_USER = str(os.environ.get("TELEGRAM_USERID"))
    TELEGRAM_DELETE_NOTIFICATIONS = 75  # after X seconds

    if TESTING_MODE:
        TELEGRAM_ENABLE_SENDING = False

    PAUSED = False
    SCHEDULE_FILE_PATH = f"{Path.cwd()}/storage/schedule.txt"
    REST_MESSAGES_FILE_PATH = f"{Path.cwd()}/storage/rest_messages.txt"
    UNPRODUCTIVE_ACTIVITIES = ["morning", "free", "dinner", "netflix"]

    # Default Pomodoro duration, minutes
    POMODORO_DURATION = 25

    # formats
    DATE_FORMAT_HUMAN: str = "%d.%m.%Y"
    DATETIME_FORMAT_TECHNICAL: str = "%Y-%m-%d %H:%M:%S"
    DATETIME_FORMAT_HUMAN: str = "%d.%m.%Y %H:%M"
    TZ = pytz.timezone("Europe/Moscow")
