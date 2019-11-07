import json
import os
import os.path as op
import pickle
import shutil
import zlib
from typing import Dict, Union, List, Any


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

        self.formats = ["json", "object"]

    def add(self, name: str, data: Any, format_: str = "json"):
        if format_ not in self.formats:
            raise TypeError(
                f"Unknown format: {format_}.\nAvailable formats: {self.formats}"
            )
        filename = op.join(self.base_path, name)
        if format_ == "json":
            self._add_json(filename, data)
        elif format_ == "object":
            self._add_object(filename, data)

    def _add_json(self, filename: str, data: Any):
        json_data = json.dumps(data).encode("utf-8")
        compressed = zlib.compress(json_data, self.compress_level)
        with open(filename, "bw") as f:
            f.write(compressed)

    def _add_object(self, filename: str, data: Any):
        pickled_data = pickle.dumps(data)
        compressed = zlib.compress(pickled_data, self.compress_level)
        with open(filename, "bw") as f:
            f.write(compressed)

    def get(self, name: str) -> Union[Dict, None]:
        filename = op.join(self.base_path, name)
        if not op.isfile(filename):
            return None

        with open(filename, "br") as f:
            decompressed = zlib.decompress(f.read())
            try:
                return json.loads(decompressed)
            except UnicodeDecodeError:
                return pickle.loads(decompressed)

    @property
    def caches(self) -> List[str]:
        return os.listdir(self.base_path)

    def invalidate(self, name: str):
        filename = op.join(self.base_path, name)
        os.remove(filename)

    def invalidate_all(self) -> None:
        shutil.rmtree(self.base_path)
        os.mkdir(self.base_path)
