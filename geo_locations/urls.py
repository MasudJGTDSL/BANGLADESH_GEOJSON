# pyrefly: ignore [missing-import]
from django.urls import path
from . import views
# from . views_geo_json import map_view

app_name = "geo_locations"

urlpatterns = [
    path("", views.index, name="index"),
    # path("map_view/", map_view, name="map_view"),
    path("get_districts/", views.get_districts, name="get_districts"),
    path("get_upazilas/", views.get_upazilas, name="get_upazilas"),
    path("get_unions/", views.get_unions, name="get_unions"),
    path("get_info/", views.get_info, name="get_info"),
    
    # Visitors List (Function Based)
    path("visitors_fb/", views.visitor_list, name="visitor_list_fb"),
    
    # Visitors List (Class Based)
    path("visitors/", views.Visitor_list.as_view(), name="visitor_list"),
]