from enum import auto

from smart_home.states import BaseEnum


class LightState(BaseEnum):
    ON = auto()
    OFF = auto()

    def __str__(self):
        return self.name.lower()


class LightColor(BaseEnum):
    COLD = auto()
    WARM = auto()
    NEUTRAL = auto()

    def __str__(self):
        return self.name.lower()


light_transitions = [
    {"trigger": "turn_on", "source": LightState.OFF, "dest": LightState.ON, "conditions": "test"},
    {"trigger": "turn_off", "source": LightState.ON, "dest": LightState.OFF},
    {
        "trigger": "set_brightness",
        "source": LightState.ON,
        "dest": LightState.ON,
        "after": "_set_brightness",
    },
    {
        "trigger": "set_color",
        "source": LightState.ON,
        "dest": LightState.ON,
        "after": "_set_color",
    },
]
