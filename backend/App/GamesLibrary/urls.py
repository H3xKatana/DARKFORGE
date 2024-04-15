from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('games/<int:pk>/', views.game_detail, name='game-detail'),
    path('customgame/',views.create_custom_game,name='custom_game'),
   path('admin/set-price/', views.set_price_view, name='set_price_view'),
]
