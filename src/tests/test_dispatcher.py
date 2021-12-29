import pytest
from dispatcher import Dispatcher

from config import config


def test_parsing():
    ds = Dispatcher()

    with open(config.SCHEDULE_FILE_PATH, "r", encoding="UTF8") as f:
        ds.parse_pomodoros(f.readlines())

    p = ds.get_pomodoro("0:00")
    assert p.fingerprint == "fingerprint 0:00 - 0:30 - free time"

    p = ds.get_pomodoro("6:00")
    assert p == None

    p = ds.get_pomodoro("8:00")
    assert p.fingerprint == "fingerprint 8:00 - 8:30 - morning"

    p = ds.get_pomodoro("23:00")
    assert p.fingerprint == "fingerprint 23:00 - 23:30 - free time"

    p = ds.get_pomodoro("23:30")
    assert p.fingerprint == "fingerprint 23:30 - 0:00 - free time"

    p = ds.get_pomodoro("23:54")
    assert p.fingerprint == "fingerprint 23:30 - 0:00 - free time"

    p = ds.get_pomodoro("23:55")
    assert p.fingerprint == "fingerprint 23:30 - 0:00 - free time"

    p = ds.get_pomodoro("23:59")
    assert p.fingerprint == "fingerprint 23:30 - 0:00 - free time"


def test_bad_input():
    ds = Dispatcher()
    with pytest.raises(ValueError) as excinfo:
        ds.parse_pomodoros("some bad input")
    assert str(excinfo.value) == "bad input string, cannot split to 4 items separated by comma"


def test_tick():
    ds = Dispatcher()
    # ds.load_schedule()

    ds.tick(str(2400))
    assert ds.active_pomodoro.fingerprint == "fingerprint 0:00 - 0:30 - free time"


def test_many_ticks():
    ds = Dispatcher()
    # ds.load_schedule()

    a = 600
    z = 3000
    t = 1

    counter = 0
    for i in range(int(a / t), int(z / t)):
        ds.tick(str(i * t))
        counter += 1

    print("=== counter:", counter)


def test_print_schedule():
    ds = Dispatcher()
    # with open(config.SCHEDULE_FILE_PATH, "r", encoding="UTF8") as f:
    #     ds.parse_pomodoros(f.readlines())

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
    # with open(config.SCHEDULE_FILE_PATH, "r", encoding="UTF8") as f:
    # ds.parse_pomodoros(f.readlines())
    # ds.load_schedule()

    cp = ds.current_pomodoro()
    ds.run_pomodoro(cp)

    for p in ds.united_pomodoros:
        caret = "   "
        if p.active:
            caret = ">> "
        line = f"{caret}{p.description}"
        print(line)
