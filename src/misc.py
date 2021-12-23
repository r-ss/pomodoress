from typing import Union
from datetime import datetime

from config import config


def midnight_fix(time: Union[int, str]) -> int:
    """recieves time in String or Int. Converting to Int, simple fix midnight problem - 00:00 as 0 and terurns as int"""
    if type(time) == str:
        time = int(time.replace(":", ""))

    # fixing time int to work propelty after midnight
    # 500 means 5:00, 2400 means 24:00
    if time < 500:
        time += 2400
    return time


def current_time(forcedtime=None):
    if forcedtime:
        return midnight_fix(forcedtime)
    time = datetime.now(config.TZ)
    time = time.strftime("%H%M")
    time = midnight_fix(time)
    return time
