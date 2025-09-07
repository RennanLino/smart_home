import logging
from datetime import datetime
from enum import Enum, auto
from typing import List

from smart_home.core.persistence import Persistence

transitions_logger = logging.getLogger("transitions.core")
transitions_logger.setLevel(logging.CRITICAL)


class LogLevel(Enum):
    INFO = auto()
    DEBUG = auto()
    WARNING = auto()
    ERROR = auto()

    def __str__(self):
        return self.name.lower()


class Logger:
    _instance = None
    __event_file_path = "data/events.csv"
    __event_headers = [
        "timestamp",
        "device_name",
        "event",
        "source_state",
        "destiny_state",
        "success",
    ]
    __report_file_path = "data/reports.csv"
    __report_headers = [
        "device_name",
        "total_wh",
        "start_time",
        "end_time",
    ]

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._initialize_logger()
        return cls._instance

    def _initialize_logger(self):
        logging.basicConfig(
            level=logging.INFO,
            format="%[(asctime)s] - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            handlers=[
                logging.FileHandler("data/system.log"),
            ],
        )
        self.logger = logging.getLogger()

    def log_event_to_csv(self, message: List[str]):
        timestamp = datetime.now().isoformat()
        message = [timestamp, *message]
        try:
            Persistence.write_to_csv(
                self.__event_file_path, self.__event_headers, message
            )
        except Exception as e:
            self.logger.error(f"Error writing to CSV: {e}")

    def log_report_to_csv(self, message: List[str]):
        try:
            Persistence.write_to_csv(
                self.__report_file_path, self.__report_headers, message
            )
        except Exception as e:
            self.logger.error(f"Error writing to CSV: {e}")
