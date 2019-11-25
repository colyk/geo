import json
import time
from math import sqrt
from typing import List

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from numba import jit, njit

from .cache import Cache
from .fetch.fetch import OSM
from .fetch.geo_types import Bbox, Coord
from .fetch.geojson_tools import create_graph_from_geojson
from .graph.algorithm.a_star import a_star
from .graph.graph import Graph


@method_decorator(csrf_exempt, name="dispatch")
class Path(View):
    def post(self, request):
        total_time = time.time()
        graph_cache = Cache(prefix="graph_cache")
        points = json.loads(request.body.decode("utf-8")).get("points", [])
        bbox = get_bbox(points)
        graph = build_graph(bbox, graph_cache)

        nodes = find_nearest_nodes(graph, points)
        if nodes[0] == nodes[-1]:
            return JsonResponse({"path": points})

        path = build_path(graph, nodes)

        if path is None:
            return JsonResponse({"path": points})

        print(f"Total time: {time.time() - total_time}")
        return JsonResponse({"path": path})


def build_path(graph, nodes):
    a_star_time = time.time()
    path = []
    for f_node, s_node in zip(nodes, nodes[1:]):
        p = a_star(graph, f_node, s_node)
        if p is not None:
            path.extend(p)
        else:
            path.append(f_node)
            path.append(s_node)
    path = [[float(round(n.lat, 7)), float(round(n.lon, 7))] for n in path]
    print(f"A* took {time.time() - a_star_time}")
    return path


def find_nearest_nodes(graph, points):
    find_nodes_time = time.time()
    coords = [Coord(lat=point[0], lon=point[1]) for point in points]
    nodes = [find_nearest_node(graph, coord) for coord in coords]
    print(f"Nodes finding took {time.time() - find_nodes_time}")
    print(f"First node {nodes[0]}")
    print(f"Last node {nodes[-1]}")
    return nodes


def build_graph(bbox, graph_cache):
    graph_from_cache_time = time.time()
    graph = get_graph_cache(graph_cache, bbox)

    if graph is None:
        osm_time = time.time()
        osm = OSM(debug=True)
        geojson = osm.fetch_by_bbox(bbox, "_pedestrian_way", ["way"])
        print(f"OSM: {time.time() - osm_time}")

        with open("test", "w") as f:
            f.write(json.dumps(geojson, indent=4))
        graph_build_time = time.time()
        graph = create_graph_from_geojson(geojson)
        s_bbox = str(bbox)
        cache_name = graph_cache.create_cache_name([s_bbox])
        graph_cache.add(cache_name, graph, format_="object")
        print(f"Build graph took {time.time() - graph_build_time}")
    else:
        print(
            f"Getting graph from cache graph took {time.time() - graph_from_cache_time}"
        )

    print(f"Nodes count {len(graph.nodes)}")
    print(f"Edge count {len(graph.edges)}")
    return graph


@jit(forceobj=True)
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


@njit(fastmath=True, cache=True)
def calc_distance(x1, x2, y1, y2):
    return sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))
