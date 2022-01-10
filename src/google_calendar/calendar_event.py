import re
import time
from datetime import datetime

import dateutil.parser
from config import config
from dateutil.relativedelta import relativedelta


class CalendarEvent:
    def __init__(self, start, end, text, is_commute_event=False) -> None:
        self.start = start
        self.end = end
        self.is_commute_event = is_commute_event

        if type(self.start) == str:
            self.start = dateutil.parser.parse(self.start)
        if type(self.end) == str:
            self.end = dateutil.parser.parse(self.end)

        self.text = text

    @property
    def duration(self):
        return self.end - self.start

    @property
    def all_day(self):
        if self.duration.seconds == 0:
            return True
        return False

    @property
    def formatted_start(self):
        return self.start.strftime(config.DATETIME_FORMAT_HUMAN)

    @property
    def formatted_end(self):
        return self.end.strftime(config.DATETIME_FORMAT_HUMAN)

    @property
    def description(self) -> str:
        return f"allday: {self.all_day} - {self.formatted_start} - {self.formatted_end} - {self.text}"


class CalendarDayHelper:
    def __init__(self) -> None:
        self.events = []
        # self.have_allday_events = None

    @property
    def have_allday_events(self):
        for event in self.events:
            if event.all_day:
                return True
        return False

    def add_event(self, event, parse=True):
        self.events.append(event)
        if parse:
            self.parse_event_text(event)

    def parse_event_text(self, event):
        def get_delta(research):
            if research["TypeNumber"]:
                num = int(research["TypeNumber"])
                delta = relativedelta(minutes=30 * num)
            if research["TypeTime"]:
                hh_mm = research["TypeTime"]
                t = time.strptime(hh_mm, "%H:%M")
                delta = relativedelta(hours=t.tm_hour, minutes=t.tm_min)
            return delta

        if "commute" in event.text:
            delta = get_delta(
                re.search(
                    ",?\s((?P<TypeDescription>commute)(?:\s)((?P<TypeTime>\d{1,2}:\d{1,2})|(?P<TypeNumber>\d)))",
                    event.text,
                ).groupdict()
            )
            start = event.start - delta
            end = event.start
            c = CalendarEvent(start, end, "Commute", is_commute_event=True)
            event.text = re.sub(",?\scommute\s\d{1,2}(:?\d{1,2})?", "", event.text)
            self.add_event(c, parse=False)
        if "back" in event.text:
            delta = get_delta(
                re.search(
                    ",?\s((?P<TypeDescription>back)(?:\s)((?P<TypeTime>\d{1,2}:\d{1,2})|(?P<TypeNumber>\d)))",
                    event.text,
                ).groupdict()
            )
            num = int(re.search("back\s(\d)", event.text)[1])
            start = event.end
            end = event.end + delta
            c = CalendarEvent(start, end, "Return", is_commute_event=True)
            event.text = re.sub(",?\sback\s\d{1,2}(:?\d{1,2})?", "", event.text)
            self.add_event(c, parse=False)

    # def get_events(self):
    #     return self.events

    def __iter__(self):
        return iter(self.events)

    def __getitem__(self, item):
        return self.events[item]
