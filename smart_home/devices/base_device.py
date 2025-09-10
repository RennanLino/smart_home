import sys
from abc import ABC

from smart_home.core import House, LoggingMachine
from smart_home.states import BaseEnum, EnumDescriptor


class BaseDevice(ABC):
    states: BaseEnum
    transitions: dict
    house = House()

    def __init__(self, name: str, initial_state):
        self.name = name
        self.machine = LoggingMachine(
            model=self,
            states=self.states,
            initial=initial_state,
            transitions=self.transitions,
        )
        self.house.add_device(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if value in [
            device.name
            for device in self.house.devices
            if isinstance(self, type(device))
        ]:
            raise ValueError(f"Name '{value}' already exists. Must be unique.")
        self._name = value

    def to_dict(self):
        return {
            "name": self.name,
            "type": self.__class__.__name__,
            "state": str(self.state),
            "atributes": {},
        }

    @staticmethod
    def from_dict(device_dict):
        device_class = getattr(sys.modules["smart_home.devices"], device_dict["type"])
        device_obj = device_class(
            device_dict["name"],
            **device_dict["atributes"],
            initial_state=device_dict["state"]
            #initial_state=device_class.states.from_str(device_dict["state"])
        )
        return device_obj

    def get_available_commands(self):
        commands = dict(filter(lambda kv: not kv[0].startswith("to_")
                                          and str(self.state).upper() in kv[1].transitions,
                               self.machine.events.items()))
        return commands

    @classmethod
    def get_command_kwargs(cls, command_name):
        return {}