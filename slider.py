import pygame


from settings import *
from colors import *
from font import DEFAULT_FONT

FIRST_COLOR = MAXIMUM_BLUE_PURPLE
SECONDARY_COLOR = PURPLE_NAVY


# TODO: step implementation; get rid of interaction rect, make it relative


class Slider:
    def __init__(self, rect, min_value, max_value, init_value=None):
        self.rect = rect

        self.min_value = min_value
        self.max_value = max_value
        self.value = init_value if init_value is not None else (self.min_value + self.max_value) // 2

        if not self.min_value <= self.value <= self.max_value:
            raise ValueError

        self.height = 4  # central line
        self.cursor_radius = 6
        self.text_padding = self.cursor_radius

        self.min_value_text_surf = DEFAULT_FONT.render(str(self.min_value), True, SECONDARY_COLOR)
        self.min_value_text_rect = self.min_value_text_surf.get_rect(midleft=self.rect.midleft)

        self.max_value_text_surf = DEFAULT_FONT.render(str(self.max_value), True, SECONDARY_COLOR)
        self.max_value_text_rect = self.max_value_text_surf.get_rect(midright=self.rect.midright)

        # make rect wider but after line's end sets values to min or max
        self.center_line_x = self.rect.left + self.min_value_text_rect.width + self.text_padding
        self.center_line_width = self.rect.width - self.min_value_text_rect.width - self.max_value_text_rect.width - self.text_padding * 2
        self.center_line_interaction_rect = pygame.Rect(self.center_line_x, self.rect.midleft[1] - self.height // 2,
                                                        self.center_line_width, self.height)
        self.center_line_interaction_rect.inflate_ip(0, self.height * 3)

        # make width dynamic
        self.badge_distance = 10
        self.cursor_badge_rect = pygame.Rect(0, 0, 30, 12)

        value_type = self._get_value_type()
        self.round = lambda n: round(n, 3) if value_type is float else int(n)

        self._recalculate_cursor_x()

        self.grabbed = False

    def _get_value_type(self):
        if all(type(value) for value in [self.min_value, self.value, self.max_value]):
            return type(self.min_value)
        return float

    def update(self, mouse_pos):
        # if pygame.mouse.get_pressed()[0] and self.center_line_interaction_rect.collidepoint(mx, my):

        # make it happen once
        if self.grabbed:
            mx, my = mouse_pos
            # mx -= 600  # surface offset  # TODO: take it out
            self.value = (mx - self.center_line_x) / self.center_line_width * (self.max_value - self.min_value) + self.min_value
            self.value = min(max(self.value, self.min_value), self.max_value)
            self._recalculate_cursor_x()
            # print(self.value)

    def handle_click(self, mx, my):
        if self.center_line_interaction_rect.collidepoint(mx, my):
            self.grabbed = True

    def grab_release(self):
        self.grabbed = False

    def _recalculate_cursor_x(self):
        self.cursor_x = self.center_line_x + (self.value - self.min_value) / (self.max_value - self.min_value) * self.center_line_width
        self.cursor_badge_rect.midbottom = self.cursor_x, self.rect.centery - self.badge_distance
        self.value_text_surf = DEFAULT_FONT.render(str(self.round(self.value)), True, AZURE_X11_WEB_COLOR)
        self.value_text_rect = self.value_text_surf.get_rect(center=self.cursor_badge_rect.center)

    def draw(self, surface):

        # center line
        pygame.draw.rect(surface, FIRST_COLOR,
                         (self.center_line_x,
                          self.rect.midleft[1] - self.height // 2,
                          self.center_line_width,
                          self.height),
                         border_radius=self.height // 2)

        # value cursor
        pygame.draw.circle(surface, FIRST_COLOR,
                           (self.cursor_x,
                            self.rect.centery),
                           self.cursor_radius)
        pygame.draw.rect(surface, SECONDARY_COLOR, self.cursor_badge_rect, border_radius=2)
        surface.blit(self.value_text_surf, self.value_text_rect)

        # left side
        surface.blit(self.min_value_text_surf, self.min_value_text_rect)

        # right side
        surface.blit(self.max_value_text_surf, self.max_value_text_rect)

        # debug rects
        if DRAW_DEBUG:
            pygame.draw.rect(surface, (255, 0, 0), self.rect, 1)
            pygame.draw.rect(surface, (255, 0, 0), self.center_line_interaction_rect, 1)
