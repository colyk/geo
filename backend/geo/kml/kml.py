import json
import kml2geojson
from xml.dom.minidom import parseString
import xml.etree.ElementTree as ElementTree
from typing import List


class KML:
    def __init__(self):
        ElementTree.register_namespace("", "http://www.opengis.net/kml/2.2")

    def load_file(self, filename):
        kml2geojson.main.convert(filename + ".kml", ".", style_type="leaflet")
        # with open(filename + ".geojson", "r", encoding="utf-8") as f:
        #     file = json.loads(f.read())
        #     with open("myplaces.geojson", "w", encoding="utf-8") as f_w:
        #         f_w.write(json.dumps(file, indent=4, sort_keys=True))

    def geojson_to_kml(self, data):
        kml_string = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<kml xmlns="http://www.opengis.net/kml/2.2">'
            "<Document>"
            "<name>gedit kml</name>"
            "</Document>"
            "</kml>"
        )
        ElementTree.register_namespace("", "http://www.opengis.net/kml/2.2")
        root = ElementTree.fromstring(kml_string)
        document = root.find("{http://www.opengis.net/kml/2.2}Document")

        for feature in data["features"]:
            # print(feature["id"])
            placemark = ElementTree.SubElement(document, "Placemark")
            name = ElementTree.SubElement(placemark, "name")
            if "name" in feature["properties"]:
                name.text = str(feature["properties"]["name"])
            ex_data = ElementTree.SubElement(placemark, "ExtendedData")
            new_data = ElementTree.SubElement(ex_data, "Data")
            new_data.set("name", "@id")
            value = ElementTree.SubElement(new_data, "value")
            value.text = str(feature["id"])
            for data in feature["properties"]:
                new_data = ElementTree.SubElement(ex_data, "Data")
                # print(data)
                new_data.set("name", str(data))
                value = ElementTree.SubElement(new_data, "value")
                value.text = str(feature["properties"][data])

            if feature["geometry"]["type"] == "LineString":
                linestring = ElementTree.SubElement(placemark, "LineString")
                coordinates = ElementTree.SubElement(linestring, "coordinates")
                new_coordinates = ""
                for node in feature["geometry"]["coordinates"]:
                    new_coordinates += (
                        "\n\t\t\t\t\t" + str(node[0]) + "," + str(node[1]) + ",0"
                    )
                coordinates.text = str(new_coordinates + "\n\t\t\t\t")
            elif feature["geometry"]["type"] == "Point":
                point = ElementTree.SubElement(placemark, "Point")
                coordinates = ElementTree.SubElement(point, "coordinates")
                new_coordinates = (
                    str(feature["geometry"]["coordinates"][0])
                    + ","
                    + str(feature["geometry"]["coordinates"][1])
                    + ",0"
                )
                coordinates.text = new_coordinates

        out = parseString(ElementTree.tostring(root))
        return out.toprettyxml()

    def kml_to_geojson(self, kml_data):
        # print(ElementTree.dump(kml_data))
        geojson_data = {}
        features = geojson_data["features"] = []
        geojson_data["type"] = "FeatureCollection"
        document = kml_data.find("{http://www.opengis.net/kml/2.2}Document")

        # print(document)
        for kml_feature in document.findall("{http://www.opengis.net/kml/2.2}Placemark"):
            # ElementTree.dump(kml_feature)
            # print("\n\n\n")
            new_feature = {}
            new_feature["geometry"] = {}
            coordinates = new_feature["geometry"]["coordinates"] = []
            # new_feature["id"] = []
            new_feature["properties"] = {}
            new_feature["type"] = "Feature"

            point = kml_feature.find("{http://www.opengis.net/kml/2.2}Point")
            if point:
                new_feature["geometry"]["type"] = "Point"
                coo_text = point.find("{http://www.opengis.net/kml/2.2}coordinates")
                coo_text = coo_text.text
                coo_text = coo_text.split(",")
                # print(coo_text[0])
                coordinates.append(float(coo_text[0]))
                coordinates.append(float(coo_text[1]))

            way = kml_feature.find("{http://www.opengis.net/kml/2.2}LineString")
            if way:
                new_feature["geometry"]["type"] = "LineString"
                coo_text = way.find("{http://www.opengis.net/kml/2.2}coordinates")
                coo_text = coo_text.text
                # coo_text = coo_text.strip("\n\t")
                # coo_text = coo_text.strip("\t", "")
                coo_text = coo_text.replace("\t", "")
                coo_text = coo_text.strip("\n")
                coo_text = coo_text.replace("\n", " ")
                coo_text = coo_text.split(" ")
                for node in coo_text:
                    coo_node = node.split(",")
                    node = []
                    node.append(float(coo_node[0]))
                    node.append(float(coo_node[1]))
                    coordinates.append(node)

            for extended_data in kml_feature.findall("{http://www.opengis.net/kml/2.2}ExtendedData"):
                for data in extended_data.findall("{http://www.opengis.net/kml/2.2}Data"):
                    value = data.find("{http://www.opengis.net/kml/2.2}value")
                    if data.attrib["name"] == "@id":
                        new_feature["id"] = str(value.text)
                    else:
                        new_feature["properties"][str(data.attrib["name"])] = str(value.text)

            features.append(new_feature)
        return geojson_data


if __name__ == "__main__":
    kml = KML()
    # kml.load_file("myplaces")
    # with open("myplaces.geojson", "r", encoding="utf-8") as f:
    #     kml.geojson_to_kml(json.loads(f.read()))

    # with open("../osm/data.json", "r", encoding="utf-8") as f:
    #     data = json.loads(f.read())
    #     result = kml.geojson_to_kml(data)
    #     print(result)
    #     with open("out.kml", "w", encoding="utf-8") as kml_file:
    #         kml_file.write

    with open("out.kml", "r", encoding="utf-8") as kml_file:
        data = kml.kml_to_geojson(ElementTree.fromstring(kml_file.read()))
        print(json.dumps(data, indent=4, sort_keys=True))
