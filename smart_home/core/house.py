from typing import List

from smart_home.devices.base_device import BaseDevice


class House:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.name = "House"
        self.version = "1.0"
        self.__devices = []
        self.__routines = []
        self.__observers = []

    def register_observer(self, observer):
        self.__observers.append(observer)

    def unregister_observer(self, observer):
        self.__observers.remove(observer)

    def notify_observers(self, data):
        for observer in self.__observers:
            observer.update(data)

    @property
    def devices(self):
        return self.__devices

    def add_device(self, device: BaseDevice):
        self.__devices.append(device)
        message = f"[EVENT] Device Added: {device}"
        self.notify_observers(message)

    def remove_device(self, device: BaseDevice):
        self.__devices.remove(device)
        message = f"[EVENT] Device Removed: {device}"
        self.notify_observers(message)

    def run_routine(self, routine_name):
        if getattr(self.routines, routine_name) is None:
            raise Exception(f"Routine {routine_name} not found")
        self.routines[routine_name].run_routine()
        message = f"[EVENT] Routine Executed: {routine_name}"
        self.notify_observers(message)

    def to_dict(self):
        return {
            "name": self.name,
            "version": self.version,
            "devices": [device.to_dict() for device in self.devices],
            "routines": [routine.to_dict() for routine in self.routines],
        }


class Routine:
    def __init__(self, name: str, commands: List["Command"]):
        self.name = name
        self.commands = commands

    def run(self):
        for command in self.commands:
            command.run()

    def to_dict(self):
        return {
            self.name: [command.to_dict() for command in self.commands],
        }


class Command:
    def __init__(self, name: str, device: BaseDevice, *args):
        self.name = name
        self.device = device
        self.args = list(*args)

    def run(self):
        return getattr(self.device, self.name)(*self.args)

    def to_dict(self):
        return {
            "device_name": self.device.to_dict(),
            "command": self.name,
        }
