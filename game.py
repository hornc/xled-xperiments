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

from led_game import Display


#BACKGROUND = "img/test.png"
#BACKGROUND = "img/pyrrhia.png"
BACKGROUND = "img/pantala.png"

COLOR = (250, 250, 0)  # player pixel color


def main():
    pygame.init()
    clock = pygame.time.Clock()

    a = Display()
    screen = a.screen
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

        # display both the pygame screen AND send data to LED matrix:
        a.display()

        clock.tick(30)
    pygame.quit()


if __name__ == '__main__':
    main()
