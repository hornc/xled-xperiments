import pygame
from PIL import Image
from xled.control import ControlInterface
from xled.discover import discover
from requests.exceptions import ConnectTimeout, HTTPError


RECONNECT = 2  # Delay before attempting to reconnect
BRIGHTNESS = 0.25  # Default brightness of the the xled display output
GAMMA = 2.2


def layout(coords):
    """
    TODO: This is hardcoded to one specifc config!
              Use the device supplied configuration
    """
    order = [0] * 9
    map_ = [2, 1, 0, 4, 3, 7, 6, 5, 8]  # ???
    #rot = [0] * 9
    rot = [0, -1, 1, 0, -1, 1, -1, -1, 2]  # TODO: don't hardcode
    chunks = [coords[i::9] for i in range(9)]
    i = 0
    for y in [0, 64 * 3, 64 * 6]:
        for x in [0, 64, 128]:
            p = coords[x + y]
            gx = int(p['x'] * 1.5 + 1.5)
            gy = int((1-p['y']) * 3)
            if gx == 3:
                gx = 2
            if gy == 3:
                gy = 2
            #print('DEBUG:', p, x, y, '|', gx, gy)
            order[3 * gx + gy] = map_[i]
            i += 1
    #print(order, rot)
    return order, rot


def rev(b:bytes):
    """Reverse RGB pixels."""
    return b''.join([b[i:i+3] for i in range(0, len(b), 3)][::-1])


# Shared pygame and xled interface display surface:
class Display(ControlInterface):
    def __init__(self):
        self.screen = pygame.display.set_mode([24, 24], flags=pygame.SCALED)
        ip_ = discover().ip_address
        print(f'Discovered LED display at {ip_}')
        super().__init__(ip_)
        self.set_mode('rt')

        d = self.get_led_layout().data
        self.coords = d['coordinates']

    def display(self, brightness:float=BRIGHTNESS) -> None:
        b = 255 * brightness ** GAMMA
        d = self.screen.copy()
        d.fill((b,)*3, special_flags=pygame.BLEND_RGB_MULT)
        raw = pygame.image.tostring(d, 'RGB')
        out = self.panels(raw)
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

    def panels(self, im:bytes) -> bytes:
        """
        Split bytes into 8x8 panels and rearrange
        them to display correctly on a specific
        square configuration.
        """
        w = 8 * 3
        h = 8 * 3
        out = [b''] * 9
        for j in range(0, len(im), 8*3):
            x = (j // (8*3)) % 3
            y = (j // (8*8*9)) % 3
            n = x + y * 3
            dir_ = (j // (8*9)) & 1
            if dir_:
                out[n] += im[j:j+8*3]
            else:
                out[n] += rev(im[j:j+8*3])
        for i in range(9):
            out[i] += b'\x00' * ((8*8*3) - len(out[i]))
        out = self.sort_panels(out)
        return b''.join(out)

    def sort_panels(self, panels: list, order=None) -> list:
        """
        Arrange (sort and rotate) panels based on the physical
        configuration of the separate Twinkly squares.
        """
        def rotate(panel, r):
            if r != 0:
                step = 8 * 3
                t = b''
                for i in range(0, len(panel), step):
                    t += rev(panel[i:i+step]) if ((i//step) & 1) else panel[i:i+step]
                panel = Image.frombytes('RGB', (8,8), t).rotate(r * 90).tobytes()
                t = b''
                for i in range(0, len(panel), step):
                    t += rev(panel[i:i+step]) if ((i//step) & 1) else panel[i:i+step]
                panel = t
            return panel

        order, rot = layout(self.coords)
        sort = [None] * 9
        for i, panel in enumerate(panels):
            sort[order[i]] = rotate(panel, rot[i])
        return sort

    def svglayout(self):
        """
        Writes the layout of the LED matrix to a SVG file (<path>)
        to inspect how the LEDs are organised.
        """
        w = 300
        h = 200
        margin = 20
        fname = 'layout.svg'
        SVG = f"""<svg version="1.1" width="{w}" height="{h}" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <marker id="arrow" refX="1" refY="5" orient="auto">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="#f00" />
          </marker>
        </defs>
        %%BODY%%
        </svg>"""
        out = '<path marker-start="url(#arrow)" d="'
        c = 'M'
        for point in self.coords:
            out += f'{c}{point["x"] * w/3 + w/2} {point["y"] * h/2 + margin} '
            c = 'L'
        out += '" style="fill:none;stroke:black;stroke-width:0.2" />'

        with open(fname, 'w') as f:
            print(f'Writing layout to {fname}')
            f.write(SVG.replace('%%BODY%%', out))
