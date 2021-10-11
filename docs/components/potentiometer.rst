Potentiometer
-------------

.. figure:: potentiometer-fig.*
   :align: right

A potentiometer is an adjustable resistor. As its schematic symbol illustrates, it consists of a track of resistive material on which a wiper can slide. The left and right end of the track are connected to the outer pins of the part, the wiper to the middle pin. When the wiper is moved to the left end, the resistance between the left and middle pins is approximately zero. As the wiper is moved to the right, it continuously increases until it reaches the full value when the wiper is at the right end. Conversely, the resistance between the middle and right pins decreases.

When the left and right ends of the track are connected to ground (0V) and +3V (which makes a small current flow through it), the potentiometer acts as a variable *voltage divider*: the middle pin smoothly moves from 0V to 3V as the wiper is moved from left to right.

We can measure this voltage using an analog-to-digital converter (ADC) contained in the microcontroller. On the PewPew, ADCs are available on pins 5, 6, and 7. They linearly convert a voltage between zero and the full supply voltage into an integer between 0 and 65535.

An analog joystick is a combination of two potentiometers.

Light-Dependent Resistor (LDR)
------------------------------

.. figure:: ldr-fig.*
   :align: right

The resistance of an LDR decreases when light shines onto it.

We can combine it to a voltage divider with a fixed resistor and measure the resulting variable voltage using an ADC.

.. raw:: latex

   ~\\ \\

::

   >>> import board
   >>> import analogio
   >>> adc = analogio.AnalogIn(board.P5)
   # potentiometer turned to the left
   >>> adc.value
   48
   # potentiometer turned to the right
   >>> adc.value
   65520
   >>> import pew
   >>> pew.init()
   >>> screen = pew.Pix()
   >>> while True:
   ...     screen.blit(screen, 0, 0, 1, 0, 7, 8)
   ...     screen.box(0, 7, 0, 1, 8)
   ...     screen.pixel(7, 7 - (adc.value >> 13), 3)
   ...     pew.show(screen)
   ...     pew.tick(0.1)
   ... 
   #   ^ delete the indenting spaces and press return to end the block
   # press ctrl-C to exit from the infinite loop
