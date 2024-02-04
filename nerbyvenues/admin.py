from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Venue
# Register your models here.

@admin.register(Venue)
class VenueAdmin(OSMGeoAdmin):
    list_display = ('name', 'location')