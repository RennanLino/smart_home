from datetime import datetime, timedelta

from smart_home.devices.base_device import BaseDevice
from smart_home.states import EnumDescriptor, SprinklerState, sprinkler_transitions


class Sprinkler(BaseDevice):
    name_pt = "Irrigador"
    state = EnumDescriptor(SprinklerState)
    states = SprinklerState
    transitions = sprinkler_transitions

    def __init__(
        self,
        name,
        flow_rate_lpm,
        total_time=0,
        turned_on_at=None,
        initial_state=SprinklerState.OFF,
    ):
        super().__init__(name, initial_state)
        self.flow_rate_lpm = flow_rate_lpm
        self.__turned_on_at: datetime | None = (
            datetime.fromisoformat(turned_on_at) if turned_on_at else None
        )
        self.__total_time = timedelta(seconds=total_time)

    def __str__(self):
        return (
            f"{self.name_pt}: '{self.name}' [{self.state}] Vazão (L/Min): {self.flow_rate_lpm}, Tempo total ligado: {self.total_time}"
        )

    @property
    def total_time(self):
        if self.state == SprinklerState.ON and self.__turned_on_at:
            self.__total_time += datetime.now() - self.__turned_on_at
        return self.__total_time

    @property
    def turned_on_at(self):
        return self.__total_time

    def on_enter_OFF(self):
        self.__total_time += datetime.now() - self.__turned_on_at
        self.__turned_on_at = None

    def on_exit_OFF(self):
        self.__turned_on_at = datetime.now()

    def to_dict(self):
        result = super().to_dict()
        result["atributes"] = {
            "total_time": (self.total_time.total_seconds() if self.total_time else 0),
            "turned_on_at": (
                self.__turned_on_at.isoformat() if self.__turned_on_at else None
            ),
        }
        return result
