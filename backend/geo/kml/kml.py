import json
import kml2geojson
from xml.dom.minidom import parseString
import xml.etree.ElementTree as ElementTree
from typing import List


class KML:
    def load_file(self, filename):
        kml2geojson.main.convert(filename + ".kml", ".", style_type="leaflet")
        with open(filename + ".geojson", "r", encoding="utf-8") as f:
            file = json.loads(f.read())
            with open("myplaces.geojson", "w", encoding="utf-8") as f_w:
                f_w.write(json.dumps(file, indent=4, sort_keys=True))
        with open("style.json", "r", encoding="utf-8") as f:
            file = json.loads(f.read())
            with open("style.json", "w", encoding="utf-8") as f_w:
                f_w.write(json.dumps(file, indent=4, sort_keys=True))

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


if __name__ == "__main__":
    kml = KML()
    # kml.load_file("myplaces")
    # with open("myplaces.geojson", "r", encoding="utf-8") as f:
    #     kml.geojson_to_kml(json.loads(f.read()))
    with open("../osm/data.json", "r", encoding="utf-8") as f:
        data = json.loads(f.read())
        result = kml.geojson_to_kml(data)
        print(result)
        with open("out.kml", "w", encoding="utf-8") as kml_file:
            kml_file.write(result)
