import random
from behaviors.base import Behavior

class IdleBehavior(Behavior):
    def enter(self):
        self.timer = 0
        self.moth.controller.double_blink = False

    def update(self, dt):
        self.moth.inactive_time += dt
        # print(self.moth.inactive_time)

        
        
    
    def exit(self):
        rand = random.random()
        if self.moth.activity_level == 0:
            self.moth.controller.set("sleep_transition")
        else:
            if self.moth.inactive_time > 3:
                self.moth.controller.set("sleepy")
            else:
                if rand < 0.18:
                    self.moth.controller.set("blink")
            
                
            
