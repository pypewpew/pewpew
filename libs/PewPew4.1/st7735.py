import ustruct


class ST7735R:
    def __init__(self, spi, dc):
        self.spi = spi
        spi.try_lock()
        spi.configure(baudrate=24000000, polarity=0, phase=0)
        self.dc = dc
        self.dc.switch_to_output(value=0)
        for command, data in (
            (b'\x01', b''),
            (b'\x11', b''),
            (b'\x36', b'\xc8'),
            (b'\x3a', b'\x05'),
            (b'\xb4', b'\x07'),
            (b'\xb1', b'\x01\x2c\x2d'),
            (b'\xb2', b'\x01\x2c\x2d'),
            (b'\xb3', b'\x01\x2c\x2d\x01\x2c\x2d'),
            (b'\xc0', b'\x02\x02\x84'),
            (b'\xc1', b'\xc5'),
            (b'\xc2', b'\x0a\x00'),
            (b'\xc3', b'\x8a\x2a'),
            (b'\xc4', b'\x8a\xee'),
            (b'\xc5', b'\x0e'),
            (b'\x20', b''),
            (b'\xe0', b'\x02\x1c\x07\x12\x37\x32\x29\x2d'
             b'\x29\x25\x2B\x39\x00\x01\x03\x10'),
            (b'\xe1', b'\x03\x1d\x07\x06\x2E\x2C\x29\x2D'
             b'\x2E\x2E\x37\x3F\x00\x00\x02\x10'),
            (b'\x13', b''),
            (b'\x29', b''),
        ):
            self._write(command, data)
        self.dc.value = 0

    def _block(self, x0, y0, x1, y1, data=None):
        xpos = ustruct.pack('>HH', x0 + 2, x1 + 2)
        ypos = ustruct.pack('>HH', y0 + 3, y1 + 3)
        self._write(b'\x2a', xpos)
        self._write(b'\x2b', ypos)
        self._write(b'\x2c', data)

    def _write(self, command=None, data=None):
        if command is not None:
            self.dc.value = 0
            self.spi.write(command)
        if data:
            self.dc.value = 1
            self.spi.write(data)

    def pixel(self, x, y, color=None):
        if not 0 <= x < 128 or not 0 <= y < 128:
            return
        self._block(x, y, x, y, color.to_bytes(2, 'big'))

    def fill_rectangle(self, x, y, width, height, color):
        x = min(128 - 1, max(0, x))
        y = min(128 - 1, max(0, y))
        w = min(128 - x, max(1, width))
        h = min(128 - y, max(1, height))
        self._block(x, y, x + w - 1, y + h - 1, b'')
        chunks, rest = divmod(w * h, 512)
        pixel = color.to_bytes(2, 'big')
        if chunks:
            data = pixel * 512
            for count in range(chunks):
                self._write(None, data)
        self._write(None, pixel * rest)

    def fill(self, color=0):
        self.fill_rectangle(0, 0, 128, 128, color)
