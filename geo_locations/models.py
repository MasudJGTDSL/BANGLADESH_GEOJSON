from django.db import models
# from . import models_geo_json

# Create your models here.
class Divisions(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, default="")
    bn_name = models.CharField(max_length=100, blank=False, null=False, default="")
    lat = models.FloatField(blank=False, null=False, default=0)
    long = models.FloatField(blank=False, null=False, default=0)
    url = models.URLField(max_length=255, blank=True, null=True, unique=False) 
    geojson = models.IntegerField(default=0, blank=False, null=False)
    
    def __str__(self):
        return self.name

    
class Districts(models.Model):
    division = models.ForeignKey(Divisions, on_delete=models.CASCADE, related_name='district')
    name = models.CharField(max_length=100, blank=False, null=False, default="")
    bn_name = models.CharField(max_length=100, blank=False, null=False, default="")
    lat = models.FloatField(blank=False, null=False, default=0)
    long = models.FloatField(blank=False, null=False, default=0)
    url = models.URLField(max_length=255, blank=True, null=True, unique=False) 
    geojson = models.IntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return f"{self.division}, {self.name}"
    
    
class Upazilas(models.Model):
    district = models.ForeignKey(Districts, on_delete=models.CASCADE, related_name='upazila')
    name = models.CharField(max_length=100, blank=False, null=False, default="")
    bn_name = models.CharField(max_length=100, blank=False, null=False, default="")
    lat = models.FloatField(blank=False, null=False, default=0)
    long = models.FloatField(blank=False, null=False, default=0)
    url = models.URLField(max_length=255, blank=True, null=True, unique=False) 
    geojson = models.IntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return f"{self.district}, {self.name}"
    
class Unions(models.Model):
    upazila = models.ForeignKey(Upazilas, on_delete=models.CASCADE, related_name='union')
    name = models.CharField(max_length=100, blank=False, null=False, default="")
    bn_name = models.CharField(max_length=100, blank=False, null=False, default="")
    lat = models.FloatField(blank=False, null=False, default=0)
    long = models.FloatField(blank=False, null=False, default=0)
    url = models.URLField(max_length=255, blank=True, null=True, unique=False) 
    geojson = models.IntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return f"{self.upazila}, {self.name}"
    
    
class GeoFeatureDivision(models.Model):
    feature_id = models.IntegerField()
    name = models.CharField(max_length=100, blank=False, null=False, default="")
    geometry = models.JSONField()     # store the geometry dict
    properties = models.JSONField()   # store the properties dict
    created_at = models.DateTimeField(auto_now_add=True)
    perimeter_km = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    area_km2 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return self.properties.get("ADM4_EN", f"Feature {self.feature_id}")
    
    
class GeoFeatureDistrict(models.Model):
    feature_id = models.IntegerField()
    name = models.CharField(max_length=100, blank=False, null=False, default="")
    geometry = models.JSONField()     # store the geometry dict
    properties = models.JSONField()   # store the properties dict
    created_at = models.DateTimeField(auto_now_add=True)
    perimeter_km = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    area_km2 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return self.properties.get("ADM4_EN", f"Feature {self.feature_id}")
    
    
class GeoFeatureUpazila(models.Model):
    feature_id = models.IntegerField()
    name = models.CharField(max_length=100, blank=False, null=False, default="")
    geometry = models.JSONField()     # store the geometry dict
    properties = models.JSONField()   # store the properties dict
    created_at = models.DateTimeField(auto_now_add=True)
    perimeter_km = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    area_km2 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return self.properties.get("ADM4_EN", f"Feature {self.feature_id}")
    

class GeoFeatureUnion(models.Model):
    feature_id = models.IntegerField()
    name = models.CharField(max_length=100, blank=False, null=False, default="")
    geometry = models.JSONField()     # store the geometry dict
    properties = models.JSONField()   # store the properties dict
    created_at = models.DateTimeField(auto_now_add=True)
    perimeter_km = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    area_km2 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return self.properties.get("ADM4_EN", f"Feature {self.feature_id}")


# class GeoFeatureBangladesh(models.Model):
#     feature_id = models.IntegerField()
#     name = models.CharField(max_length=100, blank=False, null=False, default="")
#     geometry = models.JSONField()     # store the geometry dict
#     properties = models.JSONField()   # store the properties dict
#     created_at = models.DateTimeField(auto_now_add=True)
#     perimeter_km = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
#     area_km2 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

#     def __str__(self):
#         return self.properties.get("ADM4_EN", f"Feature {self.feature_id}")


# class GeoFeatureDivisionSmall(models.Model):
#     feature_id = models.IntegerField()
#     name = models.CharField(max_length=100, blank=False, null=False, default="")
#     geometry = models.JSONField()     # store the geometry dict
#     properties = models.JSONField()   # store the properties dict
#     created_at = models.DateTimeField(auto_now_add=True)
#     perimeter_km = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
#     area_km2 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
#     def __str__(self):
#         return self.properties.get("ADM4_EN", f"Feature {self.feature_id}")


# class GeoFeatureDistrictSmall(models.Model):
#     feature_id = models.IntegerField()
#     name = models.CharField(max_length=100, blank=False, null=False, default="")
#     geometry = models.JSONField()     # store the geometry dict
#     properties = models.JSONField()   # store the properties dict
#     created_at = models.DateTimeField(auto_now_add=True)
#     perimeter_km = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
#     area_km2 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
#     def __str__(self):
#         return self.properties.get("ADM4_EN", f"Feature {self.feature_id}")

# class GeoFeatureUpazilaSmall(models.Model):
#     feature_id = models.IntegerField()
#     name = models.CharField(max_length=100, blank=False, null=False, default="")
#     geometry = models.JSONField()     # store the geometry dict
#     properties = models.JSONField()   # store the properties dict
#     created_at = models.DateTimeField(auto_now_add=True)
#     perimeter_km = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
#     area_km2 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
#     def __str__(self):
#         return self.properties.get("ADM4_EN", f"Feature {self.feature_id}")
    
    
# class GeoFeatureUnionSmall(models.Model):
#     feature_id = models.IntegerField()
#     name = models.CharField(max_length=100, blank=False, null=False, default="")
#     geometry = models.JSONField()     # store the geometry dict
#     properties = models.JSONField()   # store the properties dict
#     created_at = models.DateTimeField(auto_now_add=True)
#     union_id = models.IntegerField(default=0, blank=False, null=False)
#     perimeter_km = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
#     area_km2 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
#     def __str__(self):
#         return self.properties.get("ADM4_EN", f"Feature {self.feature_id}")
    
    
# class GeoFeatureAll_1(models.Model):
#     feature_id = models.IntegerField()
#     name = models.CharField(max_length=100, blank=False, null=False, default="")
#     geometry = models.JSONField()     # store the geometry dict
#     properties = models.JSONField()   # store the properties dict
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.properties.get("ADM4_EN", f"Feature {self.feature_id}")
    
    
# class GeoFeatureAll_2(models.Model):
#     feature_id = models.IntegerField()
#     name = models.CharField(max_length=100, blank=False, null=False, default="")
#     geometry = models.JSONField()     # store the geometry dict
#     properties = models.JSONField()   # store the properties dict
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.properties.get("ADM4_EN", f"Feature {self.feature_id}")


# class postcodes(models.Model):
#     upazila = models.ForeignKey(Upazilas, on_delete=models.CASCADE, related_name='postcode')
#     post_office = models.CharField(max_length=100, blank=False, null=False, default="")
#     postcode = models.CharField(max_length=100, blank=False, null=False, default="")

#     def __str__(self):
#         return f"{self.upazila}, {self.post_office}-{self.postcode}"


class Visitor(models.Model):
    visitor_ip = models.GenericIPAddressField(unique=True, verbose_name="Visitor IP")
    country = models.CharField(max_length=100, blank=True, null=True)
    country_code = models.CharField(max_length=10, blank=True, null=True)
    continent = models.CharField(max_length=100, blank=True, null=True)
    continent_code = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    county = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    region_code = models.CharField(max_length=10, blank=True, null=True)
    timezone = models.CharField(max_length=50, blank=True, null=True)
    owner = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    currency = models.CharField(max_length=50, blank=True, null=True)
    languages = models.CharField(max_length=255, blank=True, null=True)
    visit_count = models.IntegerField(default=1, verbose_name="Visit Count")
    device = models.CharField(max_length=255, blank=True, null=True, verbose_name="Device")
    browser = models.CharField(max_length=255, blank=True, null=True, verbose_name="Browser")
    visit_date = models.DateTimeField(auto_now=True, verbose_name="Visit Date")

    def __str__(self):
        return f"{self.visitor_ip} ({self.country or 'Unknown'})"