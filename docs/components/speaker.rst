Piezo Speaker
-------------

.. figure:: speaker-fig.*
   :align: right

A piezo speaker (also called *passive buzzer*) converts electricity into sound using a crystal that expands and contracts when placed in an electric field. It is not suitable for high-quality music, but good for simple beeps, and uses very little power. It doesn’t matter which way you connect it.

The PewPew 10 lacks most of the advanced sound generation capabilities of CircuitPython because they didn’t fit in the small flash memory of the microcontroller, but we can generate simple square waves using the pulse-width modulation facility (described on the :ref:`leds` page).

(There is a digital-to-analog converter (DAC) on pin 5 that can be used with the ``analogio`` module, but feeding it new values regularly enough for sound is hard without support from the firmware.)

.. raw:: latex

   ~\\

::

   >>> import board
   >>> import pwmio
   >>> p = pwmio.PWMOut(board.P4, variable_frequency=True)
   >>> p.duty_cycle = 32768
   # initial frequency is 500 Hz
   >>> p.frequency = 250
   >>> p.frequency = 1000
   >>> p.duty_cycle = 0

   >>> import time
   >>> def play(tune):
   ...     p.duty_cycle = 32768
   ...     for f, d in tune:
   ...         p.frequency = f
   ...         time.sleep(d)
   ...     p.duty_cycle = 0
   ... 
   >>> play(((440, 0.2), (550, 0.1), (587, 0.1), (660, 0.1)))
