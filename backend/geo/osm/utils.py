import json
from typing import Dict

from backend.geo.graph.graph import Node, Graph
import requests


def get_info_by_coord(lat: float, lon: float) -> Dict:
    url = "https://nominatim.openstreetmap.org/reverse.php"
    params = {'lat': lat, 'lon': lon, 'format': 'json'}
    res = requests.get(url, params)
    # print(res)
    return res.json()


def create_graph_from_geojson(geojson: Dict) -> Graph:
    g = Graph()
    for feature in geojson['features']:
        meta = feature['properties']
        name = feature['id']
        coords = feature['geometry']['coordinates']
        if isinstance(coords[0], float):
            coords = [coords]
        for coord in coords:
            print(coord, len(coords))
            n = Node(name, coord, meta)
            g.add_node(n)
    return g


if __name__ == '__main__':
    with open('export.geojson', 'r', encoding='utf-8') as f:
        content = f.read()
        geojson = json.loads(content)
        graph = create_graph_from_geojson(geojson)
        print(graph.nodes)

    info = get_info_by_coord(51.21824, 22.4233422)
    print(info)
