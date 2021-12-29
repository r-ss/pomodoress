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
    def __init__(self, start, end, text, is_commute_event=False) -> None:

        self.start = start
        self.end = end

        self.emoji = emojize(":calendar:")
        self.is_commute_event = is_commute_event
        if is_commute_event:
            self.emoji = emojize(":automobile:")

        self.text = text

        self.fingerprint = f"calendar_fingerprint {self.start} - {self.end} - {self.text}"

        self.active = False
        self.reformatted = False
        self.reformatted_text = self.text
        self.notified = False  # marks when notification sends to user

        # Rest object is in response for 5-minutes resting time window when pomodoros 25 minutes passes
        self.rest = None

        self.previous = None  # previous Pomodoro in queue
        self.next = None  # next Pomodoro in queue

    @property
    def description(self) -> str:
        return f"calendar event, {self.emoji} {self.start} - {self.end} - {self.formtext}"

    def start_routine(self) -> None:

        log(f"> start routine, calendar event {self.description}")

        pomodoro_notification = Notification(f"{self.emoji} {self.start} - {self.formtext}")
        self.notified = True

        self.active = True
