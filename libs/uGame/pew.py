from micropython import const
import board
import busio
import digitalio
import time
import gamepad
import st7735


_FONT = (
    b'{{{{{{wws{w{HY{{{{YDYDY{sUtGUsH[wyH{uHgHE{ws{{{{vyxyv{g[K[g{{]f]{{{wDw{{'
    b'{{{wy{{{D{{{{{{{w{K_w}x{VHLHe{wuwww{`KfyD{UKgKU{w}XDK{DxTKT{VxUHU{D[wyx{'
    b'UHfHU{UHEKe{{w{w{{{w{wy{KwxwK{{D{D{{xwKwx{eKg{w{VIHyB{fYH@H{dHdHd{FyxyF{'
    b'`XHX`{DxtxD{Dxtxx{FyxIF{HHDHH{wwwww{KKKHU{HXpXH{xxxxD{Y@DLH{IL@LX{fYHYf{'
    b'`HH`x{fYHIF{`HH`H{UxUKU{Dwwww{HHHIR{HHH]w{HHLD@{HYsYH{HYbww{D[wyD{txxxt{'
    b'x}w_K{GKKKG{wLY{{{{{{{{Dxs{{{{{BIIB{x`XX`{{ByyB{KBIIB{{WIpF{OwUwww{`YB[`'
    b'x`XHH{w{vwc{K{OKHUxHpXH{vwws_{{dD@H{{`XHH{{fYYf{{`XX`x{bYIBK{Ipxx{{F}_d{'
    b'wUws_{{HHIV{{HH]s{{HLD@{{HbbH{{HHV[a{D_}D{Cw|wC{wwwwwwpwOwp{WKfxu{@YYY@{'
)
_SALT = const(132)
_PALETTE = (b'\x00\x00' * 256, b'\x07\xe0' * 256, b'\xf8\x00' * 256,
            b'\xff\xe0' * 256)


K_X = 0x01
K_DOWN = 0x02
K_LEFT = 0x04
K_RIGHT = 0x08
K_UP = 0x10
K_O = 0x20

_tick = None
_display = None


def brightness(level):
    pass


def show(pix):
    for y in range(8):
        for x in range(8):
            color = _PALETTE[pix.pixel(x, y)]
            _display._block(112 - y * 16, x * 16, 127 - y * 16, x * 16 + 15, color)


def keys():
    global _gamepad
    return _gamepad.get_pressed()


def tick(delay):
    global _tick

    _tick += delay
    time.sleep(max(0, _tick - time.monotonic()))


class GameOver(Exception):
    pass


class Pix:
    __slots__ = ('buffer', 'width', 'height')

    def __init__(self, width=8, height=8, buffer=None):
        if buffer is None:
            buffer = bytearray(width * height)
        self.buffer = buffer
        self.width = width
        self.height = height

    @classmethod
    def from_text(cls, string, color=None, bgcolor=0, colors=None):
        pix = cls(4 * len(string), 6)
        font = memoryview(_FONT)
        if colors is None:
            if color is None:
                colors = (3, 2, bgcolor, bgcolor)
            else:
                colors = (color, color, bgcolor, bgcolor)
        x = 0
        for c in string:
            index = ord(c) - 0x20
            if not 0 <= index <= 95:
                continue
            row = 0
            for byte in font[index * 6:index * 6 + 6]:
                unsalted = byte ^ _SALT
                for col in range(4):
                    pix.pixel(x + col, row, colors[unsalted & 0x03])
                    unsalted >>= 2
                row += 1
            x += 4
        return pix

    @classmethod
    def from_iter(cls, lines):
        pix = cls(len(lines[0]), len(lines))
        y = 0
        for line in lines:
            x = 0
            for pixel in line:
                pix.pixel(x, y, pixel)
                x += 1
            y += 1
        return pix

    def pixel(self, x, y, color=None):
        if not 0 <= x < self.width or not 0 <= y < self.height:
            return 0
        if color is None:
            return self.buffer[x + y * self.width]
        self.buffer[x + y * self.width] = color

    def box(self, color, x=0, y=0, width=None, height=None):
        x = min(max(x, 0), self.width - 1)
        y = min(max(y, 0), self.height - 1)
        width = max(0, min(width or self.width, self.width - x))
        height = max(0, min(height or self.height, self.height - y))
        for y in range(y, y + height):
            xx = y * self.width + x
            for i in range(width):
                self.buffer[xx] = color
                xx += 1

    def blit(self, source, dx=0, dy=0, x=0, y=0,
             width=None, height=None, key=None):
        if dx < 0:
            x -= dx
            dx = 0
        if x < 0:
            dx -= x
            x = 0
        if dy < 0:
            y -= dy
            dy = 0
        if y < 0:
            dy -= y
            y = 0
        width = min(min(width or source.width, source.width - x),
                    self.width - dx)
        height = min(min(height or source.height, source.height - y),
                     self.height - dy)
        source_buffer = memoryview(source.buffer)
        self_buffer = self.buffer
        if key is None:
            for row in range(height):
                xx = y * source.width + x
                dxx = dy * self.width + dx
                self_buffer[dxx:dxx + width] = source_buffer[xx:xx + width]
                y += 1
                dy += 1
        else:
            for row in range(height):
                xx = y * source.width + x
                dxx = dy * self.width + dx
                for col in range(width):
                    color = source_buffer[xx]
                    if color != key:
                        self_buffer[dxx] = color
                    dxx += 1
                    xx += 1
                y += 1
                dy += 1

    def __str__(self):
        return "\n".join(
            "".join(
                ('.', '+', '*', '@')[self.pixel(x, y)]
                for x in range(self.width)
            )
            for y in range(self.height)
        )


def init():
    global _tick, _display, _gamepad

    if _tick is not None:
        return

    _tick = time.monotonic()

    _gamepad = gamepad.GamePad(
        digitalio.DigitalInOut(board.X),
        digitalio.DigitalInOut(board.DOWN),
        digitalio.DigitalInOut(board.LEFT),
        digitalio.DigitalInOut(board.RIGHT),
        digitalio.DigitalInOut(board.UP),
        digitalio.DigitalInOut(board.O),
    )

    spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI)
    dc = digitalio.DigitalInOut(board.DC)
    _display = st7735.ST7735R(spi, dc)
    _display.fill(0)
