import csv
import json
from typing import Any

from smart_home.core import ConfigNotFound


class Persistence:

    @classmethod
    def write_to_csv(cls, filepath: str, message: dict[str, Any]):
        with open(filepath, "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            if csvfile.tell() == 0:
                writer.writerow(list(message.keys()))
            writer.writerow(list(message.values()))

    @classmethod
    def write_to_json(cls, file_path: str, obj: dict):
        with open(file_path, "w", newline="") as jsonfile:
            json.dump(obj, jsonfile, indent=4)

    @classmethod
    def load_from_json(cls, file_path: str):
        try:
            with open(file_path, "r", newline="") as jsonfile:
                obj = json.load(jsonfile)
                return obj
        except json.decoder.JSONDecodeError:
            raise ConfigNotFound(file_path)
        except FileNotFoundError:
            raise ConfigNotFound(file_path)
