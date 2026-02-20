from moth.sprite import PixelSprite
import win32gui, win32con, win32api
import math

class MothController:
    def __init__(self, moth, frame_index = 0, frame_speed = 0.22):
        self.moth = moth
        self.sprite = PixelSprite((0,200))
        self.behaviors = {}
        self.affects = {}
        self.current = None
        self.frame_index = frame_index
        self.frame_speed = frame_speed
        self.asleep = False
        self.double_blink = False
        self.left_click = False
        self.secondary_particles = []
        self.current_affect = None

    def add(self, name, behavior):
        self.behaviors[name] = behavior

    def add_affect(self, name, affect):
        self.affects[name] = affect

    def set(self, name):
        self.current = self.behaviors[name]
        self.current.enter()

    def set_affect(self, name):
        self.current_affect = self.affects[name]
        self.current_affect.enter()

    def update(self, dt, screen):
        if self.current_affect:
            self.current_affect.update(dt)
            for s in self.secondary_particles:
                drift_x = s["base_x"] + math.sin(s["wave_offset"]) * s["amplitude"]
                frame_img = self.current_affect.frames[int(s["frame"])].copy()
                frame_img.set_alpha(s["alpha"])
                screen.blit(frame_img, (drift_x, s["y"]))
        if self.current:

            left_pressed = win32api.GetAsyncKeyState(win32con.VK_LBUTTON) < 0
            if left_pressed:
                if self.sprite.is_click_inside() and not self.left_click:
                    if self.current_affect:
                        self.current_affect.exit()
                    self.current_affect = None
                    print("clicked")
                    self.set("honk")
                    

                    self.frame_index = 0
                    self.moth.activity_level += 1 if self.moth.activity_level < 6 else 0
                    self.moth.inactive_time = 0
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
        
        
