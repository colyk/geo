import json
from math import sqrt
import time
from typing import List

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from numba import jit

from .cache import Cache
from .graph.algorithm.a_star import a_star
from .graph.graph import Graph
from .osm.fetch import OSM
from .osm.geo_types import Bbox, Coord
from .osm.geojson_tools import create_graph_from_geojson


@method_decorator(csrf_exempt, name="dispatch")
class Path(View):
    def post(self, request):
        total_time = time.time()
        graph_cache = Cache(prefix="graph_cache")
        points = json.loads(request.body.decode("utf-8")).get("points", [])
        bbox = get_bbox(points)
        graph = get_graph_cache(graph_cache, bbox)

        osm = OSM(debug=True)
        osm_time = time.time()
        geojson = osm.fetch_by_bbox(bbox, "_pedestrian_way", ["way"])
        print(f"OSM: {time.time() - osm_time}")

        with open("test", "w") as f:
            f.write(json.dumps(geojson, indent=4))

        if graph is None:
            graph_build_time = time.time()
            graph = create_graph_from_geojson(geojson)
            s_bbox = str(bbox)
            cache_name = graph_cache.create_cache_name([s_bbox])
            graph_cache.add(cache_name, graph, format_="object")
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

        print(f"Total time: {time.time() - total_time}")
        return JsonResponse({"path": path})


def get_graph_cache(graph_cache, bbox):
    for cache in graph_cache.caches:
        cache_bbox = graph_cache.parse_cache_name(cache)[0]
        cache_bbox = Bbox.parse(cache_bbox)
        d = [
            Coord(lat=bbox.min_lat, lon=bbox.min_lon),
            Coord(lat=bbox.max_lat, lon=bbox.max_lon),
        ]
        if is_data_inside_bbox(d, cache_bbox):
            return graph_cache.get(cache)


@jit(forceobj=True, parallel=True)
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


@jit(forceobj=True, parallel=True)
def is_data_inside_bbox(points: List[Coord], bbox: Bbox) -> bool:
    min_lat = bbox.min_lat
    min_lon = bbox.min_lon
    max_lat = bbox.max_lat
    max_lon = bbox.max_lon
    for point in points:
        lat = point.lat
        lon = point.lon
        if lon < min_lon or lon > max_lon or lat < min_lat or lat > max_lat:
            return False
    return True


@jit(forceobj=True, parallel=True)
def find_nearest_node(graph: Graph, destination: Coord):
    d_lat = destination.lat
    d_lon = destination.lon
    nearest_node = None
    min_distance = float("inf")

    for node in graph.nodes:
        distance = calc_distance(node.lat, d_lat, node.lon, d_lon)
        if distance < min_distance:
            min_distance = distance
            nearest_node = node
    return nearest_node


@jit(fastmath=True)
def calc_distance(x1, x2, y1, y2):
    return sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))
