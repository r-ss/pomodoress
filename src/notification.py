from threading import Timer

from telegram import Bot

from config import config
from log import log


def delete_notification_after_delay(notification):
    notification.thread.cancel()
    notification.delete()
    del notification


class Notification:
    def __init__(self, message) -> None:
        self.telegram_chat_id = config.TELEGRAM_USER
        self.bot = Bot(token=config.TELEGRAM_TOKEN)
        self.delete_delay = config.TELEGRAM_DELETE_NOTIFICATIONS  # Notification will be auto deleted in telegram after this period, seconds
        self.message = message

        self.telegram_message_id = None
        self.thread = None

        self.send()

    def delete(self) -> None:
        log("deleting notification", level="debug")
        self.bot.deleteMessage(chat_id=self.telegram_chat_id, message_id=self.telegram_message_id)

    def send(self) -> None:
        if config.TELEGRAM_ENABLE_SENDING:
            log(f"sending message: {self.message}")
            msg = self.bot.send_message(config.TELEGRAM_USER, text=self.message)
            if msg["message_id"]:
                self.telegram_message_id = int(msg["message_id"])
                if self.delete_delay:
                    self.thread = Timer(self.delete_delay, delete_notification_after_delay, [self])
                    self.thread.start()
        else:
            log(f"fake telegram - {self.message}", level="warning")
