import re

# from misc import midnight_fix
from config import config
from log import log
from notification import Notification
from rest import Rest
from utils import time_from_hh_mm_string


class Pomodoro:

    type = "generic"

    def __init__(self, rawrow: str) -> None:

        if not rawrow or type(rawrow) != str:
            raise ValueError("bad input, string expected")

        rawrow = re.sub(r'["/\n]', "", rawrow).split(",")

        if len(rawrow) != 4:
            raise ValueError("bad input string, cannot split to 4 items separated by comma")

        self.start = time_from_hh_mm_string(rawrow[0])
        self.end = time_from_hh_mm_string(rawrow[1])

        self.emoji = rawrow[2].strip()
        self.text = rawrow[3]
        self.fingerprint = f"fingerprint {self.start_fmt} - {self.end_fmt} - {self.text}"

        self.active = False
        self.reformatted = False
        self.reformatted_text = self.text
        self.notified = False  # marks when notification sends to user

        self.rest_allowed = True

        # Rest object is in response for 5-minutes resting time window when pomodoros 25 minutes passes
        self.rest = Rest(self)  # pass this pomodoro as parent_pomodoro for Rest object

        # self.duration = config.POMODORO_DURATION  # default pomodoro duration 25 minutes
        self.previous = None  # previous Pomodoro in queue
        self.next = None  # next Pomodoro in queue


    @property
    def description(self) -> str:
        """10:00 - 10:30 - code"""
        return f"{self.emoji} {self.start_fmt} - {self.end_fmt} - {self.formtext}"

    @property
    def readable_description(self) -> str:
        """10:00 - code until 12:00"""
        return f"{self.emoji} {self.start_fmt} - {self.formtext}"

    @property
    def extended_description(self) -> str:
        """2022-01-11 10:00:00+03:00 - 2022-01-11 10:30:00+03:00 - duration 0:30:00 - code"""
        return f"{self.emoji} {self.start} - {self.end} - duration {self.duration} - {self.text}"

    @property
    def formtext(self) -> str:
        if self.reformatted:
            return self.reformatted_text
        return self.text

    @property
    def duration(self):
        return self.end - self.start

    @property
    def start_fmt(self) -> str:
        return self.start.strftime("%H:%M")

    @property
    def end_fmt(self) -> str:
        return self.end.strftime("%H:%M")

    def run(self) -> None:
        log(f"> start routine {self.description}", level="debug")

        # not send notification if we have long unproductive activities in a row
        prevtext = ""
        if self.previous:
            prevtext = self.previous.text
        if any(w in self.text for w in config.UNPRODUCTIVE_ACTIVITIES) and any(z in prevtext for z in config.UNPRODUCTIVE_ACTIVITIES):
            self.rest_started = True
            return

        if self.previous:
            if self.previous.text == self.text and not self.rest_allowed:
                return

        _ = Notification(f"{self.emoji} {self.start.strftime('%H:%M')} - {self.formtext}")
        self.notified = True
        self.active = True

    def finish(self) -> None:
        log(f"> end routine {self.description}", level="debug")
        self.active = False

    def __repr__(self) -> str:
        return f"{id(self)} - {self.description}"
