#!/usr/bin/env python3

import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
from requests.exceptions import ConnectTimeout
from xled.control import ControlInterface
from xled.discover import discover

from led_game import display


#BACKGROUND = "img/test.png"
#BACKGROUND = "img/pyrrhia.png"
BACKGROUND = "img/pantala.png"

COLOR = (250, 250, 0)  # player pixel color


def main():
    pygame.init()
    ip_ = discover().ip_address
    a = ControlInterface(ip_)
    a.set_mode('rt')
    print(f'Initial brightness:', a.get_brightness().data)
    print(f'Saturation:', a.get_saturation().data)

    d = a.get_led_layout().data
    coords = d['coordinates']
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode([24, 24], flags=pygame.SCALED)
    bg = pygame.image.load(BACKGROUND)
    pygame.key.set_repeat(10, 10)
    running = True
    x = y = 5  # coords of player
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:  # Window close
                running = False
        screen.blit(bg, [0, 0])
        # Check user input...
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            y -= 1
        if pressed_keys[K_DOWN]:
            y += 1
        if pressed_keys[K_LEFT]:
            x -= 1
        if pressed_keys[K_RIGHT]:
            x += 1
        # Draw player pixel
        screen.set_at((x, y), COLOR)

        # Send image to the pixel grid
        try:
            display(screen, a, coords)
        except ConnectTimeout as e:
            print(f'EXCEPTION_2: {e}')
            # reset interface
            pygame.time.wait(5000)
            a = ControlInterface(ip_)
            a.set_mode('rt')
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()


if __name__ == '__main__':
    main()
