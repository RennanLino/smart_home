from smart_home.states import LightState, LightColor, light_transitions


class Light:
    def __init__(self, name):
        super().__init__(name, LightState, LightState.OFF, light_transitions)
        self.__brightness = 100
        self.__color = LightColor.NEUTRAL

    @property
    def brightness(self):
        return self.__brightness

    def set_brightness(self, brightness: int):
        if 0 > brightness > 100:
            raise ValueError("Brightness must be between 0 and 100")

        self._set_brightness()
        self.__brightness = brightness

    @property
    def color(self):
        return self.__color

    def set_color(self, color: LightColor):
        self._set_color()
        self.__color = color

    def __str__(self):
        return f"Light '{self.name}' [{self.state}] Brightness: {self.brightness}, Color: {self.color}"
