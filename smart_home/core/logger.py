import logging
from datetime import datetime
from enum import Enum, auto
from typing import Any, List

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

    def __init__(self):
        super().__init__("smart_house")
        logging.basicConfig(
            level=logging.INFO,
            format="[%(asctime)s] - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            handlers=[
                logging.FileHandler("data/system.log"),
            ],
        )

    @staticmethod
    def log_event_to_csv(event_file_path: str,  message: dict[str, Any]):
        from smart_home.core import Persistence

        timestamp = datetime.now().isoformat()
        message = {"timestamp": timestamp, **message}
        Persistence.write_to_csv( event_file_path, message)

    @staticmethod
    def log_report_to_csv(report_file_path: str, messages: List[dict[str, Any]]):
        Persistence.clear_csv(report_file_path)
        for message in messages:
            Persistence.write_to_csv(report_file_path, message)
