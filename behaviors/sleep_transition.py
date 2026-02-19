from behaviors.base import Behavior

class SleepTransitionBehavior(Behavior):
    def enter(self):
        pass

    def update(self):
        pass

    def exit(self):
        self.moth.controller.set("sleep")
