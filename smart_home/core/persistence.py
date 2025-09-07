import csv
import json
from typing import List


class Persistence:

    @staticmethod
    def write_to_csv(filepath: str, headers: List[str], message: List[str]):
        with open(filepath, "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            if csvfile.tell() == 0:
                writer.writerow(headers)
            writer.writerow(message)

    @staticmethod
    def write_to_json(file_path: str, obj: dict):
        with open(file_path, "w", newline="") as jsonfile:
            json.dump(obj, jsonfile, indent=4)
