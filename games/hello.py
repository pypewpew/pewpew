import pew


pew.init()
screen = pew.Pix()
text = pew.Pix.from_text("Hello world!")

while True:
    for dx in range(-8, text.width):
        screen.blit(text, -dx, 1)
        pew.show(screen)
        pew.tick(1/12)
