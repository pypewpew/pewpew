Mine Tutorial
*************

We will make a game inspired by titles such as Dig Dug and Boulder Dash, where
the player controls a miner, who digs tunnel in a mine filled with boulders and
treasure. The goal is to collect all the treasure without being crushed by a
boulder.

We will start with creating and displaying the map of the mine:

.. code-block:: python

    import pew


    pew.init()
    world = pew.Pix.from_iter([
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 2, 1, 2, 1, 1, 1],
        [1, 1, 2, 1, 3, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 2, 1],
        [1, 1, 1, 1, 1, 2, 3, 2],
        [1, 3, 1, 1, 1, 1, 2, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
    ])
    delay = 1/6
    end = False


    while not end:
        pew.show(world)
        pew.tick(delay)

In the above code, we initialize the ``pew`` library, create a bitmap
to hold the map of the world, and then, in an infinite loop, display it
and wait for the next frame.

Next we want to display the miner:

.. code-block:: python
    :emphasize-lines: 15-17,23,26

    import pew


    pew.init()
    world = pew.Pix.from_iter([
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 2, 1, 2, 1, 1, 1],
        [1, 1, 2, 1, 3, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 2, 1],
        [1, 1, 1, 1, 1, 2, 3, 2],
        [1, 3, 1, 1, 1, 1, 2, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
    ])
    x = 0
    y = 0
    blink = True
    delay = 1/6
    end = False


    while not end:
        world.pixel(x, y, 3 if blink else 0)
        pew.show(world)
        pew.tick(delay)
        blink = not blink

We define global variables ``x`` and ``y`` to hold the position of the
miner, and ``blink`` to track what color we should display. Then we
just color the pixel at that position depending on the state of
``blink``, and flip it to the other state.

Next, we will let the player move the miner:

.. code-block:: python
    :emphasize-lines: 23-42

    import pew


    pew.init()
    world = pew.Pix.from_iter([
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 2, 1, 2, 1, 1, 1],
        [1, 1, 2, 1, 3, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 2, 1],
        [1, 1, 1, 1, 1, 2, 3, 2],
        [1, 3, 1, 1, 1, 1, 2, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
    ])
    x = 0
    y = 0
    blink = True
    delay = 1/6
    end = False


    while not end:
        world.pixel(x, y, 4)
        buttons = pew.keys()
        while pew.keys():
            pew.tick(delay)
        dx = 0
        dy = 0
        if buttons & pew.K_UP:
            dy = -1
        elif buttons & pew.K_DOWN:
            dy = 1
        elif buttons & pew.K_LEFT:
            dx = -1
        elif buttons & pew.K_RIGHT:
            dx = 1
        if (0 <= x + dx <= 7 and 0 <= y + dy <= 7 and
                world.pixel(x + dx, y + dy) != 2):
            world.pixel(x, y, 0)
            x += dx
            y += dy
            world.pixel(x, y, 4)
        world.pixel(x, y, 3 if blink else 0)
        pew.show(world)
        pew.tick(delay)
        blink = not blink

We will paint the position of the miner with a non-existng color 4
temporarily, so that it will be easier for us later to check various
conditions. Later we overwrite it with the blinking color anyways, so
this is never visible.

Then we read the state of the buttons, wait for all buttons to be released,
and figure out the direction in which we want to move depending on which
buttons are pressed.

Then we check if the movement wouldn't take us outside the screen, horizontally and vertically, and if there isn't a boulder in the way. If everything is fine, we draw a tunnel where the miner was, and move them to the new position.

Next, we will add pushing of boulders:


.. code-block:: python
    :emphasize-lines: 43-49

    import pew


    pew.init()
    world = pew.Pix.from_iter([
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 2, 1, 2, 1, 1, 1],
        [1, 1, 2, 1, 3, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 2, 1],
        [1, 1, 1, 1, 1, 2, 3, 2],
        [1, 3, 1, 1, 1, 1, 2, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
    ])
    x = 0
    y = 0
    blink = True
    delay = 1/6
    end = False


    while not end:
        world.pixel(x, y, 4)
        buttons = pew.keys()
        while pew.keys():
            pew.tick(delay)
        dx = 0
        dy = 0
        if buttons & pew.K_UP:
            dy = -1
        elif buttons & pew.K_DOWN:
            dy = 1
        elif buttons & pew.K_LEFT:
            dx = -1
        elif buttons & pew.K_RIGHT:
            dx = 1
        if (0 <= x + dx <= 7 and 0 <= y + dy <= 7 and
                world.pixel(x + dx, y + dy) != 2):
            world.pixel(x, y, 0)
            x += dx
            y += dy
            world.pixel(x, y, 4)
        elif (dy == 0 and 1 <= x + dx <= 6 and
                world.pixel(x + 2 * dx, y + 2 * dy) == 0):
            world.pixel(x, y, 0)
            x += dx
            y += dy
            world.pixel(x, y, 4)
            world.pixel(x + dx, y + dy, 2)
        world.pixel(x, y, 3 if blink else 0)
        pew.show(world)
        pew.tick(delay)
        blink = not blink

We check that the movement is horizontal, that we are not pushing the boulder
outside the screen, and that there is an empty space behind the boulder. Then
we move both the miner and the boulder.

Finally, we need to add gravity for the boulders, so that they fall down when
there is nothing under them.

.. code-block:: python
    :emphasize-lines: 50-57

    import pew


    pew.init()
    world = pew.Pix.from_iter([
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 2, 1, 2, 1, 1, 1],
        [1, 1, 2, 1, 3, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 2, 1],
        [1, 1, 1, 1, 1, 2, 3, 2],
        [1, 3, 1, 1, 1, 1, 2, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
    ])
    x = 0
    y = 0
    blink = True
    delay = 1/6
    end = False


    while not end:
        world.pixel(x, y, 4)
        buttons = pew.keys()
        while pew.keys():
            pew.tick(delay)
        dx = 0
        dy = 0
        if buttons & pew.K_UP:
            dy = -1
        elif buttons & pew.K_DOWN:
            dy = 1
        elif buttons & pew.K_LEFT:
            dx = -1
        elif buttons & pew.K_RIGHT:
            dx = 1
        if (0 <= x + dx <= 7 and 0 <= y + dy <= 7 and
                world.pixel(x + dx, y + dy) != 2):
            world.pixel(x, y, 0)
            x += dx
            y += dy
            world.pixel(x, y, 4)
        elif (dy == 0 and 1 <= x + dx <= 6 and
                world.pixel(x + 2 * dx, y + 2 * dy) == 0):
            world.pixel(x, y, 0)
            x += dx
            y += dy
            world.pixel(x, y, 4)
            world.pixel(x + dx, y + dy, 2)
        for row in range(7, -1, -1):
            for col in range(8):
                if world.pixel(col, row) == 2:
                    if world.pixel(col, row + 1) == 0:
                        world.pixel(col, row, 0)
                        world.pixel(col, row + 1, 2)
                        if world.pixel(col, row + 2) == 4:
                            end = True
        world.pixel(x, y, 3 if blink else 0)
        pew.show(world)
        pew.tick(delay)
        blink = not blink

    import supervisor
    supervisor.reload()

We iterate over the whole world map, starting from the bottom row-by-row, and going up. Every time we find a boulder, we check if there is an empty space under it. If there is, we move it into that empty space. Since we are going from the bottom up, we will only do this once every frame, so we can see the boulder falling gradually down when there is more space below it.

In addition, if we hit the miner while falling, we end the game by setting the ``end`` variable to ``True``. We added a reload at the end of the program, to make sure we can play the game from the beginning.

But boulders only falling down is not that interesting, we also want them to slip sideways if they stand on other boulders and there is empty space on the side.


.. code-block:: python
    :emphasize-lines: 58-66

    import pew


    pew.init()
    world = pew.Pix.from_iter([
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 2, 1, 2, 1, 1, 1],
        [1, 1, 2, 1, 3, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 2, 1],
        [1, 1, 1, 1, 1, 2, 3, 2],
        [1, 3, 1, 1, 1, 1, 2, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
    ])
    x = 0
    y = 0
    blink = True
    delay = 1/6
    end = False


    while not end:
        world.pixel(x, y, 4)
        buttons = pew.keys()
        while pew.keys():
            pew.tick(delay)
        dx = 0
        dy = 0
        if buttons & pew.K_UP:
            dy = -1
        elif buttons & pew.K_DOWN:
            dy = 1
        elif buttons & pew.K_LEFT:
            dx = -1
        elif buttons & pew.K_RIGHT:
            dx = 1
        if (0 <= x + dx <= 7 and 0 <= y + dy <= 7 and
                world.pixel(x + dx, y + dy) != 2):
            world.pixel(x, y, 0)
            x += dx
            y += dy
            world.pixel(x, y, 4)
        elif (dy == 0 and 1 <= x + dx <= 6 and
                world.pixel(x + 2 * dx, y + 2 * dy) == 0):
            world.pixel(x, y, 0)
            x += dx
            y += dy
            world.pixel(x, y, 4)
            world.pixel(x + dx, y + dy, 2)
        for row in range(7, -1, -1):
            for col in range(8):
                if world.pixel(col, row) == 2:
                    if world.pixel(col, row + 1) == 0:
                        world.pixel(col, row, 0)
                        world.pixel(col, row + 1, 2)
                        if world.pixel(col, row + 2) == 4:
                            end = True
                    elif world.pixel(col, row + 1) in {2, 3}:
                        if (world.pixel(col + 1, row) == 0 and
                           world.pixel(col + 1, row + 1) == 0):
                                world.pixel(col, row, 0)
                                world.pixel(col + 1, row, 2)
                        elif (world.pixel(col - 1, row) == 0 and
                           world.pixel(col - 1, row + 1) == 0):
                                world.pixel(col, row, 0)
                                world.pixel(col - 1, row, 2)
        world.pixel(x, y, 3 if blink else 0)
        pew.show(world)
        pew.tick(delay)
        blink = not blink

    import supervisor
    supervisor.reload()

If there is no empty space below a boulder, we check if it's another boulder
or treasure. If it is, we check the two spaces to the left and to the right -- if they are empty, we can move the boulder sideways, and it will fall down in the next frame.

Finally, we need a winning condition. We need to count how many treasures are there left on the map, and end the game when there are none.

.. code-block:: python
    :emphasize-lines: 50,53-55,70-71

    import pew


    pew.init()
    world = pew.Pix.from_iter([
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 2, 1, 2, 1, 1, 1],
        [1, 1, 2, 1, 3, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 2, 1],
        [1, 1, 1, 1, 1, 2, 3, 2],
        [1, 3, 1, 1, 1, 1, 2, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
    ])
    x = 0
    y = 0
    blink = True
    delay = 1/6
    end = False


    while not end:
        world.pixel(x, y, 4)
        buttons = pew.keys()
        while pew.keys():
            pew.tick(delay)
        dx = 0
        dy = 0
        if buttons & pew.K_UP:
            dy = -1
        elif buttons & pew.K_DOWN:
            dy = 1
        elif buttons & pew.K_LEFT:
            dx = -1
        elif buttons & pew.K_RIGHT:
            dx = 1
        if (0 <= x + dx <= 7 and 0 <= y + dy <= 7 and
                world.pixel(x + dx, y + dy) != 2):
            world.pixel(x, y, 0)
            x += dx
            y += dy
            world.pixel(x, y, 4)
        elif (dy == 0 and 1 <= x + dx <= 6 and
                world.pixel(x + 2 * dx, y + 2 * dy) == 0):
            world.pixel(x, y, 0)
            x += dx
            y += dy
            world.pixel(x, y, 4)
            world.pixel(x + dx, y + dy, 2)
        gems = 0
        for row in range(7, -1, -1):
            for col in range(8):
                if world.pixel(col, row) == 3:
                    gems += 1
                elif world.pixel(col, row) == 2:
                    if world.pixel(col, row + 1) == 0:
                        world.pixel(col, row, 0)
                        world.pixel(col, row + 1, 2)
                        if world.pixel(col, row + 2) == 4:
                            end = True
                    elif world.pixel(col, row + 1) in {2, 3}:
                        if (world.pixel(col + 1, row) == 0 and
                           world.pixel(col + 1, row + 1) == 0):
                                world.pixel(col, row, 0)
                                world.pixel(col + 1, row, 2)
                        elif (world.pixel(col - 1, row) == 0 and
                           world.pixel(col - 1, row + 1) == 0):
                                world.pixel(col, row, 0)
                                world.pixel(col - 1, row, 2)
        if gems == 0:
            end = True
        world.pixel(x, y, 3 if blink else 0)
        pew.show(world)
        pew.tick(delay)
        blink = not blink

    import supervisor
    supervisor.reload()
