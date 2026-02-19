from behaviors.base import Behavior
import random

class BlinkBehavior(Behavior):
    def enter(self):
        self.timer = 0
        


    def update(self, dt):
        pass

    def exit(self):
        if not self.moth.controller.double_blink and random.random() < 0.6:
            self.moth.controller.set("blink")
            self.moth.controller.double_blink = True
        else:
            self.moth.controller.set("idle")


