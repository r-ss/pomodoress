import pytest
from chalicelib.dispatcher import Dispatcher

from chalicelib.config import Config



def test_parsing():
    ds = Dispatcher()
    
    with open(Config.SCHEDULE_FILE_PATH, 'r', encoding='UTF8') as f:
        ds.parse_pomodoros( f.readlines() )

    p = ds.get_pomodoro('0:00')
    assert p.fingerprint == 'fingerprint 0:00 - 0:30 - free time'

    p = ds.get_pomodoro('6:00')
    assert p == None

    p = ds.get_pomodoro('8:00')
    assert p.fingerprint == 'fingerprint 8:00 - 8:30 - morning'

    p = ds.get_pomodoro('23:00')
    assert p.fingerprint == 'fingerprint 23:00 - 23:30 - free time'

    p = ds.get_pomodoro('23:30')
    assert p.fingerprint == 'fingerprint 23:30 - 0:00 - free time'

    p = ds.get_pomodoro('23:54')
    assert p.fingerprint == 'fingerprint 23:30 - 0:00 - free time'

    p = ds.get_pomodoro('23:55')
    assert p.fingerprint == 'fingerprint 23:30 - 0:00 - free time'

    p = ds.get_pomodoro('23:59')
    assert p.fingerprint == 'fingerprint 23:30 - 0:00 - free time'

def test_bad_input():
    ds = Dispatcher()
    with pytest.raises(ValueError) as excinfo:
        ds.parse_pomodoros( 'some bad input' )
    assert str(excinfo.value) == 'bad input string, cannot split to 4 items separated by comma'

def test_tick():
    ds = Dispatcher()
    with open(Config.SCHEDULE_FILE_PATH, 'r', encoding='UTF8') as f:
        ds.parse_pomodoros( f.readlines() )

    ds.tick( str(2400) )
    assert ds.active_pomodoro.fingerprint == 'fingerprint 0:00 - 0:30 - free time'

def test_many_ticks():
    ds = Dispatcher()
    with open(Config.SCHEDULE_FILE_PATH, 'r', encoding='UTF8') as f:
        ds.parse_pomodoros( f.readlines() )

    for t in range(600, 3000):
        ds.tick( str(t) )

    
    # assert ds.active_pomodoro.fingerprint == 'fingerprint 0:00 - 0:30 - free time'