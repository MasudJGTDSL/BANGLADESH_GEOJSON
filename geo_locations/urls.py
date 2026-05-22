from django.urls import path
from . import views
from . views_geo_json import map_view

app_name = "geo_locations"

urlpatterns = [
    path("", views.index, name="index"),
    path("map_view/", map_view, name="map_view"),
    path("get_districts/", views.get_districts, name="get_districts"),
    path("get_upazilas/", views.get_upazilas, name="get_upazilas"),
    path("get_unions/", views.get_unions, name="get_unions"),
    path("get_info/", views.get_info, name="get_info"),
]
