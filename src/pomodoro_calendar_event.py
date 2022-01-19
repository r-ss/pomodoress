# import re

from emoji import emojize

# from misc import midnight_fix
# from config import config
from log import log
from notification import Notification
from pomodoro import Pomodoro
from rest import Rest

# from misc import midnight_fix

# import dateutil.parser


# from dateutil.relativedelta import relativedelta


class PomodoroCalendarEvent(Pomodoro):

    type = "calendar"

    def __init__(self, start, end, text, is_commute_event=False, rest_allowed=False) -> None:

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

        self.rest_allowed = rest_allowed
        self.rest = Rest(self)  # pass this pomodoro as parent_pomodoro for Rest object

        self.previous = None  # previous Pomodoro in queue
        self.next = None  # next Pomodoro in queue

    @property
    def description(self) -> str:
        return super().description + " (calendar event)"

    @property
    def readable_description(self) -> str:
        return super().readable_description + " (calendar event)"

    @property
    def extended_description(self) -> str:
        return super().extended_description + " (calendar event)"

    def start_routine(self) -> None:

        log(f"> start routine, calendar event {self.description}")

        _ = Notification(f"{self.emoji} {self.start} - {self.formtext}")
        self.notified = True

        self.active = True
