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
from test import panels


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
    bg = pygame.image.load('img/test.png')
    pygame.key.set_repeat(10, 10)
    running = True
    x = y = 5  # coords of circle
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Window close
                running = False
        #screen.fill((255, 255, 255))
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
        # draw player (circle)
        pygame.draw.circle(screen, (100, 100, 5), (x, y), 2)

        # try to send an image to the pixel grid
        display(screen, a, coords)
        pygame.display.flip()
        #pygame.time.delay(10)
        clock.tick(30)
    pygame.quit()


if __name__ == '__main__':
    main()
