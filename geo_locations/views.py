# pyrefly: ignore [missing-import]
from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
# pyrefly: ignore [missing-import]
from django.db.models import F, Case, When,Max, Min, Avg, Value, IntegerField, Count, CharField, TextField, JSONField
# pyrefly: ignore [missing-import]
from django.http import JsonResponse
import json
from .models import (Divisions, Districts, Upazilas, Unions,
                    GeoFeatureDistrict, GeoFeatureDivision, 
                    GeoFeatureUpazila, GeoFeatureUnion,
                    Visitor,
                    )
                    # GeoFeatureBangladesh,
                    # GeoFeatureDistrictSmall, GeoFeatureDivisionSmall, 
                    # GeoFeatureUpazilaSmall, GeoFeatureUnionSmall,
                    # GeoFeatureAll_1,GeoFeatureAll_2
from .chart import chart
from .utils import record_visitor

# Dynamic auto-migration trigger to bypass local CLI execution issues
_migrations_checked = False

def run_auto_migrations():
    global _migrations_checked
    if not _migrations_checked:
        _migrations_checked = True
        try:
            # pyrefly: ignore [missing-import]
            from django.core.management import call_command
            # Check and run database migrations
            call_command('makemigrations', 'geo_locations')
            call_command('migrate', 'geo_locations')
            print("[Auto-Migrations] Database migrated successfully.")
        except Exception as e:
            print(f"[Auto-Migrations] Failed to run migrations: {e}")

def index(request):
    run_auto_migrations()
    record_visitor(request)
    divisions = Divisions.objects.all().order_by("name")
    divisions_max_area = GeoFeatureDivision.objects.order_by("-area_km2").first()
    divisions_min_area = GeoFeatureDivision.objects.order_by("area_km2").first()
    divisions_avg_area = GeoFeatureDivision.objects.aggregate(avg_area=Avg('area_km2'))
    divisions_info = {"large_division":divisions_max_area, 
                      "small_division":divisions_min_area, 
                      "average_division":divisions_avg_area, 
                      }
    
    districts_max_area = GeoFeatureDistrict.objects.order_by("-area_km2").first()
    districts_min_area = GeoFeatureDistrict.objects.order_by("area_km2").first()
    districts_avg_area = GeoFeatureDistrict.objects.aggregate(avg_area=Avg('area_km2'))
    
    districts_info = {"large_district":districts_max_area, 
                      "small_district":districts_min_area, 
                      "average_district":districts_avg_area, 
                      }
    
    upazilas_max_area = GeoFeatureUpazila.objects.order_by("-area_km2").first()
    upazilas_min_area = GeoFeatureUpazila.objects.order_by("area_km2").first()
    upazilas_avg_area = GeoFeatureUpazila.objects.aggregate(avg_area=Avg('area_km2'))
    
    upazilas_info = {"large_upazila":upazilas_max_area, 
                      "small_upazila":upazilas_min_area, 
                      "average_upazila":upazilas_avg_area, 
                      }
    
    return render(request, 'index.html', {"divisions":divisions, 
                                          "chart_division":chart(Divisions, GeoFeatureDivision, "Divisions"),
                                          "chart_districts":chart(Districts, GeoFeatureDistrict, "Districts"),
                                          "divisions_info":divisions_info,
                                          "districts_info":districts_info,
                                          "upazilas_info":upazilas_info,
                                          })

def get_districts(request):
    division_id = request.GET.get("division_id")
    districts = Districts.objects.filter(division_id=division_id).values("id", "name").order_by("name")
    return JsonResponse(list(districts), safe=False)

def get_upazilas(request):
    district_id = request.GET.get("district_id")
    upazilas = Upazilas.objects.filter(district_id=district_id).values("id", "name").order_by("name")
    return JsonResponse(list(upazilas), safe=False)

def get_unions(request):
    upazila_id = request.GET.get("upazila_id")
    upazilas = Unions.objects.filter(upazila_id=upazila_id).values("id", "name").order_by("name")
    return JsonResponse(list(upazilas), safe=False)


id_list = ["division_id", "district_id", "upazila_id", "union_id"]

def get_selected_id(request):
    for key in id_list:
        value = request.GET.get(key)
        if value:   # Found a match
            return key, value
    return None, None

def get_info(request):
    key, value = get_selected_id(request)
    if key == "division_id":
        try:
            geojson_id = Divisions.objects.get(id=value)
            polygon_data = GeoFeatureDivision.objects.filter(feature_id = geojson_id.geojson).values()
            dict_data = {"features": [
                        {
                        "type": "Feature"}|{"geometry": polygon_data[0]["geometry"]}
                        |{"properties":polygon_data[0]["properties"]}
                        |{"area":float(polygon_data[0]["area_km2"])}
                        |{"perimeter":float(polygon_data[0]["perimeter_km"])}
                        ]}
        except:
            dict_data = None
            
        data = Divisions.objects.filter(id=value).values(
            "name","bn_name", "lat","long", "url"
            ).annotate(
                polygon_data = Value(dict_data, output_field=JSONField()),
            )
            
    elif key == "district_id":
        try:
            geojson_id = Districts.objects.get(id=value)
            polygon_data = GeoFeatureDistrict.objects.filter(feature_id = geojson_id.geojson).values()
            dict_data = {"features": [
                        {
                        "type": "Feature"}|{"geometry": polygon_data[0]["geometry"]}
                        |{"properties":polygon_data[0]["properties"]}
                        |{"area":float(polygon_data[0]["area_km2"])}
                        |{"perimeter":float(polygon_data[0]["perimeter_km"])}
                        ]}
        except:
            dict_data = None
            
        data = Districts.objects.filter(id=value).annotate(
            division_name = F("division__name"),
            division_name_bn = F("division__bn_name"),
            division_lat =  F("division__lat"),
            division_long = F("division__long"),
            division_url =  F("division__url"),
            polygon_data = Value(dict_data, output_field=JSONField()),
            ).values()
        
    elif key == "upazila_id":
        try:
            geojson_id = Upazilas.objects.get(id=value)
            polygon_data = GeoFeatureUpazila.objects.filter(feature_id = geojson_id.geojson).values()
            dict_data = {"features": [
                        {
                        "type": "Feature"}|{"geometry": polygon_data[0]["geometry"]}
                        |{"properties":polygon_data[0]["properties"]}
                        |{"area":float(polygon_data[0]["area_km2"])}
                        |{"perimeter":float(polygon_data[0]["perimeter_km"])}
                        ]}
        except:
            dict_data = None
            
        data = Upazilas.objects.filter(id=value).annotate(
            division_name =F("district__division__name"),
            division_name_bn =F("district__division__bn_name"),
            division_lat =F("district__division__lat"),
            division_long =F("district__division__long"),
            division_url =F("district__division__url"),
            
            district_name =F("district__name"),
            district_name_bn =F("district__bn_name"),
            district_lat =F("district__lat"),
            district_long =F("district__long"),
            district_url =F("district__url"),
            polygon_data = Value(dict_data, output_field=JSONField()),
            ).values()
        
    elif key == "union_id":
        try:
            geojson_id = Unions.objects.get(id=value)
            polygon_data = GeoFeatureUnion.objects.filter(feature_id = geojson_id.geojson).values()
            dict_data = {"features": [
                        {
                        "type": "Feature"}|{"geometry": polygon_data[0]["geometry"]}
                        |{"properties":polygon_data[0]["properties"]}
                        |{"area":float(polygon_data[0]["area_km2"])}
                        |{"perimeter":float(polygon_data[0]["perimeter_km"])}
                        ]}
        except:
            dict_data = False
            
        
        data = Unions.objects.filter(id=value).annotate(
            division_name = F("upazila__district__division__name"), 
            division_name_bn = F("upazila__district__division__bn_name"), 
            division_lat =  F("upazila__district__division__lat"),
            division_long = F("upazila__district__division__long"),
            division_url =  F("upazila__district__division__url"),
            
            district_name = F("upazila__district__name"),
            district_name_bn = F("upazila__district__bn_name"),
            district_lat =  F("upazila__district__lat"),
            district_long = F("upazila__district__long"),
            district_url =  F("upazila__district__url"),
            upazila_name =  F("upazila__name"), 
            upazila_name_bn =  F("upazila__bn_name"), 
            polygon_data = Value(dict_data, output_field=JSONField()),
            ).values()
    else:
        print("No matching ID found")

    return JsonResponse(list(data), safe=False)


@login_required
def visitor_list(request):
    run_auto_migrations()
    record_visitor(request)
    visitors = Visitor.objects.all().order_by("-visit_date")
    
    # Calculate metadata metrics
    total_visits = sum(v.visit_count for v in visitors)
    unique_visitors = visitors.count()
    
    # Calculate top country
    country_counts = {}
    for v in visitors:
        if v.country:
            country_counts[v.country] = country_counts.get(v.country, 0) + v.visit_count
    
    top_country = max(country_counts, key=country_counts.get) if country_counts else "None"
    
    # Get last visit timestamp
    last_visit = visitors.first().visit_date if visitors.exists() else None
    
    context = {
        "visitors": visitors,
        "total_visits": total_visits,
        "unique_visitors": unique_visitors,
        "top_country": top_country,
        "last_visit": last_visit,
    }
    return render(request, "visitor_list.html", context)

class Visitor_list(ListView):
    model = Visitor
    template_name = "visitor_list.html"
    context_object_name = "visitors"
    ordering = ["-visit_date"]
    paginate_by = 15
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        country_counts = {}
        for v in self.object_list:
            if v.country:
                country_counts[v.country] = country_counts.get(v.country, 0) + v.visit_count
        
        top_country = max(country_counts, key=country_counts.get) if country_counts else "None"
        
        context["total_visits"] = sum(v.visit_count for v in self.object_list)
        context["unique_visitors"] = self.object_list.count()
        context["top_country"] = top_country
        context["last_visit"] = self.object_list.first().visit_date if self.object_list else None
        return context