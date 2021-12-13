from telegram import Bot
from config import config
from threading import Timer


def delete_notification_after_delay(notification):
    notification.thread.cancel()
    notification.delete()
    del notification


class Notification():

    telegram_chat_id = config.TELEGRAM_USER
    telegram_message_id = None
    thread = None

    def __init__(self, message, deletelater = False) -> None:
        self.bot = Bot(token=config.TELEGRAM_TOKEN)
        self.delete_delay = 75
        self.message = message
        
        self.send()
        return self

    
    def delete(self) -> None:
        print('deleting notification')
        self.bot.deleteMessage(chat_id=self.telegram_chat_id, message_id=self.telegram_message_id)
        
   
    def send(self) -> None:
        if config.TELEGRAM_ENABLE_SENDING:
            msg = self.bot.send_message(config.TELEGRAM_USER, text = self.message)
            if msg['message_id']:
                self.telegram_message_id = int(msg['message_id'])
                self.thread = Timer(self.delete_delay, delete_notification_after_delay, [self])
                self.thread.start()
        else:
            print('sending telegram', self.message)

    
