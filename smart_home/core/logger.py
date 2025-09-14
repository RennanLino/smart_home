import logging
from datetime import datetime
from enum import Enum, auto
from typing import Any

from smart_home.core import Persistence
from smart_home.core.base.singleton import Singleton

transitions_logger = logging.getLogger("transitions.core")
transitions_logger.setLevel(logging.CRITICAL)


class LogLevel(Enum):
    INFO = auto()
    DEBUG = auto()
    WARNING = auto()
    ERROR = auto()

    def __str__(self):
        return self.name.lower()


class SmartHouseLogger(logging.Logger, metaclass=Singleton):
    _instance = None
    __event_file_path = "data/events.csv"
    __report_file_path = "data/reports.csv"

    def __init__(self):
        super().__init__("smart_house")
        self._initialize_logger()

    def _initialize_logger(self):
        logging.basicConfig(
            level=logging.INFO,
            format="[%(asctime)s] - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            handlers=[
                logging.FileHandler("data/system.log"),
            ],
        )

    def log_event_to_csv(self, message: dict[str, Any]):
        from smart_home.core import Persistence

        timestamp = datetime.now().isoformat()
        message = {"timestamp": timestamp, **message}
        Persistence.write_to_csv(self.__event_file_path, message)

    def log_report_to_csv(self, message: dict[str, Any]):
        Persistence.write_to_csv(self.__report_file_path, message)
