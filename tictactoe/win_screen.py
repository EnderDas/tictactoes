import ctypes
from ctypes import Structure, byref, wintypes ,sizeof
from winfunc import WindowsCtypesHandler as WinTools
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

8/31/24
    boy the difference that decorator class makes is immeasurable, quite
    happy with how well that turned out, i added a bunch more stuff and it looks
    way cleaner than it did before, found some stuff on the cbsiEx so it doesn't
    look so sketchy now, thank god i put in a little time to clean this up.

    I dont think im gonna touch this for awhile or at least until i need to add 
    more stuff to it, until them. c'est la vie to this shit
"""

STDOUT = -11
FILE_SHARE_READ = 0x00000001
FILE_SHARE_WRITE = 0x00000002
GENERIC_READ = 0x80000000
GENERIC_WRITE = 0x40000000

kernel32 = ctypes.windll.kernel32 #simplifying kernel32

WinTool = WinTools(kernel32, wintypes)

@WinTool.struct
class COORD(Structure):
    _fields_ = [('X', wintypes.SHORT),
                ('Y', wintypes.SHORT)]

LPCSTR = wintypes.LPVOID

@WinTool.struct
class SECURITY_ATTRIBUTES(Structure):
    _fields_ = [('nLength', wintypes.DWORD),
                ('lpSecurityDescriptor', LPCSTR),
                ('bInheritHandle', wintypes.DWORD)]

@WinTool.struct
class CONSOLE_SCREEN_BUFFER_INFO(Structure):
    _fields_ = [
        ("dwSize", COORD),
        ("dwCursorPosition", COORD),
        ("wAttributes", wintypes.WORD),
        ("srWindow", wintypes.SMALL_RECT),
        ("dwMaximumWindowSize", COORD),
    ]

@WinTool.struct
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

LPBUEX = ctypes.POINTER(CONSOLE_SCREEN_BUFFER_INFOEX)
WinTool.struct(LPBUEX)

LPBUFF = ctypes.POINTER(CONSOLE_SCREEN_BUFFER_INFO)
WinTool.struct(LPBUFF)

LPSCAT = ctypes.POINTER(SECURITY_ATTRIBUTES) #haha lp-scat lol
WinTool.struct(LPSCAT)

#Windows Wrapped Functions using WinTool (WindowsCtypesHandler)

kernel32 = ctypes.windll.kernel32 #simplifying kernel32


@WinTool.func_attr(kernel32.GetStdHandle,
                   [wintypes.DWORD],
                   wintypes.HANDLE)
def GetStdHandle(self, handle: int):
    """
    returns handle using given handle ID
    """
    return self(handle)


@WinTool.func_attr(kernel32.GetConsoleMode,
                   [wintypes.HANDLE, wintypes.LPDWORD],
                   wintypes.BOOL)
def GetConsoleMode(self, std_handle):
    """
    returns handle mode with given handle ID
    """
    con_mode = wintypes.DWORD()
    result = bool(self(std_handle, con_mode))
    if result:
        return con_mode.value

@WinTool.func_attr(kernel32.FillConsoleOutputAttribute,
                   [
                       wintypes.HANDLE, wintypes.WORD, wintypes.DWORD,
                       COORD, wintypes.LPDWORD],
                       wintypes.BOOL)
def FillConsoleOutputAttribute(
        self,
        std_handle,
        attributes,
        length,
        start
    ):

    """
    Fills given attributes for a given length of characters 
    from the given starting point
    """

    cells = wintypes.DWORD(length)
    style = wintypes.WORD(attributes)
    num_written = wintypes.DWORD(0)
    self(
        std_handle, style, cells, start, byref(num_written)
    )
    return num_written.value


@WinTool.func_attr(kernel32.CreateConsoleScreenBuffer,
                  [
                    wintypes.DWORD, wintypes.DWORD, LPSCAT, 
                    wintypes.DWORD, wintypes.LPVOID],
                 wintypes.HANDLE)
def CreateConsoleScreenBuffer(self, access = GENERIC_READ | GENERIC_WRITE,
                                    shared = FILE_SHARE_READ | FILE_SHARE_WRITE):
    """
    Creates and returns a windows console screen buffer handle
    """ #defaults
    flags = wintypes.DWORD(1) #defaults
    security = SECURITY_ATTRIBUTES(sizeof(SECURITY_ATTRIBUTES), None, True)
    buffer = self(access, shared, None, flags, None)
    if buffer == wintypes.HANDLE(-1):
        raise Exception("could not create buffer") #this should never be the case
    else:
        return buffer 


@WinTool.func_attr(kernel32.GetConsoleScreenBufferInfo,
                   [wintypes.HANDLE, LPBUFF],
                   wintypes.BOOL)
def GetConsoleScreenBufferInfo(self, std_handle):
    """
    Returns ConsoleScreenBuffer info using given handle
    """
    buffer_info = CONSOLE_SCREEN_BUFFER_INFO()
    self(std_handle, byref(buffer_info))
    return buffer_info


@WinTool.func_attr(kernel32.GetConsoleScreenBufferInfoEx,
                   [wintypes.HANDLE, LPBUEX],
                   wintypes.BOOL)
def GetConsoleScreenBufferInfoEx(self, std_handle):
    """
    Returns ConsoleScreenBuffer extended info using given handle
    """
    extended_buffer_info = CONSOLE_SCREEN_BUFFER_INFOEX()
    self(int(std_handle), byref(extended_buffer_info))
    return extended_buffer_info


@WinTool.func_attr(kernel32.SetConsoleCursorPosition,
                   [wintypes.HANDLE, COORD],
                   wintypes.BOOL)
def SetConsoleCursorPosition(self, std_handle, coords):
    """
    Sets console cursor position using given HANDLE and COORD
    """
    return bool(self(std_handle, coords))


@WinTool.func_attr(kernel32.SetConsoleTextAttribute,
                   [wintypes.HANDLE, wintypes.WORD],
                   wintypes.BOOL)
def SetConsoleTextAttribute(self, handle, attributes):
    """
    Sets text attribute for text rendered to console, clips
    """
    return bool(self(handle, attributes))


#testing ScreenBuffer functions
if __name__ == "__main__":
    handle = GetStdHandle(STDOUT)
    buffer_info = GetConsoleScreenBufferInfo(handle)
    print(buffer_info)
    extended_info = GetConsoleScreenBufferInfoEx(handle)
    print(extended_info)