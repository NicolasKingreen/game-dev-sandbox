import pygame
from pygame.locals import *

import os
import psutil


WIN_SIZE = WIN_WIDTH, WIN_HEIGHT = 640, 480


class Application:

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.main_surface = pygame.display.set_mode(WIN_SIZE)
        self.main_rect = self.main_surface.get_rect()
        pygame.display.set_caption("Pixelation Demo")
        self.process = psutil.Process(os.getpid())
        self.debug_time_passed_ms = 0
        self._is_running = False

        self.image_surf = pygame.image.load("data/image.jpg").convert()
        self.image_rect = self.image_surf.get_rect(center=(WIN_WIDTH//2, WIN_HEIGHT//2))
        self.temp_surf = self.image_surf.copy()
        self.temp_rect = self.image_rect.copy()

        self.image_size = pygame.Vector2(self.image_rect.size)
        self.temp_size = pygame.Vector2(self.temp_rect.size)

        self.animation_time_ms = 2000
        self.shrink_speed_x = self.image_size.x / self.animation_time_ms
        self.shrink_speed_y = self.image_size.y / self.animation_time_ms
        self.time_passed_ms = 0

        self.done = False

    def run(self):
        self._is_running = True
        while self._is_running:

            if self.debug_time_passed_ms > 100:
                print(f"CPU: {self.process.cpu_percent()}%\t"
                      f"RAM: {self.process.memory_info().rss / float(2**20):.2f} MB\t"
                      f"Current time: {self.time_passed_ms/1000.:.2f} s")
                self.debug_time_passed_ms = 0

            frame_time_ms = self.clock.tick()

            if not self.done:
                self.time_passed_ms += frame_time_ms
                self.debug_time_passed_ms += frame_time_ms

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.stop()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.stop()

            if self.temp_size.x > self.shrink_speed_x * frame_time_ms:
                self.temp_size.x -= self.shrink_speed_x * frame_time_ms
                #self.temp_rect.inflate_ip(-self.shrink_speed_x * frame_time_ms, 0)
            if self.temp_size.y > self.shrink_speed_y * frame_time_ms:
                self.temp_size.y -= self.shrink_speed_y * frame_time_ms
                #self.temp_rect.inflate_ip(0, -self.shrink_speed_y * frame_time_ms)
            else:
                self.done = True
                #print(self.temp_rect.size)

            # if self.time_passed_ms < self.animation_time_ms:
            self.temp_rect.size = int(self.temp_size.x), int(self.temp_size.y)
            self.temp_surf = pygame.transform.scale(self.image_surf, self.temp_rect.size)
            self.temp_surf = pygame.transform.scale(self.temp_surf, self.main_rect.size)

            self.main_surface.fill((255, 255, 255))
            self.main_surface.blit(self.temp_surf, (0, 0))
            pygame.display.update()

        pygame.quit()

    def stop(self):
        self._is_running = False


if __name__ == "__main__":
    Application().run()
