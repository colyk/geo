from django.http import JsonResponse
from django.views.generic.base import View


class Path(View):
    def get(self, request):
        print(request)
        return JsonResponse({})
