#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import itertools
import random
from images2gif import writeGif
from PIL import Image, ImageDraw, ImageFont

loadfont = lambda size: ImageFont.truetype('FreeSans.ttf', size)

def drawBits(pen, bits, pos, font):
    x, y = pos
    gw, gh = 16, 24
    fc, oc = "#fff", "#000"
    for idx, v in enumerate(bits):
        bit, color = v
        box = (x+idx*gw, y, x+gw*idx+gw-2, y+gh)
        pen.rectangle(box, fill=fc, outline=oc)

        box = (x+idx*gw+4, y+4)
        pen.text(box, bit, font=font, fill=color)

def genBits(v, shift, shiftbit, shiftcolor, bgcolor):
    raw = bin(v)[2:].zfill(32) if v >= 0 else bin(2**32-1-v)[2:]
    if shift == 0: return zip(raw, itertools.repeat(bgcolor))
    raw = zip(raw[:-shift], itertools.repeat(bgcolor))
    padding = zip(shiftbit*shift, itertools.repeat(shiftcolor))
    return padding+raw

def gen(dst):
    im = Image.new('RGB', (640, 480))
    ims = []

    font = loadfont(16)
    fc = "#fff"

    ## initial frame
    num = random.randint(1, 2**30)
    pen = ImageDraw.Draw(im)
    pen.text((10, 10), "Logic Shift Right with Positive Number %d" % num, font=font, fill=fc)
    drawBits(pen, genBits(num, 0, '0', 'red', 'green'), (64, 64), font)

    pen.text((10, 110), "Arithmetic Shift Right with Positive Number %d" % num, font=font, fill=fc)
    drawBits(pen, genBits(num, 0, '0', 'red', 'green'), (64, 164), font)

    pen.text((10, 210), "Logic Shift Right with Negative Number %d" % -num, font=font, fill=fc)
    drawBits(pen, genBits(-num, 0, '0', 'red', 'green'), (64, 164), font)

    pen.text((10, 310), "Arithmetic Shift Right with Negative Number %d" % -num, font=font, fill=fc)
    drawBits(pen, genBits(-num, 0, '1', 'red', 'green'), (64, 164), font)

    ims.append(im.copy())

    for idx in xrange(1, 32):
        drawBits(pen, genBits(num, idx, '0', 'red', 'green'), (64, 64), font)
        drawBits(pen, genBits(num, idx, '0', 'red', 'green'), (64, 164), font)
        drawBits(pen, genBits(num, idx, '0', 'red', 'green'), (64, 264), font)
        drawBits(pen, genBits(num, idx, '1', 'red', 'green'), (64, 364), font)
        ims.append(im.copy())

    writeGif(dst, ims, duration=0.2, repeat=True, dither=0)

if '__main__' == __name__:
    dst = sys.argv[1] if len(sys.argv) > 1 else 'test.gif'
    gen(dst)
