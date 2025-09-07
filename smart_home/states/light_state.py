from enum import Enum, auto


class LightState(Enum):
    ON = auto()
    OFF = auto()

    def __str__(self):
        return self.name.lower()


class LightColor(Enum):
    COLD = auto()
    WARM = auto()
    NEUTRAL = auto()

    def __str__(self):
        return self.name.lower()


light_transitions = [
    {"trigger": "turn_on", "source": LightState.OFF, "dest": LightState.ON},
    {"trigger": "turn_off", "source": LightState.ON, "dest": LightState.OFF},
    {"trigger": "_set_brightness", "source": LightState.ON, "dest": LightState.ON},
    {"trigger": "_set_color", "source": LightState.ON, "dest": LightState.ON},
]
