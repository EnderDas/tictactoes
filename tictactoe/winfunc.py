from functools import wraps
from inspect import getmembers, isclass
from types import ModuleType
from typing import Any

class FuncHandlerError(Exception):
    pass

class FuncHandlerArgError(Exception):
    pass

class FuncHandlerResError(Exception):
    pass

class FuncHandlerTypeError(Exception):
    pass

type WinMethod = Any
type ArgTypes = list[Any]
type ResType = Any

def _get_lib_types(lib: ModuleType) -> list:
    return dict(getmembers(lib, isclass))

class WindowsCtypesHandler:
    """
    A more intuitive class version of the WinFunc decorator

        ::To use this class you must first 
        ::initialize the base class with 
        ::two arguments.

            :lib: -> The library used to access the windows functions.
            :types: -> A module type object that has predefined windows types.

        ::Once initialized you can use
        ::the :func_attr: method to 
        ::decorate your Windows C function,
        ::creating a syntactically 
        ::appealing wrapper around it.

        ie.

            from ctypes import wintypes
            import ctypes

            kernel32 = ctypes.windll.kernel32 #renamed library access

            #initialize the function handler
            handler = WindowsCtypesHandler(kernel32, wintypes)

            #decorate at will!
            @handler.func_attr(
                kernel32.GetStdHandle,
                [wintypes.DWORD,...],
                wintypes.BOOL
            )
            def GetStdHandle(self, handle):
                #returns a std_handle with given handle
                return self(handle)

        ::The function being decorated must have at least one positional
        ::argument (preferably the first pos) to receive a copy of the 
        ::function being called from the loaded library, for semantics
        ::I only use the argument name :self:, this makes the function more
        ::readable and goes inline with how classes work. (might change later)

            STDOUT = -11
            handle = GetStdHandle(STDOUT)
            print(handle)
            #then just use the function as normal!
        
        ::My reasoning behind creating this is to make the arguments required
        ::for the functions to run easier to read and to find.
        ::does it require more boilerplate? possibly, but it creates
        ::something thats way easier to read, at least for my eyes.

        ::The :stuct: decorator is to facilitate adding more or even
        ::custom Structures to the classes type checking system. can either
        ::be used as a decorator or just used as a straight method to insert
        ::either structures or pointers to structures
    """

    def __init__(self, lib: ModuleType, types: ModuleType):
        self.library = lib
        self.lib_types = _get_lib_types(types) #dict of module class types
        self.function_names = {}

    def _get_false(self, listing: dict) -> list[bool]:
        return [a for a in listing if not listing[a]]

    def _check_type(self, obj: Any) -> bool:
        return obj in self.lib_types.values()
    
    def _check_restype(self, res: Any) -> bool:
        if not self._check_type(res):
            raise FuncHandlerResError(FuncHandlerTypeError(), res)
        else:
            return True
    
    def _check_argtypes(self, args: list[Any]) -> bool:
        arg_results = {a: self._check_type(a) for a in args}
        if not all(arg_results.values()):
            raise FuncHandlerArgError(
                FuncHandlerTypeError(),
                self._get_false(arg_results)
                )
        else:
            return True
        
    def func_attr(
            self, method: WinMethod, argtypes: ArgTypes, restype: ResType):
        """
        Decorator function for creating :ctypes: functions.
        """
        if self._check_argtypes(argtypes) & self._check_restype(restype):
            def decorator(func):
                self.function_names[func.__name__] = {
                    'function': func,
                    'method': method,
                    'argtypes': argtypes,
                    'restype': restype
                }
                @wraps(func)
                def wrapper(*args, **kwargs):
                    method.argtypes = argtypes
                    method.restype = restype
                    return func(method, *args, **kwargs)
                return wrapper
            return decorator
        
    def struct(self, cls):
        """
        Decorator function for adding :ctype.Structure:'s to the system for
        use in making functions.
        """
        struct = {cls.__name__: cls}
        self.lib_types.update(struct)
        return cls
    
    @property
    def functions(self) -> dict[Any]:
        """
        Property for accessing functions created using :func_attr: method.
        """
        return self.function_names
    
    def function(self, name) -> tuple[Any]:
        """
        Wrapper function for getting original method and wrapper function
        created from using :func_attr:
        """
        if name in self.functions:
            func = self.functions[name]
            return (func['method'], func['function'])
        

if __name__ == "__main__":
    from ctypes import wintypes
    import ctypes
    kernel32 = ctypes.windll.kernel32

    handler = WindowsCtypesHandler(kernel32, wintypes)

    @handler.func_attr(
        kernel32.GetStdHandle,
        [wintypes.DWORD,],
        wintypes.BOOL
    )
    def GetStdHandle(self, handle):
        """
        returns std_handle from given handle
        """
        return self(handle)

    STDOUT = -11

    handle = GetStdHandle(STDOUT)
    print(handle)

    @handler.struct
    class COORD(ctypes.Structure):
        _fields_ = [('X', wintypes.SHORT),
                    ('Y', wintypes.SHORT)]
    
    @handler.func_attr(kernel32.SetConsoleCursorPosition,
                       [wintypes.HANDLE, COORD],
                       wintypes.BOOL)
    def SetConsoleCursorPosition(self, std_handle, coords):
        return bool(self(std_handle, coords))
    
    coord = COORD(20, 20)
    results = SetConsoleCursorPosition(handle, coord)
    print(results)
        
        
