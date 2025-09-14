from smart_home.devices.base_device import BaseDevice
from smart_home.states import EnumDescriptor
from smart_home.states.door_state import DoorState, door_transitions


class Door(BaseDevice):
    name_pt = "Porta"
    state = EnumDescriptor(DoorState)
    states = DoorState
    transitions = door_transitions

    def __init__(self, name, initial_state=DoorState.OPEN):
        super().__init__(name, initial_state)
        self.__invalid_tries = 0

    def __str__(self):
        return f"{self.name_pt} '{self.name}' [{self.state}] Tentativas invalidas de destrancar: {self.invalid_tries}"

    @property
    def invalid_tries(self):
        return self.__invalid_tries

    def check_invalid_lock(self):
        if not self.may_lock():
            self.__invalid_tries += 1
