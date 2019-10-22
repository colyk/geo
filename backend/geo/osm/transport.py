from pprint import pprint
from typing import Union, Dict

import requests


class Transport:
    def __init__(self):
        self.stop_api = "http://transit.land/api/v1/stops"
        self.schedule_api = "http://transit.land/api/v1/schedule_stop_pairs"

    def get_bus_station_by_coords(
        self, lat: float, lon: float, radius: int = 500
    ) -> Union[Dict, None]:
        params = {"lat": lat, "lon": lon, "r": radius}
        res = requests.get(self.stop_api, params)
        if res.ok:
            # "osm_way_id" is osm id of nearest pedestrian road
            return self._parse(res.json())

        return None

    def route_path(self, from_id, to_id):
        params = {"destination_onestop_id": to_id, "origin_onestop_id": from_id}
        res = requests.get(self.schedule_api, params)
        if res.ok:
            return self._parse(res.json())

        return None

    def _parse(self, json):
        return json


if __name__ == "__main__":
    t = Transport()
    bus_info = t.get_bus_station_by_coords(51.23997, 22.5515647)

    pprint(bus_info)
