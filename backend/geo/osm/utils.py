from typing import Dict, Union

import requests


def get_info_by_coord(lat: float, lon: float) -> Union[Dict, None]:
    url = "https://nominatim.openstreetmap.org/reverse.php"
    params: Dict = {"lat": lat, "lon": lon, "format": "json"}
    res = requests.get(url, params)
    if res.ok:
        return res.json()  # If bad request is sent returns dict with 'error' field

    return None


def get_info(query) -> Union[Dict, None]:
    url = "https://nominatim.openstreetmap.org/search/"
    params = {"q": query, "format": "json"}
    res = requests.get(url, params)
    if res.ok:
        return res.json()  # If bad request is sent returns dict with 'error' field

    return None


if __name__ == "__main__":
    info = get_info_by_coord(51.21824, 22.4233422)
    print(info)

    info = get_info("Poland, Lublin, nadbystrzycka 38a")
    print(info)
