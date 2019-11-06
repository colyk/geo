import json
import os
import os.path as op
import shutil
import zlib
from typing import Dict, Union, List


class Cache:
    def __init__(self, base_path: str = None, prefix: str = "", **params):
        if base_path is None:
            base_path = op.dirname(op.abspath(__file__))

        base_path = op.join(base_path, "cache")
        if not op.isdir(base_path):
            os.mkdir(base_path)

        self.base_path = op.join(base_path, prefix)
        if not op.isdir(self.base_path):
            os.mkdir(self.base_path)

        self.compress_level = params.get("compress_level", 5)

    def add(self, name: str, data: Dict, format_: str = "json"):
        name = str(name)
        filename = op.join(self.base_path, name)
        if format_ == "json":
            self._add_json(filename, data)

    def _add_json(self, filename: str, data: Dict):
        json_data = json.dumps(data).encode("utf-8")
        compressed = zlib.compress(json_data, self.compress_level)
        with open(filename, "bw") as f:
            f.write(compressed)

    def get(self, name: str) -> Union[Dict, None]:
        filename = op.join(self.base_path, name)
        if not op.isfile(filename):
            return None

        with open(filename, "br") as f:
            decompressed = zlib.decompress(f.read()).decode("utf-8")
            json_data = json.loads(decompressed)
            return json_data

    def get_caches(self) -> List[str]:
        return os.listdir(self.base_path)

    def remove(self, name: str):
        filename = op.join(self.base_path, name)
        os.remove(filename)

    def invalidate_all(self) -> None:
        shutil.rmtree(self.base_path)
