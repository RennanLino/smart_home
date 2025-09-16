from enum import auto

from smart_home.states import BaseEnum


class ACState(BaseEnum):
    ON = auto()
    OFF = auto()


class ACMode(BaseEnum):
    AUTO = auto()
    COOLING = auto()
    FAN = auto()
    DRY = auto()


ac_transitions = [
    {"trigger": "turn_on", "source": ACState.OFF, "dest": ACState.ON},
    {"trigger": "turn_off", "source": ACState.ON, "dest": ACState.OFF},
    {
        "trigger": "set_auto",
        "source": [ACState.ON, ACState.OFF],
        "dest": ACState.ON,
        "after": "_set_auto",
    },
    {
        "trigger": "set_cooling",
        "source": [ACState.ON, ACState.OFF],
        "dest": ACState.ON,
        "after": "_set_cooling",
    },
    {
        "trigger": "set_fan",
        "source": [ACState.ON, ACState.OFF],
        "dest": ACState.ON,
        "after": "_set_cooling",
    },
    {
        "trigger": "set_dry",
        "source": [ACState.ON, ACState.OFF],
        "dest": ACState.ON,
        "after": "_set_cooling",
    },
]
