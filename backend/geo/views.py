import json
import time

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic.base import View

from .graph.algorithm.dijkstra import dijkstra
from .osm.geojson_tools import create_graph_from_geojson
from .osm.fetch import OSM
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name="dispatch")
class Path(View):
    def post(self, request):
        points = json.loads(request.body.decode("utf-8")).get("points", [])
        bbox = get_bbox(points)
        osm = OSM(debug=True)
        print('Before OSM')
        geojson = osm.fetch_by_bbox(*bbox, el_type="_pedestrian_way")
        print('Before Graph')
        with open('test', 'w') as f:
            f.write(json.dumps(geojson))
        graph_build_time = time.time()
        graph = create_graph_from_geojson(geojson)
        print(f'Build graph took {time.time() - graph_build_time}')
        f_node, *_, l_node = tuple(sorted(graph.nodes, key=lambda n: n.name))
        print('Before Dijkstra')
        dijkstra_time = time.time()
        path = dijkstra(graph, f_node, l_node)
        print(f'Dijkstra took {time.time() - dijkstra_time}')

        print('After Dijkstra')
        path = [[float(round(n.y, 6)), float(round(n.x, 6))] for n in path]
        print(path)
        return JsonResponse({"path": path})


def get_bbox(data):
    min_lat = min_lon = float("+inf")
    max_lat = max_lon = float("-inf")
    for point in data:
        lon = round(point[1], 6)
        lat = round(point[0], 6)
        if lon < min_lon:
            min_lon = lon
        if lon > max_lon:
            max_lon = lon

        if lat < min_lat:
            min_lat = lat
        if lat > max_lat:
            max_lat = lat

    return min_lat, min_lon, max_lat, max_lon
