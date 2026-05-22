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
    
    
class postcodes(models.Model):
    upazila = models.ForeignKey(Upazilas, on_delete=models.CASCADE, related_name='postcode')
    post_office = models.CharField(max_length=100, blank=False, null=False, default="")
    postcode = models.CharField(max_length=100, blank=False, null=False, default="")

    def __str__(self):
        return f"{self.upazila}, {self.post_office}-{self.postcode}"
    
    
class GeoFeatureBangladesh(models.Model):
    feature_id = models.IntegerField()
    name = models.CharField(max_length=100, blank=False, null=False, default="")
    geometry = models.JSONField()     # store the geometry dict
    properties = models.JSONField()   # store the properties dict
    created_at = models.DateTimeField(auto_now_add=True)
    perimeter_km = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    area_km2 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.properties.get("ADM4_EN", f"Feature {self.feature_id}")
    
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
    
    
class GeoFeatureDivisionSmall(models.Model):
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
    

class GeoFeatureDistrictSmall(models.Model):
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
    
    
class GeoFeatureUpazilaSmall(models.Model):
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
    
    
class GeoFeatureUnionSmall(models.Model):
    feature_id = models.IntegerField()
    name = models.CharField(max_length=100, blank=False, null=False, default="")
    geometry = models.JSONField()     # store the geometry dict
    properties = models.JSONField()   # store the properties dict
    created_at = models.DateTimeField(auto_now_add=True)
    union_id = models.IntegerField(default=0, blank=False, null=False)
    perimeter_km = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    area_km2 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return self.properties.get("ADM4_EN", f"Feature {self.feature_id}")
    
    
class GeoFeatureAll_1(models.Model):
    feature_id = models.IntegerField()
    name = models.CharField(max_length=100, blank=False, null=False, default="")
    geometry = models.JSONField()     # store the geometry dict
    properties = models.JSONField()   # store the properties dict
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.properties.get("ADM4_EN", f"Feature {self.feature_id}")
    
    
class GeoFeatureAll_2(models.Model):
    feature_id = models.IntegerField()
    name = models.CharField(max_length=100, blank=False, null=False, default="")
    geometry = models.JSONField()     # store the geometry dict
    properties = models.JSONField()   # store the properties dict
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.properties.get("ADM4_EN", f"Feature {self.feature_id}")