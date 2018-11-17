Hardware
********

PewPew Standalone v10.2
=======================

PewPew Standalone is a handheld device, it doesn't require any additional
hardware, except for two 1.5V AAA batteries.

+---------------------------------------------------------+
| Specification                                           |
+==============+==========================================+
| Display      | 8×8 red LED matrix                       |
+--------------+------------------------------------------+
| Input        | 6 buttons                                |
+--------------+------------------------------------------+
| Sound        | no sound                                 |
+--------------+------------------------------------------+
| Interface    | 12-pin connector at the back             |
+--------------+------------------------------------------+
| Controller   | Atmel SAMD21                             |
+--------------+------------------------------------------+
| Battery      | 2 x AAA 1.5V alkaline (not included)     |
+--------------+------------------------------------------+

The device includes a display, six buttons, on-off switch, USB port and a
battery holder. The batteries are required for operation, it can't be powered
from the USB port. There is also a 12-pin connector on the back of the device
that can be used for connecting other electronic devices.

The 12-pin Connector
====================

+-------+----------+----------------------------------------------+
| Label | Name     | Function                                     |
+=======+==========+==============================================+
| ``R`` | Reset    | Ground this pin to perform hard reset.       |
+-------+----------+----------------------------------------------+
| ``-`` | GND      | Negative power and ground. There are 2 pins. |
+-------+----------+----------------------------------------------+
| ``1`` | board.P1 | DigitalIO, SWC, SPI-MISO/MOSI, PWM           |
+-------+----------+----------------------------------------------+
| ``2`` | board.P2 | DigitalIO, SWD, SPI-SCK, PWM                 |
+-------+----------+----------------------------------------------+
| ``3`` | board.P3 | DigitalIO, I2C-SDA, SPI-MISO/MOSI, PWM       |
+-------+----------+----------------------------------------------+
| ``4`` | board.P4 | DigitalIO, I2C-SCL, SPI-SCK, PWM             |
+-------+----------+----------------------------------------------+
| ``5`` | board.P5 | DigitalIO, ADC, DAC, PWM, TouchIO            |
+-------+----------+----------------------------------------------+
| ``6`` | board.P6 | DigitalIO, ADC, TouchIO                      |
+-------+----------+----------------------------------------------+
| ``7`` | board.P7 | DigitalIO, SPI-MISO/MOSI, UART, TouchIO      |
+-------+----------+----------------------------------------------+
| ``+`` | VCC      | Positive 3V power. There are 2 pins.         |
+-------+----------+----------------------------------------------+

You can insert a male header into the holes at the back of the device and plug
it into a breadboard to easily gain access to the pins.

Open Development
================

This hardware is developed in the open, and all the designs and related
materials are publicly available under a permissive license. You are free to
inspect how it is build, build your own, improve and extend the design, and
even sell your own versions.

The designs are available in the
`project's repository <https://github.com/deshipu/pewpew>`_.


Buy a Kit
=========

If you want to buy a kit that you only need to solder, you can
find one at `Tindie <https://www.tindie.com/products/deshipu/small-pewpew-standalone/>`_.
