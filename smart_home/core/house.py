from collections import defaultdict
from datetime import datetime, timedelta
from enum import Enum
from typing import List

from smart_home.core import (
    Persistence,
    ConsoleObserver,
    Routine,
    Command,
    ConfigBadFormat,
    EventResult,
)
from smart_home.core.base import Subject, Singleton
from smart_home.devices import BaseDevice, Outlet, Light


class ReportType(Enum):
    OUTLET_CONSUMPTION = "Consumo por tomada inteligente"
    LIGHT_USAGE = "Tempo total em que cada luz permaneceu ligada"
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
        if device.name.lower() in [device.name.lower() for device in self.devices]:
            raise ValueError(
                f"Ja existe um dispositivo com nome '{device.name}'. O nome deve ser unico."
            )

        self.__devices.append(device)
        message = f"[EVENT] Device Added: {type(device).__name__} - {device.name}"
        self.notify(message)

    def remove_device(self, device: "BaseDevice"):
        self.__devices.remove(device)
        message = f"[EVENT] Device Removed: {type(device).__name__} - {device.name}"
        self.notify(message)

    def set_device_attr(self, device, attr_name, attr_value):
        setattr(device, attr_name, attr_value)
        message = f"[EVENT] ({type(device).__name__}) {device.name}: {attr_name} alterado para {attr_value}"
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
            case ReportType.LIGHT_USAGE:
                reports = self.report_light_usage()
            case ReportType.MOST_USED_DEVICES:
                reports = self.report_most_used_devices()
            case ReportType.MOST_USED_COMMANDS:
                reports = self.report_most_used_commands()
            case ReportType.FAILURE_PERCENTAGE:
                reports = self.report_failure_percentage()

        return reports

    def report_outlet_consumption(self, start: datetime, end: datetime):
        end = end + timedelta(hours=23, minutes=59, seconds=59)
        events = Persistence.load_from_csv(self.event_file_path)
        outlet_events = [
            event
            for event in events
            if event["device_type"] == Outlet.__name__
            and start <= datetime.fromisoformat(event["timestamp"]) <= end
        ]

        grouped_events = defaultdict(list)
        for event in outlet_events:
            event_time = datetime.fromisoformat(event["timestamp"])
            if start <= event_time <= end:
                grouped_events[event["device_name"]].append(event)

        report_list = []

        for device_name, event_list in grouped_events.items():
            device = next((d for d in self.__devices if d.name == device_name), None)

            if device:
                total_duration_seconds = 0
                is_on = False
                last_on_time = None

                event_list.sort(key=lambda x: datetime.fromisoformat(x["timestamp"]))

                for event in event_list:
                    timestamp = datetime.fromisoformat(event["timestamp"])
                    event_type = event["event"]

                    if event_type == "turn_on" and not is_on:
                        is_on = True
                        last_on_time = timestamp
                    elif event_type == "turn_off" and is_on:
                        is_on = False
                        total_duration_seconds += (
                            timestamp - last_on_time
                        ).total_seconds()

                if is_on:
                    total_duration_seconds += (end - last_on_time).total_seconds()

                duration_hours = total_duration_seconds / 3600
                total_wh = device.power_w * duration_hours

                if duration_hours > 0:
                    report_list.append(
                        {
                            "device_name": device_name,
                            "start": min(
                                datetime.fromisoformat(e["timestamp"])
                                for e in event_list
                            ).isoformat(),
                            "end": max(
                                datetime.fromisoformat(e["timestamp"])
                                for e in event_list
                            ).isoformat(),
                            "total_wh": total_wh,
                        }
                    )

        return report_list

    def report_light_usage(self):
        events = Persistence.load_from_csv(self.event_file_path)

        grouped_events = defaultdict(list)
        for event in events:
            if event["device_type"] == Light.__name__:
                grouped_events[event["device_name"]].append(event)

        total_on_times = {}

        for device_name, event_list in grouped_events.items():
            event_list.sort(key=lambda x: datetime.fromisoformat(x["timestamp"]))

            total_duration_hours = 0
            last_on_time = None
            is_on = False

            for event in event_list:
                timestamp = datetime.fromisoformat(event["timestamp"])
                event_type = event["event"]

                if event_type == "turn_on" and not is_on:
                    is_on = True
                    last_on_time = timestamp
                elif event_type == "turn_off" and is_on:
                    is_on = False
                    total_duration_hours += (
                        timestamp - last_on_time
                    ).total_seconds() / 3600

            if is_on and last_on_time:
                last_log_timestamp = datetime.fromisoformat(events[-1]["timestamp"])
                total_duration_hours += (
                    last_log_timestamp - last_on_time
                ).total_seconds() / 3600

            total_on_times[device_name] = total_duration_hours

        result_list = [
            {"device_name": name, "total_time_h": time}
            for name, time in total_on_times.items()
        ]

        return result_list

    def report_most_used_devices(self):
        events = Persistence.load_from_csv(self.event_file_path)
        result = []
        for event in events:
            device_name = event.get("device_name")
            device_dict = next(
                (
                    device_dict
                    for device_dict in result
                    if device_dict["device_name"] == device_name
                ),
                None,
            )
            if device_dict:
                device_dict["times_used"] = device_dict["times_used"] + 1
            else:
                device_dict = {"device_name": device_name, "times_used": 1}
                result.append(device_dict)
        return sorted(result, key=lambda device_dict: -device_dict["times_used"])

    def report_most_used_commands(self):
        events = Persistence.load_from_csv(self.event_file_path)
        result = []
        for event in events:
            device_name = event.get("device_name")
            event_name = event.get("event")
            device_dict = next(
                (
                    device_dict
                    for device_dict in result
                    if device_dict["device_name"] == device_name
                    and device_dict["event"] == event_name
                ),
                None,
            )
            if device_dict:
                device_dict["times_used"] = device_dict["times_used"] + 1
            else:
                device_dict = {
                    "device_name": device_name,
                    "event": event_name,
                    "times_used": 1,
                }
                result.append(device_dict)
        return sorted(
            result,
            key=lambda device_dict: (
                -device_dict["times_used"],
                device_dict["device_name"],
            ),
        )

    def report_failure_percentage(self):
        events = Persistence.load_from_csv(self.event_file_path)
        result = []
        for event in events:
            device_name = event.get("device_name")
            event_name = event.get("event")
            success = True if event.get("success") == "True" else False
            device_dict = next(
                (
                    device_dict
                    for device_dict in result
                    if device_dict["device_name"] == device_name
                    and device_dict["event"] == event_name
                ),
                None,
            )
            if device_dict:
                device_dict["times_used"] = device_dict["times_used"] + 1

                if not success:
                    device_dict["times_failed"] = device_dict["times_failed"] + 1

                if device_dict["times_failed"] != 0:
                    device_dict["failure_percentage"] = round(
                        (device_dict["times_failed"] / device_dict["times_used"] * 100),
                        2,
                    )
                else:
                    device_dict["failure_percentage"] = 0
            else:
                times_failed = 0 if success else 1
                failure_percentage = 0 if success else 100
                device_dict = {
                    "device_name": device_name,
                    "event": event_name,
                    "times_used": 1,
                    "times_failed": times_failed,
                    "failure_percentage": failure_percentage,
                }
                result.append(device_dict)
        return sorted(
            result,
            key=lambda device_dict: (
                -device_dict["failure_percentage"],
                device_dict["device_name"],
            ),
        )

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
            "routines": {
                name: commands
                for routine in self.__routines
                for name, commands in routine.to_dict().items()
            },
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
