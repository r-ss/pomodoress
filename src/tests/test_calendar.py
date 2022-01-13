from datetime import datetime

from config import config
from dispatcher import Dispatcher
from emoji import emojize
from google_calendar.calendar import GoogleCalendar
from log import log

# def test_today():
#     ds = Dispatcher()

#     today = datetime.now(config.TZ).replace(hour=0, minute=0, second=0, microsecond=0).astimezone(config.TZ)  # + relativedelta(days=1)
#     cal = GoogleCalendar()
#     calendar_events = cal.load_for_day(today)

#     if calendar_events:
#         if calendar_events.have_allday_events:
#             print("Today:\n")
#             for e in calendar_events:
#                 if e.all_day:
#                     print(e.text)

#     print(f"\nSchedule for {today.strftime(config.DATE_FORMAT_HUMAN)}:\n")

#     if calendar_events:
#         for p in ds.pomodoros:
#             for e in calendar_events:
#                 if not e.all_day:
#                     if e.start <= p.start and e.end > p.end + p.duration:
#                         p.emoji = emojize(":calendar:")
#                         p.text = f"{e.text} (was {p.text})"
#                         if e.is_commute_event:
#                             p.emoji = emojize(":automobile:")


#     for p in ds.united_pomodoros:
#         caret = "   "
#         if p.active:
#             caret = ">> "
#         line = f"{caret}{p.description}"

#         print(line)


def test_fake_calendar():
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
        print("\nSchedule:\n")

    for p in ds.pomodoros:
        for e in calendar_events:
            if not e.all_day:
                if e.start <= p.start and e.end > p.end + p.duration:
                    p.emoji = emojize(":calendar:")
                    p.text = f"{e.text} (was {p.text})"
                    if e.is_commute_event:
                        p.emoji = emojize(":automobile:")

    # cp = ds.current_pomodoro()
    # ds.run_pomodoro(cp)

    txt = "test_fake_calendar:"
    for p in ds.united_pomodoros:
        caret = "   "
        if p.active:
            caret = ">> "
        line = f"\n{caret}{p.description}"

        txt += line

    log(txt)
    assert ("13:00 - 13:30 - Commute (was code)" in txt) is True
