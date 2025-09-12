from smart_home.core import Persistence, ConsoleObserver, Routine
from smart_home.core.base import Subject
from smart_home.core.base.singleton import Singleton
from smart_home.core.logging_machine import EventResult


class House(metaclass=Singleton, Subject):
    _instance = None
    __config_path = "data/config.json"

    def __init__(self):
        super().__init__()
        self.name = "House"
        self.version = "1.0"
        self.__devices = []
        self.__routines = {}
        self.__observers = [ConsoleObserver()]


    @property
    def devices(self):
        return self.__devices

    def add_device(self, device: "BaseDevice"):
        self.__devices.append(device)
        message = f"[EVENT] Device Added: {type(device).__name__} - {device.name}"
        self.notify(message)

    def remove_device(self, device: "BaseDevice"):
        self.__devices.remove(device)
        message = f"[EVENT] Device Removed: {type(device).__name__} - {device.name}"
        self.notify(message)

    def run_routine(self, routine_name: str):
        if getattr(self.__routines, routine_name) is None:
            raise Exception(f"Routine {routine_name} not found")
        self.__routines[routine_name].run_routine()
        message = f"[EVENT] Routine Executed: {routine_name}"
        self.notify(message)

    def notify_transition_event(self, event_result: EventResult):
        message = f"[EVENT] Executed Command: {vars(event_result)}"
        self.notify(message)

    def save_config(self):
        Persistence.write_to_json(self.__config_path, self.to_dict())

    def load_config(self):
        house_dict = Persistence.load_from_json(self.__config_path)
        self.from_dict(house_dict)

    def to_dict(self):
        return {
            "hub": {
                "name": self.name,
                "version": self.version,
            },
            "devices": [device.to_dict() for device in self.devices],
            "routines": {routine.to_dict() for routine in self.__routines},
        }

    def from_dict(self, house_dict):
        from smart_home.devices import BaseDevice

        hub = house_dict["hub"]
        self.name = hub["name"]
        self.version = hub["version"]
        for device_dict in house_dict["devices"]:
            BaseDevice.from_dict(device_dict)
        self.__routines = [
            Routine.from_dict(routine_name, command_dicts, self.__devices)
            for routine_name, command_dicts in house_dict["routines"].items()
        ]
