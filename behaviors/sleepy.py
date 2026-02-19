from behaviors.base import Behavior

class SleepyBehavior(Behavior):
    def enter(self):
        self.moth.inactive_time = 0
        self.moth.activity_level -= 1 if self.moth.activity_level > 0 else 0
    def update(self, dt):
        pass

    def exit(self):
        print("eepy")
        self.moth.controller.set("idle")


