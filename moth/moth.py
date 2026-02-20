from moth.controller import MothController
import pygame

class Moth:
    def __init__(self, width, height, pose=(0,0)):
        self.controller = MothController(self)
        self.sprite_width = width
        self.sprite_height = height
        self.inactive_time = 0
        self.was_clicked = False
        self.spawn_zs = False
        self.activity_level = 1
        self.honk = [pygame.mixer.Sound('./assets/audio/honk/skysfx-default001.mp3'),
                             pygame.mixer.Sound('./assets/audio/honk/skysfx-default002.mp3'),
                             pygame.mixer.Sound('./assets/audio/honk/skysfx-default003.mp3'),
                             pygame.mixer.Sound('./assets/audio/honk/skysfx-default004.mp3')]
        
        

    def update(self, dt, screen):
        self.controller.update(dt, screen)
    
    