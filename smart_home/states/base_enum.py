from enum import Enum


class BaseEnum(Enum):

    @classmethod
    def from_str(cls, value):
        if isinstance(value, str):
            value = value.upper()
            for e in cls:
                if e.name == value:
                    return e
            raise ValueError(f"{value} não possui Prioridade correspondente.")
        return value

    @classmethod
    def from_int(cls, value):
        if isinstance(value, int):
            for e in cls:
                if e.value == value:
                    return e
            raise ValueError(f"'{value}' has no corresponding member in {cls.__name__}.")
        return value

    def __str__(self):
        return self.name.lower()


class EnumDescriptor:

    def __init__(self, enum_class):
        self._enum_class = enum_class
        self._attr_name = None

    def __set_name__(self, owner, name):
        self._attr_name = '_' + name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self._attr_name)

    def __set__(self, instance, value):
        converted_value = None

        if isinstance(value, int):
            converted_value = self._enum_class.from_int(value)
        elif isinstance(value, str):
            converted_value = self._enum_class.from_str(value)
        elif isinstance(value, self._enum_class):
            converted_value = value
        else:
            raise TypeError(
                f"Cannot convert type '{type(value).__name__}' to {self._enum_class.__name__}."
            )

        instance.__dict__[self._attr_name] = converted_value