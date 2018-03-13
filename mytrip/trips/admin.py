from django.contrib import admin

# Register your models here.
from .models import Trip, Url, Trip1 

admin.site.register(Trip)
admin.site.register(Url)
admin.site.register(Trip1)