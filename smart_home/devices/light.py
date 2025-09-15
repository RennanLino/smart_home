from datetime import timedelta, datetime

from smart_home.devices.base_device import BaseDevice
from smart_home.states import LightState, LightColor, light_transitions
from smart_home.states.base_enum import EnumDescriptor


class Light(BaseDevice):
    name_pt = "Luz"
    state = EnumDescriptor(LightState)
    states = LightState
    transitions = light_transitions
    __color = EnumDescriptor(LightColor)

    def __init__(
        self,
        name,
        brightness=100,
        color=LightColor.NEUTRAL,
        total_time=0,
        turned_on_at=None,
        initial_state=LightState.OFF,
    ):
        super().__init__(name, initial_state)
        self.brightness = brightness
        self.color = color
        self.__turned_on_at: datetime | None = datetime.fromisoformat(turned_on_at) if turned_on_at else None
        self.__total_time = timedelta(seconds=total_time)

    def __str__(self):
        return f"{self.name_pt}: '{self.name}' [{self.state}] Brilho: {self.brightness}, Cor: {self.color}"

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

    @property
    def total_time(self):
        if self.state == OutletState.ON and self.__turned_on_at:
            self.__total_time += datetime.now() - self.__turned_on_at
            return self.__total_time

    def on_enter_ON(self):
        self.__turned_on_at = datetime.now()

    def on_enter_OFF(self):
        self.__total_time += datetime.now() - self.__turned_on_at
        self.__turned_on_at = None

    def to_dict(self):
        result = super().to_dict()
        result["atributes"] = {
            "brightness": self.brightness,
            "color": str(self.color),
            "total_time": self.__turned_on_at.isoformat() if self.__turned_on_at else None,
        }
        return result

    @classmethod
    def get_available_attr_values(cls, attr_name: str):
        result = None
        match attr_name:
            case "brightness":
                result =  range(101)
            case "color":
                result =  [c.value for c in LightColor]
        return result

    @classmethod
    def get_command_kwargs(cls, command_name):
        result = super().get_command_kwargs(command_name)
        match command_name:
            case "set_brightness":
                attr = "brightness"
                result = {
                    attr : {
                        "available_values": cls.get_available_attr_values(attr),
                        "message": "Digite o brilho (entre 0 e 100):\n> "
                    }
                }
            case "set_color":
                attr = "color"
                result = {
                    attr : {
                        "available_values": cls.get_available_attr_values(attr),
                        "message": "Digite um valor para a cor :\n" + "\n".join([f"{c.value}. {c.name}" for c in LightColor]) + "\n> "
                    }
                }
        return result
