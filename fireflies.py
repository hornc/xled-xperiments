#!/usr/bin/env python3

import pygame
from pygame.locals import QUIT
from random import choice, randint
from xled.control import ControlInterface
from xled.discover import discover

from led_game import display


BACKGROUND = 'img/firefly-jar.png'
EMPTY = (127, 176, 191, 255)  # Jar bgcolor
FIREFLIES = 20


class Firefly:
    def __init__(self):
        self.x, self.y = 13, 13
        self.color = pygame.Color(0, 0, 0)
        self.color.hsla = (randint(0, 360), 100, 50, 0)

    def move(self, screen):
        adj = [(self.x, self.y)]
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                pos = (self.x + i, self.y + j)
                col = screen.get_at(pos)
                if col == EMPTY:
                    adj.append(pos)
        self.x, self.y = choice(adj)

    def draw(self, screen):
        screen.set_at((self.x, self.y), self.color)


def main():
    pygame.init()
    ip_ = discover().ip_address
    a = ControlInterface(ip_)
    a.set_mode('rt')

    d = a.get_led_layout().data
    coords = d['coordinates']
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode([24, 24], flags=pygame.SCALED)
    bg = pygame.image.load(BACKGROUND)
    running = True
    fireflies = [Firefly() for i in range(FIREFLIES)]
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        screen.blit(bg, [0, 0])

        # Draw ... fireflies
        for firefly in fireflies:
            firefly.move(screen)
            firefly.draw(screen)

        # send an image to the pixel grid
        display(screen, a, coords)
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()


if __name__ == '__main__':
    main()
