PewPew Library Reference
************************

.. module:: pew

.. function:: init()

    Initialize the module.

    This function switches the display on and performs some basic setup.


.. function:: brightness(level)

    Set the brightness of the display, from 0 (minimum) to 15 (maximum). On
    devices that don't support varying the brightness this does nothing.


.. function:: show(pix)

    Show the provided image on the display, starting at the top left corner.
    You will want to call this once for every frame.


.. function:: keys()

    Return a number telling which keys (or buttons) have been pressed since the
    last check.  The number can then be filtered with the ``&`` operator and
    the ``K_X``, ``K_DOWN``, ``K_LEFT``, ``K_RIGHT``, ``K_UP``, and ``K_O``
    constants to see whether any of the keys was pressed.


.. function:: tick(delay)

    Wait until ``delay`` seconds have passed since the last call to this
    function. You can call it every frame to ensure a constant frame rate.


.. class:: Pix(width=8, height=8, buffer=None)

    Pix represents a drawing surface, ``width`` pixels wide and ``height``
    pixels high.

    If no ``buffer`` is specified for storing the data, a suitable one will
    be automatically created.

    .. classmethod:: from_iter(cls, lines)

        Creates a new Pix and initialzes its contents by iterating over
        ``lines`` and then over individual pixels in each line. All the lines
        have to be at least as long as the first one.

    .. classmethod:: from_text(cls, text, color=None, background=0, colors=None)

        Creates a new Pix and renders the specified text on it. It is exactly
        the size needed to fit the specified text. Newlines and other control
        characters are rendered as spaces.

        If ``color`` is not specified, it will use yellow and red for the
        letters by default. Otherwise it will use the specified color, with
        ``background`` color as the background.

        Alternatively, ``colors`` may be specified as a 4-tuple of colors,
        and then the ``color`` and ``background`` arguments are ignored, and
        the four specified colors are used for rendering the text.

    .. method:: pixel(self, x, y, color=None)

        If ``color`` is specified, sets the pixel at location ``x``, ``y`` to
        that color. If not, returns the color of the pixel at that location.

        If the location is out of bounds of the drawing surface, returns 0.

    .. method:: box(self, color, x=0, y=0, width=self.width, height=self.height)

        Draws a filled box with the specified ``color`` with its top left
        corner at the specified location and of the specified size. If no
        location and size are specified, fills the whole drawing surface.

    .. method:: blit(self, source, dx=0, dy=0, x=0, y=0, width=None, height=None, key=None)

        Copied the ``source`` drawing surface onto this surface at location
        specified with ``dx`` and ``dy``.

        If ``x``, ``y``, ``widht`` and ``height`` are specified, only copies
        that fragment of the ``source`` image, otherwise copies it whole.

        If ``key`` color is specified, that color is considered transparent
        on the source image, and is not copied onto this drawing surface.
