import pew
import random


pew.init()
screen = pew.Pix()

game_speed = 4
snake = [(2, 4)]
dx, dy = 1, 0
apple_x, apple_y = 6, 4
screen.pixel(apple_x, apple_y, 2)

while True:
    if len(snake) > 1:
        x, y = snake[-2]
        screen.pixel(x, y, 1)
    x, y = snake[-1]
    screen.pixel(x, y, 3)

    pew.show(screen)
    pew.tick(1 / game_speed)

    keys = pew.keys()
    if keys & pew.K_UP and dy == 0:
        dx, dy = 0, -1
    elif keys & pew.K_LEFT and dx == 0:
        dx, dy = -1, 0
    elif keys & pew.K_RIGHT and dx == 0:
        dx, dy = 1, 0
    elif keys & pew.K_DOWN and dy == 0:
        dx, dy = 0, 1
    x = (x + dx) % 8
    y = (y + dy) % 8

    if (x, y) in snake:
        break
    snake.append((x, y))

    if x == apple_x and y == apple_y:
        screen.pixel(apple_x, apple_y, 0)
        apple_x, apple_y = snake[0]
        while (apple_x, apple_y) in snake:
            apple_x = random.getrandbits(3)
            apple_y = random.getrandbits(3)
        screen.pixel(apple_x, apple_y, 2)
        game_speed += 0.2
    else:
        x, y = snake.pop(0)
        screen.pixel(x, y, 0)

text = pew.Pix.from_text("Game over!")
for dx in range(-8, text.width):
    screen.blit(text, -dx, 1)
    pew.show(screen)
    pew.tick(1 / 12)
