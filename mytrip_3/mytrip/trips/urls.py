from django.urls import path

from . import views

app_name = 'trips'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('map.html', views.get_attraction, name='map'),
    path('find_routes.html', views.get_map_attraction, name='route'),
]

# path('map.html', views.get_map(), name='map')
# path('map.html', views.MapView.as_view(), name='map')
# path('', views.IndexView.as_view(), name='index'),
# path('find_routes.html', views.get_map_attraction, name='map'),