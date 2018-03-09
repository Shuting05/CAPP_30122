import sys
sys.path.insert(0, '/Users/shuting/Winter_2018/CAPP_30122/Project/Tripadvisor/mytrip/trips/')
#Users/shuting/Winter_2018/CAPP_30122
import attractions_1

from django.http import HttpResponse
from django.urls import reverse 
from django.views import generic
from django.utils import timezone
from django.shortcuts import render
from django.template import loader



from .models import Trip #, Map #, Choice,  Map,

class IndexView(generic.ListView):
    template_name = 'trips/index.html'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        pass

def get_map_attraction(request):
    if request.method == 'GET':
        org = request.GET.get('origin')
        des = request.GET.get('destination')
    else:
        org = "INVALID"
        des = "INVALID"

    #factory = attractions.Factory()
    loc1, loc2 = attractions_1.determine_region(org, des)

    lat1 = min(loc1['lat'], loc2['lat'])
    lat2 = max(loc1['lat'], loc2['lat'])
    lng1 = min(loc1['lng'], loc2['lng'])
    lng2 = max(loc1['lng'], loc2['lng'])
    lat_c = (loc1['lat'] + loc2['lat']) / 2
    lng_c = (loc1['lng'] + loc2['lng']) / 2

    attr = Trip.objects.filter(lat__lte=lat2, lat__gte=lat1, lng__lte=lng2, 
        lng__gte=lng1).order_by('-rating', '-reviews_count')[:20]
    
    attr_list = []
    attr_lat_lng = []
    for i in attr:
        attr_list.append(i.attraction.replace('&', '') + ', CA')
        attr_lat_lng.append((i.lat, i.lng))

        # attr_list.append(i.attraction.replace('&', '') + ' ca')
    return render(request, 'trips/find_routes.html', \
        {'org':org, 'des':des, 'list':attr_list, 'c_lat':lat_c, \
        'c_lng':lng_c, 'lat_lng':attr_lat_lng})

def get_attraction(request):
    return render(request, 'trips/map.html')
    # for i in range(0, 20):
    #     d[i] = attr_0[i].attraction

    #print(attr_0[0].attraction)
    
    # return render(request, 'trip_recommendation/map.html', {'org':org, 'des':des})

# def get_attraction(request):
#     if request.method == 'GET':
#         org = request.GET.get('origin')
#         des = request.GET.get('destination')
#     else:
#         org = "INVALID"
#         des = "INVALID"

    

# class MapView(generic.ListView):
#     template_name = 'trip_recommendation/map.html'
#     attraction = set()

#     def get_queryset(self):
#         template = loader.get_template('trip_recommendation/map.html')
#         context = {'org':'Chicago', 'des':'Los Angeles'}
#         print(self.request)
#         print("Printing template:")
#         print(template.render(context, self.request))
#         print(template.render(context, self.request).__class__)
#         print("Printing HttpResponse:")
#         print(HttpResponse(template.render(context, self.request)).content)
#         print(dir(HttpResponse(template.render(context, self.request))))
#         return HttpResponse(template.render(context, self.request))
#         orgin = 0
#         desti = 0
#         if self.request.method == 'GET':
#             orgin = self.request.GET['origin']
#             desti = self.request.GET['destination']
#         print("JHDKJFSJDHFJKSDHFKHSDKJF")
#         print(orgin, desti)
#         return render(self.request, 'trip_recommendation/map.html', context = {'org':orgin, 'des':desti})
    
    # def get_attraction(self):
    #     orgin = 0
    #     desti = 0
    #     if self.request.method == 'GET':
    #         orgin = self.request.GET.get('Origin')
    #         desti = self.request.GET.get('Destination')
    #         lat1 = 
    #         lng1 = 
    #         lat2 = 
    #         lng2 = 
    #         Trip.objects.filter()

# class MapView(generic.ListView):
#     template_name = 'trip_recommendation/map.html'

#     def get_queryset(self):
#         API = 'AIzaSyAOskXNHkasGvENKEVD-P1SkHUllCfn4ho'
#         o = self.request.GET.get('Origin')
#         d = self.request.GET.get('Destination')

#         return [API, o, d] 
