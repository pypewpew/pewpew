Bouncing Ball Tutorial
**********************

Let's try to write a simple bouncing ball demo, where a single pixel moves
around the screen and bounces off its edges. This will let us get familiar
with the library.

Start by creating a file called "code.py" --- that is where all our code
will go. As long as such a file exists, PewPew will try to run it on startup
and on reset. Later, when you finish working on your game, you can rename it
to whatever you call your game, and then PewPew will fall back to running
"main.py", which contains the game selection menu.

To use the PewPew library, we need to first import it into our code. So we need to start with this line::

    import pew

Then we need to tell the library to switch the display on and generally prepare
everything for displaying our ball. We do that by calling the ``init`` function
like this::

    import pew


    pew.init()

We will want our demo program to run all the time in a loop, so we will need an
infinite loop. We can limit the loop's speed to run 12 times a second, which is
slow enough to see the movements, but not too slow::

    import pew


    pew.init()
    while True:
        pew.tick(1/12)

Now, we will need an image that we will display on the screen. In PewPew,
images are represented as ``Pix`` objects. So we can create an empty image the
size of the display, and display it in our loop::

    import pew


    pew.init()
    screen = pew.Pix()
    while True:
        pew.show(screen)
        pew.tick(1/12)

Now we will add our pixel. We will make it start at coordinates ``0, 0``, and
we will draw it with color ``3``, which is the brightest::

    import pew


    pew.init()
    screen = pew.Pix()
    x = 0
    y = 0
    while True:
        screen.pixel(x, y, 3)
        pew.show(screen)
        pew.tick(1/12)

Now let's make the pixel actually move::

    import pew


    pew.init()
    screen = pew.Pix()
    x = 0
    y = 0
    dx = 1
    dy = 1
    while True:
        x += dx
        y += dy
        screen.pixel(x, y, 3)
        pew.show(screen)
        pew.tick(1/12)

After running this, you will see a diagonal line on the display. That's because
the old positions of the pixel are not getting deleted. And the pixel
keeps on going forever outside the screen. We can fix that. Let's start by
deleting the old position::

    import pew


    pew.init()
    screen = pew.Pix()
    x = 0
    y = 0
    dx = 1
    dy = 1
    while True:
        screen.pixel(x, y, 0)
        x += dx
        y += dy
        screen.pixel(x, y, 3)
        pew.show(screen)
        pew.tick(1/12)

We simply draw a black pixel at the old position before drawing a bright one at
the new one. Since we only update the screen once a frame, those two operations
are visible at the same time. Now, let's make the pixel bounce off the edges::

    import pew


    pew.init()
    screen = pew.Pix()
    x = 1
    y = 1
    dx = 1
    dy = 1
    while True:
        screen.pixel(x, y, 0)
        if not 0 < x < 7:
            dx = -dx
        if not 0 < y < 7:
            dy = -dy
        x += dx
        y += dy
        screen.pixel(x, y, 3)
        pew.show(screen)
        pew.tick(1/12)

We had to move our starting point a bit, because otherwise it will get stuck in
the corner. Now you should see our pixel going from one corner to the other.
That's neat, but a little bit boring. Maybe if we changed the starting position
it would be better::

    import pew


    pew.init()
    screen = pew.Pix()
    x = 3
    y = 1
    dx = 1
    dy = 1
    while True:
        screen.pixel(x, y, 0)
        if not 0 < x < 7:
            dx = -dx
        if not 0 < y < 7:
            dy = -dy
        x += dx
        y += dy
        screen.pixel(x, y, 3)
        pew.show(screen)
        pew.tick(1/12)

Maybe we could affect the ball's behavior with the buttons? For instance,
pressing `O` could make it bounce horizontally, and pressing `X` vertically::

    import pew


    pew.init()
    screen = pew.Pix()
    x = 3
    y = 1
    dx = 1
    dy = 1
    while True:
        keys = pew.keys()
        screen.pixel(x, y, 0)
        if not 0 < x < 7 or keys & pew.K_O:
            dx = -dx
        if not 0 < y < 7 or keys & pew.K_X:
            dy = -dy
        x += dx
        y += dy
        screen.pixel(x, y, 3)
        pew.show(screen)
        pew.tick(1/12)

Could we have a nicer background than just black? Let's try a check board::

    import pew


    pew.init()
    screen = pew.Pix()
    background = pew.Pix.from_iter((
        (1, 0, 1, 0, 1, 0, 1, 0),
        (0, 1, 0, 1, 0, 1, 0, 1),
        (1, 0, 1, 0, 1, 0, 1, 0),
        (0, 1, 0, 1, 0, 1, 0, 1),
        (1, 0, 1, 0, 1, 0, 1, 0),
        (0, 1, 0, 1, 0, 1, 0, 1),
        (1, 0, 1, 0, 1, 0, 1, 0),
        (0, 1, 0, 1, 0, 1, 0, 1),
    ))
    x = 3
    y = 1
    dx = 1
    dy = 1
    while True:
        keys = pew.keys()
        screen.blit(background)
        if not 0 < x < 7 or keys & pew.K_O:
            dx = -dx
        if not 0 < y < 7 or keys & pew.K_X:
            dy = -dy
        x += dx
        y += dy
        screen.pixel(x, y, 3)
        pew.show(screen)
        pew.tick(1/12)

Instead of deleting our pixel with a black pixel, we simply copy the whole
background all over the screen, and then draw our pixel in the new position.

How about making the ball larger::

    import pew


    pew.init()
    screen = pew.Pix()
    ball = pew.Pix.from_iter((
        (3, 2),
        (2, 1),
    ))
    background = pew.Pix.from_iter((
        (1, 0, 1, 0, 1, 0, 1, 0),
        (0, 1, 0, 1, 0, 1, 0, 1),
        (1, 0, 1, 0, 1, 0, 1, 0),
        (0, 1, 0, 1, 0, 1, 0, 1),
        (1, 0, 1, 0, 1, 0, 1, 0),
        (0, 1, 0, 1, 0, 1, 0, 1),
        (1, 0, 1, 0, 1, 0, 1, 0),
        (0, 1, 0, 1, 0, 1, 0, 1),
    ))
    x = 3
    y = 1
    dx = 1
    dy = 1
    while True:
        keys = pew.keys()
        screen.blit(background)
        if not 0 < x < 6 or keys & pew.K_O:
            dx = -dx
        if not 0 < y < 6 or keys & pew.K_X:
            dy = -dy
        x += dx
        y += dy
        screen.blit(ball, x, y)
        pew.show(screen)
        pew.tick(1/12)

We had to adjust the boundaries of the screen for the larger ball here.

Now experiment with this code yourself and see what you can make.
