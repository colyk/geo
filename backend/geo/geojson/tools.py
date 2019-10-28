import json
from typing import List
from math import radians, cos, sin, asin, sqrt


class GeoJSONTools:
    def get_bbox(self, data):
        min_lat = min_lon = max_lat = max_lon = 0
        for i, key in enumerate(data["features"]):
            if bool(key["properties"]) is False:
                if i == 0:
                    min_lon = key["geometry"]["coordinates"][0]
                    max_lon = key["geometry"]["coordinates"][0]
                    min_lat = key["geometry"]["coordinates"][1]
                    max_lat = key["geometry"]["coordinates"][1]
                else:
                    lon = key["geometry"]["coordinates"][0]
                    lat = key["geometry"]["coordinates"][1]
                    if lon < min_lon:
                        min_lon = lon
                    elif lon > max_lon:
                        max_lon = lon
                    if lat < min_lat:
                        min_lat = lat
                    elif lat > max_lat:
                        max_lat = lat
        if min_lat == 0 and min_lon == 0 and max_lat == 0 and max_lon == 0:
            return None
        return [min_lat, min_lon, max_lat, max_lon]

    def scale_bbox(self, bbox: List[float], increase: float = 0.2):
        increase_lat = increase * (bbox[2] - bbox[0])
        increase_lon = increase * (bbox[3] - bbox[1])
        min_lat = bbox[0] - increase_lat
        min_lon = bbox[1] - increase_lon
        max_lat = bbox[2] + increase_lat
        max_lon = bbox[3] + increase_lon
        return [min_lat, min_lon, max_lat, max_lon]

    def is_data_inside_bbox(self, data, bbox: List[float]):
        found = False
        min_lat, min_lon, max_lat, max_lon = bbox
        for i, key in enumerate(data["features"]):
            if bool(key["properties"]) is False:
                found = True
                x = key["geometry"]["coordinates"][0]
                y = key["geometry"]["coordinates"][1]
                if x < min_lon or x > max_lon or y < min_lat or y > max_lat:
                    return False
        if found:
            return True
        return None

    def haversine_formula(self, lat1: float, lon1: float, lat2: float, lon2: float):
        lat1 = radians(lat1)
        lon1 = radians(lon1)
        lat2 = radians(lat2)
        lon2 = radians(lon2)
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        return (
            6371
            * 2
            * asin(
                sqrt(sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2)
            )
        )

    def find_the_nearest_point(self, data, point_lat: float, point_lon: float):
        found = False
        nearest_lat = nearest_lon = 0
        for i, key in enumerate(data["features"]):
            if bool(key["properties"]) is False:
                lat = key["geometry"]["coordinates"][1]
                lon = key["geometry"]["coordinates"][0]
                if i == 0:
                    found = True
                    nearest_lat = lat
                    nearest_lon = lon
                    distance = self.haversine_formula(point_lat, point_lon, lat, lon)
                if self.haversine_formula(point_lat, point_lon, lat, lon) < distance:
                    nearest_lat = lat
                    nearest_lon = lon
        if found:
            return [nearest_lat, nearest_lon]

    def find_ways_by_point(self, data, lat, lon):
        ways = []
        for i, key in enumerate(data["features"]):
            if (
                key["geometry"]["type"] == "LineString"
                and [lon, lat] in key["geometry"]["coordinates"]
            ):
                ways.append(key["id"])
                # ways.append(key['properties']['name'])
        if not ways:
            return False
        return ways


if __name__ == "__main__":
    geo = GeoJSONTools()
    with open("../osm/data.json", "r", encoding="utf-8") as f:
        data = json.loads(f.read())
        bbox = geo.get_bbox(data)
        print(bbox)
        print(geo.is_data_inside_bbox(data, bbox))
        bbox = geo.scale_bbox(bbox)
        print(bbox)
        print(geo.is_data_inside_bbox(data, bbox))
        print(geo.is_data_inside_bbox(data, [51.2468, 22.547, 51.2481, 22.5479]))
        print(geo.find_the_nearest_point(data, 51.24703, 22.54887))
        print(geo.find_ways_by_point(data, 51.24703, 22.54887))
        print(geo.find_ways_by_point(data, 51.246355, 22.549775))
        print(geo.find_ways_by_point(data, 51.247223, 22.549579))
