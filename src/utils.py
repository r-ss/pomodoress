from datetime import datetime

import dateutil.parser
from dateutil.relativedelta import relativedelta

from config import config


def bytes_to_human_readable_size(num, suffix="b"):
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


def time_from_hh_mm_string(hh_mm: str) -> datetime:
    time = config.TZ.localize(dateutil.parser.parse(hh_mm))
    if time.hour < 4:
        time += relativedelta(days=1)
    return time


def current_time():
    return datetime.now(config.TZ)
