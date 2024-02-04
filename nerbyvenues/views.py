from django.shortcuts import render
from django.http import JsonResponse
from django.views import generic
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import fromstr
from django.contrib.gis.db.models.functions import Distance
from .models import Venue

# Create your views here.
latitude = 51.522687
longitude = -0.132855
usrLocation = Point(longitude, latitude, srid=4326)

class ExactLoc(generic.ListView):
    model = Venue
    context_object_name="venues"
    queryset = Venue.objects.annotate(distance=Distance("location", usrLocation)).order_by("distance")[0:10]
    template_name = "venues/index.html"


def get_nearest_museums(request):
    lat = request.GET.get("lat")
    lng = request.GET.get("lng")
    if not lat or not lng:
        return JsonResponse({'error': 'Missing latitude or longitude parameter'}, status=400)

    user_location = fromstr(f"POINT({lng} {lat})", srid=4326)
    museums = (
        Venue.objects.annotate(distance=Distance("location", user_location))
        .order_by("distance")[:10]
    )

    data = [
        {
            "name": museum.name,
            "address": museum.address,
            "distance": museum.distance.m,  
            "latitude": museum.location.y,
            "longitude": museum.location.x,
        }
        for museum in museums
    ]

    return JsonResponse(data, safe=False)
