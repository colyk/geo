import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic.base import View

from .osm.fetch import OSM
from .graph.utils import create_graph_from_geo_data
from .graph.algorithm.bruteforce import build_path
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name="dispatch")
class Path(View):
    def post(self, request):
        points = json.loads(request.body.decode("utf-8")).get("points", [])
        bbox = get_bbox(points)
        osm = OSM()
        osm.fetch_data_by_bbox(*bbox, el_type="_pedestrian_way")
        g = create_graph_from_geo_data(points)
        g_json = g.json()
        path_idx = build_path(g_json)[1]
        path = []
        for idx in path_idx:
            path.append(points[idx])
        return JsonResponse({"path": path})


def get_bbox(data):
    min_lat = min_lon = float("+inf")
    max_lat = max_lon = float("-inf")
    for point in data:
        lon = point[0]
        lat = point[1]
        if lon < min_lon:
            min_lon = lon
        if lon > max_lon:
            max_lon = lon

        if lat < min_lat:
            min_lat = lat
        if lat > max_lat:
            max_lat = lat

    return min_lat, min_lon, max_lat, max_lon
