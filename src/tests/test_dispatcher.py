import pytest
from dispatcher import Dispatcher

from config import config

import dateutil.parser
from dateutil.relativedelta import relativedelta


def test_parsing():
    ds = Dispatcher()

    p = ds.get_pomodoro("00:00")
    assert p.fingerprint == "fingerprint 00:00 - 00:30 - free time"

    p = ds.get_pomodoro("06:00")
    assert p == None

    p = ds.get_pomodoro("08:00")
    assert p.fingerprint == "fingerprint 08:00 - 08:30 - morning"

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
    ds = Dispatcher()
    with pytest.raises(ValueError) as excinfo:
        ds.parse_pomodoros("some bad input")
    assert str(excinfo.value) == "bad input string, cannot split to 4 items separated by comma"


def test_tick():
    ds = Dispatcher()
    ds.tick("00:00")
    assert ds.active_pomodoro.fingerprint == "fingerprint 00:00 - 00:30 - free time"


def test_many_ticks():
    ds = Dispatcher()

    start = config.TZ.localize(dateutil.parser.parse("12:00"))
    end = config.TZ.localize(dateutil.parser.parse("18:00"))
    step = relativedelta(minutes=3)

    now = start
    while now < end:
        now += step
        ds.tick(now)


def test_print_schedule():
    ds = Dispatcher()

    cp = ds.current_pomodoro()
    ds.run_pomodoro(cp)

    for p in ds.pomodoros:
        caret = "   "
        if p.active:
            caret = ">> "
        line = f"{caret}{p.description}"
        print(line)


def test_print_united_pomodoros():
    ds = Dispatcher()

    cp = ds.current_pomodoro()
    ds.run_pomodoro(cp)

    for p in ds.united_pomodoros:
        caret = "   "
        if p.active:
            caret = ">> "
        line = f"{caret}{p.description}"
        print(line)


"""
def test_just_list_them():
    ds = Dispatcher()
    cp = ds.current_pomodoro()
    ds.run_pomodoro(cp)

    for p in ds.pomodoros:
        print(p.extended_description)
"""
