import random
from behaviors.base import Behavior

class IdleBehavior(Behavior):
    def enter(self):
        self.timer = 0
        self.moth.controller.double_blink = False

    def update(self):
        self.timer += dt

        
        
    
    def exit(self):
        rand = random.random()
        if rand < 0.18:
            self.moth.controller.set("blink")
        elif rand < 0.2:
            self.moth.controller.set("sleepy")
            
