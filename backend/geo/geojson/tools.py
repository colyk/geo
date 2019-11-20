import json
from typing import List
from math import radians, cos, sin, asin, sqrt
from backend.geo.converter.converter import Converter

class GeoJSONTools:
    def get_bbox(self, data):
        min_lat = min_lon = max_lat = max_lon = 0
        for key in data["features"]:
            lon, lat = self.get_coordinates(key["geometry"]["coordinates"])
            if min_lat == min_lon == max_lat == max_lon == 0:
                min_lon = max_lon = lon
                min_lat = max_lat = lat
            else:
                if lon < min_lon:
                    min_lon = lon
                elif lon > max_lon:
                    max_lon = lon
                if lat < min_lat:
                    min_lat = lat
                elif lat > max_lat:
                    max_lat = lat
        if min_lat == min_lon == max_lat == max_lon == 0:
            return None
        return min_lat, min_lon, max_lat, max_lon

    def is_data_inside_bbox(self, data, bbox: List[float]):
        min_lat, min_lon, max_lat, max_lon = bbox
        for key in data["features"]:
            lon, lat = self.get_coordinates(key["geometry"]["coordinates"])
            if lon < min_lon or lon > max_lon or lat < min_lat or lat > max_lat:
                return False
        return True

    def get_coordinates(self, coordinates):
        lon = coordinates[0]
        if isinstance(lon, List):
            for node in coordinates:
                lon = node[0]
                lat = node[1]
        else:
            lat = coordinates[1]
        return lon, lat

    def scale_bbox(self, bbox: List[float], scale: float = 0.2):
        scale_lat = scale * (bbox[2] - bbox[0])
        scale_lon = scale * (bbox[3] - bbox[1])
        min_lat = bbox[0] - scale_lat
        min_lon = bbox[1] - scale_lon
        max_lat = bbox[2] + scale_lat
        max_lon = bbox[3] + scale_lon
        return min_lat, min_lon, max_lat, max_lon

    def haversine(self, lat1: float, lon1: float, lat2: float, lon2: float):
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
        i = nearest_lat = nearest_lon = 0
        for key in data["features"]:
            if key["geometry"]["type"] == "Point":
                lat = key["geometry"]["coordinates"][1]
                lon = key["geometry"]["coordinates"][0]
                if i == 0:
                    found = True
                    nearest_lat = lat
                    nearest_lon = lon
                else:
                    distance = self.haversine(point_lat, point_lon, lat, lon)
                    if self.haversine(point_lat, point_lon, nearest_lat, nearest_lon) > distance:
                        nearest_lat = lat
                        nearest_lon = lon
                i += 1
            elif key["geometry"]["type"] == "LineString":
                for node in key["geometry"]["coordinates"]:
                    lat = node[1]
                    lon = node[0]
                    if i == 0:
                        found = True
                        nearest_lat = lat
                        nearest_lon = lon
                    else:
                        distance = self.haversine(point_lat, point_lon, lat, lon)
                        if self.haversine(point_lat, point_lon, nearest_lat, nearest_lon) > distance:
                            nearest_lat = lat
                            nearest_lon = lon
                    i += 1
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

    def invert_way(self, way):
        way["features"][0]["geometry"]["coordinates"] = way["features"][0]["geometry"]["coordinates"][::-1]
        return way

    def select_way_part(self, way, cut_0, cut_1, chosen: bool = False):
        inner = []
        outer = []
        add = None
        i = 0
        for node in way["features"][0]["geometry"]["coordinates"]:
            # print(node)
            if (node == cut_0 or node == cut_1) and add is True:
                add = False
            if (node == cut_0 or node == cut_1) and add is None:
                add = True
            if add is None:
                outer.append(node)
            elif not add:
                outer.insert(i, node)
                i += 1
            elif add:
                inner.append(node)
        outer.append(cut_0)
        inner.append(cut_1)
        if chosen:
            way["features"][0]["geometry"]["coordinates"] = outer
        else:
            way["features"][0]["geometry"]["coordinates"] = inner
        return way


if __name__ == "__main__":
    geo = GeoJSONTools()
    converter = Converter()
    with open("../converter/way.kml", "r", encoding="utf-8") as f:
        data = converter.kml_to_geojson(f.read())
        with open("../fetch/out.json", "w", encoding="utf-8") as f_json:
            f_json.write(json.dumps(data, indent=4, sort_keys=True))
        # with open("../converter/out1.kml", "w", encoding="utf-8") as f1_kml:
        #     f1_kml.write(converter.geojson_to_kml(data))
        # print(json.dumps(data, indent=4, sort_keys=True))
        # data = geo.select_way_part(data, [21.02474222713885, 52.21099240630714], [21.04736976957647, 52.21141107009144])
        one = geo.find_the_nearest_point(data, 52.21099, 21.02474)
        two = geo.find_the_nearest_point(data, 52.21141, 21.04736)
        data = geo.select_way_part(data, one[::-1], two[::-1])
        with open("../converter/out2.kml", "w", encoding="utf-8") as f2_kml:
            f2_kml.write(converter.geojson_to_kml(data))
        # bbox = geo.get_bbox(data)
        # print(bbox)
        # print(geo.is_data_inside_bbox(data, bbox))
        # bbox = geo.scale_bbox(bbox)
        # print(bbox)
        # print(geo.is_data_inside_bbox(data, bbox))
        # print(geo.is_data_inside_bbox(data, [51.2468, 22.547, 51.2481, 22.5479]))
        # print(geo.find_the_nearest_point(data, 51.24703, 22.54887))
        # print(geo.find_ways_by_point(data, 51.24703, 22.54887))
        # print(geo.find_ways_by_point(data, 51.246355, 22.549775))
        # print(geo.find_ways_by_point(data, 51.247223, 22.549579))

