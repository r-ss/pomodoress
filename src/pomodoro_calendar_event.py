# import re

from emoji import emojize

# from misc import midnight_fix
# from config import config
from log import log
from notification import Notification
from pomodoro import Pomodoro

# from misc import midnight_fix

# import dateutil.parser


# from dateutil.relativedelta import relativedelta


class PomodoroCalendarEvent(Pomodoro):

    type = "calendar"

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

    @property
    def description(self) -> str:
        """10:00 - 10:30 - code (calendar event)"""
        return f"{self.emoji} {self.start_fmt} - {self.end_fmt} - {self.formtext} (calendar event)"

    @property
    def readable_description(self) -> str:
        """13:00 - Commute until 15:00 (calendar event)"""
        return f"{self.emoji} {self.start_fmt} - {self.formtext} (calendar event)"

    def start_routine(self) -> None:

        log(f"> start routine, calendar event {self.description}")

        _ = Notification(f"{self.emoji} {self.start} - {self.formtext}")
        self.notified = True

        self.active = True
