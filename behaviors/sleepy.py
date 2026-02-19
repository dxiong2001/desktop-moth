from behaviors.base import Behavior

class SleepyBehavior(Behavior):
    def enter(self):
        self.timer = 0

    def update(self):
        pass

    def exit(self):
        self.moth.controller.set("idle")


