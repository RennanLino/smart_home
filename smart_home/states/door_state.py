from enum import auto

from smart_home.states.base_enum import BaseEnum


class DoorState(BaseEnum):
    LOCKED = auto()
    UNLOCKED = auto()
    OPEN = auto()

    def __str__(self):
        return self.name.lower()


door_transitions = [
    {"trigger": "unlock", "source": DoorState.LOCKED, "dest": DoorState.UNLOCKED},
    {"trigger": "lock", "source": DoorState.UNLOCKED, "dest": DoorState.LOCKED},
    {"trigger": "open", "source": DoorState.UNLOCKED, "dest": DoorState.OPEN},
    {"trigger": "close", "source": DoorState.OPEN, "dest": DoorState.UNLOCKED},
]
