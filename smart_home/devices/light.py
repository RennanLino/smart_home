from smart_home.devices.base_device import BaseDevice
from smart_home.states import LightState, LightColor, light_transitions
from smart_home.states.base_enum import EnumDescriptor


class Light(BaseDevice):
    states = LightState
    state = EnumDescriptor(LightState)
    __color = EnumDescriptor(LightColor)
    transitions = light_transitions

    def __init__(
        self,
        name,
        brightness=100,
        color=LightColor.NEUTRAL,
        initial_state=LightState.OFF,
    ):
        super().__init__(name, initial_state)
        self.brightness = brightness
        self.color = color

    def __str__(self):
        return f"Light '{self.name}' [{self.state}] Brightness: {self.brightness}, Color: {self.color}"

    @property
    def brightness(self):
        return self.__brightness

    @brightness.setter
    def brightness(self, brightness):
        if 0 > brightness or brightness > 100:
            raise ValueError("Brightness must be between 0 and 100")
        self.__brightness = brightness

    # Used after set_brightness transition
    def _set_brightness(self, brightness):
        self.brightness = brightness

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, color):
        self.__color = color

    # Used after set_color transition
    def _set_color(self, color: LightColor):
        self.color = color

    def to_dict(self):
        result = super().to_dict()
        result["atributes"] = {
            "brightness": self.brightness,
            "color": str(self.color),
        }
        return result

    def get_command_kwargs(self, command_name):
        result = {}
        match command_name:
            case "set_brightness":
                result = {
                    "brightness": {
                        "available_values": range(100),
                        "message": "Digite o brilho (entre 0 e 100):\n> "
                    }
                }
            case "set_color":
                result = {
                    "color": {
                        "available_values": [c.value for c in LightColor],
                        "message": "Digite um valor para a cor :\n" + "\n".join([f"{c.value}. {c.name}" for c in LightColor]) + "\n> "
                    }
                }
        return result