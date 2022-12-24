import pygame
from pygame.locals import *

from random import randint
from math import exp


from settings import *
from colors import *
from slider import Slider
from label import Label


WIN_SIZE = 1280, 720

SPLIT_SCREEN_COEFFICIENT = 0.8
RENDER_SIZE = int(WIN_SIZE[0] * SPLIT_SCREEN_COEFFICIENT), WIN_SIZE[1]
UI_SIZE = int(WIN_SIZE[0] * (1 - SPLIT_SCREEN_COEFFICIENT)), WIN_SIZE[1]

TARGET_FPS = 0


# TODO: labels, slider functionality, slider fix: make central line width the same no matter labels width,
# TODO: lerp update (rate and anim time), ui elements packing
# smooth time gotta be less than animation time


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
    render_surface = pygame.Surface(RENDER_SIZE)
    ui_surface = pygame.Surface(UI_SIZE)

    clock = pygame.time.Clock()

    x, y = RENDER_SIZE[0] // 2, RENDER_SIZE[1] // 2  # start position
    x1, y1 = randint(0, RENDER_SIZE[0]), randint(0, RENDER_SIZE[1])  # end position

    animation_time = 1000  # ms
    current_time = 0
    smooth_time = 250
    rate = 0.005

    padding = 10
    label_height = 20
    slider_height = 25

    animation_time_label = Label(pygame.Rect(UI_SIZE[0] * 0.05,
                                             padding,
                                             UI_SIZE[0] * 0.9,
                                             label_height),
                                 "Animation Time (ms)")
    animation_time_slider = Slider(pygame.Rect(UI_SIZE[0] * 0.05,
                                               label_height + padding * 2,
                                               UI_SIZE[0] * 0.9,
                                               slider_height),
                                   min_value=250,
                                   max_value=2000,
                                   init_value=animation_time)

    rate_slider_label = Label(pygame.Rect(UI_SIZE[0] * 0.05,
                                          label_height + slider_height + padding * 3,
                                          UI_SIZE[0] * 0.9,
                                          label_height),
                              "Rate (not working)")
    rate_slider = Slider(pygame.Rect(UI_SIZE[0] * 0.05,
                                     label_height * 2 + slider_height + padding * 4,
                                     UI_SIZE[0] * 0.9,
                                     slider_height),
                         min_value=0.001,
                         max_value=0.01,
                         init_value=rate)

    smooth_time_label = Label(pygame.Rect(UI_SIZE[0] * 0.05,
                                          label_height * 2 + slider_height * 2 + padding * 5,
                                          UI_SIZE[0] * 0.9,
                                          label_height),
                              "Smooth Time (ms)")
    smooth_time_slider = Slider(pygame.Rect(UI_SIZE[0] * 0.05,
                                            label_height * 3 + slider_height * 2 + padding * 6,
                                            UI_SIZE[0] * 0.9,
                                            slider_height),
                                min_value=1,
                                max_value=1500,
                                init_value=smooth_time)

    while True:

        # system

        frame_time_ms = clock.tick(TARGET_FPS)  # ms
        current_time += frame_time_ms
        print(int(clock.get_fps()))

        # input

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
                elif event.key == K_d:
                    # DRAW_DEBUG = not DRAW_DEBUG
                    pass
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mx, my = event.pos
                    # render surface  # TODO: detect on which canvas click as made

                    # ui surface
                    mx -= RENDER_SIZE[0]  # surface offset  # better refactor
                    animation_time_slider.handle_click(mx, my)
                    rate_slider.handle_click(mx, my)
                    smooth_time_slider.handle_click(mx, my)
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    # ui surface  # TODO: release only grabbed sliders
                    animation_time_slider.grab_release()
                    rate_slider.grab_release()
                    smooth_time_slider.grab_release()

        mx, my = pygame.mouse.get_pos()
        animation_time_slider.update((mx - RENDER_SIZE[0], my))
        animation_time = animation_time_slider.value
        rate_slider.update((mx - RENDER_SIZE[0], my))
        rate = rate_slider.value
        smooth_time_slider.update((mx - RENDER_SIZE[0], my))
        smooth_time = smooth_time_slider.value

        # updates

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

        x = lerp(x, x1, smooth_over(frame_time_ms, smooth_time, 0.95))
        y = lerp(y, y1, smooth_over(frame_time_ms, smooth_time, 0.95))

        # rendering

        render_surface.fill(WHITE)
        pygame.draw.circle(render_surface, PURPLE_NAVY, (x1, y1), 15, 2)
        pygame.draw.circle(render_surface, PURPLE_NAVY, (x, y), 10)

        ui_surface.fill(AZURE_X11_WEB_COLOR)
        animation_time_label.draw(ui_surface)
        animation_time_slider.draw(ui_surface)
        rate_slider_label.draw(ui_surface)
        rate_slider.draw(ui_surface)
        smooth_time_label.draw(ui_surface)
        smooth_time_slider.draw(ui_surface)

        display_surface.blit(render_surface, (0, 0))
        display_surface.blit(ui_surface, (RENDER_SIZE[0], 0))
        pygame.display.update()


if __name__ == "__main__":
    main()

