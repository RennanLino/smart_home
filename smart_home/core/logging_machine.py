from transitions import Machine, MachineError, Event

from smart_home.core.logger import LogLevel


class LoggingEvent(Event):
    def trigger(self, model, *args, **kwargs):
        try:
            result = super().trigger(model, *args, **kwargs)

            if result:
                model.notify(
                    f"[{type(model).__name__} - {model.name}] Transition successful, now in '{model.state}'",
                    LogLevel.INFO,
                )
            else:
                model.notify(
                    f"[{type(model).__name__} - {model.name}] No transition executed for trigger '{self.name}'",
                    LogLevel.WARNING,
                )

            return result
        except MachineError:
            model.notify(
                f"[{type(model).__name__} - {model.name}] Invalid trigger '{self.name}' from state '{model.state}'",
                LogLevel.ERROR,
            )
            return False


class LoggingMachine(Machine):
    event_cls = LoggingEvent
