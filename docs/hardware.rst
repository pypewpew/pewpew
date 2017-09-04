Hardware
********


PewPew Lite FeatherWing
=======================

PewPew Lite is a shield for the Adafruit Feather series of development boards
(a FeatherWing, as they call them). You put it on top of one of their boards,
and then program that board (preferably in CircuitPython) to create games and
other interactive programs.

The shield contains six buttons and an eight-by-eight bi-color LED display,
capable of displaying four different colors (black, green, red and yellow). It
also includes a HT16K33 chip that handles the display and the buttons, so that
you can focus on just writing the code for your game. Optionally, you can add a
LiPO battery to it, to make the whole thing into a portable handheld game
console. The shield includes a power switch for that battery.


Future Development
==================

The first prototypes of the PewPew shield used a different chip, allowing it to
have thousands of different colors. However, it couldn't handle key presses, so
it also had to have an additional chip for that. It complicated the whole
design and made it more expensive. During tests, we noticed that you really
don''t need all those colors to make simple and fun games, so we simplified and
made PewPew Lite that is available now. We will keep working on other versions,
though, and quite possibly there will be a version of PewPew with more colors,
or even with a higher resolution display. But we can't really promise anything.
