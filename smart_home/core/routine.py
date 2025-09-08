from typing import List

from smart_home.core import Command


class Routine:
    def __init__(self, name: str, commands: List[Command]):
        self.name = name
        self.commands = commands

    def run(self):
        for command in self.commands:
            command.run()

    def to_dict(self):
        return {
            self.name: [command.to_dict() for command in self.commands],
        }

    @staticmethod
    def from_dict(routine_name, command_dicts, devices):
        commands = [
            Command.from_dict(command_dict, devices) for command_dict in command_dicts
        ]
        return Routine(routine_name, commands)
