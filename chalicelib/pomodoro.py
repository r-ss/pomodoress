import re

from chalicelib.rest import Rest
from chalicelib.misc import midnight_fix

from chalicelib.config import Config

class Pomodoro():
    def __init__(self, rawrow: str) -> None:

        if not rawrow or type(rawrow) != str:
            raise ValueError('bad input, string expected')

        rawrow = re.sub(r'["/\n]', '', rawrow).split(',')

        if len(rawrow) != 4:
            raise ValueError('bad input string, cannot split to 4 items separated by comma')

        self.start, self.startint = rawrow[0], midnight_fix(rawrow[0])
        self.end, self.endint = rawrow[1], midnight_fix(rawrow[1])

        self.emoji = rawrow[2]
        self.text = rawrow[3]
        self.fingerprint = f'fingerprint {self.start} - {self.end} - {self.text}'

        self.active = False
        # self.notified = False # marks when notification sends to user

        # Rest object is in response for 5-minutes resting time window when pomodoros 25 minutes passes
        self.rest = Rest(self) # pass this pomodoro as parent_pomodoro for Rest object

        self.duration = Config.POMODORO_DURATION # default pomodoro duration 25 minutes
        self.next = None # next Pomodoro in timed queue

    @property
    def description(self) -> str:
        return f'Pomodoro - {self.start} - {self.end}, {self.emoji} {self.text}'

    def start_routine(self) -> None:
        # print('> start routine', self.description)
        self.active = True
    
    def end_routine(self) -> None:
        # print('> end routine', self.description)
        self.active = False

    
