import pytest
from pomodoro import Pomodoro


def test_basic():
    p = Pomodoro('"14:00","14:30","","sport"\n')
    assert p.fingerprint == "fingerprint 14:00 - 14:30 - sport"
    assert p.rest.parent_pomodoro == p


def test_midnight():
    p = Pomodoro('"0:00","0:30","","free time\n"')
    assert p.fingerprint == "fingerprint 0:00 - 0:30 - free time"


def test_incomplete_input_string():
    with pytest.raises(ValueError) as excinfo:
        p = Pomodoro('"0:00","0:30","free time"')
    assert (
        str(excinfo.value)
        == "bad input string, cannot split to 4 items separated by comma"
    )


def test_empty_string():
    with pytest.raises(ValueError) as excinfo:
        p = Pomodoro("")
    assert str(excinfo.value) == "bad input, string expected"


def test_bad_input_type():
    with pytest.raises(ValueError) as excinfo:
        p = Pomodoro(666)
    assert str(excinfo.value) == "bad input, string expected"
