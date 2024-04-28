
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Game,CustomGame,FavoriteGames, Genre, Platforms,Order,OrderItem
from django.http import HttpResponse,JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from .forms import CustomGameForm, SetPriceForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponseBadRequest
from django.urls import reverse
from django.db import transaction
import json
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings

def myGames(request):
    return render(request,"myGames.html")

def discoverGames(request):
    return render(request,"discoverGames.html")

def about(request):
    return render(request,"about.html")

def game(request):
    return render(request,"game.html")



def index(request):
    items = Game.objects.all()
    order = None
    
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user, is_completed=False)
    
    context = {"items": items, "order": order}
    return render(request, "shop/store.html", context)


def add_to_order(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    order, created = Order.objects.get_or_create(user=request.user, is_completed=False)
    
    # Check if the item already exists in the order
    order_item, item_created = OrderItem.objects.get_or_create(order=order, game=game)
    
    # If item already exists, increase quantity
    if not item_created:
        order_item.quantity = 1
        order_item.save()
    
    return redirect('index') 


def remove_from_cart(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id)
    item.remove_from_cart()
    return redirect('view_order', order_reference=item.order.order_reference)

def view_order(request, order_reference):
    order = get_object_or_404(Order, order_reference=order_reference)
    return render(request, 'shop/cart.html', {'order': order})





def game_detail(request, pk):
    game = get_object_or_404(Game, pk=pk)
    context = {
        'game': game,
    }
    return render(request, 'shop/game_detail.html', context)

def checkout(request):  # Checking checkout page
    
    return render(request,'store/checkout.html')






def create_custom_game(request):
    if request.method == 'POST':
        form = CustomGameForm(request.POST, request.FILES)
        if form.is_valid():
            custom_game = form.save(commit=False)
            custom_game.user = request.user  # Assuming user is authenticated
            custom_game.save()
            messages.success(request, 'Your custom game order has been submitted. It will be processed shortly.An email will be sent for the interview with our devs team')
            return redirect('users:home')  # Redirect to a success URL
    else:
        form = CustomGameForm()
    return render(request, 'shop/custom_game_form.html', {'form': form})




################
@login_required
def add_to_favorites(request, game_id):
    if request.method == 'GET':
        favorite, created = FavoriteGames.objects.get_or_create(user=request.user, game_id=game_id)
        # You can handle cases where the favorite already exists
        return HttpResponseRedirect(reverse('game-detail', args=[game_id]))
    else:
        return HttpResponseBadRequest("Invalid request method: POST requests are not allowed.")

@login_required
def favorites_list(request):
    favorites = FavoriteGames.objects.filter(user=request.user)
    return render(request, 'shop/favorites_list.html', {'favorites': favorites})


#############
def game_search(request):
    title = request.GET.get('title')
    description = request.GET.get('description')
    genres_filter = request.GET.getlist('genres')
    platforms_filter = request.GET.getlist('platforms')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    games = Game.objects.filter(is_published=True)

    if title:
        games = games.filter(title__icontains=title)

    if description:
        games = games.filter(description__icontains=description)

    if genres_filter:
        games = games.filter(genres__name__in=genres_filter)

    if platforms_filter:
        games = games.filter(platforms__name__in=platforms_filter)

    if min_price:
        games = games.filter(price__gte=float(min_price))

    if max_price:
        games = games.filter(price__lte=float(max_price))

    # Get available genres and platforms
    available_genres = Genre.objects.all()
    available_platforms = Platforms.objects.all()

    context = {
        'games': games,
        'available_genres': available_genres,
        'available_platforms': available_platforms,
        'selected_genres': genres_filter,
        'selected_platforms': platforms_filter,
        'selected_title': title,
        'selected_description': description,
        'selected_min_price': min_price,
        'selected_max_price': max_price,
    }

    return render(request, 'shop/game_search.html', context)



@login_required
def order_detail(request, order_uuid):
    order = get_object_or_404(Order, uuid=order_uuid)
    return render(request, 'shop/order_detail.html', {'order': order})






def CheckOut(request, order_reference):
    order = get_object_or_404(Order, order_reference=order_reference)

    host = request.get_host()

    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': order.total,
        'item_name': 'Order',
        'invoice': order.order_reference,
        'currency_code': 'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",
        'return_url': f"http://{host}{reverse('payment-success', kwargs={'order_reference': order_reference})}",
        'cancel_url': f"http://{host}{reverse('payment-failed', kwargs={'order_reference': order_reference})}",
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

    context = {
        'order': order,
        'paypal': paypal_payment
    }

    return render(request, 'shop/checkout.html', context)

def PaymentSuccessful(request, order_reference):
    order = get_object_or_404(Order, order_reference=order_reference)

    return render(request, 'shop/payment-success.html', {'order': order})



def paymentFailed(request, order_reference):

    order = get_object_or_404(Order, order_reference=order_reference)


    return render(request, 'store/payment-failed.html', {'order': order})

