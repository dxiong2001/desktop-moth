from abc import ABC, abstractmethod
class Behavior(ABC):
    def __init__(self, moth, frames):
        self.moth = moth
        self.frames = frames
        self.timer = 0

    @abstractmethod
    def enter(self):
        """Called when behavior starts"""
        pass

    @abstractmethod
    def update(self):
        """Called every frame"""
        pass
    
    @abstractmethod
    def exit(self):
        """Called when behavior ends"""
        pass