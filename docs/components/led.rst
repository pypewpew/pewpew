.. _leds:

Light-Emitting Diodes (LEDs)
----------------------------

.. figure:: led-fig.*
   :align: center

.. raw:: latex

   \vspace{4mm}

An LED must be connected in the right orientation: it has a negative lead (cathode) and a positive lead (anode). The cathode is usally marked by being shorter and by a flat part on the rim of the transparent body. Nothing breaks it you insert it the wrong way, it just doesn’t light up.

An LED needs a resistor connected in series, otherwise too much current flows through it and destroys it. It doesn’t matter which way around and on which side of the LED the resistor is placed.

An RGB LED is simply three individual LEDs in the same case, with their cathodes (or anodes) connected together to the longest lead, and the anodes (or cathodes) exposed individually. We use a larger resistance on the green LED because otherwise it is much brighter than the other two, this brings them closer to making white together.

To turn LEDs on and off, we can use any of the PewPew pins as digital outputs.

::

   >>> import board
   >>> import digitalio
   >>> led = digitalio.DigitalInOut(board.P1)
   >>> led.direction = digitalio.Direction.OUTPUT
   >>> led.value = 1
   >>> led.value = 0

Pulse-Width Modulation (PWM)
----------------------------

To dim an LED, we can make use of the microcontroller’s ability to blink an output very quickly, with a fixed frequency, but a variable duration of the “on” part of the period. This is called *pulse-width modulation* (PWM) and is easier for a microcontroller to do than outputting a continuously variable voltage. The ratio of the “on” part to the whole period is called *duty cycle* and is specified as an integer from 0 (always off) to 65535 (always on).

::

   >>> import board
   >>> import pwmio
   >>> r = pwmio.PWMOut(board.P1)
   >>> g = pwmio.PWMOut(board.P3)
   >>> b = pwmio.PWMOut(board.P4)
   >>> r.duty_cycle = 0
   >>> r.duty_cycle = 100
   >>> r.duty_cycle = 10000
   >>> r.duty_cycle = 65535
   >>> import time
   >>> import math
   >>> while True:
   ...     r.duty_cycle = int(65535*(0.5 + 0.5*math.sin(time.monotonic())))
   ...     g.duty_cycle = int(65535*(0.5 + 0.5*math.sin(time.monotonic() - 2.1)))
   ...     b.duty_cycle = int(65535*(0.5 + 0.5*math.sin(time.monotonic() - 4.2)))
   ... 
   #   ^ delete the indenting spaces and press return to end the block
   # press ctrl-C to exit from the infinite loop
