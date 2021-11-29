from chalicelib.ssm_parameter import SSMParameter

from chalicelib.pomodoro import Pomodoro
from chalicelib.misc import current_time

from chalicelib.config import Config

from chalicelib.cw_log import CWLog

class Dispatcher():
    def __init__(self, pomodoros = None) -> None:
        if pomodoros:
            self.pomodoros = pomodoros

        self.previous_pomodoro = None
        self.active_pomodoro = None
        self.reformatted = False

    def load_schedule(self) -> None:
        with open(Config.SCHEDULE_FILE_PATH, 'r', encoding='UTF8') as f:
            self.parse_pomodoros( f.readlines() )

    def parse_pomodoros(self, raw_lines) -> None:
        self.pomodoros = []
        for line in raw_lines:
            self.pomodoros.append(Pomodoro(line))

        # filling .previous value in every pomodoro
        for i in range(1, len(self.pomodoros)):
            self.pomodoros[i].previous = self.pomodoros[i - 1]

        # filling .next value in every pomodoro
        for i in range(len(self.pomodoros) - 1):
            self.pomodoros[i].next = self.pomodoros[i + 1]

        
    def get_pomodoro(self, time):
        for p in self.pomodoros:
            if p.startint <= time and p.endint > time:
                return p
        return None
    
    def current_pomodoro(self):
        current = self.get_pomodoro(current_time())
        
        return current

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

        for p in self.pomodoros:
            p.active = False
        
        self.active_pomodoro = pomodoro
        self.mark_next_pomodoros_as_active()
        self.reformat_pomodoros()
        pomodoro.start_routine()


    def tick(self, forcedtime = None):
        # print('tick:', forcedtime)

        CWLog.send_cw_log('Dispatcher tick event')

        time = current_time(forcedtime)

        if self.active_pomodoro:
            active_minutes = int(time) - self.active_pomodoro.startint
            if active_minutes >= self.active_pomodoro.duration:
                self.active_pomodoro.rest.start()

        p = self.get_pomodoro(time)
        if p:
            self.check_and_fire(p)


    def check_and_fire(self, pomodoro: Pomodoro) -> None:

        if SSMParameter.get() == pomodoro.fingerprint:
            return

        SSMParameter.save(pomodoro.fingerprint)
        self.run_pomodoro(pomodoro)
        

    def mark_next_pomodoros_as_active(self):
        for i in range(len(self.pomodoros)):
            p = self.pomodoros[i]
            if p.active or i == 0:
                continue
            
            prev = self.pomodoros[i-1]
            if p.text == prev.text and prev.active:
                p.active = True

    @property
    def united_pomodoros(self):
        united = [self.pomodoros[0]]
        last = self.pomodoros[0]        
        for i, p in enumerate(self.pomodoros):
            if p == last:
                continue
            if p.text == last.text:
                last.end, last.endint = p.end, p.endint
                continue
            else:
                last = p            
            united.append(last)        
        return united

    def reformat_pomodoros(self):
        if self.reformatted:
            return

        l = len(self.pomodoros)
        for i in range(len(self.pomodoros)):
            p = self.pomodoros[i]

            for j in range( min(20, l - i) ):
                if i+j+1 >= l:
                    continue
                
                n = self.pomodoros[i+j+1]
                if n.text == p.text:
                    if not n.reformatted:
                        n.reformatted_text = f'{n.text}...'
                        n.reformatted = True                    
                        p.reformatted_text = f'{p.text } until {n.end}'
                        p.reformatted = True
                    continue
                    
                break
        self.reformatted = True
