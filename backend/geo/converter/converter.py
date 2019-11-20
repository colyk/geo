import json
import xml.etree.ElementTree as ET
from typing import Dict
from xml.dom.minidom import parseString


class XMLError(TypeError):
    def __init__(self, message=None):
        if message is None:
            message = "Invalid XML"
        super().__init__(message)


class Converter:
    def __init__(self):
        ET.register_namespace("", "http://www.opengis.net/kml/2.2")

    def geojson_to_kml(self, geojson: Dict):
        root = ET.fromstring(
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<kml xmlns="http://www.opengis.net/kml/2.2">'
            "<Document>"
            "<name>gedit kml</name>"
            "</Document>"
            "</kml>"
        )
        document = root.find("{http://www.opengis.net/kml/2.2}Document")
        for feature in geojson["features"]:
            placemark = ET.SubElement(document, "Placemark")  # type: ignore
            name = ET.SubElement(placemark, "name")
            if "name" in feature["properties"]:
                name.text = str(feature["properties"]["name"])
            ex_data = ET.SubElement(placemark, "ExtendedData")
            new_data = ET.SubElement(ex_data, "Data")
            new_data.set("name", "@id")
            if "id" in feature:
                value = ET.SubElement(new_data, "value")
                value.text = str(feature["id"])
            for data in feature["properties"]:
                new_data = ET.SubElement(ex_data, "Data")
                # print(data)
                new_data.set("name", str(data))
                value = ET.SubElement(new_data, "value")
                value.text = str(feature["properties"][data])

            if feature["geometry"]["type"] == "LineString":
                linestring = ET.SubElement(placemark, "LineString")
                coordinates = ET.SubElement(linestring, "coordinates")
                new_coordinates = ""
                for node in feature["geometry"]["coordinates"]:
                    new_coordinates += (
                        "\n\t\t\t\t\t" + str(node[0]) + "," + str(node[1]) + ",0"
                    )
                coordinates.text = str(new_coordinates + "\n\t\t\t\t")
            elif feature["geometry"]["type"] == "Point":
                point = ET.SubElement(placemark, "Point")
                coordinates = ET.SubElement(point, "coordinates")
                new_coordinates = (
                    str(feature["geometry"]["coordinates"][0])
                    + ","
                    + str(feature["geometry"]["coordinates"][1])
                    + ",0"
                )
                coordinates.text = new_coordinates

        out = parseString(ET.tostring(root))
        return out.toprettyxml()

    def kml_to_geojson(self, kml: str):
        try:
            kml_data = ET.fromstring(kml)
        except Exception:
            raise XMLError()
        geojson_data: Dict = {}
        features = geojson_data["features"] = []
        geojson_data["type"] = "FeatureCollection"
        document = kml_data.find("{http://www.opengis.net/kml/2.2}Document")
        if document is None:
            raise XMLError()

        placemarks = document.findall("{http://www.opengis.net/kml/2.2}Placemark")
        for kml_feature in placemarks:
            f_coordinates, new_feature = self._create_geojson_feature()

            point = kml_feature.find("{http://www.opengis.net/kml/2.2}Point")
            if point:
                new_feature["geometry"]["type"] = "Point"
                coordinates = point.find("{http://www.opengis.net/kml/2.2}coordinates")
                if coordinates is None:
                    raise TypeError()
                coords = coordinates.text.split(",")  # type: ignore
                f_coordinates.extend([float(coords[0]), float(coords[1])])

            way = kml_feature.find("{http://www.opengis.net/kml/2.2}LineString")
            if way:
                new_feature["geometry"]["type"] = "LineString"
                coordinates = way.find("{http://www.opengis.net/kml/2.2}coordinates")
                if coordinates is None:
                    raise TypeError()
                coords_text = coordinates.text
                if coords_text is None:
                    raise TypeError()
                coords_text = (
                    coords_text.replace("\t", "").strip("\n ").replace("\n", " ")
                )
                for node in coords_text.split(" "):
                    coord = node.split(",")
                    f_coordinates.append([float(coord[0]), float(coord[1])])

            self._parse_kml_props(kml_feature, new_feature)

            features.append(new_feature)
        return geojson_data

    def _parse_kml_props(self, kml_feature, new_feature):
        for extended_data in kml_feature.findall(
            "{http://www.opengis.net/kml/2.2}ExtendedData"
        ):
            for data in extended_data.findall("{http://www.opengis.net/kml/2.2}Data"):
                value = data.find("{http://www.opengis.net/kml/2.2}value")
                if data.attrib["name"] == "@id":
                    new_feature["id"] = str(value.text)
                else:
                    new_feature["properties"][str(data.attrib["name"])] = str(
                        value.text
                    )

    @classmethod
    def _create_geojson_feature(cls):
        new_feature = {"geometry": {}}
        coordinates = new_feature["geometry"]["coordinates"] = []
        new_feature["properties"] = {}
        new_feature["type"] = "Feature"
        return coordinates, new_feature


if __name__ == "__main__":
    converter = Converter()
    with open("../osm/data.json", "r", encoding="utf-8") as f:
        data = json.loads(f.read())
        result = converter.geojson_to_kml(data)
        print(result)

    with open("out.kml", "r", encoding="utf-8") as kml_file:
        data = converter.kml_to_geojson(kml_file.read())
        print(json.dumps(data, indent=4, sort_keys=True))
