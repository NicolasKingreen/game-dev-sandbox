import pygame


class Slider:
    def __init__(self, rect, init_value=0.0):
        self.rect = rect
        self.value = 0.0

    def draw(self, surface):
        pygame.draw.line(surface, (12, 12, 12),
                         self.rect.midleft,
                         self.rect.midright)
