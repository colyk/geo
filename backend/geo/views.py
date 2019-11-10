import json
import math
import time

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from .graph.algorithm.a_star import a_star
from .graph.graph import Graph
from .osm.fetch import OSM
from .osm.geo_types import Bbox, Coord
from .osm.geojson_tools import create_graph_from_geojson


@method_decorator(csrf_exempt, name="dispatch")
class Path(View):
    def post(self, request):
        points = json.loads(request.body.decode("utf-8")).get("points", [])
        bbox = get_bbox(points)

        osm = OSM(debug=True)
        osm_time = time.time()
        geojson = osm.fetch_by_bbox(bbox, "_pedestrian_way", ["way"])
        print(f"OSM: {time.time() - osm_time}")

        with open("test", "w") as f:
            f.write(json.dumps(geojson))

        graph_build_time = time.time()
        graph = create_graph_from_geojson(geojson)
        print(f"Build graph took {time.time() - graph_build_time}")
        print(f"Nodes count {len(graph.nodes)}")
        print(f"Edge count {len(graph.edges)}")

        find_nodes_time = time.time()
        f_coord = Coord(lat=points[0][0], lon=points[0][1])
        l_coord = Coord(lat=points[-1][0], lon=points[-1][1])
        f_node = find_nearest_node(graph, f_coord)
        l_node = find_nearest_node(graph, l_coord)
        print(f"Nodes finding took {time.time() - find_nodes_time}")
        print(f"First node {f_node}")
        print(f"Second node {l_node}")

        a_star_time = time.time()
        path = a_star(graph, f_node, l_node)
        print(f"A* took {time.time() - a_star_time}")
        if path is None:
            return JsonResponse({"path": points})

        path = [[float(round(n.lat, 7)), float(round(n.lon, 7))] for n in path]
        path.insert(0, points[0])
        path.append(points[-1])
        return JsonResponse({"path": path})


def get_bbox(data):
    min_lat = min_lon = float("inf")
    max_lat = max_lon = float("-inf")
    for point in data:
        lat = round(point[0], 7)
        lon = round(point[1], 7)
        if lon < min_lon:
            min_lon = lon
        if lon > max_lon:
            max_lon = lon

        if lat < min_lat:
            min_lat = lat
        if lat > max_lat:
            max_lat = lat

    return Bbox(min_lat, min_lon, max_lat, max_lon)


def find_nearest_node(graph: Graph, destination: Coord):
    d_lat = destination.lat
    d_lon = destination.lon
    nearest_node = None
    min_distance = float("inf")

    for node in graph.nodes:
        distance = math.sqrt((node.lat - d_lat) ** 2 + (node.lon - d_lon) ** 2)
        if distance < min_distance:
            min_distance = distance
            nearest_node = node
    return nearest_node
