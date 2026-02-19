from moth.sprite import PixelSprite

class MothController:
    def __init__(self, moth, frame_index = 0, frame_speed = 0.22):
        self.moth = moth
        self.sprite = PixelSprite()
        self.behaviors = {}
        self.current = None
        self.frame_index = frame_index
        self.frame_speed = frame_speed
        self.asleep = False
        self.double_blink = False

    def add(self, name, behavior):
        self.behaviors[name] = behavior

    def set(self, name):
        self.current = self.behaviors[name]
        self.current.enter()

    def update(self, screen):
        if self.current:
            self.sprite.set_frame(self.current.frames[int(self.frame_index)])
            self.frame_index += self.frame_speed
            if self.frame_index >= len(self.current.frames):
                self.frame_index = 0
                self.current.exit()
            self.current.update(dt)
            self.sprite.draw(screen)
        
