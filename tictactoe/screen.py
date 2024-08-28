#errors

#color pallet for colorful to use
color_pallet = { #generated using coolors.co
    "dark": "#3F3F37", #Black Olive
    "light": "#D3BDB0", #Pale Dogwood
    "blue": "#3F88C5", #Steel Blue
    "green": "#49BEAA", #Keppel
    "red": "#FF495C", #Folly
    "yellow": "#EEB868", #Earth Yellow
    "purple": "#593C8F", #Rebecca Purple
    "pink": "#E0479E", #Hollywood Cerise
}

from msvcrt import kbhit, getch
from errors import *
from option import *
import time

#colors.replace_pallet(color_pallet)
#this throws an error, figure it out bubba

#basic screen class
class Screen:

    class WinScreen:

        import ctypes
        STD_OUTPUT_HANDLE = -11

        class POINT(ctypes.Structure):
            pass
        POINT._fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

        def __init__(self):
            from os import get_terminal_size
            self.width, self.height = get_terminal_size()

        def setCursor(self, x, y):
            h = self.ctypes.windll.kernel32.GetStdHandle(
                self.STD_OUTPUT_HANDLE
                )
            self.ctypes.windll.kernel32.SetConsoleCursorPosition(
                h, self.POINT(int(x), int(y))
            )

        def refresh(self):
            self.setCursor(0, 0)

        def clear(self):
            chars = ' ' * (self.width-2) + "\n"
            chars = chars * (self.height-2)
            print(chars, end=" ", flush=False)
            self.refresh()

    def __init__(self):
        from platform import system
        self.system = system()
        if self.system != "Windows":
            raise GameError("System not supported, could not resolve system")
        else:
            #no curses... womp womp
            #curses seems to be broken with everything ive looked into
            #at least PDcurses is broken for windows thats for sure
            self.screen = self.WinScreen()
        self.width = self.screen.width
        self.height = self.screen.height

    def setCursor(self, x, y):
        self.screen.setCursor(x, y)

    def refresh(self):
        self.screen.refresh()

    def clear(self):
        self.screen.clear()

    def menu(self, options):
        #raise NotImplementedError("still working on it")
        if isinstance(options, OptionGroup):
            itemized = []
            for i in options.keys:
                item = f"[{i.upper()}] {options.get_option(key=i).name}"
                itemized.append(item)
            text = '\n'.join(itemized)
            self.printAtCenter(text)
        else:
            raise ScreenError(
                f"cannot use :{options}: must use :OptionGroup:"
                )

    def printAt(self, text, coords):
        texts = text.split('\n')
        next_line = 0
        for i in texts:
            self.setCursor(coords[0], coords[1]+next_line)
            print(i, end="", flush=False)
            next_line+=1
        self.setCursor(0, 0)

    def printAtCenter(self, text):
        text = text.split('\n')
        center = (
            (
                abs(self.width/2) - len(max(text))
            ),
            (
                abs(self.height/2) - len(text)
            )
        )
        text = '\n'.join(text)
        self.printAt(text, center)

class Handler:

    def __init__(self, input):
        self.input = input
        self.binds = {}
        self.bind_keys = []
        
    def is_binded(self, func, key=None) -> tuple:
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
                raise Exception("Cannot bind function twice to same key")
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

    def clear_bindings(self):
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
            raise KeyError("No keypress awaited")
    
    @property
    def handle(self):
        """
        returns a handler that handles and binds input to functions
        """
        return self.handler
    


if __name__ == "__main__":

    def function():
        print("a key pressed!")

    inp = Inputs()
    handler = inp.handle
    handler.bind(function, 'a')
    
    while True:
        #handler.listen('a') you can use this or
        handler.listener()
        #wow this works better than i thought it would.. lol