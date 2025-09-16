from enum import auto

from smart_home.states import BaseEnum


class SprinklerState(BaseEnum):
    OFF = auto()
    WATERING = auto()
    PAUSED = auto()


sprinkler_transitions = [
    {"trigger": "turn_on", "source": SprinklerState.OFF, "dest": SprinklerState.PAUSED},
    {"trigger": "turn_off", "source": [SprinklerState.WATERING, SprinklerState.PAUSED], "dest": SprinklerState.OFF},
    {
        "trigger": "resume",
        "source": SprinklerState.PAUSED,
        "dest": SprinklerState.WATERING,
    },
    {
        "trigger": "pause",
        "source": SprinklerState.WATERING,
        "dest": SprinklerState.PAUSED,
    }
]
