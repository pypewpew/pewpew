import pew


pew.init()
screen = pew.Pix()
x, y = 4, 7
grass = pew.Pix.from_iter(([1]*8,))
pedestrians = pew.Pix.from_iter(([0, 2, 0, 0] * 4,))
cars = pew.Pix.from_iter(([0, 2, 2, 0] * 4,))
screen.blit(grass, 0, 0)
screen.blit(grass, 0, 3)
screen.blit(grass, 0, 4)
screen.blit(grass, 0, 7)
old_pixel = screen.pixel(x, y)
traffic = 0
alive = True
pressing = False
while alive:
    keys = pew.keys()
    screen.pixel(x, y, old_pixel)
    if not pressing:
        if keys & pew.K_UP and y > 0:
            y -= 1
        elif keys & pew.K_DOWN and y < 7:
            y += 1
        if keys & pew.K_LEFT and x > 0:
            x -= 1
        elif keys & pew.K_RIGHT and x < 7:
            x += 1
        if keys:
            pressing = True
    else:
        if not keys:
            pressing = False
    screen.blit(pedestrians, (traffic // 2) % 8 - 8, 1)
    screen.blit(cars, -((traffic // 2) % 8), 2)
    screen.blit(cars, traffic // 4 - 8, 5)
    screen.blit(pedestrians, -traffic // 4, 6)
    old_pixel = screen.pixel(x, y)
    if old_pixel == 2:
        alive = False
    traffic = (traffic + 1) % 32
    screen.pixel(x, y, 3)
    pew.show(screen)
    pew.tick(1/6)
text = pew.Pix.from_text("Game over!")
for dx in range(-8, text.width):
    screen.blit(text, -dx, 1)
    pew.show(screen)
    pew.tick(1/12)
