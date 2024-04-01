
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Game
from django.http import HttpResponse


def index(request):  # Checking homepage
    games = Game.objects.all().filter(is_published=True)
    context = {
        'games' : games,
        'nav' : 'store'
    }
    return render(request, 'shop/store.html', context)


def game_page(request, game_id): # Products page
    game_page = get_object_or_404(Game, pk=game_id)
    context = {
        'game_page' : game_page
    }
    return render(request, 'shop/game_page.html', context)