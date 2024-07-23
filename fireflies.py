#!/usr/bin/env python3

import pygame
from pygame.locals import QUIT
from random import choice, randint

from led_game import Display


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
    a = Display()

    clock = pygame.time.Clock()
    screen = a.screen
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
        a.display()
        clock.tick(30)
    pygame.quit()


if __name__ == '__main__':
    main()
