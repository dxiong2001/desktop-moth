import pygame

class PixelSprite:
    def __init__(self, pos=(0, 0)):
        self.x, self.y = pos
        self.frame = None
        self.mask = None

    def set_frame(self, surface):
        """Update current frame and rebuild mask."""
        self.frame = surface
        self.mask = pygame.mask.from_surface(surface)

    def set_pos(self, pos):
        self.x, self.y = pos

    def draw(self, screen):
        if self.frame:
            screen.blit(self.frame, (self.x, self.y), special_flags = pygame.BLEND_PREMULTIPLIED)

    def fade_surface(self, sprite, alpha):
        faded = sprite.copy()

        # Directly scale alpha channel
        arr = pygame.surfarray.pixels_alpha(faded)
        arr[:] = alpha
        del arr  # unlock the surface

        return faded
    
    def is_click_inside(self):
        """Pixel-perfect click detection."""
        if not self.frame or not self.mask:
            return False

        mx, my = pygame.mouse.get_pos()

        # Convert screen coords → sprite-local coords
        rel_x = mx - self.x
        rel_y = my - self.y

        # Bounds check first (prevents IndexError)
        if 0 <= rel_x < self.frame.get_width() and \
           0 <= rel_y < self.frame.get_height():
            return self.mask.get_at((rel_x, rel_y))

        return False
