
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Game,CustomGame
from django.http import HttpResponse
from .forms import CustomGameForm, SetPriceForm


def index(request):  # Checking homepage
    items = Game.objects.all().filter(is_published=True)
    context = {
        'games' : items,
        
    }
    return render(request, 'shop/store.html', context)


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



def set_price_view(request):
    if request.method == 'POST':
        form = SetPriceForm(request.POST)
        if form.is_valid():
            price = form.cleaned_data['price']
            # Do something with the price, such as updating the database
            # For example, you could save the price to a model instance
            game.price = price
            game.save()
            return redirect('success_url')  # Redirect to a success page
    else:
        form = SetPriceForm()
    return render(request, 'set_price_form.html', {'form': form})