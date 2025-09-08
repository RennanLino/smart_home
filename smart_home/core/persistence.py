import csv
import json
from typing import Any

from smart_home.core import Logger, LogLevel


class Persistence:
    logger = Logger()

    @classmethod
    def write_to_csv(cls, filepath: str, message: dict[str, Any]):
        try:
            with open(filepath, "a", newline="") as csvfile:
                writer = csv.writer(csvfile)
                if csvfile.tell() == 0:
                    writer.writerow(list(message.keys()))
                writer.writerow(list(message.values()))
        except Exception as e:
            cls.logger.log(str(e), LogLevel.ERROR)

    @classmethod
    def write_to_json(cls, file_path: str, obj: dict):
        try:
            with open(file_path, "w", newline="") as jsonfile:
                json.dump(obj, jsonfile, indent=4)
        except Exception as e:
            cls.logger.log(str(e), LogLevel.ERROR)

    @classmethod
    def load_from_json(cls, file_path: str):
        try:
            with open(file_path, "r", newline="") as jsonfile:
                obj = json.load(jsonfile)
                return obj
        except json.decoder.JSONDecodeError:
            cls.logger.log(
                f"Config file {file_path} not found or empty", LogLevel.ERROR
            )
        except Exception as e:
            cls.logger.log(str(e), LogLevel.ERROR)
