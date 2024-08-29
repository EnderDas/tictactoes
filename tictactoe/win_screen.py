import ctypes
from ctypes import Structure, byref, wintypes

"""
8/29/24
reading refs & writing this has given me a splitting headache
i want to claw my eyes out...

i dont have it in me to comment or doc any of this code right now
i will do so on a later date (im still missing a lot of things LMAO)

i couldn't find a single fucking thing of anyone using ctypes.windll.kernel32
GetConsoleScreenBufferInfoEx ANYWHERE but alas it works
this function was really the only thing i absolutely needed working and it does

so for now, thank you and goodnight :)
"""

STDOUT = -11 #Standard output handle

COORD = wintypes._COORD

class WindowCOORD:

    row: int
    col: int

    @classmethod
    def from_param(cls, value: "WindowCOORD"):
        return COORD(value.col, value.row)
    
class CONSOLE_SCREEN_BUFFER_INFO(Structure):
    _fields_ = [
        ("dwSize", COORD),
        ("dwCursorPosition", COORD),
        ("wAttributes", wintypes.WORD),
        ("srWindow", wintypes.SMALL_RECT),
        ("dwMaximumWindowSize", COORD),
    ]

kernel32 = ctypes.windll.kernel32

_GetStdHandle = kernel32.GetStdHandle
_GetStdHandle.argtypes = [
    wintypes.DWORD,
]
_GetStdHandle.restype = wintypes.HANDLE

def GetStdHandle(handle: int):
    return _GetStdHandle(handle)

_GetConsoleMode = kernel32.GetConsoleMode
_GetConsoleMode.argtypes = [wintypes.HANDLE, wintypes.LPDWORD]
_GetConsoleMode.restype = wintypes.BOOL

def GetConsoleMode(std_handle):
    con_mode = wintypes.DWORD()
    result = bool(_GetConsoleMode(std_handle, con_mode))
    if result:
        return con_mode.value
    
_FillConsoleOutputAttribute = kernel32.FillConsoleOutputAttribute
_FillConsoleOutputAttribute.argtypes = [
    wintypes.HANDLE,
    wintypes.WORD,
    wintypes.DWORD,
    WindowCOORD,
    ctypes.POINTER(wintypes.DWORD),
]
_FillConsoleOutputAttribute.restype = wintypes.BOOL

def FillConsoleOutputAttribute(
        std_handle,
        attributes,
        length,
        start
    ):
    cells = wintypes.DWORD(length)
    style = wintypes.WORD(attributes)
    num_written = wintypes.DWORD(0)
    _FillConsoleOutputAttribute(
        std_handle, style, cells, start, byref(num_written)
    )
    return num_written.value

_CreateConsoleScreenBuffer = kernel32.CreateConsoleScreenBuffer
"""
_CreateConsoleScreenBuffer.argtypes = [
    wintypes.DWORD,
    wintypes.DWORD,
    None,
    wintypes.DWORD,
    None
]
no from_param for CreateConsoleScreenBuffer, but it still works? idk
"""
_CreateConsoleScreenBuffer.restype = wintypes.HANDLE

def CreateConsoleScreenBuffer(access = None, shared = None, flags = None):
    access = access if access else wintypes.DWORD(0x80000000 | 0x40000000)
    shared = shared if shared else wintypes.DWORD(0x00000001 | 0x00000002)
    flags = flags if flags else wintypes.DWORD(1)
    buffer = _CreateConsoleScreenBuffer(access, shared, None, flags, None)
    if buffer == wintypes.HANDLE(-1):
        raise Exception("could not create buffer")
    else:
        return buffer

class CONSOLE_SCREEN_BUFFER_INFOEX(Structure):
    _fields_ = (('cbSize',               wintypes.ULONG),
                ('dwSize',               COORD),
                ('dwCursorPosition',     COORD),
                ('wAttributes',          wintypes.WORD),
                ('srWindow',             wintypes.SMALL_RECT),
                ('dwMaximumWindowSize',  COORD),
                ('wPopupAttributes',     wintypes.WORD),
                ('bFullscreenSupported', wintypes.BOOL),
                ('ColorTable',           wintypes.DWORD * 16))

class CONSOLE_SCREEN_BUFFER_INFO(Structure):
    _fields_ = [
        ("dwSize", COORD),
        ("dwCursorPosition", COORD),
        ("wAttributes", wintypes.WORD),
        ("srWindow", wintypes.SMALL_RECT),
        ("dwMaximumWindowSize", COORD),
    ]

_GetConsoleScreenBufferInfo = kernel32.GetConsoleScreenBufferInfo
_GetConsoleScreenBufferInfo.argtypes = [
    wintypes.HANDLE,
    ctypes.POINTER(CONSOLE_SCREEN_BUFFER_INFO),
]
_GetConsoleScreenBufferInfo.restype = wintypes.BOOL

def GetConsoleScreenBufferInfo(std_handle):
    buffer_info = CONSOLE_SCREEN_BUFFER_INFO()
    _GetConsoleScreenBufferInfo(std_handle, byref(buffer_info))
    return buffer_info

_GetConsoleScreenBufferInfoEx = kernel32.GetConsoleScreenBufferInfoEx
_GetConsoleScreenBufferInfoEx.argtypes = [
    wintypes.HANDLE,
    ctypes.POINTER(CONSOLE_SCREEN_BUFFER_INFOEX)
]
_GetConsoleScreenBufferInfoEx.restype = wintypes.BOOL

def GetConsoleScreenBufferInfoEx(std_handle):
    extended_buffer_info = CONSOLE_SCREEN_BUFFER_INFOEX()
    _GetConsoleScreenBufferInfoEx(int(std_handle), byref(extended_buffer_info))
    return extended_buffer_info

_SetConsoleCursorPosition = kernel32.SetConsoleCursorPosition
_SetConsoleCursorPosition.argtypes = [
    wintypes.HANDLE,
    WindowCOORD,
]
_SetConsoleCursorPosition.restype = wintypes.BOOL

def SetConsoleCursorPosition(std_handle, coords):
    return bool(_SetConsoleCursorPosition(std_handle, coords))

_SetConsoleTextAttribute = kernel32.SetConsoleTextAttribute
_SetConsoleTextAttribute.argtypes = [
    wintypes.HANDLE,
    wintypes.WORD,
]
_SetConsoleTextAttribute.restype = wintypes.BOOL

def SetConsoleTextAttribute(handle, attributes):
    return bool(_SetConsoleTextAttribute(handle, attributes))

handle = GetStdHandle(STDOUT)
buffer_info = GetConsoleScreenBufferInfo(handle)
print(buffer_info)
extended_info = GetConsoleScreenBufferInfoEx(handle)
print(extended_info)

def _decode_RGB(color_hex):
    red = color_hex & 255
    green = (color_hex >> 8) & 255
    blue = (color_hex >> 16) & 255
    return (red, green, blue)

color_pallet = { #generated using coolors.co
    "black": 0x00000000,
    "white": 0x00FFFFFF,
    #"grey": 0x003F3F37, #Black Olive
    #"light": 0x00D3BDB0, #Pale Dogwood
    "blue": 0x003F88C5, #Steel Blue
    "green": 0x0049BEAA, #Keppel
    "red": 0x00FF495C, #Folly
    "yellow": 0x00EEB868, #Earth Yellow
    "purple": 0x00593C8F, #Rebecca Purple
    "pink": 0x00E0479E, #Hollywood Cerise
}

class Colors:
    BLACK = 0
    WHITE = 1
    BLUE = 2
    GREEN = 3
    RED = 4
    YELLOW = 5
    PURPLE = 6
    PINK = 7


class Styles(object):
    NORMAL              = 0x00 # dim text, dim background
    BRIGHT              = 0x08 # bright text, dim background
    BRIGHT_BACKGROUND   = 0x80 # dim text, bright background

class WindowColor:

    def __init__(self):
        self._default = GetConsoleScreenBufferInfo(STDOUT).wAttributes
        self.set_attrs(self._default)
        self._light = 0

    def set_attrs(self, value):
        self._fore = value & 7
        self._back = (value >> 4) & 7
        self._style = value & (Styles.BRIGHT | Styles.BRIGHT_BACKGROUND)

    def get_attrs(self):
        return self._fore + self._back * 16 + (self._style)
    
    def fore(self, color):
        self._fore = color

    def back(self, color):
        self._back = color

    def style(self, style):
        self._style = style

if __name__ == "__main__":
    color = WindowColor()
    color.fore(Colors.WHITE)
    color.back(Colors.PURPLE)
    color.style(Styles.BRIGHT_BACKGROUND)
    handle = GetStdHandle(STDOUT)
    SetConsoleTextAttribute(handle, color.get_attrs())