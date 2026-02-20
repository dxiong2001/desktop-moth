from affects.base import Behavior
import random

class HonkGlowBehavior(Behavior):
    def enter(self):
        self.moth.controller.secondary_particles.append({
            "base_x":  -10,
            "y": 160,
            "scale": 0.5,
            "alpha": 220,
            "frame": 0,
            "frame_speed": 1.2,
            "wave_offset": 0,
            "wave_speed": 0,
            "amplitude": 0,
        })
        
    def update(self, dt):
        for s in self.moth.controller.secondary_particles:
            s["scale"] += 0.2
            s["alpha"] -= 35
            s["frame"] += s["frame_speed"]
            if s["frame"] >= len(self.moth.controller.current_affect.frames):
                s["frame"] = 0
                self.moth.controller.secondary_particles.pop()
            

           
        self.moth.controller.secondary_particles = [s for s in self.moth.controller.secondary_particles if s["alpha"] > 0]

    def exit(self):
        self.moth.controller.current_affect = None
        


