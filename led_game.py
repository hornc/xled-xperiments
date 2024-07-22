import pygame
from xled.control import ControlInterface
from requests.exceptions import ConnectTimeout, HTTPError

from test import panels


BRIGHTNESS = 0.25  # Default brightness of the the xled display output
GAMMA = 2.2


def display(im:pygame.Surface, disp:ControlInterface, coords:list, brightness:float=BRIGHTNESS) -> None:
    b = 255 * brightness ** GAMMA
    d = im.copy()
    d.fill((b,)*3, special_flags=pygame.BLEND_RGB_MULT)
    raw = pygame.image.tostring(d, 'RGB')
    out = panels(raw)
    try:
        disp.set_rt_frame_rest(out)
    except HTTPError as e:
        print(f'EXCEPTION_1b: {e}')
