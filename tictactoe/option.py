from errors import *

class Option:
    """
                options = Option([{
                    "key": 'p',
                    "name": "Play",
                    "action": self.Play
                }])
    """

    def __init__(self, data=None):
        #using only lists to keep order and make mutable
        if data:
            if isinstance(data, list):
                raise OptionError("please use :OptionGroup:")
            self.key = data['key']
            self.action = data['action']
            self.name = data['name']
        else:
            raise OptionError("must give option data to create")

    def __cmp__(self, object) -> bool:
        return (
            (self.key == object.key) & 
            (self.action == object.action) & 
            (self.name == object.name)
        )
    
    def __dict__(self) -> dict:
        return {
            "key": self.key,
            "action": self.action,
            "name": self.name
        }

class OptionGroup:

    def __init__(self, options=None):
        self.group = []
        if options:
            for i in options:
                if isinstance(i, Option):
                    self.append_group(i)
                else:
                    try:
                        opt = Option(i)
                        self.append_group(opt)
                    except:
                        raise OptionGroupError(
                "Please use only a list of option objects or a list of dicts"
                            )
    
    def append_group(self, option: Option):
        if option in self.group:
            raise OptionError("cannot add two of the same options")
        else:
            self.group.append(option)

    @property
    def keys(self):
        return [i.key for i in self.group]
    
    @property
    def names(self):
        return [i.name for i in self.group]
    
    @property
    def actions(self):
        return [i.action for i in self.group]

    def get_option(self, key = None, action = None, name = None) -> Option:
        if not key and not action and not name:
            raise OptionError("must specify option data to retrieve")
        else:
            if not key:
                if not action:
                    for i in self.group:
                        if i.name == name:
                            return i
                else:
                    for i in self.group:
                        if isinstance(i.action, action):
                            return i
            else:
                for i in self.group:
                    if i.key == key:
                        return i
