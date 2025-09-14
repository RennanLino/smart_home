from enum import Enum, auto
from typing import List


from smart_home.core.base import Subject, Singleton, Observer
from smart_home.devices import BaseDevice
from smart_home.core import Persistence, ConsoleObserver, Routine, Command, ConfigBadFormat, EventResult


class HouseNotificationType(Enum):
    EVENT = auto()
    INVALID_EVENT = auto()
    ERROR = auto()

class House(Subject, metaclass=Singleton):
    _instance = None
    __config_path = "data/config.json"

    def __init__(self):
        super().__init__()
        self.name = "House"
        self.version = "1.0"
        self.__devices: List[BaseDevice] = []
        self.__routines: List[Routine] = []
        self.__observers: List[Observer] = [ConsoleObserver()]


    @property
    def devices(self):
        return self.__devices

    @property
    def routines(self):
        return self.__routines

    def add_device(self, device: "BaseDevice"):
        if device.name in [device.name for device in self.devices]:
            raise ValueError(f"Ja existe um dispositivo com nome '{device_name}'. O nome deve ser unico.")

        self.__devices.append(device)
        message = f"[EVENT] Device Added: {type(device).__name__} - {device.name}"
        self.notify(message)

    def remove_device(self, device: "BaseDevice"):
        self.__devices.remove(device)
        message = f"[EVENT] Device Removed: {type(device).__name__} - {device.name}"
        self.notify(message)

    def set_device_attr(self, device, attr_name, attr_value):
        setattr(device, attr_name, attr_value)
        message = f"[EVENT] ({type(device).__name__}) {device.name} - {attr_name} = {attr_value}"

    def run_routine(self, routine: Routine):
        # if getattr(self.__routines, routine_name) is None:
        #     raise Exception(f"Routine {routine_name} not found")
        routine.run()
        message = f"[EVENT] Routine Executed: {routine.name}"
        self.notify(message)

    def run_command(self, device, command_name, kwargs):
        command = Command(device, command_name, **kwargs)
        event_result = command.run()
        self.notify_transition_event(event_result)
        return event_result

    def notify_transition_event(self, event_result: EventResult):
        message = f"[EVENT] Executed Command: {vars(event_result)}"
        self.notify(message)

    def save_config(self):
        Persistence.write_to_json(self.__config_path, self.to_dict())

    def load_config(self):
        house_dict = Persistence.load_from_json(self.__config_path)
        self.from_dict(house_dict)

    def to_dict(self):
        result = {
            "hub": {
                "name": self.name,
                "version": self.version,
            },
            "devices": [device.to_dict() for device in self.devices],
            "routines": {name: commands for routine in self.__routines for name, commands in routine.to_dict().items()},
        }
        return result

    def from_dict(self, house_dict):
        from smart_home.devices import BaseDevice

        try:
            hub = house_dict["hub"]
            self.name = hub["name"]
            self.version = hub["version"]
            for device_dict in house_dict["devices"]:
                BaseDevice.from_dict(device_dict)
            self.__routines = [
                Routine.from_dict(routine_name, command_dicts, self.__devices)
                for routine_name, command_dicts in house_dict["routines"].items()
            ]
        except KeyError as e:
            raise ConfigBadFormat(self.__config_path)
