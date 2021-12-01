from pathlib import Path
import pytz



# sheet_id = '16MvAmxu2gzrRYGyepzxe19w7zKr8Zr8RIB898bQBTIs'
# sheet_name = 'home'
# sheet_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

class config:

    APP_NAME = 'pomodoress'

    TESTING_MODE = False
    # PRODUCTION = True

    SECRETS_ENV_PATH = f'{Path.cwd()}/chalicelib/.env.secrets'

    

    AWS_REGION = 'eu-north-1'
    AWS_SSM_ENABLED = True
    SSM_PARAMETER_LAST_POMODORO = 'pomodoro_last'

    AWS_LOGGING_ENABLED = True
    AWS_LOG_GROUP_NAME = 'Pomodoress_Logs'
    AWS_LOG_GENEGAL_STREAM_NAME = 'GeneralAppLogs'

    TELEGRAM_ENABLED = True  # Not send actual telegram messages if False

    SCHEDULE_FILE_PATH = f'{Path.cwd()}/chalicelib/schedule/schedule.txt'
    REST_MESSAGES_FILE_PATH = f'{Path.cwd()}/chalicelib/schedule/rest_messages.txt'


    # Default Pomodoro duration, in minutes
    POMODORO_DURATION = 25

    UNPRODUCTIVE_ACTIVITIES = ['free', 'dinner', 'netflix']

    TZ = pytz.timezone('Europe/Moscow')
    