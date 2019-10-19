import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from .graph.utils import create_graph_from_geo_data
from .graph.algorithm.bruteforce import build_path
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name="dispatch")
class Path(View):
    def post(self, request):
        points = json.loads(request.body.decode("utf-8")).get("points", [])
        g = create_graph_from_geo_data(points)
        g_json = g.json()
        path_idx = build_path(g_json)[1]
        path = []
        for idx in path_idx:
            path.append(points[idx])
        return JsonResponse({"path": path})
