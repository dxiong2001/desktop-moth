from affects.base import Behavior
import random

class HonkGlowBehavior(Behavior):
    def enter(self):
        self.moth.controller.secondary_particles.append({
            "base_x":  -10,
            "y": 190,
            "scale": 1,
            "alpha": 255,
            "frame": 0,
            "frame_speed": 1.35,
            "wave_offset": 0,
            "wave_speed": 0,
            "amplitude": 0,
        })
        
    def update(self, dt):
        for s in self.moth.controller.secondary_particles:
            s["frame"] += s["frame_speed"]
            if s["frame"] >= len(self.moth.controller.current_affect.frames):
                s["frame"] = 0
                self.moth.controller.secondary_particles.pop()
            

           

    def exit(self):
        self.moth.controller.current_affect = None
        


