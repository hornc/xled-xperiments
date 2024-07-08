#!/usr/bin/env python3

from xled.discover import discover
from xled.control import ControlInterface
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
from random import choice, randint
from test import panels


BACKGROUND = 'img/firefly-jar.png'
FF_COLOR = (0xff, 0xff, 0xff)
EMPTY = (127, 176, 191, 255)  # Jar bgcolor
FIREFLIES = 20


def ff_rgb():
    return randint(255-150, 255)


class Firefly:
    def __init__(self):
        self.x = 13
        self.y = 13
        self.color = (ff_rgb(), ff_rgb(), ff_rgb()) 

    def move(self, screen):
        adj = [(self.x, self.y)]
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                pos = (self.x + i, self.y + j)
                col = screen.get_at(pos)
                #print('DEBUG:', col)
                if col == EMPTY:
                    adj.append(pos)
        self.x, self.y = choice(adj)

    def draw(self, screen):
        screen.set_at((self.x, self.y), self.color)


def display(im, disp, coords):
    #raw = im.tobytes()
    print('TYPE:', type(im))
    print('TYPE:', type(im.get_view('3')))
    print('pixel size', im.get_bytesize())
    raw = im.get_view('3')
    raw = pygame.image.tostring(im, 'RGB') 
    print('TYPE:', raw) 
    out = panels(raw)
    disp.set_rt_frame_rest(out)


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
    pygame.key.set_repeat(10, 10)
    running = True
    x = y = 5  # coords of circle
    fireflies = [Firefly() for i in range(FIREFLIES)]
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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
