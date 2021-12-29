# import pytest
from datetime import datetime
from google_calendar.calendar import GoogleCalendar
from dispatcher import Dispatcher

# from pomodoro import Pomodoro
from config import config

from dateutil.relativedelta import relativedelta
from emoji import emojize


# def test_basic():
#     cal = GoogleCalendar()
#     calendar_events = cal.load_today()


def test_today():
    ds = Dispatcher()

    today = datetime.now(config.TZ).replace(hour=0, minute=0, second=0, microsecond=0).astimezone(config.TZ)  # + relativedelta(days=1)
    cal = GoogleCalendar()
    calendar_events = cal.load_for_day(today)

    if calendar_events:
        if calendar_events.have_allday_events:
            print("Today:\n")
            for e in calendar_events:
                if e.all_day:
                    print(e.text)

    print(f"\nShedule for {today.strftime(config.DATE_FORMAT_HUMAN)}:\n")

    if calendar_events:
        for p in ds.pomodoros:
            for e in calendar_events:
                if not e.all_day:
                    if e.start <= p.start_as_datetime and e.end > p.end_as_datetime + relativedelta(minutes=29):
                        # line = f"cal {e.description}"
                        # p = Pomodoro(f'11:00,11:30,tdd,commute')
                        p.emoji = emojize(":calendar:")
                        p.text = f"{e.text} (was {p.text})"
                        if e.is_commute_event:
                            p.emoji = emojize(":automobile:")

    cp = ds.current_pomodoro()
    ds.run_pomodoro(cp)

    for p in ds.united_pomodoros:
        caret = "   "
        if p.active:
            caret = ">> "
        line = f"{caret}{p.description}"

        # for e in calendar_events:
        #     if not e.all_day:
        #         if e.start <= p.calc_start and e.end > p.calc_start + relativedelta(minutes=29):
        #             line = f"cal {e.description}"

        print(line)


# def test_midnight():
#     p = Pomodoro('"0:00","0:30","","free time\n"')
#     assert p.fingerprint == "fingerprint 0:00 - 0:30 - free time"


def test_fake():
    ds = Dispatcher()
    with open(config.SCHEDULE_FILE_PATH, "r", encoding="UTF8") as f:
        ds.parse_pomodoros(f.readlines())

    cal = GoogleCalendar()
    calendar_events = cal.load_fake()

    if calendar_events.have_allday_events:
        print("Today:\n")
        for e in calendar_events:
            if e.all_day:
                print(e.text)
        print("\nShedule:\n")

    for p in ds.pomodoros:
        for e in calendar_events:
            if not e.all_day:
                if e.start <= p.start_as_datetime and e.end > p.end_as_datetime + relativedelta(minutes=29):
                    # line = f"cal {e.description}"
                    # p = Pomodoro(f'11:00,11:30,tdd,commute')
                    p.emoji = emojize(":calendar:")
                    p.text = f"{e.text} (was {p.text})"
                    if e.is_commute_event:
                        p.emoji = emojize(":automobile:")

    cp = ds.current_pomodoro()
    ds.run_pomodoro(cp)

    for p in ds.united_pomodoros:
        caret = "   "
        if p.active:
            caret = ">> "
        line = f"{caret}{p.description}"

        # for e in calendar_events:
        #     if not e.all_day:
        #         if e.start <= p.calc_start and e.end > p.calc_start + relativedelta(minutes=29):
        #             line = f"cal {e.description}"

        print(line)


# def test_midnight():
#     p = Pomodoro('"0:00","0:30","","free time\n"')
#     assert p.fingerprint == "fingerprint 0:00 - 0:30 - free time"
