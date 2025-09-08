from transitions import Machine, Event, MachineError

from smart_home.core import LogLevel, Logger


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


class LoggingEvent(Event):
    logger = Logger()

    def trigger(self, model: "BaseDevice", *args, **kwargs):
        result = False
        source_state = str(model.state).lower()
        destiny_state = list(self.transitions.values())[0][0].dest.lower()
        event_name = self.name[1:] if self.name.startswith("_") else self.name
        try:
            result = super().trigger(model, *args, **kwargs)
        except MachineError as e:
            self.logger.log(str(e), LogLevel.WARNING)
        except Exception as e:
            self.logger.log(str(e), LogLevel.ERROR)
        finally:
            result = EventResult(
                model.name, event_name, source_state, destiny_state, result
            )
            self.logger.log_event_to_csv(vars(result))
            model.house.notify_transition_event(result)
            return result


class LoggingMachine(Machine):
    event_cls = LoggingEvent
