import random
import re

from config import config
from log import log
from notification import Notification


class Rest:

    active = False

    def __init__(self, parent_pomodoro) -> None:

        # self.rest_messages = self.load_rest_messages()
        self.rest_messages = self.load_rest_messages()

        self.parent_pomodoro = parent_pomodoro

    def load_rest_messages(self) -> None:
        log("load_rest_messages")
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
            return f" next: {self.parent_pomodoro.next.text}"
        return ""

    def run(self) -> None:
        """fires when pomodoros' 25 minutes ends and rest time for 5 minutes starts"""

        if self.active:
            return

        log(f"rest.run() for {self.parent_pomodoro.description}", level="debug")

        if any(w in self.parent_pomodoro.text for w in config.UNPRODUCTIVE_ACTIVITIES):
            self.active = True
            return

        # also not send rest announces before 10:00
        if self.parent_pomodoro.start.hour < 10:
            self.active = True
            return

        self.active = True
        _ = Notification(f"{self.random_message()}{self.next_announce}")
