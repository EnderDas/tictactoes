class GameError(Exception):
    pass

class GameNotFound(Exception):
    pass

class GameValueError(Exception):
    pass

class GameConstError(Exception):
    pass

class ScreenError(Exception):
    pass

class WinScreenError(ScreenError):
    pass

class OptionError(Exception):
    pass

class OptionGroupError(OptionError):
    pass

class InputError(Exception):
    pass

class KeyError(InputError):
    pass