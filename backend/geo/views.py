from django.http import HttpResponse, JsonResponse


def index(request):
    return JsonResponse({"1": 1})
