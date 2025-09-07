import csv
import logging
from datetime import datetime
from enum import Enum, auto
from typing import List

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

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._initialize_logger()
        return cls._instance

    def _initialize_logger(self):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s,%(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            handlers=[
                logging.FileHandler("data/system.log"),
            ],
        )
        self.logger = logging.getLogger()

    def log_event_to_csv(self, message: str):
        self.log_to_csv(self.__event_file_path, self.__event_headers, message)

    @staticmethod
    def log_to_csv(filepath: str, headers: List[str], message: List[str]):
        try:
            timestamp = datetime.now().isoformat()
            message = [timestamp, *message]
            with open(filepath, "a", newline="") as csvfile:
                writer = csv.writer(csvfile)
                if csvfile.tell() == 0:
                    writer.writerow(headers)
                writer.writerow(message)
        except Exception as e:
            logging.error(f"Error writing to CSV: {e}")
