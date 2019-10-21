#!/usr/bin/env python3

import json
import overpass

api = overpass.API()


def fetch_data_by_id(area_id, ref_class, el_class, el_type, responseformat):
    query = ref_class + '(' + str(area_id) + ');\nmap_to_area;\n' + el_class + '(area)'
    selector = type_to_selector(el_type)
    if selector is None:
        return None
    query += selector + ';\n(._;>;);\nout;'
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
        "bank": '["amenity"="bank"]',
        "bus": '["route"="bus"]',
        "trolleybus": '["route"="trolleybus"]',
        "polish_city": '["name:prefix"="miasto"]',
        "highway": '[highway]',
        "underground_parking_entrance": '[amenity=parking_entrance][parking=underground]'
    }
    return type_selector_map.get(el_type, None)


if __name__ == "__main__":
    data = fetch_data_by_id(374172786, 'way', 'node', 'underground_parking_entrance', 'geojson')
    # print(json.dumps(data, indent=4, sort_keys=True))
    r = json.dumps(data, indent=4, sort_keys=True)
    with open("data.json", "w", encoding="utf-8") as f:
        f.write(r)
