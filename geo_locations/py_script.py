import os, django, json, sys
from tqdm import tqdm
from django.conf import settings

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BANGLADESH_GEOJSON.settings")

django.setup()

from geo_locations.models import (GeoFeatureBangladesh,
                                GeoFeatureDistrict, GeoFeatureDivision, 
                                GeoFeatureUpazila, GeoFeatureUnion,
                                GeoFeatureDistrictSmall, GeoFeatureDivisionSmall, 
                                GeoFeatureUpazilaSmall, GeoFeatureUnionSmall,
                                GeoFeatureAll_1,GeoFeatureAll_2)

def geo_json_data_process(GeoJasonPath, model_name, ADM):
    with open(GeoJasonPath, "r", encoding="utf-8") as f:
        geojson_data = json.load(f)

    for feature in tqdm(geojson_data["features"], desc="Processing feature", unit="feature"):
        model_name.objects.create(
            feature_id=feature.get("id", 0),
            name=feature["properties"].get(ADM, "Not Found"),
            geometry=feature.get("geometry", {}),
            properties=feature.get("properties", {})
        )
        
json_path = os.path.join(settings.BASE_DIR, 
                         "Bangladesh_GeoJSON_Data", 
                         "bangladesh_geojson_admALL_2_entire_bd_division_district_unions.json")

#! To run: python geo_locations/py_script.py

if __name__ == "__main__":
    geo_json_data_process(json_path, GeoFeatureAll_2, "ADM4_EN")
