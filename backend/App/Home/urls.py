from django.urls import path
from . import views
from GamesLibrary.views import MyGames ,favorites_list




urlpatterns=[
    path("",views.Home,name="Home_page"),
    path("404",views.unfound,name='404'),
    path('mygames/',MyGames,name='MyGames'),
    path('favs',favorites_list,name='favs')
    
]
