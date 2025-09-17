class Command:
    def __init__(self, device: "BaseDevice", name: str, **kwargs):
        self.device = device
        self.name = name
        self.kwargs = kwargs

    def run(self):
        return getattr(self.device, self.name)(**self.kwargs)

    def to_dict(self):
        return {
            "device_name": self.device.name,
            "command": self.name,
            "arguments": self.kwargs,
        }

    @staticmethod
    def from_dict(command_dict, devices):
        command_name = command_dict["command"]
        device = next(
            device for device in devices if device.name == command_dict["device_name"]
        )
        kwargs = command_dict["arguments"]
        return Command(device, command_name, **kwargs)
