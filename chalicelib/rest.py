import random
import re

from chalicelib.config import Config
from chalicelib.telegram import send_telegram_message

class Rest():

    def __init__(self, parent_pomodoro) -> None:
        self.rest_messages = []
        self.load_rest_messages()
        self.rest_started = False
        self.parent_pomodoro = parent_pomodoro
  
    def load_rest_messages(self) -> None:
        with open(Config.REST_MESSAGES_FILE_PATH, 'r', encoding='UTF8') as f:
            lines = f.readlines()
            for line in lines:
                self.rest_messages.append(re.sub(r'[\n]', '', line))

    def random_message(self) -> str:
        return random.choice(self.rest_messages)

    @property
    def next_announce(self) -> str:
        if self.parent_pomodoro.next.text == self.parent_pomodoro.text:
            return ''

        line = f', next: {self.parent_pomodoro.next.text}'

        return line

    def start(self) -> None:
        ''' fires when pomodoros' 25 minutes ends and rest time for 5 minutes starts '''

        if self.rest_started:
            return # return early to prevent multiple notifications

        send_telegram_message(f'                                                          {self.random_message()}{self.next_announce}\n------- ------- ------- ------- ------- ------- ------- ------- ')
        self.rest_started = True
