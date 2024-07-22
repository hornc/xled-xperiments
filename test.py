#!/usr/bin/env python3

import io
from math import floor
from PIL import Image
from random import shuffle
from time import sleep
from xled.control import ControlInterface
from xled.discover import discover


out = b'\x00' * 8*8*9*3


def frame(n):
    # tmp = out[:n] + b'\x18\x9B\xCC\x00\x00\x00\x10\x10\x44' + out[(n+9):]
    tmp = out[:n*3] + b'\x70\x00\x70' + out[(n*3+3):]
    return io.BytesIO(tmp)


def get_pos(panel, coords):
    pos = 8*8*panel
    a.set_mode('rt')
    a.set_rt_frame_rest(frame(pos))
    x = floor(coords[pos]['x']*3)
    y = floor(coords[pos]['y']*6)
    #print(x, y)


def corner_loops(coords):
    while 1:
        for i in range(9):
             get_pos(i, coords)


def rev(b):
    # reverse the RGB pixels
    return b''.join([b[i:i+3] for i in range(0, len(b), 3)][::-1])


def rotate(panel, r):
    if r != 0:
        #panel = bytes(bytearray(64*3))
        step = 8*3
        t = b''
        for i in range(0, len(panel), step):
            t += rev(panel[i:i+step]) if ((i//step) & 1) else panel[i:i+step]

        panel = Image.frombytes('RGB', (8,8), t).rotate(r * 90).tobytes()
        t = b''

        for i in range(0, len(panel), step):
            t += rev(panel[i:i+step]) if ((i//step) & 1) else panel[i:i+step]
        panel = t
    return panel


def sort_panels(panels: list, order=None) -> list:
    """
    Arrange (sort and rotate) panels based on the physical
    configuration of the separate Twinkly squares.
    TODO: This is hardcoded to one specifc config!
          Use the device supplied configuration
    """
    #        *     *  *
    order = [1, 2, 3, 0, 6, 7, 4, 5, 8]
    rot   = [0, -1, 1, 0, -1, 1, -1, -1, 2]
    sort = [None] * 9
    for i, panel in enumerate(panels):
        sort[order[i]] = rotate(panel, rot[i])
    return sort


def panels(im:bytes) -> bytes:
    """
    Split bytes into 8x8 panels and rearrange
    them to display correctly on a specific
    square configuration.
    """
    w = 8 * 3
    h = 8 * 3
    out = [b''] * 9
    #print('LEN:', len(im))
    for j in range(0, len(im), 8*3):
        x = (j // (8*3)) % 3
        y = (j // (8*8*9)) % 3
        n = x + y * 3
        dir_ = (j // (8*9)) & 1
        if dir_:
            out[n] += im[j:j+8*3]
        else:
            out[n] += rev(im[j:j+8*3])
        #print(j, x, y)
    for i in range(9):
        #print('LEN panel:', len(out[i]))
        out[i] += b'\x00' * ((8*8*3) - len(out[i]))
        #print('NEW:', len(out[i]))
    out = sort_panels(out)
    return b''.join(out)


def display(im, disp, coords):
    # Displays a PIL image in RT mode
    raw = im.tobytes()
    out = panels(raw)
    disp.set_rt_frame_rest(out)


if __name__ == '__main__':
    ip_ = discover().ip_address
    a = ControlInterface(ip_)
    a.set_mode('rt')

    d = a.get_led_layout().data
    coords = d['coordinates']
    #corner_loops(coords)

    infile = 'img/test.png'
    location = 0
    with Image.open(infile) as im:
        while 1:
            display(im, a, coords)
            sleep(3)
