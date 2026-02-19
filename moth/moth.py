from moth.controller import MothController

class Moth:
    def __init__(self, pose=(0,0)):
        self.controller = MothController(self)
        self.inactive_time = 0
        self.was_clicked = False
        self.spawn_zs = False
        self.activity_level = 3
        
        

    def update(self, dt, screen):
        self.controller.update(dt, screen)
    
    