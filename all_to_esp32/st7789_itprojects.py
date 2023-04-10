import ustruct
import utime
import ustruct as struct

_NOP = const(0x00)
_SWRESET = const(0x01)
_RDDID = const(0x04)
_RDDST = const(0x09)

_SLPIN = const(0x10)
_SLPOUT = const(0x11)
_PTLON = const(0x12)
_NORON = const(0x13)

_INVOFF = const(0x20)
_INVON = const(0x21)
_DISPOFF = const(0x28)
_DISPON = const(0x29)
_CASET = const(0x2A)
_RASET = const(0x2B)
_RAMWR = const(0x2C)
_RAMRD = const(0x2E)

_PTLAR = const(0x30)
_COLMOD = const(0x3A)
_MADCTL = const(0x36)

_FRMCTR1 = const(0xB1)
_FRMCTR2 = const(0xB2)
_FRMCTR3 = const(0xB3)
_INVCTR = const(0xB4)
_DISSET5 = const(0xB6)

_PWCTR1 = const(0xC0)
_PWCTR2 = const(0xC1)
_PWCTR3 = const(0xC2)
_PWCTR4 = const(0xC3)
_PWCTR5 = const(0xC4)
_VMCTR1 = const(0xC5)

_RDID1 = const(0xDA)
_RDID2 = const(0xDB)
_RDID3 = const(0xDC)
_RDID4 = const(0xDD)

_PWCTR6 = const(0xFC)

_GMCTRP1 = const(0xE0)
_GMCTRN1 = const(0xE1)

BLACK = const(0x0000)
BLUE = const(0x001F)
RED = const(0xF800)
GREEN = const(0x07E0)
CYAN = const(0x07FF)
MAGENTA = const(0xF81F)
YELLOW = const(0xFFE0)
WHITE = const(0xFFFF)

ST7789_VSCRDEF = const(0x33)
ST7789_VSCSAD = const(0x37)

_MIRROR=const(0x50)

_BIT7 = const(0x80)
_BIT6 = const(0x40)
_BIT5 = const(0x20)
_BIT4 = const(0x10)
_BIT3 = const(0x08)
_BIT2 = const(0x04)
_BIT1 = const(0x02)
_BIT0 = const(0x01)

WIDTH_320 = [(240, 320,  0,  0),
             (320, 240,  0,  0),
             (240, 320,  0,  0),
             (320, 240,  0,  0)]

WIDTH_240 = [(240, 240,  0,  0),
             (240, 240,  0,  0),
             (240, 240,  0, 80),
             (240, 240, 80,  0)]

WIDTH_135 = [(135, 240, 52, 40),
             (240, 135, 40, 53),
             (135, 240, 53, 40),
             (240, 135, 40, 52)]


# MADCTL ROTATIONS[rotation % 4]
ROTATIONS = [0x00, 0x60, 0xc0, 0xa0]


def color565(r, g, b):
    return (r & 0xf8) << 8 | (g & 0xfc) << 3 | b >> 3

def _encode_pos(x, y):
    """Encode a postion into bytes."""
    return struct.pack(_ENCODE_POS, x, y)


def _encode_pixel(color):
    """Encode a pixel color into bytes."""
    return struct.pack(_ENCODE_PIXEL, color)


class DummyPin:
    """A fake gpio pin for when you want to skip pins."""

    OUT = 0
    IN = 0
    PULL_UP = 0
    PULL_DOWN = 0
    OPEN_DRAIN = 0
    ALT = 0
    ALT_OPEN_DRAIN = 0
    LOW_POWER = 0
    MED_POWER = 0
    HIGH_PWER = 0
    IRQ_FALLING = 0
    IRQ_RISING = 0
    IRQ_LOW_LEVEL = 0
    IRQ_HIGH_LEVEL = 0

    def __call__(self, *args, **kwargs):
        return False

    init = __call__
    value = __call__
    out_value = __call__
    toggle = __call__
    high = __call__
    low = __call__
    on = __call__
    off = __call__
    mode = __call__
    pull = __call__
    drive = __call__
    irq = __call__


class Display:
    _PAGE_SET = None
    _COLUMN_SET = None
    _RAM_WRITE = None
    _RAM_READ = None
    _INIT = ()
    _ENCODE_PIXEL = ">H"
    _ENCODE_POS = ">HH"
    _DECODE_PIXEL = ">BBB"

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.init()


    def init(self):
        """Run the initialization commands."""
        for command, data in self._INIT:
            self._write(command, data)
            
    

    def _block(self, x0, y0, x1, y1, data=None):
        """Read or write a block of data."""
        self._write(self._COLUMN_SET, self._encode_pos(x0, x1))
        self._write(self._PAGE_SET, self._encode_pos(y0+80, y1+80))
        if data is None:
            size = ustruct.calcsize(self._DECODE_PIXEL)
            return self._read(self._RAM_READ, (x1 - x0 + 1) * (y1 - y0 + 1) * size)
    
        self._write(self._RAM_WRITE, data)

    def _encode_pos(self, a, b):
        """Encode a postion into bytes."""
        return ustruct.pack(self._ENCODE_POS, a, b)

    def _encode_pixel(self, color):
        """Encode a pixel color into bytes."""
        return ustruct.pack(self._ENCODE_PIXEL, color)

    def _decode_pixel(self, data):
        """Decode bytes into a pixel color."""
        return color565(*ustruct.unpack(self._DECODE_PIXEL, data))

    def pixel(self, x, y, color=None):
        """Read or write a pixel."""
        if color is None:
            return self._decode_pixel(self._block(x, y, x, y))
        if not 0 <= x < self.width or not 0 <= y < self.height:
            return
        self._block(x, y, x, y, self._encode_pixel(color))

    def fill_rectangle(self, x, y, width, height, color):
        """Draw a filled rectangle."""
        x = min(self.width - 1, max(0, x))
        y = min(self.height - 1, max(0, y))
        w = min(self.width - x, max(1, width))
        h = min(self.height - y, max(1, height))
        self._block(x, y, x + w - 1, y + h - 1, b'')
        chunks, rest = divmod(w * h, 512)
        print("color:", color)
        pixel = self._encode_pixel(color)
        print("decode:", pixel)
        if chunks:
            data = pixel * 512
            for count in range(chunks):
                self._write(None, data)
        if rest:
            self._write(None, pixel * rest)

    def fill(self, color=0):
        """Fill whole screen."""
        self.fill_rectangle(0, 0, self.width, self.height, color)

    def hline(self, x, y, width, color):
        """Draw a horizontal line."""
        self.fill_rectangle(x, y, width, 1, color)
        
    def rotation(self):
        self._write(_MADCTL, bytes([_BIT7]))
        
    def vscrdef(self, tfa, vsa, bfa):
        struct.pack(">HHH", tfa, vsa, bfa)
        self._write(ST7789_VSCRDEF, struct.pack(">HHH", tfa, vsa, bfa))
    
    def vscsad(self, vssa):
        self._write(ST7789_VSCSAD, struct.pack(">H", vssa))

    def vline(self, x, y, height, color):
        """Draw a vertical line."""
        self.fill_rectangle(x, y, 1, height, color)

    def blit_buffer(self, buffer, x, y, width, height):
        """Copy pixels from a buffer."""
        if (not 0 <= x < self.width or
            not 0 <= y < self.height or
            not 0 < x + width <= self.width or
            not 0 < y + height <= self.height):
                raise ValueError("out of bounds")
        self._block(x, y, x + width - 1, y + height - 1, buffer)


class DisplaySPI(Display):
    def __init__(self, spi, dc, cs=None, rst=None, width=1, height=1):
        self.spi = spi
        self.cs = cs
        self.dc = dc
        self.rst = rst
        if self.rst is None:
            self.rst = DummyPin()
        if self.cs is None:
            self.cs = DummyPin()
        self.cs.init(self.cs.OUT, value=1)
        self.dc.init(self.dc.OUT, value=0)
        self.rst.init(self.rst.OUT, value=1)
        self.reset()
        super().__init__(width, height)

    def reset(self):
        self.rst(0)
        utime.sleep_ms(50)
        self.rst(1)
        utime.sleep_ms(50)

    def _write(self, command=None, data=None):
        if command is not None:
            self.dc(0)
            self.cs(0)
            self.spi.write(bytearray([command]))
            self.cs(1)
        if data:
            self.dc(1)
            self.cs(0)
            self.spi.write(data)
            self.cs(1)

    def _read(self, command=None, count=0):
        self.dc(0)
        self.cs(0)
        if command is not None:
            self.spi.write(bytearray([command]))
        if count:
            data = self.spi.read(count)
        self.cs(1)
        return data


class ST7789(DisplaySPI):
    _COLUMN_SET = _CASET
    _PAGE_SET = _RASET
    _RAM_WRITE = _RAMWR
    _RAM_READ = _RAMRD
    _INIT = (
        (_SWRESET, None),
        (_SLPOUT, None),
        (_COLMOD, b"\x55"),  # 16bit color
        (_MADCTL, b"\x08"),
    )

    def __init__(self, spi, dc, cs, rst=None, width=240, height=240):
        super().__init__(spi, dc, cs, rst, width, height)

    def init(self):

        super().init()
        cols = ustruct.pack(">HH", 0, self.width)
        rows = ustruct.pack(">HH", 0, self.height)
        for command, data in (
            (_CASET, cols),
            (_RASET, rows),
            (_INVON, None),
            (_NORON, None),
            (_DISPON, None),
            (_MADCTL, b"\xc0"),  # Set rotation to 0 and use RGB
        ):
            self._write(command, data)
    
    def _text8(self, font, text, x0, y0, color=WHITE, background=BLACK):
        """
        Internal method to write characters with width of 8 and
        heights of 8 or 16.

        Args:
            font (module): font module to use
            text (str): text to write
            x0 (int): column to start drawing at
            y0 (int): row to start drawing at
            color (int): 565 encoded color to use for characters
            background (int): 565 encoded color to use for background
        """
        for char in text:
            ch = ord(char)
            if (font.FIRST <= ch < font.LAST
                    and x0+font.WIDTH <= self.width
                    and y0+font.HEIGHT <= self.height):

                if font.HEIGHT == 8:
                    passes = 1
                    size = 8
                    each = 0
                else:
                    passes = 2
                    size = 16
                    each = 8

                for line in range(passes):
                    idx = (ch-font.FIRST)*size+(each*line)
                    buffer = struct.pack(
                        '>64H',
                        color if font.FONT[idx] & _BIT7 else background,
                        color if font.FONT[idx] & _BIT6 else background,
                        color if font.FONT[idx] & _BIT5 else background,
                        color if font.FONT[idx] & _BIT4 else background,
                        color if font.FONT[idx] & _BIT3 else background,
                        color if font.FONT[idx] & _BIT2 else background,
                        color if font.FONT[idx] & _BIT1 else background,
                        color if font.FONT[idx] & _BIT0 else background,
                        color if font.FONT[idx+1] & _BIT7 else background,
                        color if font.FONT[idx+1] & _BIT6 else background,
                        color if font.FONT[idx+1] & _BIT5 else background,
                        color if font.FONT[idx+1] & _BIT4 else background,
                        color if font.FONT[idx+1] & _BIT3 else background,
                        color if font.FONT[idx+1] & _BIT2 else background,
                        color if font.FONT[idx+1] & _BIT1 else background,
                        color if font.FONT[idx+1] & _BIT0 else background,
                        color if font.FONT[idx+2] & _BIT7 else background,
                        color if font.FONT[idx+2] & _BIT6 else background,
                        color if font.FONT[idx+2] & _BIT5 else background,
                        color if font.FONT[idx+2] & _BIT4 else background,
                        color if font.FONT[idx+2] & _BIT3 else background,
                        color if font.FONT[idx+2] & _BIT2 else background,
                        color if font.FONT[idx+2] & _BIT1 else background,
                        color if font.FONT[idx+2] & _BIT0 else background,
                        color if font.FONT[idx+3] & _BIT7 else background,
                        color if font.FONT[idx+3] & _BIT6 else background,
                        color if font.FONT[idx+3] & _BIT5 else background,
                        color if font.FONT[idx+3] & _BIT4 else background,
                        color if font.FONT[idx+3] & _BIT3 else background,
                        color if font.FONT[idx+3] & _BIT2 else background,
                        color if font.FONT[idx+3] & _BIT1 else background,
                        color if font.FONT[idx+3] & _BIT0 else background,
                        color if font.FONT[idx+4] & _BIT7 else background,
                        color if font.FONT[idx+4] & _BIT6 else background,
                        color if font.FONT[idx+4] & _BIT5 else background,
                        color if font.FONT[idx+4] & _BIT4 else background,
                        color if font.FONT[idx+4] & _BIT3 else background,
                        color if font.FONT[idx+4] & _BIT2 else background,
                        color if font.FONT[idx+4] & _BIT1 else background,
                        color if font.FONT[idx+4] & _BIT0 else background,
                        color if font.FONT[idx+5] & _BIT7 else background,
                        color if font.FONT[idx+5] & _BIT6 else background,
                        color if font.FONT[idx+5] & _BIT5 else background,
                        color if font.FONT[idx+5] & _BIT4 else background,
                        color if font.FONT[idx+5] & _BIT3 else background,
                        color if font.FONT[idx+5] & _BIT2 else background,
                        color if font.FONT[idx+5] & _BIT1 else background,
                        color if font.FONT[idx+5] & _BIT0 else background,
                        color if font.FONT[idx+6] & _BIT7 else background,
                        color if font.FONT[idx+6] & _BIT6 else background,
                        color if font.FONT[idx+6] & _BIT5 else background,
                        color if font.FONT[idx+6] & _BIT4 else background,
                        color if font.FONT[idx+6] & _BIT3 else background,
                        color if font.FONT[idx+6] & _BIT2 else background,
                        color if font.FONT[idx+6] & _BIT1 else background,
                        color if font.FONT[idx+6] & _BIT0 else background,
                        color if font.FONT[idx+7] & _BIT7 else background,
                        color if font.FONT[idx+7] & _BIT6 else background,
                        color if font.FONT[idx+7] & _BIT5 else background,
                        color if font.FONT[idx+7] & _BIT4 else background,
                        color if font.FONT[idx+7] & _BIT3 else background,
                        color if font.FONT[idx+7] & _BIT2 else background,
                        color if font.FONT[idx+7] & _BIT1 else background,
                        color if font.FONT[idx+7] & _BIT0 else background
                    )
                    self.blit_buffer(buffer, x0, y0+8*line, 8, 8)

                x0 += 8
            
    def _text16(self, font, text, x0, y0, color=WHITE, background=BLACK):
        for char in text:
            ch = ord(char)
            if (font.FIRST <= ch < font.LAST
                    and x0+font.WIDTH <= self.width
                    and y0+font.HEIGHT <= self.height):

                each = 16
                if font.HEIGHT == 16:
                    passes = 2
                    size = 32
                else:
                    passes = 4
                    size = 64

                for line in range(passes):
                    idx = (ch-font.FIRST)*size+(each*line)
                    buffer = struct.pack(
                        '>128H',
                        color if font.FONT[idx] & _BIT7 else background,
                        color if font.FONT[idx] & _BIT6 else background,
                        color if font.FONT[idx] & _BIT5 else background,
                        color if font.FONT[idx] & _BIT4 else background,
                        color if font.FONT[idx] & _BIT3 else background,
                        color if font.FONT[idx] & _BIT2 else background,
                        color if font.FONT[idx] & _BIT1 else background,
                        color if font.FONT[idx] & _BIT0 else background,
                        color if font.FONT[idx+1] & _BIT7 else background,
                        color if font.FONT[idx+1] & _BIT6 else background,
                        color if font.FONT[idx+1] & _BIT5 else background,
                        color if font.FONT[idx+1] & _BIT4 else background,
                        color if font.FONT[idx+1] & _BIT3 else background,
                        color if font.FONT[idx+1] & _BIT2 else background,
                        color if font.FONT[idx+1] & _BIT1 else background,
                        color if font.FONT[idx+1] & _BIT0 else background,
                        color if font.FONT[idx+2] & _BIT7 else background,
                        color if font.FONT[idx+2] & _BIT6 else background,
                        color if font.FONT[idx+2] & _BIT5 else background,
                        color if font.FONT[idx+2] & _BIT4 else background,
                        color if font.FONT[idx+2] & _BIT3 else background,
                        color if font.FONT[idx+2] & _BIT2 else background,
                        color if font.FONT[idx+2] & _BIT1 else background,
                        color if font.FONT[idx+2] & _BIT0 else background,
                        color if font.FONT[idx+3] & _BIT7 else background,
                        color if font.FONT[idx+3] & _BIT6 else background,
                        color if font.FONT[idx+3] & _BIT5 else background,
                        color if font.FONT[idx+3] & _BIT4 else background,
                        color if font.FONT[idx+3] & _BIT3 else background,
                        color if font.FONT[idx+3] & _BIT2 else background,
                        color if font.FONT[idx+3] & _BIT1 else background,
                        color if font.FONT[idx+3] & _BIT0 else background,
                        color if font.FONT[idx+4] & _BIT7 else background,
                        color if font.FONT[idx+4] & _BIT6 else background,
                        color if font.FONT[idx+4] & _BIT5 else background,
                        color if font.FONT[idx+4] & _BIT4 else background,
                        color if font.FONT[idx+4] & _BIT3 else background,
                        color if font.FONT[idx+4] & _BIT2 else background,
                        color if font.FONT[idx+4] & _BIT1 else background,
                        color if font.FONT[idx+4] & _BIT0 else background,
                        color if font.FONT[idx+5] & _BIT7 else background,
                        color if font.FONT[idx+5] & _BIT6 else background,
                        color if font.FONT[idx+5] & _BIT5 else background,
                        color if font.FONT[idx+5] & _BIT4 else background,
                        color if font.FONT[idx+5] & _BIT3 else background,
                        color if font.FONT[idx+5] & _BIT2 else background,
                        color if font.FONT[idx+5] & _BIT1 else background,
                        color if font.FONT[idx+5] & _BIT0 else background,
                        color if font.FONT[idx+6] & _BIT7 else background,
                        color if font.FONT[idx+6] & _BIT6 else background,
                        color if font.FONT[idx+6] & _BIT5 else background,
                        color if font.FONT[idx+6] & _BIT4 else background,
                        color if font.FONT[idx+6] & _BIT3 else background,
                        color if font.FONT[idx+6] & _BIT2 else background,
                        color if font.FONT[idx+6] & _BIT1 else background,
                        color if font.FONT[idx+6] & _BIT0 else background,
                        color if font.FONT[idx+7] & _BIT7 else background,
                        color if font.FONT[idx+7] & _BIT6 else background,
                        color if font.FONT[idx+7] & _BIT5 else background,
                        color if font.FONT[idx+7] & _BIT4 else background,
                        color if font.FONT[idx+7] & _BIT3 else background,
                        color if font.FONT[idx+7] & _BIT2 else background,
                        color if font.FONT[idx+7] & _BIT1 else background,
                        color if font.FONT[idx+7] & _BIT0 else background,
                        color if font.FONT[idx+8] & _BIT7 else background,
                        color if font.FONT[idx+8] & _BIT6 else background,
                        color if font.FONT[idx+8] & _BIT5 else background,
                        color if font.FONT[idx+8] & _BIT4 else background,
                        color if font.FONT[idx+8] & _BIT3 else background,
                        color if font.FONT[idx+8] & _BIT2 else background,
                        color if font.FONT[idx+8] & _BIT1 else background,
                        color if font.FONT[idx+8] & _BIT0 else background,
                        color if font.FONT[idx+9] & _BIT7 else background,
                        color if font.FONT[idx+9] & _BIT6 else background,
                        color if font.FONT[idx+9] & _BIT5 else background,
                        color if font.FONT[idx+9] & _BIT4 else background,
                        color if font.FONT[idx+9] & _BIT3 else background,
                        color if font.FONT[idx+9] & _BIT2 else background,
                        color if font.FONT[idx+9] & _BIT1 else background,
                        color if font.FONT[idx+9] & _BIT0 else background,
                        color if font.FONT[idx+10] & _BIT7 else background,
                        color if font.FONT[idx+10] & _BIT6 else background,
                        color if font.FONT[idx+10] & _BIT5 else background,
                        color if font.FONT[idx+10] & _BIT4 else background,
                        color if font.FONT[idx+10] & _BIT3 else background,
                        color if font.FONT[idx+10] & _BIT2 else background,
                        color if font.FONT[idx+10] & _BIT1 else background,
                        color if font.FONT[idx+10] & _BIT0 else background,
                        color if font.FONT[idx+11] & _BIT7 else background,
                        color if font.FONT[idx+11] & _BIT6 else background,
                        color if font.FONT[idx+11] & _BIT5 else background,
                        color if font.FONT[idx+11] & _BIT4 else background,
                        color if font.FONT[idx+11] & _BIT3 else background,
                        color if font.FONT[idx+11] & _BIT2 else background,
                        color if font.FONT[idx+11] & _BIT1 else background,
                        color if font.FONT[idx+11] & _BIT0 else background,
                        color if font.FONT[idx+12] & _BIT7 else background,
                        color if font.FONT[idx+12] & _BIT6 else background,
                        color if font.FONT[idx+12] & _BIT5 else background,
                        color if font.FONT[idx+12] & _BIT4 else background,
                        color if font.FONT[idx+12] & _BIT3 else background,
                        color if font.FONT[idx+12] & _BIT2 else background,
                        color if font.FONT[idx+12] & _BIT1 else background,
                        color if font.FONT[idx+12] & _BIT0 else background,
                        color if font.FONT[idx+13] & _BIT7 else background,
                        color if font.FONT[idx+13] & _BIT6 else background,
                        color if font.FONT[idx+13] & _BIT5 else background,
                        color if font.FONT[idx+13] & _BIT4 else background,
                        color if font.FONT[idx+13] & _BIT3 else background,
                        color if font.FONT[idx+13] & _BIT2 else background,
                        color if font.FONT[idx+13] & _BIT1 else background,
                        color if font.FONT[idx+13] & _BIT0 else background,
                        color if font.FONT[idx+14] & _BIT7 else background,
                        color if font.FONT[idx+14] & _BIT6 else background,
                        color if font.FONT[idx+14] & _BIT5 else background,
                        color if font.FONT[idx+14] & _BIT4 else background,
                        color if font.FONT[idx+14] & _BIT3 else background,
                        color if font.FONT[idx+14] & _BIT2 else background,
                        color if font.FONT[idx+14] & _BIT1 else background,
                        color if font.FONT[idx+14] & _BIT0 else background,
                        color if font.FONT[idx+15] & _BIT7 else background,
                        color if font.FONT[idx+15] & _BIT6 else background,
                        color if font.FONT[idx+15] & _BIT5 else background,
                        color if font.FONT[idx+15] & _BIT4 else background,
                        color if font.FONT[idx+15] & _BIT3 else background,
                        color if font.FONT[idx+15] & _BIT2 else background,
                        color if font.FONT[idx+15] & _BIT1 else background,
                        color if font.FONT[idx+15] & _BIT0 else background
                    )
                    self.blit_buffer(buffer, x0, y0+8*line, 16, 8)
            x0 += font.WIDTH
            
    def text(self, font, text, x0, y0, color=WHITE, background=BLACK):
        if font.WIDTH == 8:
            self._text8(font, text, x0, y0, color, background)
        else:
            self._text16(font, text, x0, y0, color, background)


class ST7889_Image(ST7789):
    
    def _set_columns(self, start, end):
        if start <= end:
            self._write(_CASET, self._encode_pos(start, end))

            
    def _set_rows(self, start, end):
        if start <= end:
            self._write(_RASET, self._encode_pos(start, end))
    
    def _set_window(self, x0, y0, x1, y1):
        self._set_columns(x0, x1)
        self._set_rows(y0, y1)
        self._write(_RAMWR)
        
    def show_img(self, x0, y0, x1, y1, img_data):
        self._set_window(x0, y0 + 80, x1, y1 + 80)
        self._write(None, img_data)
