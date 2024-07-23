import pygame
from xled.control import ControlInterface
from xled.discover import discover
from requests.exceptions import ConnectTimeout, HTTPError

from test import panels

RECONNECT = 2  # Delay before attempting to reconnect
BRIGHTNESS = 0.25  # Default brightness of the the xled display output
GAMMA = 2.2


# Shared pygame and xled interface display surface:
class Display(ControlInterface):
    def __init__(self):
        self.screen = pygame.display.set_mode([24, 24], flags=pygame.SCALED)
        ip_ = discover().ip_address
        print(f'Discovered LED display at {ip_}')
        super().__init__(ip_)
        self.set_mode('rt')
        #print(f'Initial brightness:', self.get_brightness().data)
        #print(f'Saturation:', self.get_saturation().data)

        d = self.get_led_layout().data
        self.coords = d['coordinates']

    def display(self, brightness:float=BRIGHTNESS) -> None:
        b = 255 * brightness ** GAMMA
        d = self.screen.copy()
        d.fill((b,)*3, special_flags=pygame.BLEND_RGB_MULT)
        raw = pygame.image.tostring(d, 'RGB')
        out = panels(raw)
        try:
            self.set_rt_frame_rest(out)
        except HTTPError as e:
            print(f'EXCEPTION_1b: {e}')
        except ConnectTimeout as e:
            print(f'EXCEPTION: {e} \nWaiting {RECONNECT}s before reconnecting to LEDs...')
            # reset interface:
            pygame.time.wait(RECONNECT * 1000)
            self.set_mode('rt')
        pygame.display.flip()
