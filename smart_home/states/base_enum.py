from enum import Enum


class BaseEnum(Enum):

    @classmethod
    def __set__(cls, value):
        if isinstance(value, str):
            value = value.upper()
            for e in cls:
                if e.name == value:
                    return e
            raise ValueError(f"{value} não possui Prioridade correspondente.")
        return value
