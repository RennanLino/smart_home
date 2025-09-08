class Command:
    def __init__(self, name: str, device: "BaseDevice", **kwargs):
        self.name = name
        self.device = device
        self.kwargs = kwargs

    def run(self):
        return getattr(self.device, self.name)(**self.kwargs)

    def to_dict(self):
        return {
            "device_name": self.device.to_dict(),
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
        return Command(command_name, device, **kwargs)
