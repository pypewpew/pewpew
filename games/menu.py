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
    global hold

    try:
        keys = pew.keys()
    except pew.GameOver:
        keys = 0
    if keys:
        hold = 0
    while pew.keys() and time.monotonic() - hold < 0.25:
        return 0
    hold = time.monotonic()
    return keys


def menu(entries):
    brightness = 7
    pew.brightness(brightness)
    selected = 0
    pix = pew.Pix.from_text(entries[selected])
    x = 0
    animation = scroll(pix)
    while True:
        keys = hold_keys()
        if keys & pew.K_O:
            return
        if keys & pew.K_RIGHT:
            brightness = min(brightness + 1, 15)
            pew.brightness(brightness)
        if keys & pew.K_LEFT:
            brightness = max(brightness - 1, 0)
            pew.brightness(brightness)
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


def importspew(name):
    with open(name, 'r') as f:
        for l in range(2):
            if f.readline().strip() == 'import pew':
                return True
    return False


pew.init()
pew.init()
while True:
    hold = 0
    screen = pew.Pix()
    files = [name[:-3] for name in os.listdir()
             if name.endswith('.py') and name != 'main.py' and importspew(name)]
    m = menu(files)
    selected = 0
    try:
        while pew.keys():
            pew.tick(1/24)
    except pew.GameOver:
        pass
    while True:
        try:
            selected = next(m)
        except StopIteration:
            break
        pew.show(screen)
        pew.tick(1/24)
    screen.box(0)
    pew.show(screen)
    game = files[selected]
    del screen
    del m
    del files
    try:
        __import__(game)
    except pew.GameOver:
        continue
    del sys.modules[game]

