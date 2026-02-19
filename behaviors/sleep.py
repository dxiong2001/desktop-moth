from behaviors.base import Behavior

class SleepBehavior(Behavior):
    def enter(self):
        self.moth.spawn_zs = True

    def update(self, dt):
        # Wake if clicked
        if self.moth.was_clicked:
            self.moth.spawn_zs = False
            self.moth.controller.set("idle")

    def exit(self):
        pass