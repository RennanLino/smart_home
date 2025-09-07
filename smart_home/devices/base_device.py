from smart_home.core.house import House
from smart_home.core.logger import Logger
from smart_home.core.logging_machine import LoggingMachine


class BaseDevice:
    house = House()

    def __init__(self, name: str, states, initial_state, transitions):
        self._name = name
        self.logger = Logger()
        self.machine = LoggingMachine(
            model=self,
            states=states,
            initial=initial_state,
            transitions=transitions,
        )
        self.house.devices.append(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if value != self._name:
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
            "state": self.state,
            "atibutes": {},
        }
