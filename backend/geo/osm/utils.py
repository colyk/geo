from typing import Dict, Union

import requests

if __package__ is None or not __package__:
    from backend.geo.osm import Coord
else:
    from . import Coord


def get_info_by_coord(coord: Coord) -> Union[Dict, None]:
    url = "https://nominatim.openstreetmap.org/reverse"
    params: Dict = {"lat": coord.lat, "lon": coord.lon, "format": "json"}
    res = requests.get(url, params)
    if res.ok:
        return res.json()  # If bad request is sent returns dict with 'error' field

    return None


def get_info(query: str) -> Union[Dict, None]:
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": query, "format": "json"}
    res = requests.get(url, params)
    if res.ok:
        return res.json()  # If bad request is sent returns dict with 'error' field

    return None


if __name__ == "__main__":
    c = Coord(51.21824, 22.4233422)
    info = get_info_by_coord(c)
    print(info)

    info = get_info("Poland, Lublin, nadbystrzycka 38a")
    print(info)
