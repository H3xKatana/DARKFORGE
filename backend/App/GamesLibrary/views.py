
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Game,CustomGame
from django.http import HttpResponse
from .forms import CustomGameForm


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
            messages.success(request, 'Your custom game order has been submitted. It will be processed shortly.')
            return redirect('users:home')  # Redirect to a success URL
    else:
        form = CustomGameForm()
    return render(request, 'shop/custom_game_form.html', {'form': form})