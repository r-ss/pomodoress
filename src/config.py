from pathlib import Path
from dotenv import load_dotenv
import logging
import pytz
import os

SECRETS_ENV_PATH = f'{Path.cwd()}/.env.secrets'
load_dotenv(dotenv_path=SECRETS_ENV_PATH)

# sheet_id = '16MvAmxu2gzrRYGyepzxe19w7zKr8Zr8RIB898bQBTIs'
# sheet_name = 'home'
# sheet_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

class config:

    APP_NAME = 'pomodoress'

    TESTING_MODE = False
    # PRODUCTION = True

    PAUSED = False

    


    TELEGRAM_ENABLE_SENDING = True
    TELEGRAM_TOKEN = os.environ.get('TELEGRAM_HTTP_TOKEN')
    TELEGRAM_USER = os.environ.get('TELEGRAM_USERID')

    SCHEDULE_FILE_PATH = f'{Path.cwd()}/storage/schedule.txt'
    REST_MESSAGES_FILE_PATH = f'{Path.cwd()}/storage/rest_messages.txt'


    # Default Pomodoro and Rest duration, in minutes
    POMODORO_DURATION = 25
    REST_DURATION = 5

    UNPRODUCTIVE_ACTIVITIES = ['free', 'dinner', 'netflix']

    TZ = pytz.timezone('Europe/Moscow')
    DT_FORMAT = '%d %B %Y %H:%M:%S %Z'


    LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    # LOGGING_LEVEL = logging.WARNING  # logging.INFO
    LOGGING_LEVEL = logging.INFO  # logging.INFO
    