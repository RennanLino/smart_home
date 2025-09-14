from transitions import Machine, Event


class EventResult:
    def __init__(
        self,
        device_name: str,
        event: str,
        source_state: str,
        destiny_state: str,
        success: bool,
    ):
        self.device_name = device_name
        self.event = event
        self.source_state = source_state
        self.destiny_state = destiny_state
        self.success = success


class CustomEvent(Event):

    def trigger(self, model: "BaseDevice", *args, **kwargs):
        result = False
        source_state = str(model.state).lower()
        destiny_state = list(self.transitions.values())[0][0].dest.lower()
        event_name = self.name[1:] if self.name.startswith("_") else self.name
        try:
            result = super().trigger(model, *args, **kwargs)
        finally:
            event_result = EventResult(model.name, event_name, source_state, destiny_state, result)
            return event_result

class CustomMachine(Machine):
    event_cls = CustomEvent
