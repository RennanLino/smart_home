from transitions import Machine, MachineError, Event


class LoggingEvent(Event):
    def trigger(self, model, *args, **kwargs):
        result = False
        source_state = str(model.state).lower()
        destiny_state = list(self.transitions.values())[0][0].dest.lower()
        try:
            result = super().trigger(model, *args, **kwargs)
            return result
        except MachineError:
            return False
        finally:
            event_name = self.name[1:] if self.name.startswith("_") else self.name
            message = [model.name, event_name, source_state, destiny_state, result]
            model.logger.log_event_to_csv(message)


class LoggingMachine(Machine):
    event_cls = LoggingEvent
