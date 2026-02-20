from behaviors.base import Behavior
import random
import pygame

class HonkBehavior(Behavior):
    def enter(self):
        self.timer = 0
        self.moth.controller.set_affect("honk_glow")
        self.moth.honk[random.randint(0,3)].play()
        
    def update(self, dt):
        pass

    def exit(self):
        self.moth.controller.set("idle")


