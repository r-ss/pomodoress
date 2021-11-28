import re

from chalicelib.rest import Rest
from chalicelib.misc import midnight_fix
from chalicelib.config import Config
from chalicelib.telegram import send_telegram_message

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
        self.reformatted = False
        self.reformatted_text = self.text
        # self.notified = False # marks when notification sends to user

        # Rest object is in response for 5-minutes resting time window when pomodoros 25 minutes passes
        self.rest = Rest(self) # pass this pomodoro as parent_pomodoro for Rest object

        self.duration = Config.POMODORO_DURATION # default pomodoro duration 25 minutes
        self.previous = None # previous Pomodoro in queue
        self.next = None # next Pomodoro in queue


    @property
    def description(self) -> str:
        return f'{self.emoji} {self.start} - {self.end} - {self.formtext}'

    @property
    def formtext(self) -> str:
        if self.reformatted:
            return self.reformatted_text
        return self.text

    def start_routine(self) -> None:
        # print('> start routine', self.description)

        # not send notification if we have long uuproductive activities in a row
        if any(w in self.text for w in Config.UNPRODUCTIVE_ACTIVITIES) and any(z in self.previous.text for z in Config.UNPRODUCTIVE_ACTIVITIES):
            self.rest_started = True
            return


        send_telegram_message(f'{self.emoji} {self.start} - {self.formtext}')
        self.active = True

    
    def end_routine(self) -> None:
        # print('> end routine', self.description)
        self.active = False

    
