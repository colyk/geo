from pprint import pprint
from typing import Union, Dict

import requests


class Transport:
    def __init__(self):
        self.api = "http://transit.land/api/v1/"

    def get_bus_station_by_coords(
        self, lat: float, lon: float, radius: int = 500
    ) -> Union[Dict, None]:
        api = self.api + "stops"
        params = {"lat": lat, "lon": lon, "r": radius}
        res = requests.get(api, params)
        if res.ok:
            # "osm_way_id" is osm id of nearest pedestrian road
            return self._parse_stops(res.json())

        return None

    def route_path(self, from_id, to_id):
        api = self.api + "schedule_stop_pairs"
        params = {"destination_onestop_id": to_id, "origin_onestop_id": from_id}
        res = requests.get(api, params)
        if res.ok:
            return self._parse_path(res.json())

        return None

    def _parse_stops(self, json):
        return json

    def _parse_path(self, json):
        return json


if __name__ == "__main__":
    t = Transport()
    bus_info = t.get_bus_station_by_coords(51.23997, 22.5515647)

    pprint(bus_info)
