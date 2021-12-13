from pomodoro import Pomodoro
from misc import current_time, midnight_fix

from config import config


class Dispatcher():
    def __init__(self, pomodoros = None) -> None:
        if pomodoros:
            self.pomodoros = pomodoros
        else:
            self.load_schedule()

        self.previous_pomodoro = None
        self.active_pomodoro = None
        self.reformatted = False

    def load_schedule(self) -> None:
        with open(config.SCHEDULE_FILE_PATH, 'r', encoding='UTF8') as f:
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
        if type(time) == str:
            time = midnight_fix(time)

        for p in self.pomodoros:
            if p.startint <= time and p.endint > time:
                return p
        return None
    
    def current_pomodoro(self):
        return self.get_pomodoro(current_time())

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
        self.reformat_pomodoros()
        pomodoro.start_routine()


    def tick(self, forcedtime = None):
        time = current_time(forcedtime)
        print('Dispatcher tick event', time)

        if self.active_pomodoro:
            
            active_minutes = int(time - self.active_pomodoro.startint)
            if active_minutes >= config.POMODORO_DURATION:
                if self.active_pomodoro.next:
                    self.active_pomodoro.rest.start()

        p = self.get_pomodoro(time)
        if p:
            self.check_and_fire(p)


    def check_and_fire(self, pomodoro: Pomodoro) -> None:
        if not pomodoro.active:
            self.run_pomodoro(pomodoro)
        
    @property
    def united_pomodoros(self):
        """ skipped repeated pomodoros of same type """
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

    def get_schedule(self, united = True):
        """ used for print shedule to user on request """
        pool = self.pomodoros
        if united:
            pool = self.united_pomodoros
        
        s = []
        for p in pool:
            s.append(p.description)
        return '\n'.join(s)

            
