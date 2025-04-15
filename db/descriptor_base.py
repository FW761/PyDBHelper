class DescriptorBase:
    def __init__(self, expected_type=str, allow_none=False):
        self.allow_none = allow_none
        self.expected_type = expected_type

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, owner):
        return obj.__dict__[self.name]

    def __set__(self, obj, value):
        if value is None and self.allow_none:
            obj.__dict__[self.name] = None
        elif not isinstance(value, self.expected_type) and self.allow_none == False:
            raise TypeError(f"Значение {self.name} должно быть типа {self.expected_type.__name__}")
        else:
            obj.__dict__[self.name] = value