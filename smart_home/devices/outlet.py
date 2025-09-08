from datetime import datetime, timedelta

from smart_home.devices.base_device import BaseDevice
from smart_home.states.outlet_state import OutletState, outlet_transitions


class Outlet(BaseDevice):
    states = OutletState
    transitions = outlet_transitions

    def __init__(self, name, power_w, initial_state=OutletState.OFF):
        super().__init__(name, initial_state)
        self.__power_w = 0
        self.power_w = power_w
        self.__turned_on_at: datetime | None = None
        self.__total_time = timedelta(0)

    def __str__(self):
        return (
            f"Outlet '{self.name}' [{self.state}] Power: {self.power_w}, "
            f"Total time on: {self.__total_time}, Total consumption: {self.consumption:.2f} Wh"
        )

    @property
    def power_w(self):
        return self.__power_w

    @power_w.setter
    def power_w(self, power_w: int):
        if power_w < 0:
            raise ValueError("Power (W) must be >= then 0")

        self.__power_w = power_w

    @property
    def consumption(self):
        total_time = self.__total_time
        if self.state == OutletState.ON and self.__turned_on_at:
            total_time += datetime.now() - self.__turned_on_at

        hours = total_time.total_seconds() / 3600
        return hours * self.__power_w

    def on_enter_ON(self):
        self.__turned_on_at = datetime.now()

    def on_enter_OFF(self):
        self.__total_time += datetime.now() - self.__turned_on_at
        self.__turned_on_at = None

    def to_dict(self):
        result = super().to_dict()
        result["atributes"] = {
            "power_w": self.power_w,
        }
        return result
