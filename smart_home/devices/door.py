import os

from dotenv import load_dotenv

from smart_home.devices.base_device import BaseDevice
from smart_home.states.door_state import DoorState, door_transitions

load_dotenv()
debug_mode = os.getenv("DEBUG")


class Door(BaseDevice):
    states = DoorState
    initial_state = DoorState.OPEN
    transitions = door_transitions

    def __init__(self, name, initial_state=None):
        initial_state = initial_state if initial_state else self.initial_state
        super().__init__(name, self.states, initial_state, self.transitions)
        self.__invalid_tries = 0

    def __str__(self):
        return f"Door '{self.name}' [{self.state}] Invalid lock tries: {self.invalid_tries}"

    @property
    def invalid_tries(self):
        return self.__invalid_tries

    def lock(self):
        result = self._lock()
        if not result.success:
            self.__invalid_tries += 1
        return result
