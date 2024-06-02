from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('games/<int:pk>/', views.game_detail, name='game-detail'),
     path('games/<int:game_id>/report/', views.report_game_view, name='report_game'),
    path('add-to-favorites/<int:game_id>/', views.add_to_favorites, name='add-to-favorites'),
    path('favorites/', views.favorites_list, name='favorites-list'),
    path('customgame/',views.create_custom_game,name='custom_game'),
    path('search/',views.search,name='search'),
    path('add-to-order/<int:game_id>/', views.add_to_order, name='add_to_order'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('view-order/<uuid:order_reference>/', views.view_order, name='view_order'),
    path('checkout/<uuid:order_reference>/',views.CheckOut,name='checkout'),
    path('payment-success/<uuid:order_reference>/', views.PaymentSuccessful, name='payment-success'),
    path('payment-failed/<uuid:order_reference>/', views.paymentFailed, name='payment-failed'),
    path('track-game/', views.track_game, name='track_game'),
]



