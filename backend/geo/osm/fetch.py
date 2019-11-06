import json
import time
from collections import namedtuple
from typing import List, Sequence

import overpass
import requests


if __package__ is None or not __package__:
    from backend.geo.osm.osm_types import types
    from backend.geo.cache import Cache
else:
    from .osm_types import types
    from ..cache import Cache

Bbox = namedtuple('Bbox', ['min_lat', 'min_lon', 'max_lat', 'max_lon'])
class OSMError(Exception):
    def __init__(self, message):
        super().__init__(message)


def is_data_inside_bbox(data, bbox: Bbox) -> bool:
    min_lat, min_lon, max_lat, max_lon = bbox
    for point in data:
        lat, lon = point
        if lon < min_lon or lon > max_lon or lat < min_lat or lat > max_lat:
            return False
    return True

class OSM:
    def __init__(self, responseformat: str = "geojson", debug: bool = False):
        self.api = overpass.API(timeout=60)
        self.responseformat = responseformat
        self.debug = debug
        self.bbox_cache = Cache(prefix='bbox')

        self.default_el_classes = ["node", "way", "relation"]

    def fetch(
        self,
        q: str,
        ref_class: str,
        el_type: List[Sequence[str]],
        el_classes: List[str] = None,
    ):
        if self.debug:
            self.status()
        if el_classes is None:
            el_classes = self.default_el_classes

        selector = self.type_to_selector(el_type)

        query = f"{ref_class}({q});\nmap_to_area->.a;\n(\n"
        for el_class in el_classes:
            for val in selector:
                query += f"\t{el_class}(area .a){val};\n"
        query += ");\n(._;>;);"

        if self.debug:
            print(query)
        time_fetch = time.time()
        response = self.api.get(query, responseformat=self.responseformat, verbosity="geom")
        time_filter = time.time()
        filtered = self.strip_data(response)
        if self.debug:
            print(f'Fetch time {time.time() - time_fetch}')
            print(f'Filter time {time.time() - time_filter}')
        return filtered

    def status(self):
        r = requests.get('https://overpass-api.de/api/status')
        print(r.text)

    def fetch_by_bbox(
        self,
        bbox: Bbox,
        el_type,
        el_classes: List[str] = None,
    ):
        caches = self.bbox_cache.get_caches()
        sbbox = f"{bbox.min_lat}, {bbox.min_lon}, {bbox.max_lat}, {bbox.max_lon}"

        for cache in caches:
            d = cache.split(',')
            d = list(map(float, d))
            d = [[d[0], d[1]], [d[2], d[3]]]
            if is_data_inside_bbox(d, bbox):
                return self.bbox_cache.get(sbbox)

        data = self.fetch(sbbox, "way", el_type, el_classes)

        self.bbox_cache.add(sbbox, data)
        return data

    def strip_data(self, data):
        striped_data = str(data)
        for key in data["features"]:
            if not key["properties"]:
                striped_data = striped_data.replace(str(key) + ", ", "")
                striped_data = striped_data.replace(str(key), "")
        return json.loads(striped_data)

    def type_to_selector(self, el_type):
        selector = ""
        if isinstance(el_type, List):
            for i, val in enumerate(el_type):
                if isinstance(val, List):
                    selector += types[el_type[i][0]][:-1] + '="' + el_type[i][1] + '"]'
                else:
                    selector += types.get(el_type[i], "")
        else:
            selector = types.get(el_type, "")
        type_list = selector.split("|")
        if len(type_list) > 1:
            for i, val in enumerate(type_list):
                type_list[i] = types.get(val)

        if not type_list:
            raise OSMError("Unknown el_type")
        return type_list


if __name__ == "__main__":
    osm = OSM(debug=True)
    # data = osm.fetch(
    #     "2904797",
    #     "relation",
    #     [["address_street", "Artura Grottgera"], "name", "building"],
    #     ["way"],
    # )
    start = time.time()
    bbox = Bbox(min_lat=51.1952, min_lon=22.5384, max_lat=51.2012, max_lon=22.5485)
    data = osm.fetch_by_bbox(bbox, "_pedestrian_way")
    print(f'Fetch took {time.time() - start}')
    # data = osm.fetch(
    #     "2904797",
    #     "relation",
    #     [
    #         ["address_street", "Dolna Panny Marii"],
    #         ["address_housenumber", "28"],
    #         "building",
    #     ],
    # )
    # data = osm.strip_data(data)
    r = json.dumps(data, indent=4, sort_keys=True)
    with open("data.json", "w", encoding="utf-8") as f:
        f.write(r)
