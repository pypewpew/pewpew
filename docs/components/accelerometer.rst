Accelerometer
-------------

.. figure:: accelerometer-fig.*
   :align: right

An accelerometer senses gravity and acceleration using microscopic mechanical parts that are integrated on a silicon chip. It can be used to detect orientation, motion, and gestures like tapping.

The LIS3DH is a low-cost model of accelerometer among many others by different manufacturers. It is a digital device that talks to the microcontroller bidirectionally using a protocol named I²C (*I*\ nter *I*\ ntegrated *C*\ ircuit). I²C uses two signal lines, SDA (*s*\ erial *da*\ ta) and SCL (*s*\ erial *cl*\ ock), plus a common ground. Additionally, I²C requires two resistors (*pull-up resistors*) between each of the signal lines and the positive supply voltage (VCC), this is already done on our LIS3DH breakout board. Multiple devices can be connected to the same I²C bus, the microcontroller can identify them by their address.

To avoid having to remember the raw commands that the microcontroller needs to send over I²C to talk to the accelerometer (they are documented in the `data sheet <https://learn.adafruit.com/adafruit-lis3dh-triple-axis-accelerometer-breakout/downloads>`_ of the part), we use a library that encapsulates that knowledge and abstracts away the specifics of the device. Check the documentation at https://learn.adafruit.com/adafruit-lis3dh-triple-axis-accelerometer-breakout and https://circuitpython.readthedocs.io/projects/lis3dh to learn more about its capabilities, such as tap and double-tap detection. Some of them require additional wiring.

Libraries required: https://github.com/adafruit/Adafruit_CircuitPython_LIS3DH and https://github.com/adafruit/Adafruit_CircuitPython_BusDevice

::

   >>> import board
   >>> import adafruit_lis3dh
   >>> a = adafruit_lis3dh.LIS3DH_I2C(board.I2C(), address=0x1d)
   >>> a.acceleration
   acceleration(x=-0.0862066, y=0.019157, z=9.73177)
   # in m/s^2
   
   >>> import pew
   >>> pew.init()
   >>> screen = pew.Pix()
   >>> while True:
   ...     x, y, z = a.acceleration
   ...     screen.box(0)
   ...     screen.pixel(4 + math.floor(0.3*x), 3 - math.floor(0.3*y), 3)
   ...     pew.show(screen)
   ... 
