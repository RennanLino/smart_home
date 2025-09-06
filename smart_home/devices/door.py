import os

from dotenv import load_dotenv
from transitions import MachineError

from smart_home.devices.base_device import BaseDevice
from smart_home.states.door_state import DoorState, door_transitions

load_dotenv()
debug_mode = os.getenv("DEBUG")


class Door(BaseDevice):
    def __init__(self, name):
        super().__init__(name, DoorState, DoorState.OPEN, door_transitions)
        self.__invalid_tries = 0

    @property
    def invalid_tries(self):
        return self.__invalid_tries

    def lock(self):
        try:
            self._lock()
            self.notify()
        except MachineError as e:
            self.__invalid_tries += 1
            if debug_mode:
                print(e)
            else:
                raise

    def __str__(self):
        return f"Door '{self.name}' [{self.state}] Invalid lock tries: {self.invalid_tries}"
