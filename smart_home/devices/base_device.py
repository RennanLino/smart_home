import sys
from abc import ABC

from smart_home.core import House, LoggingMachine


class BaseDevice(ABC):
    house = House()

    def __init__(self, name: str, states, initial_state, transitions):
        self.name = name
        self.machine = LoggingMachine(
            model=self,
            states=states,
            initial=initial_state,
            transitions=transitions,
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
            initial_state=device_dict["state"],
        )
        return device_obj
