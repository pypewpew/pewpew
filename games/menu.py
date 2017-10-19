import sys
import os
import time
import pew


def scroll(pix, dx=1):
    x = 0
    while True:
        for x in range(x, pix.width, dx):
            screen.blit(pix, -x, 1)
            yield x
        x = -8


def change(pix, next_pix, x, dy):
    for y in range(1, 1 + 8 * dy, dy):
        screen.box(0)
        screen.blit(pix, -x, y)
        screen.blit(next_pix, 0, y - 7 * dy)
        yield


def hold_keys():
    global _hold

    try:
        keys = pew.keys()
    except pew.GameOver:
        keys = 0
    if keys:
        hold = 0
    try:
        while pew.keys() and time.monotonic() - hold < 0.25:
            return 0
    except pew.GameOver:
        keys = 0
    hold = time.monotonic()
    return keys


def menu(entries):
    animation = scroll(pix)
    while True:
        if keys & pew.K_UP:
            selected = (selected - 1) % len(entries)
            next_pix = pew.Pix.from_text(entries[selected])
            yield from change(pix, next_pix, x, 1)
            hold_keys()
            pix = next_pix
            animation = scroll(pix)
            keys = 0
        if keys & pew.K_DOWN:
            selected = (selected + 1) % len(entries)
            next_pix = pew.Pix.from_text(entries[selected])
            yield from change(pix, next_pix, x, -1)
            hold_keys()
            pix = next_pix
            animation = scroll(pix)
            keys = 0
        x = next(animation)
        yield selected
        yield selected


pew.init()
pew.init()
while True:
    _hold = 0
    _brightness = 7
    pew.brightness(_brightness)
    screen = pew.Pix()
    files = [name[:-3] + ' ' for name in os.listdir()
             if name.endswith('.py') and name != 'main.py']
    selected = 0
    x = 0
    while pew.keys():
        pew.tick(1/24)
    while True:
        pix = pew.Pix.from_text(files[selected])
        keys = hold_keys()
        if keys & pew.K_O:
            break
        if keys & pew.K_RIGHT:
            _brightness = min(_brightness + 1, 15)
            pew.brightness(_brightness)
        if keys & pew.K_LEFT:
            _brightness = max(_brightness - 1, 0)
            pew.brightness(_brightness)

        pew.show(screen)
        pew.tick(1/24)
    screen.box(0)
    pew.show(screen)
    game = files[selected]
    del screen
    del files
    try:
        __import__(game)
    except pew.GameOver:
        continue
    del sys.modules[game]

