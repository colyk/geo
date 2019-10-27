import json
from typing import List


def get_bbox(data):
    min_lat = 0
    min_lon = 0
    max_lat = 0
    max_lon = 0
    for i, key in enumerate(data["features"]):
        if bool(key["properties"]) is False:
            if i == 0:
                min_lon = key["geometry"]["coordinates"][0]
                max_lon = key["geometry"]["coordinates"][0]
                min_lat = key["geometry"]["coordinates"][1]
                max_lat = key["geometry"]["coordinates"][1]
            else:
                x = key["geometry"]["coordinates"][0]
                y = key["geometry"]["coordinates"][1]
                if x < min_lon:
                    min_lon = x
                elif x > max_lon:
                    max_lon = x
                if y < min_lat:
                    min_lat = y
                elif y > max_lat:
                    max_lat = y
            # print(min_lat, min_lon, max_lat, max_lon)
    if min_lat == 0 and min_lon == 0 and max_lat == 0 and max_lon == 0:
        return None
    bbox = []
    bbox.append(min_lat)
    bbox.append(min_lon)
    bbox.append(max_lat)
    bbox.append(max_lon)
    # bbox.extend(min_lat, min_lon, max_lat, max_lon)
    return bbox


def get_extended_bbox(bbox: List[float], increase: float = 0.2):
    new_bbox = []
    increase_lat = increase * (bbox[2] - bbox[0])
    increase_lon = increase * (bbox[3] - bbox[1])
    min_lat = bbox[0] - increase_lat
    min_lon = bbox[1] - increase_lon
    max_lat = bbox[2] + increase_lat
    max_lon = bbox[3] + increase_lon
    new_bbox.append(min_lat)
    new_bbox.append(min_lon)
    new_bbox.append(max_lat)
    new_bbox.append(max_lon)
    # new_bbox.extend(min_lat, min_lon, max_lat, max_lon)
    return new_bbox


def is_data_inside_bbox(data, bbox: List[float]):
    found = False
    min_lat = bbox[0]
    min_lon = bbox[1]
    max_lat = bbox[2]
    max_lon = bbox[3]
    for i, key in enumerate(data["features"]):
        if bool(key["properties"]) is False:
            found = True
            x = key["geometry"]["coordinates"][0]
            y = key["geometry"]["coordinates"][1]
            if x < min_lon:
                return False
            elif x > max_lon:
                return False
            if y < min_lat:
                return False
            elif y > max_lat:
                return False
    if found is True:
        return True
    return None


if __name__ == "__main__":
    with open("../osm/data.json", "r", encoding="utf-8") as f:
        data = f.read()
        bbox = get_bbox(json.loads(data))
        print(bbox)
        print("debug", bbox[1], bbox[0], bbox[3], bbox[2])
        print(is_data_inside_bbox(json.loads(data), bbox))
        bbox = get_extended_bbox(bbox)
        print(bbox)
        print("debug", bbox[1], bbox[0], bbox[3], bbox[2])
        print(is_data_inside_bbox(json.loads(data), bbox))
        print(
            is_data_inside_bbox(json.loads(data), [51.2468, 22.547, 51.2481, 22.5479])
        )
