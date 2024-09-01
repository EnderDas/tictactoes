#custom color pallet
color_pallet = { #generated using coolors.co
    "black": 0x00000000, #black
    "white": 0x00FFFFFF, #white
    "blue": 0x003F88C5, #Steel Blue
    "green": 0x0049BEAA, #Keppel
    "red": 0x00FF495C, #Folly
    "yellow": 0x00EEB868, #Earth Yellow
    "purple": 0x00593C8F, #Rebecca Purple
    "pink": 0x00E0479E, #Hollywood Cerise
}
#expand this and add more colors at least 16

from enum import Enum

FOREGROUND_BLUE = 0x0001
FOREGROUND_GREEN = 0x0002
FOREGROUND_RED = 0x0004
INTENSITY = 0x0008
NORMAL = 0x0000
#i can just shift these left (<<) 4 bits to get background
BLACK = 0x0000
BLUE = FOREGROUND_BLUE
GREEN = FOREGROUND_GREEN
CYAN = FOREGROUND_BLUE | FOREGROUND_GREEN
RED = FOREGROUND_RED
MAGENTA = FOREGROUND_RED | FOREGROUND_BLUE
YELLOW = FOREGROUND_RED | FOREGROUND_GREEN
GREY = FOREGROUND_GREEN | FOREGROUND_BLUE | FOREGROUND_RED
LIGHT_GREY = BLACK | INTENSITY
LIGHT_BLUE = BLUE | INTENSITY
LIGHT_GREEN = GREEN | INTENSITY
LIGHT_CYAN = CYAN | INTENSITY
LIGHT_RED = RED | INTENSITY
LIGHT_MAGENTA = MAGENTA | INTENSITY
LIGHT_YELLOW = YELLOW | INTENSITY
LIGHT_WHITE = GREY | INTENSITY

color_codes = {
    'BLACK': BLACK,
    'BLUE': BLUE,
    'GREEN': GREEN,
    'CYAN': CYAN,
    'RED': RED,
    'MAGENTA': MAGENTA,
    'YELLOW': YELLOW,
    'GREY': GREY,
    'LIGHT_GREY': LIGHT_GREY,
    'LIGHT_BLUE': LIGHT_BLUE,
    'LIGHT_GREEN': LIGHT_GREEN,
    'LIGHT_CYAN': LIGHT_CYAN,
    'LIGHT_RED': LIGHT_RED,
    'LIGHT_MAGENTA': LIGHT_MAGENTA,
    'LIGHT_YELLOW': LIGHT_YELLOW,
    'LIGHT_WHITE': LIGHT_WHITE
}

#should just make this into a dict instead of having it
class ColorPos(Enum):
    BLACK = 0
    BLUE = 1
    GREEN = 2
    CYAN = 3
    RED = 4
    MAGENTA = 5
    YELLOW = 6
    GREY = 7
    LIGHT_GREY = 8
    LIGHT_BLUE = 9
    LIGHT_GREEN = 10
    LIGHT_CYAN = 11
    LIGHT_RED = 12
    LIGHT_MAGENTA = 13
    LIGHT_YELLOW = 14
    LIGHT_WHITE = 15

#this will do for now lol
color_dict = {color.value: color.name for color in ColorPos}

class WinColors:

    def __init__(self):
        self.fore = GREY
        self.back = BLACK

    def set_color(self, fore, back):
        self.fore = fore
        self.back = back

    def set_color_index(self, fore=None, back=None):
        if fore or back:
            if fore:
                self.fore = color_codes[color_dict[fore]]
            if back:
                self.back = color_codes[color_dict[back]]
    @property
    def flag(self):
        return (self.fore | (self.back << 4))
    
color = WinColors()
color.set_color_index(ColorPos.LIGHT_BLUE.value, ColorPos.MAGENTA.value)
from win_screen import *
handle = GetStdHandle(STDOUT)
set_color = lambda flags: SetConsoleTextAttribute(handle, flags)
SetConsoleTextAttribute(handle, color.flag)
print("AYYOOOOOO, it works bb")
color.set_color(LIGHT_RED, GREEN)
set_color(color.flag)
print("this also works")
color.fore = LIGHT_GREY
color.back = BLACK
set_color(color.flag)
print("and even this!!")
color.set_color(GREY, BLACK)
set_color(color.flag)
print("now back to normal...")


"""
TODO
    ::expand and clean up the WinColor class, move from something crude to
    ::something pretty, make it look cleaner and more methods and handle
    ::changing the ColorTable[1-16] with it.
"""
