from smart_home.core.logger import Logger
from smart_home.core.logging_machine import LoggingMachine


class BaseDevice:
    def __init__(self, name: str, states, initial_state, transitions):
        self.name = name
        self.logger = Logger()
        self.machine = LoggingMachine(
            model=self,
            states=states,
            initial=initial_state,
            transitions=transitions,
        )
