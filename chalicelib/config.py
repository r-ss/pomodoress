from pathlib import Path

# sheet_id = '16MvAmxu2gzrRYGyepzxe19w7zKr8Zr8RIB898bQBTIs'
# sheet_name = 'home'
# sheet_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

class Config:

    SECRETS_ENV_PATH = f'{Path.cwd()}/chalicelib/.env.secrets'

    SCHEDULE_FILE_PATH = f'{Path.cwd()}/chalicelib/schedule/schedule.txt'
    REST_MESSAGES_FILE_PATH = f'{Path.cwd()}/chalicelib/schedule/rest_messages.txt'


    # interval between Dispatch.tick() events, in seconds
    TICK_INTERVAL = 2

    # Default Pomodoro duration, in minutes
    POMODORO_DURATION = 25