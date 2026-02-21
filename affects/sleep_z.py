from affects.base import Behavior
import random

class SleepZBehavior(Behavior):
    def enter(self):
        print("aaa")
        
    def update(self, dt):
        if random.random() < 0.008 and len(self.moth.controller.secondary_particles) < 3:
            self.moth.controller.secondary_particles.append({
                    "base_x":  80,
                    "y": 200,
                    "vy": -0.4,
                    "alpha": 255,
                    "frame": 0,
                    "frame_speed": random.uniform(0.1, 0.25),
                    "wave_offset": random.uniform(0, 6.28),  # start phase
                    "wave_speed": random.uniform(0.03, 0.06),
                    "amplitude": random.uniform(6, 14)
                })
        for s in self.moth.controller.secondary_particles:
            s["y"] += s["vy"]
            s["alpha"] -= 3

            # Animate frame
            s["frame"] += s["frame_speed"]
            if s["frame"] >= len(self.moth.controller.current_affect.frames):
                s["frame"] = 0

            # ⭐ Update sine phase
            s["wave_offset"] += s["wave_speed"]
        self.moth.controller.secondary_particles = [s for s in self.moth.controller.secondary_particles if s["alpha"] > 0]

    def exit(self):
        self.moth.controller.secondary_particles = []
        


