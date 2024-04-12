from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('customgame/',views.create_custom_game,name='custom_game'),
   
]