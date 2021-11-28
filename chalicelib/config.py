from pathlib import Path
import pytz



# sheet_id = '16MvAmxu2gzrRYGyepzxe19w7zKr8Zr8RIB898bQBTIs'
# sheet_name = 'home'
# sheet_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

class Config:

    TESTING_MODE = False
    PRODUCTION = False

    SECRETS_ENV_PATH = f'{Path.cwd()}/chalicelib/.env.secrets'

    SSM_PARAMETER_LAST_POMODORO = 'pomodoro_last'

    # AWS_SSM_ENABLED = False
    # TELEGRAM_ENABLED = False  # Not send actual telegram messages if True

    AWS_SSM_ENABLED = True
    TELEGRAM_ENABLED = True  # Not send actual telegram messages if False

    SCHEDULE_FILE_PATH = f'{Path.cwd()}/chalicelib/schedule/schedule.txt'
    REST_MESSAGES_FILE_PATH = f'{Path.cwd()}/chalicelib/schedule/rest_messages.txt'

    # Rate to invoke main app, in minutes
    TICK_INTERVAL = 1  

    # Default Pomodoro duration, in minutes
    POMODORO_DURATION = 25

    UNPRODUCTIVE_ACTIVITIES = ['free', 'dinner', 'netflix']

    TZ = pytz.timezone('Europe/Moscow')
    