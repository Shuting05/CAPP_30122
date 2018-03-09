from django.db import models

# Create your models here.

class Trip(models.Model):
    attraction = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)  
    types = models.CharField(max_length=200, blank=True, null=True)
    place_id = models.CharField(max_length=50, blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)  
    lng = models.FloatField(blank=True, null=True)  
    reviews = models.CharField(max_length=100, blank=True, null=True)
    reviews_count = models.IntegerField(blank=True, null=True)
    
    class Meta:
        db_table = 'trip'

class Url(models.Model):
    attraction = models.CharField(max_length=100, blank=True, null=True)
    url = models.CharField(max_length=500, blank=True, null=True)
    
    class Meta:
        db_table = 'url'

