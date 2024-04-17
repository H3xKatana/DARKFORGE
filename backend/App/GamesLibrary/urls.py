from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('games/<int:pk>/', views.game_detail, name='game-detail'),
    path('add-to-favorites/<int:game_id>/', views.add_to_favorites, name='add-to-favorites'),
    path('favorites/', views.favorites_list, name='favorites-list'),
    path('customgame/',views.create_custom_game,name='custom_game'),
   path('search/',views.game_search,name='game_search')
]
