from datetime import datetime, timedelta

from smart_home.devices.base_device import BaseDevice
from smart_home.states.outlet_state import OutletState, outlet_transitions


class Outlet(BaseDevice):
    def __init__(self, name, power_w):
        super().__init__(name, OutletState, OutletState.OFF, outlet_transitions)
        self.__power = 0
        self.power = power_w
        self.__turned_on_at: datetime | None = None
        self.__total_time = timedelta(0)

    def __str__(self):
        return (
            f"Outlet '{self.name}' [{self.state}] Power: {self.power}, "
            f"Total time on: {self.__total_time}, Total consumption: {self.consumption:.2f} Wh"
        )

    @property
    def power(self):
        return self.__power

    @power.setter
    def power(self, power_w: int):
        if power_w < 0:
            raise ValueError("Power (W) must be >= then 0")

        self.__power = power_w

    @property
    def consumption(self):
        total_time = self.__total_time
        if self.state == OutletState.ON and self.__turned_on_at:
            total_time += datetime.now() - self.__turned_on_at

        hours = total_time.total_seconds() / 3600
        return hours * self.__power

    def turn_on(self):
        self._turn_on()
        self.__turned_on_at = datetime.now()

    def turn_off(self):
        self._turn_off()
        self.__total_time += datetime.now() - self.__turned_on_at
        self.__turned_on_at = None

    def to_dict(self):
        result = super().to_dict()
        result["atributes"] = {
            "power_w": self.power,
        }
        return result
