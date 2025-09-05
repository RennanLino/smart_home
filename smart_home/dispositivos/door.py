from transitions import Machine

from smart_home.states.door_state import DoorState, door_transitions


class TransitionNotAllowed:
    pass


class Door:
    def __init__(self):
        self.invalid_tries = 0
        self.machine = Machine(
            model=self,
            states=DoorState,
            initial=DoorState.OPEN,
            transitions=door_transitions
        )

    def lock(self):
        try:
            self.machine.lock()
        except TransitionNotAllowed as e:
            self.invalid_tries += 1
            print(e)
