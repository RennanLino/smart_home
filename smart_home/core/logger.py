import logging
from enum import Enum, auto

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

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._initialize_logger()
        return cls._instance

    def _initialize_logger(self):
        logging.basicConfig(
            level=logging.INFO,
            format="[%(asctime)s] %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            handlers=[
                logging.FileHandler("data/smart_home.log"),
            ],
        )
        self.logger = logging.getLogger()

    def update(self, message: str, log_level: LogLevel):
        log_level_name = str(log_level)
        if hasattr(self.logger, log_level_name):
            log_method = getattr(self.logger, log_level_name)
            log_method(message)
