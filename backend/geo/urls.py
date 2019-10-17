from django.urls import path

from . import views

urlpatterns = [path("path", views.Path.as_view(), name="path")]
