
from msvcrt import kbhit, getch
from errors import *
from option import *
from colors import WinColors
from win_screen import *
import math
import time

class WinScreen: #move to separate file and make a proper wrapper

    def __init__(self):
        self.handle = GetStdHandle(STDOUT)
        self.csbi = GetConsoleScreenBufferInfo(self.handle)
        self.csbiex = GetConsoleScreenBufferInfoEx(self.handle)
        self.width = self.csbi.dwSize.X
        self.height = self.csbi.dwSize.Y

    def set_title(self, name):
        SetConsoleTitle(name)

    def set_cursor(self, x, y):
        coords = COORD(x, y)
        SetConsoleCursorPosition(self.handle, coords)

    def set_cursor_vis(self, setting: bool):
        cursor = GetConsoleCursorInfo(self.handle)
        cursor.bVisible = setting
        results = SetConsoleCursorInfo(self.handle, cursor)
        if not results:
            raise WinScreenError("Could not set cursor visibility!")

    def reset_cursor(self):
        self.set_cursor(0, 0)

    def clearSec(self, start, stop):
        """
        takes two tuples of coords and clears just that section
        """
        pass

    def clear(self):
        #have to use -2 since windows is really weird
        chars = ' ' * (self.width-2) + "\n"
        chars = chars * (self.height-2)
        print(chars, end=" ", flush=False)
        self.reset_cursor()

    def fill_color(self, start, stop, color):
        num_rows = stop.Y - start.Y
        chars_per_row = stop.X - start.X
        for row in range(num_rows):
            coord = COORD(start.X, start.Y + row)
            FillConsoleOutputAttribute(self.handle, color, chars_per_row, coord)

#basic screen class
class Screen:

    def __init__(self):
        from platform import system
        self.system = system()
        if self.system != "Windows":
            raise GameError("System not supported, could not resolve system")
        else:
            self.screen = WinScreen()
        self.width = self.screen.width
        self.height = self.screen.height
        self.menu = self.basic_key_menu
        self.colors = WinColors()

    def hide_cursor(self):
        self.screen.set_cursor_vis(False)

    def show_cursor(self):
        self.screen.set_cursor_vis(True)

    def set_cursor(self, x, y):
        self.screen.set_cursor(x, y)

    def refresh(self):
        self.screen.reset_cursor()

    def clear(self):
        self.screen.clear()

    def basic_key_menu(self, options):
        #raise NotImplementedError("still working on it")
        if isinstance(options, OptionGroup):
            itemized = []
            for i in options.keys:
                item = f"[{i.upper()}] {options.get_option(key=i).name}"
                itemized.append(item)
            text = '\n'.join(itemized)
            self.print_at_center(text)
        else:
            raise ScreenError(
                f"cannot use :{options}: must use :OptionGroup:"
                )

    def print_at(self, text, coords):
        texts = text.split('\n')
        next_line = 0
        for i in texts:
            self.set_cursor(coords[0], coords[1]+next_line)
            print(i, end="", flush=False)
            next_line+=1
        self.set_cursor(0, 0)

    def print_at_center(self, text):
        text = text.split('\n')
        center = (
            (
                math.floor(self.width/2) - len(max(text,key=len))
            ),
            (
                math.floor(self.height/2) - len(text)
            )
        )
        text = '\n'.join(text)
        self.print_at(text, center)

    def color_print_at(self, text, color, coord):
        data = text.split('\n')
        start = coord
        end = (len(max(data, key=len))+start[0], len(data)+start[1])
        print("\n",start, end)
        print(data)
        print(max(data))
        print(data[0] > data[1])
        #assume color is handled
        self.print_at(text, start)
        self.screen.fill_color(COORD(*start), COORD(*end), color)
        

class Handler:

    def __init__(self, input):
        self.input = input
        self.binds = {}
        self.bind_keys = []
        
    def is_bound(self, func, key=None) -> tuple:
        for i in self.binds.keys():
            if func in self.binds[i]:
                return (True, i)
            else:
                return (False, None)
            
    def call_binding(self, key):
        if isinstance(self.binds[key], set):
            for i in self.binds[key]:
                i() #call the func
        else:
            self.binds[key]()

    def bind(self, func, key) -> None:
        if key in self.binds.keys():
            new_binds = {self.binds[key],}
            if self.binds[key] != func:
                new_binds.append(func) 
            else:
                raise InputError(
                    "Cannot bind function twice, use Handler.clear_binds first")
            self.binds[key] = new_binds
            self.bind_keys.append(key)
        else:
            self.binds[key] = func
            self.bind_keys.append(key)

    def bind_option(self, option: Option):
        self.bind(option.action, option.key)

    def bind_options(self, options: OptionGroup):
        #bind options to handler
        #handle as a list of options
        for i in options.group:
            self.bind_option(i)

    def clear_binds(self):
        self.binds = {}
        self.bind_keys = []

    def listen(self, key):
        """
        call this function in your main loop to call and check for
        key presses and call the subsequent binded func/functions to the given
        key.
        """
        if self.input.awaiting():
            k = self.input.getKey()
            if k == key:
                self.call_binding(key)

    def listener(self): #probably not a good idea to iterate through each key
        if self.input.awaiting(): #AND then start handling the keys lol
            keypress = self.input.getKey() 
            if keypress in self.bind_keys:
                self.call_binding(keypress)


class Inputs:

    #start writing all key options into this lil dict for easier handling
    #mainly use the arrow keys, no need to have predefined chars
    #most chars will just convert to char using :chr(): 
    keys = {
        '224': { #ARROW KEYS
            '75': 'LEFT_ARROW',
            '77': 'RIGHT_ARROW',
            '80': 'DOWN_ARROW',
            '72': 'UP_ARROW'
        },
        '27': 'ESC',
        '13': 'ENTER',
        '113': 'q',
        '119': 'w',
        '101': 'e',
        '114': 'r',
        '116': 't',
        '121': 'y',
        '117': 'u',
        '105': 'i',
        '111': 'o',
        '112': 'p',
        '97': 'a',
        '115': 's',
        '100': 'd',
        '102': 'f',
        '103': 'g',
        '104': 'h',
        '106': 'j',
        '107': 'k',
        '108': 'l',
        '122': 'z',
        '120': 'x',
        '99': 'c',
        '118': 'v',
        '98': 'b',
        '110': 'n',
        '109': 'm',
        '44': ',',
        '46': '.',
        '47': '/',
        '59': ';',
        '91': '[',
        '93': ']',
        '43': '+',
        '45': '-', #alias of _ at least on my computer
        '61': '=' #alias of + at least on my computer
        }
    
    def __init__(self):
        self.bindings = []
        self.handler = Handler(self)
    
    def awaiting(self) -> bool:
        return False if kbhit() == 0 else True
    
    def getKey(self) -> str:
        return self.keys[str(ord(getch()))]
    
    def getAwaitedKey(self) -> str:
        """
        should only be used if we are assuming we are waiting for the system
        to handle a keypress, ie. during handling of arrow keys were two key
        presses are pulled from :getch():
        """
        if self.awaiting:
            return self.getKey()
        else: 
            raise KeyboardError("No keypress awaited")
    
    @property
    def handle(self):
        """
        returns a handler that handles and binds input to functions
        """
        return self.handler
    

TESTING_INPUT = False
TESTING_SCREEN = True
if TESTING_INPUT:
    def function():
        print("a key pressed!")

    inp = Inputs()
    handler = inp.handle
    handler.bind(function, 'a')
    
    while True:
        #handler.listen('a') you can use this or
        handler.listener()
        #wow this works better than i thought it would.. lol

if TESTING_SCREEN:
    screen = Screen()
    start = COORD(20,20)
    stop = COORD(40,40)
    color = screen.colors.produce_flag(
        screen.colors.LIGHT_MAGENTA,
        screen.colors.BLUE
    )
    #screen.screen.fill_color(start, stop, color)
    screen.color_print_at(
        "ayy lmao whats up dog\neat my butt lol",
        color,
        (15,20)
        )