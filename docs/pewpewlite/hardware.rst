Hardware
********


PewPew Lite FeatherWing
=======================

PewPew Lite is a shield for the Adafruit Feather series of development boards
(a FeatherWing, as they call them). You put it on top of one of their boards,
and then program that board (preferably in CircuitPython) to create games and
other interactive programs.

+---------------------------------------------------------+
| Specification                                           |
+==============+==========================================+
| Display      | 8×8 4-color LED matrix                   |
+--------------+------------------------------------------+
| Input        | 6 buttons                                |
+--------------+------------------------------------------+
| Sound        | no sound                                 |
+--------------+------------------------------------------+
| Interface    | 2-wire I²C at address 0x70               |
+--------------+------------------------------------------+
| Controller   | Holtek HT16K33                           |
+--------------+------------------------------------------+
| Battery      | Optional 3.7V 100mAh LiPO (not included) |
+--------------+------------------------------------------+


The shield contains six buttons and an eight-by-eight bi-color LED display,
capable of displaying four different colors (black, green, red and yellow). It
also includes a HT16K33 chip that handles the display and the buttons, so that
you can focus on just writing the code for your game. Optionally, you can add a
LiPO battery to it, to make the whole thing into a portable handheld game
console. The shield includes a power switch for that battery.


Open Development
================

This hardware is developed in the open, and all the designs and related
materials are publicly available under a permissive license. You are free
to inspect how it is build, build your own, improve and extend the design,
and even sell your own versions.

The designs are available in the
`project's repository <https://github.com/deshipu/pewpew>`_.


Buy a Kit
=========

If you want to buy a complete kit that doesn't require soldering, you can find
one at `Tindie <https://www.tindie.com/products/deshipu/pewpew-lite-featherwing/>`_.
