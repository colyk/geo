import os
import json
from typing import Dict


class Cache:
    def __init__(self, base_path: str = None, subdir: str = "", **params):
        if base_path is None:
            base_path = os.path.dirname(os.path.abspath(__file__))

        base_path = os.path.join(base_path, "cache")
        if not os.path.isdir(base_path):
            os.mkdir(base_path)

        self.base_path = os.path.join(base_path, subdir)
        if os.path.isdir(self.base_path):
            print(f"Dir {self.base_path} already exists.")
        else:
            os.mkdir(base_path)

    def add(self, name: str, data: Dict, format_: str = "json"):
        name = str(name)
        filename = os.path.join(self.base_path, name)
        if format_ == "json":
            self._add_json(filename, data)

    def _add_json(self, filename: str, data: Dict):
        json_data = json.dumps(data)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(json_data)

    def get(self, name: str) -> Dict:
        filename = os.path.join(self.base_path, name)

        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
            json_data = json.loads(content)
            return json_data

    def remove(self, name: str):
        filename = os.path.join(self.base_path, name)
        os.remove(filename)


if __name__ == "__main__":
    c = Cache()
    data = {"example": "data"}
    c.add("data", data)
    data = c.get("data")
    print(data)
    c.remove("data")
