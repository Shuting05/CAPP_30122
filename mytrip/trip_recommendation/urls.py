from django.urls import path

from . import views

app_name = 'trip_recommendation'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('map.html', views.get_map, name='map'),
]

# path('map.html', views.get_map(), name='map')
# path('map.html', views.MapView.as_view(), name='map')
# path('', views.IndexView.as_view(), name='index'),