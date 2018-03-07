import sys
sys.path.insert(0, '/Users/shuting/Winter_2018/CAPP_30122/Project/Tripadvisor/mytrip/trip_recommendation/')

import attractions

from django.http import HttpResponse
from django.urls import reverse 
from django.views import generic
from django.utils import timezone
from django.shortcuts import render
from django.template import loader



from .models import Trip #, Map #, Choice,  Map,

class IndexView(generic.ListView):
    template_name = 'trip_recommendation/index.html'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return

def get_map(request):
    if request.method == 'GET':
        org = request.GET.get('origin')
        des = request.GET.get('destination')
    else:
        org = "INVALID"
        des = "INVALID"
    return render(request, 'trip_recommendation/map.html', {'org':org, 'des':des})

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
