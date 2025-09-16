from datetime import datetime, timedelta

from smart_home.devices.base_device import BaseDevice
from smart_home.states import EnumDescriptor, ac_transitions, ACState, ACMode


class AC(BaseDevice):
    available_attributes = ["power_w", "temperature", "mode"]
    name_pt = "Ar Condicionado"
    state = EnumDescriptor(ACState)
    states = ACState
    transitions = ac_transitions

    def __init__(
        self,
        name,
        power_w,
        temperature=24,
        mode=ACMode.AUTO,
        total_time=0,
        turned_on_at=None,
        initial_state=ACState.OFF,
    ):
        super().__init__(name, initial_state)
        self.__power_w = 0
        self.power_w = power_w
        self.temperature = temperature
        self.mode = mode
        self.__turned_on_at: datetime | None = (
            datetime.fromisoformat(turned_on_at) if turned_on_at else None
        )
        self.__total_time = timedelta(seconds=total_time)  # if total_time else None

    def __str__(self):
        return (
            f"{self.name_pt}: '{self.name}' [{self.state}] Potencia nominal: {self.power_w}, \n"
            f"Modo: {self.mode}, Tempo total ligado: {self.total_time}"
        )

    @property
    def power_w(self):
        return self.__power_w

    @power_w.setter
    def power_w(self, power_w: int):
        if power_w < 0:
            raise ValueError("Power (W) must be >= then 0")

        self.__power_w = power_w

    @property
    def total_time(self):
        if self.state == ACState.ON and self.__turned_on_at:
            self.__total_time += datetime.now() - self.__turned_on_at
        return self.__total_time

    @property
    def turned_on_at(self):
        return self.__total_time

    @property
    def current_power_w(self):
        current_power_w = 0
        if self.state == ACState.ON:
            match self.mode:
                case ACMode.AUTO:
                    current_power_w = self.power_w * 0.8
                case ACMode.COOLING:
                    current_power_w = self.power_w * (self.temperature - 18) * (1 - 0.8) / (24 - 18) + 0.8
                case ACMode.DRY:
                    current_power_w = self.power_w * 0.7
                case ACMode.FAN:
                    current_power_w = self.power_w * 0.5
        return current_power_w

    def on_enter_ON(self):
        self.__turned_on_at = datetime.now()

    def on_enter_OFF(self):
        self.__total_time += datetime.now() - self.__turned_on_at
        self.__turned_on_at = None

    def _set_cooling(self):
        self.mode = ACMode.COOLING

    def _set_fan(self):
        self.mode = ACMode.FAN

    def _set_dry(self):
        self.mode = ACMode.DRY

    def to_dict(self):
        result = super().to_dict()
        result["atributes"] = {
            "power_w": self.power_w,
            "temperature": self.temperature,
            "mode": str(self.mode),
            "total_time": (self.total_time.total_seconds() if self.total_time else 0),
            "turned_on_at": (
                self.__turned_on_at.isoformat() if self.__turned_on_at else None
            ),
        }
        return result

    @classmethod
    def get_available_attr_req(cls, attr_name: str):
        match attr_name:
            case "power_w":
                return {
                    "available_values": range(2001),
                    "message": f"Digite a potência (Entre 0 e 2000 W):\n> ",
                }
            case "temperature":
                return {
                    "available_values": range(18, 25),
                    "message": "Digite a temperatura (Entre 18 e 24):\n> ",
                }
            case "mode":
                return {
                    "available_values": ACMode,
                    "message": "Escolha o modo:\n"
                    + "\n".join([f"{m.value}. {m.name}" for m in ACMode])
                    + "\n> ",
                }
        return None

    @classmethod
    def get_command_kwargs(cls, command_name):
        result = {}
        match command_name:
            case "__init__":
                result = {"power_w": cls.get_available_attr_req("power_w")}
        return result
