import pygame


from settings import DRAW_DEBUG
from colors import *
from font import DEFAULT_FONT_18 as DEFAULT_FONT


class Label:
    def __init__(self, rect, text):
        self.rect = rect

        self.text_surf = DEFAULT_FONT.render(text, True, PURPLE_NAVY)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, surface):
        surface.blit(self.text_surf, self.text_rect)
        if DRAW_DEBUG:
            pygame.draw.rect(surface, (255, 0, 0), self.rect, 1)
            pygame.draw.rect(surface, (255, 0, 0), self.text_rect, 1)
