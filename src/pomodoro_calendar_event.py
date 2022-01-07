import re

# from misc import midnight_fix
from config import config

from notification import Notification
from log import log

# from misc import midnight_fix

# import dateutil.parser

from pomodoro import Pomodoro

# from dateutil.relativedelta import relativedelta

from emoji import emojize


class PomodoroCalendarEvent(Pomodoro):

    type = 'calendar'

    def __init__(self, start, end, text, is_commute_event=False) -> None:

        self.start = start
        self.end = end

        self.emoji = emojize(":calendar:")
        self.is_commute_event = is_commute_event
        if is_commute_event:
            self.emoji = emojize(":automobile:")

        self.text = text

        self.fingerprint = f"calendar_fingerprint {self.start_fmt} - {self.end_fmt} - {self.text}"

        self.active = False
        self.reformatted = False
        self.reformatted_text = self.text
        self.notified = False  # marks when notification sends to user

        self.previous = None  # previous Pomodoro in queue
        self.next = None  # next Pomodoro in queue

    @property
    def description(self) -> str:
        # return f"calendar event, {self.emoji} {self.start} - {self.end} - {self.formtext}"
        return f"{self.emoji} {self.start_fmt} - {self.end_fmt} - {self.formtext} (calendar event)"

    def start_routine(self) -> None:

        log(f"> start routine, calendar event {self.description}")

        _ = Notification(f"{self.emoji} {self.start} - {self.formtext}")
        self.notified = True

        self.active = True

