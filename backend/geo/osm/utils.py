from pprint import pprint
from typing import Dict, Union

import requests


def get_info_by_coord(lat: float, lon: float) -> Union[Dict, None]:
    url = "https://nominatim.openstreetmap.org/reverse.php"
    params = {"lat": lat, "lon": lon, "format": "json"}
    res = requests.get(url, params)
    if res.ok:
        return res.json()  # If bad request is sent returns dict with 'error' field

    return None


def get_bus_station_by_coord(lat: float, lon: float) -> Union[Dict, None]:
    url = "http://transit.land/api/v1/stops"
    params = {"lat": lat, "lon": lon}
    res = requests.get(url, params)
    if res.ok:
        return res.json()

    return None


if __name__ == "__main__":
    info = get_info_by_coord(51.21824, 22.4233422)
    bus_info = get_bus_station_by_coord(51.23997, 22.5515647)
    print(info)
    pprint(bus_info)
