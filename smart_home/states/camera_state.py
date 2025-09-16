from enum import auto

from smart_home.states import BaseEnum


class CameraState(BaseEnum):
    OFF = auto()
    AT_HOME = auto()
    AWAY = auto()
    INACTIVE = auto()


camera_transitions = [
    {"trigger": "turn_on", "source": CameraState.OFF, "dest": CameraState.AT_HOME},
    {"trigger": "turn_off", "source": [CameraState.AT_HOME, CameraState.AWAY, CameraState.INACTIVE], "dest": CameraState.OFF},
    {
        "trigger": "set_at_home",
        "source": [CameraState.AWAY, CameraState.INACTIVE],
        "dest": CameraState.AT_HOME,
    },
    {
        "trigger": "set_away",
        "source": [CameraState.AT_HOME, CameraState.INACTIVE],
        "dest": CameraState.AWAY,
    },
    {
        "trigger": "set_inactive",
        "source": [CameraState.AT_HOME, CameraState.AWAY],
        "dest": CameraState.INACTIVE,
    }
]
