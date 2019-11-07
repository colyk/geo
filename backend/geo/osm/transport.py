import time
from pprint import pprint
from typing import Union, Dict

import requests

from backend.geo.cache import Cache

if __package__ is None or not __package__:
    from backend.geo.osm import Coord
else:
    from . import Coord


class Transport:
    def __init__(self):
        self.api = "http://transit.land/api/v1/"
        self.cache = Cache(prefix="transport")

    def get_bus_station_by_coords(
        self, coord: Coord, radius: int = 500
    ) -> Union[Dict, None]:
        cache_file = str(coord) + str(radius)
        cache = self.cache.get(cache_file)
        if cache is not None:
            return cache
        api = self.api + "stops"
        lat = coord.lat
        lon = coord.lon
        params = {"lat": lat, "lon": lon, "r": radius}
        res = requests.get(api, params)
        if res.ok:
            json_res = self._parse_stops(res.json())
            self.cache.add(cache_file, json_res)
            return json_res

        return None

    def route_path(self, from_id, to_id):
        api = self.api + "schedule_stop_pairs"
        params = {"destination_onestop_id": to_id, "origin_onestop_id": from_id}
        res = requests.get(api, params)
        if res.ok:
            return self._parse_path(res.json())

    def _parse_stops(self, json):
        return json

    def _parse_path(self, json):
        return json


if __name__ == "__main__":
    t = Transport()
    c = Coord(51.23997, 22.5515648)

    start = time.time()
    bus_info = t.get_bus_station_by_coords(c)
    print(time.time() - start)
    pprint(bus_info)
