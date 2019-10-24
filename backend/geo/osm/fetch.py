import json
import overpass
from typing import List

api = overpass.API()


def fetch_data_by_id(area_id, ref_class, el_class, el_type, responseformat):
    query = ref_class + "(" + str(area_id) + ");\nmap_to_area->.a;\n(\n"
    selector = type_to_selector(el_type)
    if selector is None:
        return None
    for i, val in enumerate(el_class):
        for val in selector:
            query += "\t" + el_class[i] + "(area .a)" + val + ";\n"
    query += ");\n(._;>;);"
    # print(query)
    return api.get(query, responseformat=responseformat)


def fetch_data_by_bbox(south, west, north, east, el_class, el_type, responseformat):
    query = (
        "way("
        + str(south)
        + ","
        + str(west)
        + ","
        + str(north)
        + ","
        + str(east)
        + ");\nmap_to_area->.a;\n(\n"
    )
    selector = type_to_selector(el_type)
    if selector is None:
        return None
    for i, val in enumerate(el_class):
        for val in selector:
            query += "\t" + el_class[i] + "(area.a)" + val + ";\n"
    query += ");\n(._;>;);"
    print(query)
    return api.get(query, responseformat=responseformat)


def type_to_selector(el_type):
    type_selector_map = {
        "attraction": '["tourism"="attraction"]',
        "museum": '["tourism"="museum"]',
        "theatre": '["amenity"="theatre"]',
        "restaurant": '["amenity"="restaurant"]',
        "mall": '["shop"="mall"]',
        "supermarket": '["shop"="supermarket"]',
        "university": '["amenity"="university"]',
        "school": '["amenity"="school"]',
        "kindergarten": '["amenity"="kindergarten"]',
        "castle": '["historic"="castle"]',
        "catholic_place": '["denomination"="roman_catholic"]',
        "parking": '["amenity"="parking"]',
        "bicycle_parking": "[amenity=bicycle_parking]",
        "bank": '["amenity"="bank"]',
        "bus": '["route"="bus"]',
        "trolleybus": '["route"="trolleybus"]',
        "polish_city": '["name:prefix"="miasto"]',
        "highway": "[highway]",
        "underground_parking_entrance": "[amenity=parking_entrance][parking=underground]",
        "footway": "[highway=footway]",
        "pedestrian": "[highway=pedestrian]",
        "steps": "[highway=steps]",
        "path": "[highway=path]",
        "track": "[highway=track]",
        "cycleway": "[highway=cycleway]",
        "bridleway": "[highway=bridleway]",
        "motorway": "[highway=motorway]",
        "motorway_link": '[highway="motorway_link"]',
        "trunk": "[highway=trunk]",
        "trunk_link": '[highway="trunk_link"]',
        "primary": "[highway=primary]",
        "primary_link": '[highway="primary_link"]',
        "secondary": "[highway=secondary]",
        "secondary_link": '[highway="secondary_link"]',
        "tertiary": "[highway=tertiary]",
        "tertiary_link": '[highway="tertiary_link"]',
        "residential": "[highway=residential]",
        "living_street": '[highway="living_street"]',
        "service_road": "[highway=service]",
        "unclassified": "[highway=unclassified]",
        "street_address": '["addr:street"]',
        "name": "[name]",
        "building": "[building]",
        "_pedestrian_way": "footway|steps|path|track",
        "_car_way": "motorway|motorway_link|primary|primary_link|secondary|secondary_link|tertiary|tertiary_link|residential|living_street|service_road|unclassified",
    }
    selector = ""
    if isinstance(el_type, List):
        for i, val in enumerate(el_type):
            if isinstance(val, List):
                selector += (
                    type_selector_map.get(el_type[i][0])[0:-1]
                    + '="'
                    + el_type[i][1]
                    + '"]'
                )
            else:
                selector += type_selector_map.get(el_type[i])
    else:
        selector = type_selector_map.get(el_type, None)
    type_list = selector.split("|")
    if len(type_list) > 1:
        for i, val in enumerate(type_list):
            type_list[i] = type_selector_map.get(val)
    return type_list


if __name__ == "__main__":
    # data = fetch_data_by_id(574812157, 'way', 'way', 'steps', 'geojson')
    data = fetch_data_by_id(
        2904797,
        "relation",
        ["node", "way"],
        [["street_address", "Krakowskie Przedmieście"], "name", "building"],
        "geojson",
    )
    # data = fetch_data_by_bbox(51.1952, 22.5384, 51.2012, 22.5485, ['node', 'way'], 'bicycle_parking', 'geojson')
    print(json.dumps(data, indent=4, sort_keys=True))
    r = json.dumps(data, indent=4, sort_keys=True)
    with open("data.json", "w", encoding="utf-8") as f:
        f.write(r)
