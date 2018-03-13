# Original Codes - Shuting Chen 
import attractions_1 # This is the outside python file used for getting 
                     # latitudes and longitute
from django.http import HttpResponse
from django.urls import reverse 
from django.views import generic
from django.shortcuts import render
from django.template import loader

from .models import Trip, Url, Trip1, Reviews, Tag

class IndexView(generic.ListView):
    template_name = 'trips/index.html'

    def get_queryset(self):
        '''
        Link to the 'index.html'
        '''
        pass

def get_tags(request):
    '''
    Want to pass attractions with their key phrases under each category
    to the second page; but this is not successful 
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

    attr = Trip1.objects.filter(lat__lte=lat2, lat__gte=lat1, lng__lte=lng2, 
        lng__gte=lng1, reviews_count__gte=1000)

    c_str = ''
    attr_list = []
    attr_list_0 = []
    for a in attr:
        c_str += Reviews.objects.filter(\
            attraction=a.attraction)[0].categories.strip('[]') + ','
        attr_list_0.append(a.attraction)
        attr_list.append(a.attraction.replace('&', '').replace('â€™', '') + ', CA')
    c_list = c_str.split(',')
    for i in range(len(c_list)):
        c_list[i] = c_list[i].strip("'").strip(" '")
    c_set = set(c_list)
    c_set.remove('')

    d = {'c_set':c_set, 'a_list':attr_list, 'a_list_0':attr_list_0}
    for c in c_set:
        attr_tag = []
        for a in attr:
            attr_r = Reviews.objects.filter(attraction=a.attraction)[0]
            attr_r_tag = attr_r.tags.strip('[]').split(", ")
            a_tag = []
            for i in range(0, len(attr_r_tag) - 1):
                if i%2 == 0:
                    a_tag.append((attr_r_tag[i], attr_r_tag[i+1]))

            if c in attr_r.categories:
                for s in a_tag:
                    if c in s[0]:
                        attr_tag.append((a.attraction.replace('&', '').replace('â€™', '') \
                            + ', CA', s[1].strip("')")))
        d[c] = attr_tag

    return render(request, 'trips/find_tags.html', d)
        


def get_attractions_and_routes(request):
    '''
    Obtain the users inputs of origin and destination, list of attractions, 
    latitude and longitute of each attraction 
    Inputs:
        request: Django object 
    Returns:
        passing values to 'trips/find_routes.html'
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
        lng__gte=lng1).order_by('-reviews_count', '-rating')[:20]
    
    attr_list = []
    attr_list_0 = []
    attr_lat_lng = []
    list_urls = []
    for i in attr:
        attr_list_0.append(i.attraction)
        attr_list.append(i.attraction.replace('&', '').replace('â€™', '') + ', CA')
        attr_lat_lng.append((i.lat, i.lng))

    for i in range(0, 20):
        attr_url = Url.objects.filter(attraction=attr_list_0[i])

        if len(attr_url) != 0:
            list_urls.append((attr_list[i], attr_url[0].url))
        else:
            list_urls.append((attr_list[i], \
                "https://www.tripadvisor.com/Attractions"))

    return render(request, 'trips/find_routes.html', \
        {'org':org, 'des':des, 'list':attr_list, 'c_lat':lat_c, \
        'c_lng':lng_c, 'lat_lng':attr_lat_lng, 'urls':list_urls})
    
    