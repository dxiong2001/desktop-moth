from moth.sprite import PixelSprite
import win32gui, win32con, win32api

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
        self.left_click = False

    def add(self, name, behavior):
        self.behaviors[name] = behavior

    def set(self, name):
        self.current = self.behaviors[name]
        self.current.enter()

    def update(self, dt, screen):
        if self.current:

            left_pressed = win32api.GetAsyncKeyState(win32con.VK_LBUTTON) < 0
            if left_pressed:
                if self.sprite.is_click_inside() and not self.left_click:
                    print("clicked")
                    self.moth.activity_level += 1 if self.moth.activity_level < 6 else 0
                    self.moth.inactive_level = 0
                    self.left_click = True
            else:
                self.left_click = False
                

            self.sprite.set_frame(self.current.frames[int(self.frame_index)])
            self.frame_index += self.frame_speed
            if self.frame_index >= len(self.current.frames):
                self.frame_index = 0
                self.current.exit()
            self.current.update(dt)
            self.sprite.draw(screen)
        
