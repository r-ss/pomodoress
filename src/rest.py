import random
import re

from config import config

from notification import Notification
from log import log


class Rest:

    active = False

    def __init__(self, parent_pomodoro) -> None:
        self.rest_messages = self.load_rest_messages()
        self.parent_pomodoro = parent_pomodoro
        self.duration = config.REST_DURATION  # default rest duration 5 minutes

    def load_rest_messages(self) -> None:
        messages = []
        with open(config.REST_MESSAGES_FILE_PATH, "r", encoding="UTF8") as f:
            lines = f.readlines()
            for line in lines:
                messages.append(re.sub(r"[\n]", "", line))
        return messages

    def random_message(self) -> str:
        return random.choice(self.rest_messages)

    @property
    def next_announce(self) -> str:
        if self.parent_pomodoro.next:
            if self.parent_pomodoro.next.text == self.parent_pomodoro.text:
                return ""

            line = f" next: {self.parent_pomodoro.next.text}"
            return line
        return ""

    def start(self) -> None:
        """fires when pomodoros' 25 minutes ends and rest time for 5 minutes starts"""

        if self.active:
            return

        # CWLog.send_cw_log(f'Rest start for: { self.parent_pomodoro.text }')

        # if self.rest_started:
        # return # return early to prevent multiple notifications

        # do we actually need rest here? If we have free time, no need to announce Rest
        if any(w in self.parent_pomodoro.text for w in config.UNPRODUCTIVE_ACTIVITIES):
            self.active = True
            return

        # also not send rest announces before 10:00
        if self.parent_pomodoro.startint < 1000:
            self.active = True
            return

        # if SSMParameter.get() == f'rest for {self.parent_pomodoro.fingerprint}':
        #     CWLog.send_cw_log(f'Rest skip because ssmparameter says it already fired: { self.parent_pomodoro.text }')
        #     return

        # send_telegram_message(f'{self.random_message()}{self.next_announce}')
        self.active = True
        rest_notification = Notification(f"{self.random_message()}{self.next_announce}")

        # SSMParameter.save(f'rest for {self.parent_pomodoro.fingerprint}')

        # CWLog.send_cw_log(f'Rest has been started for: { self.parent_pomodoro.text }')
