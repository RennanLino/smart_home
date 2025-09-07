from enum import Enum, auto


class OutletState(Enum):
    ON = auto()
    OFF = auto()

    def __str__(self):
        return self.name.lower()


outlet_transitions = [
    {"trigger": "_turn_on", "source": OutletState.OFF, "dest": OutletState.ON},
    {"trigger": "_turn_off", "source": OutletState.ON, "dest": OutletState.OFF},
]
