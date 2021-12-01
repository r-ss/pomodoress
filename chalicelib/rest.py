import random
import re

from chalicelib.config import config
from chalicelib.telegram import send_telegram_message

from chalicelib.cw_log import CWLog

class Rest():

    def __init__(self, parent_pomodoro) -> None:
        self.rest_messages = []
        self.load_rest_messages()
        self.rest_started = False
        self.parent_pomodoro = parent_pomodoro
  
    def load_rest_messages(self) -> None:
        with open(config.REST_MESSAGES_FILE_PATH, 'r', encoding='UTF8') as f:
            lines = f.readlines()
            for line in lines:
                self.rest_messages.append(re.sub(r'[\n]', '', line))

    def random_message(self) -> str:
        return random.choice(self.rest_messages)

    @property
    def next_announce(self) -> str:
        if self.parent_pomodoro.next.text == self.parent_pomodoro.text:
            return ''

        line = f' next: {self.parent_pomodoro.next.text}'

        return line

    def start(self) -> None:
        ''' fires when pomodoros' 25 minutes ends and rest time for 5 minutes starts '''

        CWLog.send_cw_log(f'Rest start for: { self.parent_pomodoro.text }')

        if self.rest_started:
            return # return early to prevent multiple notifications

        # do we actually need rest here? If we have free time, no need to announce Rest
        if any(w in self.parent_pomodoro.text for w in config.UNPRODUCTIVE_ACTIVITIES):
            self.rest_started = True
            return

        # also not send rest announces before 10:00
        if self.parent_pomodoro.startint < 1000:
            self.rest_started = True
            return

        send_telegram_message(f'{self.random_message()}{self.next_announce}')
        self.rest_started = True

        CWLog.send_cw_log(f'Rest has been started for: { self.parent_pomodoro.text }')
