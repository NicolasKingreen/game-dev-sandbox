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


# TODO: labels, slider functionality, slider fix: make central line width the same, lerp update (rate and anim time)


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
    smooth_time = 5
    rate = 0.005

    animation_time_slider = Slider(pygame.Rect(UI_SIZE[0] * 0.05,
                                               30,
                                               UI_SIZE[0] * 0.9,
                                               25),
                                   min_value=250,
                                   max_value=1000,
                                   init_value=500)

    rate_slider = Slider(pygame.Rect(UI_SIZE[0] * 0.05,
                                     85,
                                     UI_SIZE[0] * 0.9,
                                     25),
                         min_value=0.001,
                         max_value=0.01,
                         init_value=0.005)

    smooth_time_slider = Slider(pygame.Rect(UI_SIZE[0] * 0.05,
                                            140,
                                            UI_SIZE[0] * 0.9,
                                            25),
                                min_value=0,
                                max_value=10,
                                init_value=5)

    while True:
        frame_time = clock.tick(TARGET_FPS)  # ms
        current_time += frame_time

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    # ui surface
                    mx, my = event.pos
                    mx -= RENDER_SIZE[0]  # surface offset
                    animation_time_slider.handle_click(mx, my)
                    rate_slider.handle_click(mx, my)
                    smooth_time_slider.handle_click(mx, my)
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    # ui surface
                    animation_time_slider.handle_release()
                    rate_slider.handle_release()
                    smooth_time_slider.handle_release()

        if current_time >= animation_time:
            current_time = 0
            # x0, x1 = x1, x0
            x1 = randint(0, RENDER_SIZE[0])
            y1 = randint(0, RENDER_SIZE[1])

        # print(current_time / animation_time)
        # x = lerp(x, x1, current_time / animation_time)
        # y = lerp(y, y1, current_time / animation_time)

        # TODO: frame time independence
        # x = lerp(x, x1, rate * frame_time)
        # y = lerp(y, y1, rate * frame_time)

        x = lerp(x, x1, smooth_over(frame_time / 1000, smooth_time, 0.95))
        y = lerp(y, y1, smooth_over(frame_time / 1000, smooth_time, 0.95))

        animation_time_slider.update()
        animation_time = animation_time_slider.value
        rate_slider.update()
        rate = rate_slider.value
        smooth_time_slider.update()
        smooth_time = smooth_time_slider.value

        render_surface.fill(WHITE)
        pygame.draw.circle(render_surface, PURPLE_NAVY, (x1, y1), 15, 2)
        pygame.draw.circle(render_surface, PURPLE_NAVY, (x, y), 10)

        ui_surface.fill(AZURE_X11_WEB_COLOR)
        animation_time_slider.draw(ui_surface)
        rate_slider.draw(ui_surface)
        smooth_time_slider.draw(ui_surface)

        display_surface.blit(render_surface, (0, 0))
        display_surface.blit(ui_surface, (WIN_SIZE[0] * 0.75, 0))
        pygame.display.update()


if __name__ == "__main__":
    main()

