Addressable LED Strip
---------------------

.. figure:: dotstar-fig.*
   :align: right

These strips can be several meters long and contain hundreds of LEDs, each of them individually controllable. Each of the addressable LED packages contains three LEDs (red, green, blue; some also have a fourth white one) and a controller chip with communication input and output pins. They are daisy-chained on the strip so that the output of one goes to the input of the next. The input of the first one is connected to the microcontroller, which sends out a stream of color values. The first LED takes the first set of them and keeps it for itself, then passes all the rest through to the next one, and so on, until the last LED on the strip only receives the last set of values left for it.

Addressable LEDs exist in two common varieties, “Neopixels” (WS2812B, SK6812), which have one communication line (data), and “Dotstars” (APA102, SK9822), which have two (clock and data). They are all intended for 5 V, but the Dotstars used here happen to work acceptably on 3 V.

Powering 3 addressable LEDs from the PewPew battery or USB supply works, but for longer strips you need a separate power supply (unless you keep very few LEDs on at any time). Each LED can use up to 60 mA (3*20) – multiplied by a large number, this quickly overwhelms small power supplies.

Arrows on the strip indicate the data flow direction – make sure you connect the controller to the input end of the strip. The 5V and GND supply lines run through the whole strip and connect all LEDs in parallel, these can be connected on either end (or even both).

Libraries required: https://github.com/adafruit/Adafruit_CircuitPython_Pixelbuf and https://github.com/adafruit/Adafruit_CircuitPython_Dotstar

::

   >>> import adafruit_dotstar
   >>> import board
   >>> d = adafruit_dotstar.DotStar(board.P2, board.P1, 3, pixel_order=adafruit_dotstar.RBG)
   >>> d
   [[0, 0, 0, 1.0], [0, 0, 0, 1.0], [0, 0, 0, 1.0]]
   # [R (0-255), G (0-255), B (0-255), brightness (0.0-1.0 in steps of 1/31)]
   >>> d[0] = 0x100000
   >>> d[0] = 0x001000
   >>> d[0] = 0x000010
   >>> d[0] = (20, 10, 0)
   >>> d.fill(0)
   >>> import time
   >>> import math
   >>> d.brightness = 0.2
   >>> while True:
   ...     for i in range(3):
   ...         d[i] = [int(255*math.sin(time.monotonic() - 0.5*j + 2.1*i)**12) for j in range(3)]
   ... 
   >>> d.deinit()
   # send raw data using a lower-level interface without the adafruit_dotstar library
   >>> import busio
   >>> spi = busio.SPI(board.P2, MOSI=board.P1)
   >>> spi.try_lock()
   True
   >>> spi.write(b'\x00\x00\x00\x00\xff\x33\x00\x00\xff\x00\x33\x00\xff\x00\x00\x33\xff')
   >>> spi.unlock()
   >>> spi.deinit()
