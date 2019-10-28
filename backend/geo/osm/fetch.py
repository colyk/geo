import json
import overpass
from typing import List, Sequence


class OSM:
    def __init__(self):
        self.api = overpass.API(timeout=60)

    def fetch_data_by_id(
        self,
        area_id: float,
        ref_class: str,
        el_type: List[Sequence[str]],
        el_classes: List[str] = ["node", "way", "relation"],
        responseformat="geojson",
    ):
        query = ref_class + "(" + str(area_id) + ");\nmap_to_area->.a;\n(\n"
        selector = self.type_to_selector(el_type)
        if selector is None:
            return None
        for el_class in el_classes:
            for val in selector:
                query += (
                    "\t" + el_class + "(area .a)(if: count_tags() > 0)" + val + ";\n"
                )
        query += ");\n(._;>;);"
        print(query)
        return self.api.get(query, responseformat=responseformat, verbosity="geom")

    def fetch_data_by_bbox(
        self,
        south: float,
        west: float,
        north: float,
        east: float,
        el_class,
        el_type,
        responseformat="geojson",
    ):
        query = (
            "way("
            + ",".join([str(south), str(west), str(north), str(east)])
            + ");\nmap_to_area->.a;\n(\n"
        )
        selector = self.type_to_selector(el_type)
        if selector is None:
            return None
        for i, val in enumerate(el_class):
            for val in selector:
                query += (
                    "\t" + el_class[i] + "(area.a)(if: count_tags() > 0)" + val + ";\n"
                )
        query += ");\n(._;>;);"
        print(query)
        return self.api.get(query, responseformat=responseformat, verbosity="geom")

    def type_to_selector(self, el_type):
        with open("types.json", "r", encoding="utf-8") as f:
            type_selector_map = json.loads(f.read())
            # with open("types.json", "w", encoding="utf-8") as f1:
            # f1.write(json.dumps(type_selector_map, indent=4, sort_keys=True))
            selector = ""
            if isinstance(el_type, List):
                for i, val in enumerate(el_type):
                    if isinstance(val, List):
                        selector += (
                            type_selector_map[el_type[i][0]][:-1]
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
    osm = OSM()
    # data = osm.fetch_data_by_id(
    #     2904797,
    #     "relation",
    #     ["way"],
    #     [["street_address", "Artura Grottgera"], "name", "building"],
    # )
    # data = fetch_data_by_bbox(
    #     51.1952, 22.5384, 51.2012, 22.5485, ["way"], "bicycle_parking"
    # )
    data = osm.fetch_data_by_id(
        2904797,
        "relation",
        [
            ["address_street", "Dolna Panny Marii"],
            ["address_housenumber", "28"],
            "building",
        ],
    )
    r = json.dumps(data, indent=4, sort_keys=True)
    print(r)
    with open("data.json", "w", encoding="utf-8") as f:
        f.write(r)
