from django.urls import path
from . import views




urlpatterns=[
    path("",views.Home,name="Home_page"),
    path("404",views.unfound,name='404')
    
]
