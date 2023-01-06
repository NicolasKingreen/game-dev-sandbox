import pygame
from pygame.locals import *

import os
import psutil

from util import *


WIN_SIZE = WIN_WIDTH, WIN_HEIGHT = 640, 420


class Application:

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.main_surface = pygame.display.set_mode(WIN_SIZE)
        pygame.display.set_caption("Transformations Demo")
        self.process = psutil.Process(os.getpid())
        self.is_running = False

        # self.text_surf = pygame.image.load("text.png").convert_alpha()
        self.text_surf = pygame.font.Font("data/fonts/alagard.ttf", 65).render("Hello World!", True, (0, 0, 0))
        self.text_rect = self.text_surf.get_rect(center=(WIN_WIDTH//2, WIN_HEIGHT//2))

        scaling = 0.15  # 1 + x times
        self.max_width, self.max_height = [d * (1 + scaling) for d in self.text_rect.size]
        self.min_width, self.min_height = [d * (1 - scaling) for d in self.text_rect.size]

        self.temp_surf = self.text_surf.copy()
        self.temp_rect = self.text_rect.copy()
        self.temp_width, self.temp_height = self.text_rect.size
        self.target_width, self.target_height = self.max_width, self.max_height

        self.angle = 0
        self.target_angle = 360  # deg

        self.time_passed_ms = 0

    def run(self):
        self.is_running = True
        while self.is_running:
            frame_time_ms = self.clock.tick()
            frame_time_s = frame_time_ms / 1000.
            self.time_passed_ms += frame_time_ms
            # print(self.time_passed_ms)
            # print(int(self.clock.get_fps()))
            if self.time_passed_ms > 100:
                # print("System Resources Usage:")
                # print(f"CPU: {self.process.cpu_percent()}%\tRAM: {self.process.memory_info().rss / float(2**20):.2f} MB", end="\r")
                print(f"CPU: {self.process.cpu_percent()}%\tRAM: {self.process.memory_info().rss / float(2**20):.2f} MB")
                self.time_passed_ms = 0

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.stop()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.stop()
                    elif event.key == K_SPACE:
                        print(f"{memory_usage():.2f} MB")
                        self.textures = [self.text_surf.copy() for _ in range(1000)]
                        print(f"{memory_usage():.2f} MB")
                        import sys
                        print(sys.getrefcount(self.text_surf))
                        print(sys.platform)

            # updates
            self.update(frame_time_ms)

            # renders
            self.main_surface.fill((255, 255, 255))
            self.main_surface.blit(self.temp_surf, self.temp_rect)
            pygame.display.update()

        pygame.quit()

    def update(self, frame_time_ms):
        # TODO: sync animations time

        frame_time_s = frame_time_ms / 1000.

        # both sides eased
        self.temp_width = lerp(self.temp_width, self.target_width, f(1.0 - 0.1 ** frame_time_s))
        self.temp_height = lerp(self.temp_height, self.target_height, f(1.0 - 0.1 ** frame_time_s))
        self.angle = lerp(self.angle, self.target_angle, f(1.0 - 0.1 ** frame_time_s))
        if abs(self.temp_width - self.target_width) < self.target_width / self.temp_width * 1 \
                or abs(self.temp_height - self.target_width) < self.target_height / self.temp_height * 1 \
                or abs(self.angle - self.target_angle) < self.angle / self.target_angle * 1:
            self.target_width = self.min_width if self.target_width == self.max_width else self.max_width
            self.target_height = self.min_height if self.target_height == self.max_height else self.max_height
            self.angle = 0

        self.temp_surf = pygame.transform.scale(self.text_surf, (int(self.temp_width), int(self.temp_height)))
        self.temp_surf = pygame.transform.rotate(self.temp_surf, self.angle)
        self.temp_rect = self.temp_surf.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2))

    def stop(self):
        self.is_running = False


if __name__ == "__main__":
    Application().run()
