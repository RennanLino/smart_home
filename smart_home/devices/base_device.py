import sys
from abc import ABC

from smart_home.core import CustomMachine
from smart_home.states import BaseEnum


class BaseDevice(ABC):
    name_pt: str
    states: BaseEnum
    transitions: dict

    def __init__(self, name: str, initial_state):
        self.name = name
        self.__machine = CustomMachine(
            model=self,
            states=self.states,
            initial=initial_state,
            transitions=self.transitions,
        )

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
                               self.__machine.events.items()))
        return commands

    @classmethod
    def get_available_attr(cls):
        return [name for name, attr in vars(cls).items()
                if not callable(attr)
                and not name.startswith("__")
                and not name == "name_pt"]

    def get_available_attr_values(self, attr_name):
        pass

    @classmethod
    def get_command_kwargs(cls, command_name):
        return {}