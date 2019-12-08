Sokoban Tutorial
****************

When looking for simple games to implement on PewPew, it helps to look back to
the times when computers were so young and underpowered, compared to today, that
simple games were all they could run. One of those games is Sokoban. Let’s try
to write a Sokoban for PewPew!

`Sokoban <https://en.wikipedia.org/wiki/Sokoban>`_ is a puzzle game where you
play a warehouse worker who has to push packing crates around until they are
where they are supposed to be, which is indicated by marks on the floor.
Unfortunately, your warehouse is a bit labyrinthine, and you can only push the
crates, not pull them, so you need to plan carefully: if you push a crate into a
corner, you can never get it back out.

As in the :doc:`tutorial`, create a file named *code.py* containing the basic
setup and game loop. Instead of a blank screen, we put the game board on the
screen right away: some walls, indicated by color 1 (dim or green), surrounding
free space of color 0 (black). ::

    import pew

    pew.init()
    screen = pew.Pix.from_iter((
        (1, 1, 1, 1, 1, 1, 1, 1),
        (1, 0, 0, 0, 0, 0, 0, 1),
        (1, 0, 0, 0, 0, 0, 0, 1),
        (1, 0, 0, 0, 0, 0, 0, 1),
        (1, 0, 0, 0, 0, 0, 0, 1),
        (1, 0, 0, 0, 0, 0, 0, 1),
        (1, 0, 0, 0, 0, 0, 0, 1),
        (1, 1, 1, 1, 1, 1, 1, 1),
    ))

    while True:
        keys = pew.keys()

        pew.show(screen)
        pew.tick(1/6)

Let’s add a player character, indicated by a bright pixel, that can be moved
around with the directional keys. We erase the pixel in the old position at the
beginning of the loop by replacing it with 0 (black floor), then move the
position if any keys are pressed, and finally paint it at the new position:

.. code-block:: python
    :emphasize-lines: 5,6,9,11-19

    ...
        (1, 1, 1, 1, 1, 1, 1, 1),
    ))

    x = 4
    y = 1

    while True:
        screen.pixel(x, y, 0)
        keys = pew.keys()
        if keys & pew.K_UP:
            y -= 1
        elif keys & pew.K_DOWN:
            y += 1
        elif keys & pew.K_LEFT:
            x -= 1
        elif keys & pew.K_RIGHT:
            x += 1
        screen.pixel(x, y, 3)
        pew.show(screen)
        pew.tick(1/6)

Note that we use ``elif`` (Python’s shorthand for “else, if”) to check for
different keys, which means that we can only move in one of the four directions
at once. If we used ``if`` for every key, we could move e.g. right and down at
the same time, that is, move diagonally. (We could also move up and down at the
same time, which means not moving at all.) For Sokoban, we don’t want to be able
to move diagonally, only horizontally and vertically, so we use ``elif``.

If you try this, you will notice that the player can move through walls and
outside of the screen, leaving holes in the walls. Let’s fix that.

Instead of moving right away when a key is pressed, we first record in what
direction we want to move in the variables ``dx`` and ``dy`` (the ``d`` stands
for “delta” or “difference”, because this is going to be the difference between
the new and old position). Then we look ahead what is in that direction, the
``target`` pixel, and only move when it is “floor” (0).

.. code-block:: python
    :emphasize-lines: 5,6,8,10,12,14-18

    ...
    while True:
        screen.pixel(x, y, 0)
        keys = pew.keys()
        dx = 0
        dy = 0
        if keys & pew.K_UP:
            dy = -1
        elif keys & pew.K_DOWN:
            dy = 1
        elif keys & pew.K_LEFT:
            dx = -1
        elif keys & pew.K_RIGHT:
            dx = 1
        target = screen.pixel(x+dx, y+dy)
        if target == 0:
            x += dx
            y += dy
        screen.pixel(x, y, 3)
        pew.show(screen)
        pew.tick(1/6)

Now that that works as it should, let’s add the next element, a crate,
represented by a bright pixel (3):

.. code-block:: python
    :emphasize-lines: 6

    ...
        (1, 1, 1, 1, 1, 1, 1, 1),
        (1, 0, 0, 0, 0, 0, 0, 1),
        (1, 0, 0, 0, 0, 0, 0, 1),
        (1, 0, 0, 0, 0, 0, 0, 1),
        (1, 0, 0, 3, 0, 0, 0, 1),
        (1, 0, 0, 0, 0, 0, 0, 1),
        (1, 0, 0, 0, 0, 0, 0, 1),
        (1, 1, 1, 1, 1, 1, 1, 1),
    ...

When a crate is in front of a player wanting to move, it will be pushed away one
pixel further in the same direction, and the player can move:

.. code-block:: python
    :emphasize-lines: 5-8

    ...
        if target == 0:
            x += dx
            y += dy
        elif target == 3:
            screen.pixel(x+dx+dx, y+dy+dy, 3)
            x += dx
            y += dy
        screen.pixel(x, y, 3)
        pew.show(screen)
        pew.tick(1/6)

There is no need to erase the crate at its old position, because it will
immediately be overwritten with the player anyway.

Test it and you will notice that you can push the crate through walls, punching
holes in the walls again. We obviously need to check what’s *behind* the crate
first, before we decide to move it.

.. code-block:: python
    :emphasize-lines: 3,7

    ...
        target = screen.pixel(x+dx, y+dy)
        behind = screen.pixel(x+dx+dx, y+dy+dy)
        if target == 0:
            x += dx
            y += dy
        elif target == 3 and behind == 0:
            screen.pixel(x+dx+dx, y+dy+dy, 3)
            x += dx
            y += dy
    ...

That works, but we now have two bright pixels on the screen, the player and the
crate, and when the player isn’t moving, you can’t tell which is which. We still
have an unused color available that we could use for one of them, 2 (medium
brightness or red), but we’d like to use that for the marks on the floor later.
Instead, let’s make the player blink. That needs another variable to keep track
of what the last state was, which is then reversed after every time the player
is drawn. A natural choice for such a variable with two states is a boolean with
its two values ``True`` and ``False``.

.. code-block:: python
    :emphasize-lines: 4

    ...
    x = 4
    y = 1
    blink = True

    while True:
    ...

.. code-block:: python
    :emphasize-lines: 3,4

    ...
            y += dy
        screen.pixel(x, y, 3 if blink else 2)
        blink = not blink
        pew.show(screen)
        pew.tick(1/6)

Time for the last missing element: the marks on the floor. We represent them by
color 2:

.. code-block:: python
    :emphasize-lines: 6

    ...
        (1, 1, 1, 1, 1, 1, 1, 1),
        (1, 0, 0, 0, 0, 0, 0, 1),
        (1, 0, 0, 0, 0, 0, 0, 1),
        (1, 0, 0, 0, 0, 0, 0, 1),
        (1, 0, 0, 3, 0, 2, 0, 1),
        (1, 0, 0, 0, 0, 0, 0, 1),
        (1, 0, 0, 0, 0, 0, 0, 1),
        (1, 1, 1, 1, 1, 1, 1, 1),
    ...

And the player and crates can move over them just like over bare floor:

.. code-block:: python
    :emphasize-lines: 3,6

    ...
        behind = screen.pixel(x+dx+dx, y+dy+dy)
        if target in {0, 2}:
            x += dx
            y += dy
        elif target == 3 and behind in {0, 2}:
            screen.pixel(x+dx+dx, y+dy+dy, 3)
            x += dx
            y += dy
    ...

Try it out, and you will find the next problem: the mark is erased by either
player or crate moving over it. This is because when overwriting the respective
pixel with 2 or 3 to draw the player, we lose the information whether there was
a mark there, and in the first line of the next loop, we will restore bare floor
(0) even when there should have been a mark (2). We somehow need to preserve
this information.

To solve this, there is a trick we can use. So far, we have always used pixel
values 0–3 for black, dim, medium, bright or black, green, red, orange. These
are all the colors that our hardware can display. But what happens if we use
higher numbers? If you try it, you will find that 4 produces black, 5 produces
dim/green again, 6 medium/red, 7 bright/orange, 8 black, and so on – the pattern
just repeats every four steps. In other words, you can add 4 to a pixel value
without changing its apparent color.

We can use this to our advantage: If we represent a crate-on-bare-floor as 3 and
a crate-on-mark as 7, they will both look the same, but we can still distinguish
them in the code. The same goes for the player: if the pixel blinks between 2
and 3, it’s on bare floor, if it blinks between 6 and 7, it’s on a mark.

For the player, this needs to be applied on the line where we erase the player
and restore the floor (with or without mark), and on the line where we draw the
new player over the previous floor or crate (each with or without mark):

.. code-block:: python
    :emphasize-lines: 3

    ...
    while True:
        screen.pixel(x, y, 0 if screen.pixel(x, y) < 4 else 2)
        keys = pew.keys()
    ...

.. code-block:: python
    :emphasize-lines: 3

    ...
            y += dy
        screen.pixel(x, y, (3 if blink else 2) + (4 if screen.pixel(x, y) in {2, 7} else 0))
        blink = not blink
    ...

For the crate, it needs to be applied on the line where we detect a crate in
front of the player and on the line where we draw the new crate over the
previous floor:

.. code-block:: python
    :emphasize-lines: 5,6

    ...
        if target in {0, 2}:
            x += dx
            y += dy
        elif target in {3, 7} and behind in {0, 2}:
            screen.pixel(x+dx+dx, y+dy+dy, 3 if behind == 0 else 7)
            x += dx
            y += dy
    ...

Test this and check that you can now both walk over the mark and push the crate
over the mark without erasing it. Congratulations – with this, our game
mechanics are now complete! The game still does not detect when all crates are
placed on their marks and therefore the level is solved, though. Let’s add that.

The easiest way of checking that is to count all bare marks: if none of them are
left, the puzzle is solved. So, iterate over all pixels (with an outer loop over
all rows and an inner loop over the pixels of each row) and count up every time
you see a bare mark. If the count remains 0, break out of the top-level ``while
True`` loop, at which point the program ends because there’s no more code after
the loop. It’s important to do this before we draw the player, who might stand
on a mark and thereby hide it from the counting otherwise.

.. code-block:: python
    :emphasize-lines: 6-12

    ...
        elif target in {3, 7} and behind in {0, 2}:
            screen.pixel(x+dx+dx, y+dy+dy, 3 if behind == 0 else 7)
            x += dx
            y += dy
        count = 0
        for b in range(8):
            for a in range(8):
                if screen.pixel(a, b) == 2:
                    count += 1
        if count == 0:
            break
        screen.pixel(x, y, (3 if blink else 2) + (4 if screen.pixel(x, y) in {2, 7} else 0))
        blink = not blink
        pew.show(screen)
        pew.tick(1/6)

You can test this, but testing it with only one crate is not a very general
test, so add another one, and a mark for it.

.. code-block:: python
    :emphasize-lines: 4,7

    ...
        (1, 1, 1, 1, 1, 1, 1, 1),
        (1, 0, 0, 0, 0, 0, 0, 1),
        (1, 0, 3, 0, 0, 0, 0, 1),
        (1, 0, 0, 0, 0, 0, 0, 1),
        (1, 0, 0, 3, 0, 2, 0, 1),
        (1, 0, 2, 0, 0, 0, 0, 1),
        (1, 0, 0, 0, 0, 0, 0, 1),
        (1, 1, 1, 1, 1, 1, 1, 1),
    ...

After you verify that the completion detection works properly – the game exits
when both crates are on their marks, no earlier and no later – it’s now up to
you to make the game more interesting by adding more walls to the level. Or
maybe you want to extend the game to support multiple levels of increasing
difficulty? Or add a nice reward animation for a completed level? Have fun!

Here is the complete code in its final state again::

    import pew

    pew.init()
    screen = pew.Pix.from_iter((
        (1, 1, 1, 1, 1, 1, 1, 1),
        (1, 0, 0, 0, 0, 0, 0, 1),
        (1, 1, 3, 1, 0, 0, 0, 1),
        (1, 0, 0, 1, 0, 1, 1, 1),
        (1, 0, 0, 3, 0, 2, 0, 1),
        (1, 0, 2, 1, 0, 1, 0, 1),
        (1, 0, 0, 0, 0, 1, 0, 1),
        (1, 1, 1, 1, 1, 1, 1, 1),
    ))

    x = 4
    y = 1
    blink = True

    while True:
        screen.pixel(x, y, 0 if screen.pixel(x, y) < 4 else 2)
        keys = pew.keys()
        dx = 0
        dy = 0
        if keys & pew.K_UP:
            dy = -1
        elif keys & pew.K_DOWN:
            dy = 1
        elif keys & pew.K_LEFT:
            dx = -1
        elif keys & pew.K_RIGHT:
            dx = 1
        target = screen.pixel(x+dx, y+dy)
        behind = screen.pixel(x+dx+dx, y+dy+dy)
        if target in {0, 2}:
            x += dx
            y += dy
        elif target in {3, 7} and behind in {0, 2}:
            screen.pixel(x+dx+dx, y+dy+dy, 3 if behind == 0 else 7)
            x += dx
            y += dy
        count = 0
        for b in range(8):
            for a in range(8):
                if screen.pixel(a, b) == 2:
                    count += 1
        if count == 0:
            break
        screen.pixel(x, y, (3 if blink else 2) + (4 if screen.pixel(x, y) in {2, 7} else 0))
        blink = not blink
        pew.show(screen)
        pew.tick(1/6)

You can also find this at https://github.com/pewpew-game/game-sokoban.
