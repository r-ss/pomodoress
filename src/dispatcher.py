from datetime import datetime, timedelta
from typing import Union

from config import config
from google_calendar.calendar import GoogleCalendar
from log import log
from pomodoro import Pomodoro
from pomodoro_calendar_event import PomodoroCalendarEvent
from utils import current_time, time_from_hh_mm_string


class Dispatcher:
    def __init__(self, pomodoros=None) -> None:

        self.day = datetime.now(config.TZ).replace(hour=0, minute=0, second=0, microsecond=0).astimezone(config.TZ)
        self.calendar = None
        self.calendar_events = None
        self.reformatted = False

        if pomodoros:
            self.pomodoros = pomodoros
        else:
            self.load_schedule()

        self.active_pomodoro: Union[Pomodoro, PomodoroCalendarEvent] = None

    def load_schedule(self) -> None:
        with open(config.SCHEDULE_FILE_PATH, "r", encoding="UTF8") as f:
            self.parse_pomodoros(f.readlines())

        self.load_calendar()
        self.merge_calendar_with_schedule()
        self.setup_prev_and_next()
        self.reformatted = False
        self.reformat_pomodoros()

    def load_calendar(self) -> None:
        self.calendar = GoogleCalendar()
        if config.TESTING_MODE:
            self.calendar_events = self.calendar.load_fake()
        else:
            self.calendar_events = self.calendar.load_for_day(self.day)

    def reload_schedule(self):
        log(f"Reloading schedule...", level="debug")

        hotreplace = None
        if self.active_pomodoro:
            hotreplace = self.active_pomodoro

        self.pomodoros = []
        self.load_schedule()

        if hotreplace:
            # self.active_pomodoro = hotreplace

            self.replace_pomodoro(self.active_pomodoro, hotreplace)
            self.active_pomodoro.active = True
            self.active_pomodoro.notified = True

    def replace_pomodoro(self, a, b):
        self.pomodoros = [b if p.start == a.start else p for p in self.pomodoros]
        self.setup_prev_and_next()

    def merge_calendar_with_schedule(self) -> None:
        if not self.calendar_events:
            return
        for p in self.pomodoros:
            for e in self.calendar_events:
                if not e.all_day:

                    if e.start <= p.start and e.end >= p.end:

                        # log(f"e.start: {e.start}", level="debug")
                        # log(f"e.end: {e.end}", level="debug")
                        # log(f"p.start: {p.start}", level="debug")
                        # log(f"p.end: {p.end}", level="debug")

                        c = PomodoroCalendarEvent(e.start, e.end, e.text, is_commute_event=e.is_commute_event)

                        log(
                            f"replacing pomodoro: {p.description} with {c.description}",
                            level="debug",
                        )

                        self.replace_pomodoro(p, c)

    def setup_prev_and_next(self) -> None:
        """filling .previous value in every pomodoro"""
        for i in range(1, len(self.pomodoros)):
            self.pomodoros[i].previous = self.pomodoros[i - 1]

        """ filling .next value in every pomodoro """
        for i in range(len(self.pomodoros) - 1):
            self.pomodoros[i].next = self.pomodoros[i + 1]

    def parse_pomodoros(self, raw_lines) -> None:
        self.pomodoros = []
        for line in raw_lines:
            self.pomodoros.append(Pomodoro(line))

    def get_pomodoro(self, time: Union[datetime, str]) -> Union[Pomodoro, None]:

        if type(time) == str:
            time = time_from_hh_mm_string(time)

        for p in self.pomodoros:
            if p.start <= time and p.end > time:
                return p
        return None

    def current_pomodoro(self):
        return self.get_pomodoro(current_time())

    def run_pomodoro(self, pomodoro: Union[Pomodoro, PomodoroCalendarEvent]):
        if not pomodoro:
            self.active_pomodoro = None
            return

        if self.active_pomodoro:
            if self.active_pomodoro == pomodoro:
                return
            self.active_pomodoro.finish()

        self.active_pomodoro = pomodoro

        pomodoro.run()

    def tick(self, time=None):

        if type(time) == str:
            time = time_from_hh_mm_string(time)

        if not time:
            time = current_time()

        # if time.minute == 40:
        #     log(f"Schedule will be reloaded now, {time}", level="debug")
        #     self.reload_schedule()

        # log(f"Dispatcher tick event {time}", level="debug")

        if self.active_pomodoro:
            active_time = time - self.active_pomodoro.start
            log(
                f"tick active_pomodoro: {self.active_pomodoro}, active_time: {active_time}",
                level="debug",
            )
            if active_time >= timedelta(minutes=25):
                if self.active_pomodoro.next:
                    if self.active_pomodoro.type == "generic":
                        self.active_pomodoro.rest.run()

        p = self.get_pomodoro(time)
        if p != self.active_pomodoro:
            self.check_and_fire(p)
        # log("Nothing more in tick_event()", level="debug")

    def check_and_fire(self, pomodoro: Union[Pomodoro, PomodoroCalendarEvent]) -> None:
        log(f"> check_and_fire for {pomodoro}", level="debug")
        if not pomodoro.active:
            self.run_pomodoro(pomodoro)

    @property
    def united_pomodoros(self):
        """skip repeated pomodoros of same type"""
        united = [self.pomodoros[0]]
        last = self.pomodoros[0]
        for i, p in enumerate(self.pomodoros):
            if p == last:
                continue
            if p.text == last.text:
                # last.end = p.end
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
                        p.reformatted_text = f"{p.text } until {n.end_fmt}"
                        p.reformatted = True
                    continue

                break
        self.reformatted = True

    def get_schedule(self, united=True):
        """used for print shedule to user on request"""

        s = []

        if self.calendar_events:
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
