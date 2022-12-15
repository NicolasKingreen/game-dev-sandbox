import pygame
from pygame.locals import *

from random import randint
from math import exp


from colors import *
from slider import Slider


WIN_SIZE = 800, 600

SPLIT_SCREEN_COEFFICIENT = 0.75
RENDER_SIZE = int(WIN_SIZE[0] * SPLIT_SCREEN_COEFFICIENT), WIN_SIZE[1]
UI_SIZE = int(WIN_SIZE[0] * (1 - SPLIT_SCREEN_COEFFICIENT)), WIN_SIZE[1]

TARGET_FPS = 60


# TODO: labels, slider functionality


def lerp(start, end, time):
    # time is a value between 0 and 1
    return start * (1 - time) + end * time


def lerp2(start, end, log_rate, frame_time):
    rate = exp(log_rate)
    return lerp(end, start, exp(-rate * frame_time))


def smooth_over(dt, smooth_time, convergence_fraction):
    return 1 - (1 - convergence_fraction) ** (dt / smooth_time)


def main():
    pygame.init()
    pygame.display.set_caption("Game Dev Sandbox")
    display_surface = pygame.display.set_mode(WIN_SIZE)
    render_surface = pygame.Surface((WIN_SIZE[0] * 0.75, WIN_SIZE[1]))
    ui_surface = pygame.Surface((WIN_SIZE[0] * 0.25, WIN_SIZE[1]))

    clock = pygame.time.Clock()

    x, y = RENDER_SIZE[0] // 2, RENDER_SIZE[1] // 2  # start position
    x1, y1 = randint(0, RENDER_SIZE[0]), randint(0, RENDER_SIZE[1])  # end position

    animation_time = 500  # ms
    current_time = 0

    animation_time_slider = Slider(pygame.Rect(UI_SIZE[0] * 0.05,
                                               30,
                                               UI_SIZE[0] * 0.9,
                                               25),
                                   min_value=0,
                                   max_value=1000,
                                   init_value=500)

    rate_slider = Slider(pygame.Rect(UI_SIZE[0] * 0.05,
                                     85,
                                     UI_SIZE[0] * 0.9,
                                     25),
                         min_value=0.001,
                         max_value=0.01,
                         init_value=0.005)

    while True:
        frame_time = clock.tick(TARGET_FPS)  # ms
        current_time += frame_time

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return

        if current_time >= animation_time:
            current_time = 0
            # x0, x1 = x1, x0
            x1 = randint(0, RENDER_SIZE[0])
            y1 = randint(0, RENDER_SIZE[1])

        # print(current_time / animation_time)
        # x = lerp(x, x1, current_time / animation_time)
        # y = lerp(y, y1, current_time / animation_time)

        # TODO: frame time independence
        x = lerp(x, x1, 0.005 * frame_time)
        y = lerp(y, y1, 0.005 * frame_time)

        animation_time_slider.update()
        rate_slider.update()

        render_surface.fill(WHITE)
        pygame.draw.circle(render_surface, PURPLE_NAVY, (x, y), 10)

        ui_surface.fill(AZURE_X11_WEB_COLOR)
        animation_time_slider.draw(ui_surface)
        rate_slider.draw(ui_surface)

        display_surface.blit(render_surface, (0, 0))
        display_surface.blit(ui_surface, (WIN_SIZE[0] * 0.75, 0))
        pygame.display.update()


if __name__ == "__main__":
    main()

