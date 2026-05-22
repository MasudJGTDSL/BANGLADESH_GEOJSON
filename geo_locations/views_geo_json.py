import os
import json
from django.shortcuts import render
from django.conf import settings

from .models import (GeoFeatureBangladesh,
                    GeoFeatureDistrict, GeoFeatureDivision, 
                    GeoFeatureUpazila, GeoFeatureUnion,
                    GeoFeatureDistrictSmall, GeoFeatureDivisionSmall, 
                    GeoFeatureUpazilaSmall, GeoFeatureUnionSmall,
                    GeoFeatureAll_1,GeoFeatureAll_2)

def map_view(request):
    # Path to your GeoJSON file
    # geojson_path = os.path.join(settings.BASE_DIR, "small_bangladesh_geojson_adm4_5160_unions_thanas.json")
    geojson_path = os.path.join(settings.BASE_DIR,"Bangladesh_GeoJSON_Data", "bangladesh_geojson_adm2_64_districts_zillas.json")

    # Load JSON file
    with open(geojson_path, "r", encoding="utf-8") as f:
        geojson_data = json.load(f)

    # Example: extract features and properties
    features = geojson_data.get("features", [])
    polygons = []
    for feature in features:
        geometry = feature.get("geometry", {})
        properties = feature.get("properties", {})
        polygons.append({
            "coordinates": geometry.get("coordinates"),
            "name": properties.get("ADM4_EN"),
            "area": properties.get("Shape_Area"),
            "length": properties.get("Shape_Leng"),
            "id": feature.get("id"),
        })

    # Pass both raw GeoJSON and parsed keys to template
    context = {
        "geojson": json.dumps(geojson_data),  # for Leaflet
        "polygons": polygons                  # for table/list display
    }
    return render(request, "map.html", context)
