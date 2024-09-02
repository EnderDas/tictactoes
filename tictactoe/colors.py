TESTING = False

color_pallet = {
    'Raisin black': 0x00282828,
    'Denim': 0x002c63b0,
    'Mantis': 0x006cbf57,
    'Keppel': 0x002bc0aa,
    'Auburn': 0x009b2c2a,
    'Purpureus': 0x00b041b8,
    'Old gold': 0x00b6ab44,
    'Ash gray': 0x00a7a796
}

from enum import Enum

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

class WinColors:

    #basic color flags
    FOREGROUND_BLUE = 0x0001
    FOREGROUND_GREEN = 0x0002
    FOREGROUND_RED = 0x0004
    #color intensity flags
    INTENSITY = 0x0008
    NORMAL = 0x0000

    #combined flags to make up basic 16 colors
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

    color_dict = {
        0: BLACK,
        1: BLUE,
        2: GREEN,
        3: CYAN,
        4: RED,
        5: MAGENTA,
        6: YELLOW,
        7: GREY,
        8: LIGHT_GREY,
        9: LIGHT_BLUE,
        10: LIGHT_GREEN,
        11: LIGHT_CYAN,
        12: LIGHT_RED,
        13: LIGHT_MAGENTA,
        14: LIGHT_YELLOW,
        15: LIGHT_WHITE
    }

    def __init__(self):
        self.default_fore = self.GREY
        self.default_back = self.BLACK
        self.fore = self.default_fore
        self.back = self.default_back

    def set_colors(self, fore, back):
        """
        Sets current color of :WinColor: instance, use :WinColors.flag:
        property to get color flag for screen

        utilized in follow WinScreen functions

            :fore: - Set Foreground color
            :back: - Set Background color
        """
        self.fore = back
        self.back = back

    def set_fore(self, fore=None):
        if fore:
            self.fore = fore
        else:
            self.fore = self.default_fore

    def set_back(self, back=None):
        if back:
            self.back = back
        else:
            self.back = self.default_back


    def set_color_index(self, fore=None, back=None):
        """
        Same as :WinColors.set_color: method except for the following.
        
            :fore: - Can either use 0-15 or any value from :ColorPos: class
            :back: - Can either use 0-15 or any value from :ColorPos: class
        """
        if fore or back:
            if fore:
                self.fore = self.color_dict[fore]
            if back:
                self.back = self.color_dict[back]

    @staticmethod
    def produce_flag(fore, back):
        return (WinColors.color_dict[fore] | (WinColors.color_dict[back] << 4))
    
    @property
    def flag(self):
        return (self.fore | (self.back << 4))

if TESTING:
    print("need tests first!!!")



"""
TODO
    ::expand and clean up the WinColor class, move from something crude to
    ::something pretty, make it look cleaner and more methods and handle
    ::changing the ColorTable[1-16] with it.
"""
