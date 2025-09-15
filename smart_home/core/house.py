from collections import defaultdict
from datetime import datetime
from enum import auto, Enum
from typing import List
from unittest import case

from smart_home.core.base import Subject, Singleton, Observer
from smart_home.devices import BaseDevice, Outlet, Light
from smart_home.core import Persistence, ConsoleObserver, Routine, Command, ConfigBadFormat, EventResult


class ReportType(Enum):
    OUTLET_CONSUMPTION = "Consumo por tomada inteligente"
    LIGHT_TOTAL_TIME = "Tempo total em que cada luz permaneceu ligada"
    MOST_USED_DEVICES = "Dispositivos mais usados"
    MOST_USED_COMMANDS = "Comandos mais usados por dispositivo"
    FAILURE_PERCENTAGE = "Percentual de falhas de transição"

class House(Subject, metaclass=Singleton):
    event_file_path = "data/events.csv"
    _instance = None
    __config_path = "data/config.json"

    def __init__(self):
        super().__init__()
        self.name = "House"
        self.version = "1.0"
        self.__devices: List[BaseDevice] = []
        self.__routines: List[Routine] = []
        self.subscribe(ConsoleObserver())


    @property
    def devices(self):
        return self.__devices

    @property
    def routines(self):
        return self.__routines


    def add_device(self, device: "BaseDevice"):
        if device.name in [device.name for device in self.devices]:
            raise ValueError(f"Ja existe um dispositivo com nome '{device.name}'. O nome deve ser unico.")

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
        self.notify(message)

    def run_routine(self, routine: Routine):
        routine.run()
        message = f"[EVENT] Routine Executed: {routine.name}"
        self.notify(message)

    def run_command(self, device, command_name, kwargs):
        command = Command(device, command_name, **kwargs)
        event_result = command.run()
        self.notify_transition_event(event_result)
        return event_result

    def generate_report(self, report_type: ReportType, *args, **kwargs):
        reports = []
        match report_type:
            case ReportType.OUTLET_CONSUMPTION:
                reports = self.report_outlet_consumption(*args, **kwargs)
            case ReportType.LIGHT_TOTAL_TIME:
                reports = self.report_light_total_time()
            case ReportType.MOST_USED_DEVICES:
                reports = self.report_most_used_devices()
            case ReportType.MOST_USED_COMMANDS:
                reports = self.report_most_used_commands()
            case ReportType.FAILURE_PERCENTAGE:
                reports = self.report_failure_percentage()

        return reports

    def report_outlet_consumption(self, start:datetime, end:datetime):
        events = Persistence.load_from_csv(self.event_file_path)
        outlet_events = list(filter(lambda e: e['device_type'] == Outlet.__name__, events))

        pass

    def repot_light_total_time(self):
        pass

    def report_most_used_devices(self):
        events = Persistence.load_from_csv(self.event_file_path)
        result = []
        for event in events:
            device_name = event.get('device_name')
            device_dict = next((device_dict for device_dict in result if device_dict['device_name'] == device_name), None)
            if device_dict:
                device_dict['times_used'] = device_dict['times_used'] + 1
            else:
                device_dict = {"device_name": device_name, "times_used": 1}
                result.append(device_dict)
        return sorted(result, key=lambda device_dict: -device_dict['times_used'])

    def report_most_used_commands(self):
        events = Persistence.load_from_csv(self.event_file_path)
        result = []
        for event in events:
            device_name = event.get('device_name')
            event_name = event.get('event')
            device_dict = next((device_dict for device_dict in result
                                if device_dict['device_name'] == device_name
                                and device_dict['event'] == event_name), None)
            if device_dict:
                device_dict['times_used'] = device_dict['times_used'] + 1
            else:
                device_dict = {"device_name": device_name, "event": event_name, "times_used": 1}
                result.append(device_dict)
        return sorted(result, key=lambda device_dict: (-device_dict['times_used'], device_dict['device_name'] ))

    def report_failure_percentage(self):
        events = Persistence.load_from_csv(self.event_file_path)
        result = []
        for event in events:
            device_name = event.get('device_name')
            event_name = event.get('event')
            success = True if event.get('success') == "True" else False
            device_dict = next((device_dict for device_dict in result
                                if device_dict['device_name'] == device_name
                                and device_dict['event'] == event_name), None)
            if device_dict:
                device_dict['times_used'] = device_dict['times_used'] + 1

                if not success:
                    device_dict['times_failed'] = device_dict['times_failed'] +1

                if device_dict['times_failed'] != 0:
                    device_dict['failure_percentage'] = round((device_dict['times_failed'] / device_dict['times_used'] * 100), 2)
                else:
                    device_dict['failure_percentage'] = 0
            else:
                times_failed = 0 if success else 1
                failure_percentage = 0 if success else 100
                device_dict = {"device_name": device_name, "event": event_name, "times_used": 1,
                               "times_failed": times_failed, "failure_percentage": failure_percentage}
                result.append(device_dict)
        return sorted(result, key=lambda device_dict: (-device_dict['failure_percentage'], device_dict['device_name'] ))


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
                device = BaseDevice.from_dict(device_dict)
                self.devices.append(device)
            self.__routines = [
                Routine.from_dict(routine_name, command_dicts, self.__devices)
                for routine_name, command_dicts in house_dict["routines"].items()
            ]
        except KeyError as e:
            raise ConfigBadFormat(self.__config_path)
