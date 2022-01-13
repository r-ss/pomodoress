import dateutil.parser
import pytest
from config import config
from dateutil.relativedelta import relativedelta
from dispatcher import Dispatcher
from log import log


def test_parsing():
    ds = Dispatcher()

    p = ds.get_pomodoro("00:00")
    assert p.fingerprint == "fingerprint 00:00 - 00:30 - wind down"

    p = ds.get_pomodoro("06:00")
    assert p == None

    p = ds.get_pomodoro("08:00")
    assert p.fingerprint == "fingerprint 08:00 - 08:30 - morning routine"

    p = ds.get_pomodoro("23:00")
    assert p.fingerprint == "fingerprint 23:00 - 23:30 - free time"

    p = ds.get_pomodoro("23:30")
    assert p.fingerprint == "fingerprint 23:30 - 00:00 - free time"

    p = ds.get_pomodoro("23:54")
    assert p.fingerprint == "fingerprint 23:30 - 00:00 - free time"

    p = ds.get_pomodoro("23:55")
    assert p.fingerprint == "fingerprint 23:30 - 00:00 - free time"

    p = ds.get_pomodoro("23:59")
    assert p.fingerprint == "fingerprint 23:30 - 00:00 - free time"


def test_bad_input():
    with pytest.raises(ValueError) as excinfo:
        Dispatcher().parse_pomodoros("some bad input")
    assert str(excinfo.value) == "bad input string, cannot split to 4 items separated by comma"


def test_tick():
    ds = Dispatcher()
    ds.tick("00:00")
    assert ds.active_pomodoro.fingerprint == "fingerprint 00:00 - 00:30 - wind down"


def test_many_ticks():
    ds = Dispatcher()

    start = config.TZ.localize(dateutil.parser.parse("7:00"))
    end = config.TZ.localize(dateutil.parser.parse("23:00"))
    step = relativedelta(minutes=1)

    now = start
    while now < end:
        now += step
        if now.minute == 40:
            ds.get_schedule(united=True)
        if now.minute == 42:
            ds.reload_schedule()
        if now.minute == 44:
            ds.get_schedule(united=False)
        if now.minute == 44:
            ds.get_schedule(united=True)
        ds.tick(now)


def test_print_schedule():
    txt = "test_print_schedule:"
    for p in Dispatcher().pomodoros:
        caret = "   "
        if p.active:
            caret = ">> "
        line = f"\n{caret}{p.description}"
        txt += line
    # log(txt)
    assert ("10:00 - 10:30 - code" in txt) is True
    assert ("16:00 - 17:00 - Return... (calendar event)" in txt) is True
    assert ("00:00 - 00:30 - wind down" in txt) is True


def test_print_united_pomodoros():
    txt = "test_print_united_pomodoros:"
    for p in Dispatcher().united_pomodoros:
        caret = "   "
        if p.active:
            caret = ">> "
        line = f"\n{caret}{p.readable_description}"
        txt += line
    # log(txt)
    assert ("10:00 - code until 12:00" in txt) is True
    assert ("13:00 - Commute until 15:00 (calendar event)" in txt) is True
    assert ("00:00 - wind down" in txt) is True


def test_count_total_times():
    output = Dispatcher().count_total_times()
    assert ("morning routine: 2.0" in output) is True
    assert ("exercise: 0.5" in output) is True
    assert ("sleep: 7.5" in output) is True
