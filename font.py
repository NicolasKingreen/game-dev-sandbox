import pygame


pygame.font.init()
DEFAULT_FONT = pygame.font.SysFont(None, 12)
DEFAULT_FONT_18 = pygame.font.SysFont(None, 18)
DEFAULT_FONT_24 = pygame.font.SysFont(None, 24)


class FontManager:
    def __init__(self):
        pygame.font.init()
        self.DEFAULT_FONT = pygame.font.SysFont(None, 12)
