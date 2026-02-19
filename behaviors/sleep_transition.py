from behaviors.base import Behavior

class SleepTransitionBehavior(Behavior):
    def enter(self):
        self.moth.activity_level = 1

    def update(self, dt):
        pass

    def exit(self):
        self.moth.controller.set("sleep")
