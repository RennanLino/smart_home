from enum import auto

from smart_home.states.base_enum import BaseEnum


class OutletState(BaseEnum):
    ON = auto()
    OFF = auto()

    def __str__(self):
        return self.name.lower()


outlet_transitions = [
    {"trigger": "turn_on", "source": OutletState.OFF, "dest": OutletState.ON},
    {"trigger": "turn_off", "source": OutletState.ON, "dest": OutletState.OFF},
]
