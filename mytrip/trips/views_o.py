# Original - Shuting Chen 
import attractions_1 # This is the outside python file used for getting 
                     # latitudes and longitute
from django.http import HttpResponse
from django.urls import reverse 
from django.views import generic
from django.shortcuts import render
from django.template import loader



from .models import Trip, Url, Trip1

class IndexView(generic.ListView):
    template_name = 'trips/index.html'

    def get_queryset(self):
        '''
        Link to the 'index.html'
        '''
        pass

def get_map_attraction(request):
    '''
    Obtain the users inputs of origin and destination, list of attractions, 
    latitude and longitute of each attraction 
    Inputs:
        request: Django object 
    '''
    if request.method == 'GET':
        org = request.GET.get('origin')
        des = request.GET.get('destination')
    else:
        org = "INVALID"
        des = "INVALID"

    loc1, loc2 = attractions_1.determine_region(org, des)

    lat1 = min(loc1['lat'], loc2['lat'])
    lat2 = max(loc1['lat'], loc2['lat'])
    lng1 = min(loc1['lng'], loc2['lng'])
    lng2 = max(loc1['lng'], loc2['lng'])
    lat_c = (loc1['lat'] + loc2['lat']) / 2
    lng_c = (loc1['lng'] + loc2['lng']) / 2

    attr = Trip1.objects.filter(lat__lte=lat2, lat__gte=lat1, lng__lte=lng2, 
        lng__gte=lng1).order_by('-reviews_count', '-rating')[:21]
    
    attr_list = []
    attr_list_0 = []
    attr_lat_lng = []
    list_urls = []
    for i in attr:
        attr_list_0.append(i.attraction)
        attr_list.append(i.attraction.replace('&', '') + ', CA')
        attr_lat_lng.append((i.lat, i.lng))

    for i in range(0, 21):
        attr_url = Url.objects.filter(attraction=attr_list_0[i])

        if len(attr_url) != 0:
            list_urls.append((attr_list[i], attr_url[0].url))
        else:
            list_urls.append((attr_list[i], \
                "https://www.tripadvisor.com/Attractions"))

    return render(request, 'trips/find_routes.html', \
        {'org':org, 'des':des, 'list':attr_list, 'c_lat':lat_c, \
        'c_lng':lng_c, 'lat_lng':attr_lat_lng, 'urls':list_urls})
