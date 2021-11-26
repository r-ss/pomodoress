from datetime import datetime

from chalicelib.ssm_parameter import SSMParameter

from chalicelib.pomodoro import Pomodoro
from chalicelib.misc import midnight_fix

from chalicelib.config import Config

class Dispatcher():
    def __init__(self, pomodoros = None) -> None:
        if pomodoros:
            self.pomodoros = pomodoros

        self.previous_pomodoro = None
        self.active_pomodoro = None

    def load_schedule(self) -> None:
        with open(Config.SCHEDULE_FILE_PATH, 'r', encoding='UTF8') as f:
            self.parse_pomodoros( f.readlines() )

    def parse_pomodoros(self, raw_lines) -> None:
        self.pomodoros = []
        for line in raw_lines:
            self.pomodoros.append(Pomodoro(line))

        # filling .next value in every pomodoro
        for i in range(len(self.pomodoros) - 1):
            self.pomodoros[i].next = self.pomodoros[i + 1]

    def get_pomodoro(self, time: str):

        if type(time) == str:
            time = midnight_fix(time)

        for p in self.pomodoros:
            if p.startint <= time and p.endint > time:
                return p
        return None
    
    def current_pomodoro(self):
        return self.get_pomodoro(datetime.now().strftime('%H%M'))

    def run_pomodoro(self, pomodoro) -> None:
        if not pomodoro:
            self.active_pomodoro = None
            return None

        if self.active_pomodoro:
            if self.active_pomodoro == pomodoro:
                return
            if self.previous_pomodoro:
                self.previous_pomodoro.end_routine()
            self.previous_pomodoro = self.active_pomodoro
        
        self.active_pomodoro = pomodoro
        # self.active_pomodoro.start_routine()
        pomodoro.start_routine()
        print('pomodoro run', pomodoro.description)

    def tick(self, time = None):
        if not time:
            time = datetime.now().strftime('%H%M')

        # print('input-time:', time)

        time = midnight_fix(time)

        if self.active_pomodoro:
            active_minutes = int(time) - self.active_pomodoro.startint
            if active_minutes >= self.active_pomodoro.duration:
                self.active_pomodoro.rest.start()

        p = self.get_pomodoro(time)
        if p:
            self.check_and_fire(p)

        # if time == cp.startint:
            # self.run_pomodoro(cp)

        # self.run_pomodoro()

    def check_and_fire(self, pomodoro: Pomodoro) -> None:

        if SSMParameter.get() == pomodoro.fingerprint:
            return

        SSMParameter.save(pomodoro.fingerprint)
        self.run_pomodoro(pomodoro)