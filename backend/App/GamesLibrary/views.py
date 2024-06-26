
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Game,CustomGame,FavoriteGames, Genre, Platforms,Order,OrderItem,MyGames,Report
from users.models import Notification
from django.http import HttpResponse,JsonResponse
from django.core.exceptions import ObjectDoesNotExist,ValidationError
from .forms import CustomGameForm, SetPriceForm,ReportForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponseBadRequest
from django.urls import reverse
from django.db import transaction
import json
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from django.db.models import Q

def index(request):
    items = Game.objects.filter(rate__gt=4)
    all_games =Game.objects.all()
    genres = Genre.objects.all()
    
    order = None
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user, is_completed=False)

    
    context = {
        "items": items,
        "order": order,
        "genres": genres,
        "all_games": all_games, 
    }

    return render(request, "shop/store.html", context)



def search(request):
    items = Game.objects.filter(rate__gt=4)
    all_games =Game.objects.all()
    genres = Genre.objects.all()
   

    # Calculate total spendings and total games owned
   
   

   
   
    active_category = request.GET.get('genre', '')
    query = request.GET.get('query', '')

    if active_category:
        items = items.filter(genres__name__icontains=active_category)

    if query:
        items = Game.objects.filter(Q(title__icontains=query) | Q(description__icontains=query), rate__gt=4)

    context = {
        
        "items": items,
       'active_category': active_category,
        "genres": genres,
    }

    return render(request, "shop/games.html", context)

@login_required
def MyGames(request):
    # Retrieve games associated with the current user
    user_games = Game.objects.filter(mygames__user=request.user)
    favorites = FavoriteGames.objects.filter(user=request.user)

    # Calculate total spendings and total games owned
   
    total_games_owned = user_games.count()

    context = {
        "items": user_games,
        "favorites": favorites,
        "total_games_owned": total_games_owned
    }
    return render(request, "users/mygames.html", context)


@login_required
def favorites_list(request):
    items =  Game.objects.filter(favoritegames__user=request.user)


    context = {
        "items": items,
        
    }
    return render(request, "users/mygames.html", context)

@login_required
def add_to_order(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    order, created = Order.objects.get_or_create(user=request.user, is_completed=False)
    
    # Check if the item already exists in the order
    order_item, item_created = OrderItem.objects.get_or_create(order=order, game=game)
    
    # If item already exists, increase quantity
    if not item_created:
        order_item.quantity = 1
        order_item.save()
    messages.success(request, 'added to Cart .')
    
    return redirect('index') 

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id)
    item.remove_from_cart()
    return redirect('view_order', order_reference=item.order.order_reference)


@login_required
def view_order(request, order_reference):
    order = get_object_or_404(Order, order_reference=order_reference)
    
    # Check if the current user is the owner of the order
    if order.user != request.user:
        return render('404.html')
    
    return render(request, 'shop/cart.html', {'order': order})





def game_detail(request, pk):
    game = get_object_or_404(Game, pk=pk)
    context = {
        'user': request.user, 
        'game': game,
    }
    return render(request, 'shop/game_detail.html', context)

def checkout(request):  # Checking checkout page
    
    return render(request,'store/checkout.html')

##################################################
@login_required
def create_custom_game(request):
    if request.method == 'POST':
        form = CustomGameForm(request.POST, request.FILES)
        if form.is_valid():
            custom_game = form.save(commit=False)
            custom_game.user = request.user  # Assuming user is authenticated
            custom_game.save()

            # Send email to the user
            subject = 'Your Custom Game Order'
            html_message = render_to_string('email/custom_game_email.html', {'custom_game': custom_game})
            plain_message = strip_tags(html_message)
            from_email = 'your@example.com'  # Update with your email address
            to_email = custom_game.user.email

            # Create message container - the correct MIME type is multipart/alternative.
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = from_email
            msg['To'] = to_email

            # Create the body of the message (a plain-text and an HTML version).
            text_part = MIMEText(plain_message, 'plain')
            html_part = MIMEText(html_message, 'html')

            # Attach parts into message container.
            msg.attach(text_part)
            msg.attach(html_part)

            # Send the message via the debugging server.
            with smtplib.SMTP('localhost', 1025) as server:
                server.sendmail(from_email, to_email, msg.as_string())

            messages.success(request, 'Your custom game order has been submitted. It will be processed shortly. An email has been sent to you with the details.')
            
            return redirect('users:home')  # Redirect to a success URL
    else:
        form = CustomGameForm()
    return render(request, 'shop/custom_game_form.html', {'form': form})


@login_required
def track_game(request):
    if request.method == 'POST':
        order_reference = request.POST.get('order_reference')
        try:
            user_custom_games = CustomGame.objects.filter(user=request.user)
            custom_game = get_object_or_404(CustomGame, order_reference=order_reference)
            return render(request, 'shop/track_game.html', {'custom_game': custom_game,'user_custom_games': user_custom_games})
        except ValidationError:
            # If the order reference is not a valid UUID, render a 404 error page
            return render(request, 'shop/track_game.html', {'custom_game': '404','user_custom_games': user_custom_games})
    else:
        # Retrieve custom game order references of the current user
        user_custom_games = CustomGame.objects.filter(user=request.user)
        return render(request, 'shop/track_game.html', {'user_custom_games': user_custom_games})

################
@login_required
def add_to_favorites(request, game_id):
    if request.method == 'GET':
        # Check if the game exists
        try:
            game = Game.objects.get(pk=game_id)
        except Game.DoesNotExist:
           
            return HttpResponseBadRequest("Game does not exist.")
        
        # Check if the game is already a favorite for the user
        if FavoriteGames.objects.filter(user=request.user, game=game).exists():
            messages.success(request, 'aleardy in favs')
            return HttpResponseRedirect(reverse('game-detail', args=[game_id]))
        
        # Add the game to favorites
        favorite = FavoriteGames.objects.create(user=request.user)
        favorite.save()


        
        
        noti = Notification.objects.create(recipient=request.user,message = f'new favorite game{game.title}',title='new favorite ')
        noti.save()
       
        return HttpResponseRedirect(reverse('game-detail', args=[game_id]))
    else:
        return HttpResponseBadRequest("Invalid request method: POST requests are not allowed.")

@login_required
def rm_from_favorites(request, game_id):
    if request.method == 'GET':
        try:
            game = Game.objects.get(pk=game_id)
        except Game.DoesNotExist:
            return HttpResponseBadRequest("Game does not exist.")

        # Check if the game is already a favorite for the user
        if FavoriteGames.objects.filter(user=request.user, game=game).exists():
            favorite = FavoriteGames.objects.get(user=request.user, game=game)
            favorite.delete()
            messages.success(request, 'Game removed from favorites')
        else:
            # Handle the case where the game is not already a favorite
            messages.warning(request, 'Game is not currently in your favorites')

        return HttpResponseRedirect(reverse('game-detail', args=[game_id]))
    else:
        return HttpResponseBadRequest("Invalid request method: Only POST requests allowed.")




#############

@login_required
def order_detail(request, order_uuid):
    order = get_object_or_404(Order, uuid=order_uuid)
    return render(request, 'shop/order_detail.html', {'order': order})





@login_required
def CheckOut(request, order_reference):
    order = get_object_or_404(Order, order_reference=order_reference)
    full_price = order.total
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
        'total':full_price,
        'paypal': paypal_payment
    }

    return render(request, 'shop/checkout.html', context)

@login_required
def PaymentSuccessful(request, order_reference):
    order = get_object_or_404(Order, order_reference=order_reference)
    
    return render(request, 'shop/payment-success.html', {'order': order})
@login_required
def paymentFailed(request, order_reference):

    order = get_object_or_404(Order, order_reference=order_reference)


    return render(request, 'store/payment-failed.html', {'order': order})



@login_required
def report_game_view(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.game = game
            report.reported_by = request.user
            report.save()
            messages.success(request, 'Your report has been submitted.')
            return redirect('game-detail', pk=game_id)
    else:
        form = ReportForm()

    return render(request, 'report_game.html', {'form': form, 'game': game})