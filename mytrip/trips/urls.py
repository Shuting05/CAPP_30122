# Original - Shuting Chen 
from django.urls import path

from . import views

app_name = 'trips'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('find_tags.html', views.get_tags, name='tag'),
    path('find_routes.html', views.get_attractions_and_routes, name='route'),
]

