import os

from dotenv import load_dotenv
from transitions import Machine, MachineError

from smart_home.states.door_state import DoorState, door_transitions

load_dotenv()
debug_mode = os.getenv("DEBUG")


class Door:
    def __init__(self, name):
        self.name = name
        self.__invalid_tries = 0
        self.machine = Machine(
            model=self,
            states=DoorState,
            initial=DoorState.OPEN,
            transitions=door_transitions,
        )

    @property
    def invalid_tries(self):
        return self.__invalid_tries

    def lock(self):
        try:
            return self._lock()
        except MachineError as e:
            self.__invalid_tries += 1
            if debug_mode:
                print(e)
            else:
                raise

    def __str__(self):
        return f"Door '{self.name}' [{self.state}] Invalid lock tries: {self.invalid_tries}"
