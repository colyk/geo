import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from .graph.graph import Graph, Node, Edge
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
class Path(View):
    def post(self, request):
        data = json.loads(request.body)
        print(request)
        return JsonResponse(data)
