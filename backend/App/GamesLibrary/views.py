
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Game,CustomGame,FavoriteGames, Genre, Platforms,Cart,CartItem
from django.http import HttpResponse
from .forms import CustomGameForm, SetPriceForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponseBadRequest
from django.urls import reverse
from django.db import transaction

def index(request):  # Checking homepage
    items = Game.objects.all().filter(is_published=True)
    context = {
        'games' : items,
        
    }
    return render(request, 'shop/store.html', context)



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

@transaction.atomic
def add_to_cart(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    
    # Get or create the cart associated with the session
    cart_id = request.session.get('cart_id')
    if cart_id:
        cart = Cart.objects.get_or_create(cart_id=cart_id)
    else:
        cart = Cart.objects.create()
        request.session['cart_id'] = cart.cart_id

    # Create the cart item
    cart_item, created = CartItem.objects.get_or_create(cart=cart, game=game)

    return redirect('cart_view')

def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    context = {
        'cart': cart,
    }
    return render(request, 'shop/cart.html', context)

