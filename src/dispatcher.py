from typing import Union
from datetime import datetime
from google_calendar.calendar import GoogleCalendar
from pomodoro import Pomodoro
from pomodoro_calendar_event import PomodoroCalendarEvent

from config import config
from log import log

from dateutil.relativedelta import relativedelta
from emoji import emojize

from misc import current_time, midnight_fix


class Dispatcher:
    def __init__(self, pomodoros=None) -> None:

        self.day = datetime.now(config.TZ).replace(hour=0, minute=0, second=0, microsecond=0).astimezone(config.TZ)  # + relativedelta(days=1)
        self.calendar = None
        self.calendar_events = None

        if pomodoros:
            self.pomodoros = pomodoros
        else:
            self.load_schedule()

        self.previous_pomodoro = None
        self.active_pomodoro = None
        self.reformatted = False

    def load_schedule(self) -> None:
        with open(config.SCHEDULE_FILE_PATH, "r", encoding="UTF8") as f:
            self.parse_pomodoros(f.readlines())

        self.load_calendar()
        self.merge_calendar_with_schedule()

    def load_calendar(self) -> None:

        self.calendar = GoogleCalendar()
        self.calendar_events = self.calendar.load_for_day(self.day)

    def replace_pomodoro(self, a, b):
        self.pomodoros = [b if p.start == a.start else p for p in self.pomodoros]

    def merge_calendar_with_schedule(self) -> None:
        for p in self.pomodoros:
            for e in self.calendar_events:
                if not e.all_day:

                    if e.start <= p.calc_start and e.end >= p.calc_end:

                        log(f"e.start: {e.start}", level="debug")
                        log(f"e.end: {e.end}", level="debug")
                        log(f"p.calc_start: {p.calc_start}", level="debug")
                        log(f"p.calc_end: {p.calc_end}", level="debug")

                        c = PomodoroCalendarEvent(e.start, e.end, e.text, is_commute_event=e.is_commute_event)

                        log(
                            f"replacing pomodoro: {p.description} with {c.description}",
                            level="debug",
                        )

                        self.replace_pomodoro(p, c)

    def parse_pomodoros(self, raw_lines) -> None:
        self.pomodoros = []
        for line in raw_lines:
            self.pomodoros.append(Pomodoro(line))

        # filling .previous value in every pomodoro
        for i in range(1, len(self.pomodoros)):
            self.pomodoros[i].previous = self.pomodoros[i - 1]

        # filling .next value in every pomodoro
        for i in range(len(self.pomodoros) - 1):
            self.pomodoros[i].next = self.pomodoros[i + 1]

    def get_pomodoro(self, time):
        if type(time) == str:
            time = midnight_fix(time)

        for p in self.pomodoros:
            if p.startint <= time and p.endint > time:
                return p
        return None

    def current_pomodoro(self):
        return self.get_pomodoro(current_time())

    def run_pomodoro(self, pomodoro: Union[Pomodoro, PomodoroCalendarEvent]) -> None:
        if not pomodoro:
            self.active_pomodoro = None
            return None

        if self.active_pomodoro:
            if self.active_pomodoro == pomodoro:
                return
            if self.previous_pomodoro:
                self.previous_pomodoro.end_routine()
            self.previous_pomodoro = self.active_pomodoro

        self.active_pomodoro = pomodoro
        self.reformat_pomodoros()
        pomodoro.start_routine()

    def tick(self, forcedtime=None):
        time = current_time(forcedtime)
        log(f"Dispatcher tick event {time}", level="debug")

        if self.active_pomodoro:
            active_minutes = int(time - self.active_pomodoro.startint)
            if active_minutes >= config.POMODORO_DURATION:
                if self.active_pomodoro.next:
                    self.active_pomodoro.rest.start()

        p = self.get_pomodoro(time)
        if p:
            self.check_and_fire(p)

    def check_and_fire(self, pomodoro: Union[Pomodoro, PomodoroCalendarEvent]) -> None:
        if not pomodoro.active:
            self.run_pomodoro(pomodoro)

    @property
    def united_pomodoros(self):
        """skipped repeated pomodoros of same type"""
        united = [self.pomodoros[0]]
        last = self.pomodoros[0]
        for i, p in enumerate(self.pomodoros):
            if p == last:
                continue
            if p.text == last.text:
                last.end, last.endint = p.end, p.endint
                continue
            else:
                last = p
            united.append(last)
        return united

    def reformat_pomodoros(self):
        if self.reformatted:
            return

        l = len(self.pomodoros)
        for i in range(len(self.pomodoros)):
            p = self.pomodoros[i]

            for j in range(min(20, l - i)):
                if i + j + 1 >= l:
                    continue

                n = self.pomodoros[i + j + 1]
                if n.text == p.text:
                    if not n.reformatted:
                        n.reformatted_text = f"{n.text}..."
                        n.reformatted = True
                        p.reformatted_text = f"{p.text } until {n.end}"
                        p.reformatted = True
                    continue

                break
        self.reformatted = True

    def get_schedule(self, united=True):
        """used for print shedule to user on request"""

        s = []

        if self.calendar_events.have_allday_events:
            s.append(f"Schedule for {self.day.strftime(config.DATE_FORMAT_HUMAN)}:\n")
            for e in self.calendar_events:
                if e.all_day:
                    s.append(e.text)
            s.append("")  # for line break in output

        pool = self.pomodoros
        if united:
            pool = self.united_pomodoros

        for p in pool:
            s.append(p.description)
        return "\n".join(s)