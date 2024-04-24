from django.utils.safestring import mark_safe
from django.contrib import admin,messages
from django.urls import path
from django.shortcuts import render, redirect
from django.utils.translation import ngettext
from .models import Genre,Comments, Game, GamesImages,Rating,Developers,CustomGame,Platforms,FavoriteGames,Order
from .forms import SetPriceForm,EmailForm
from django.core.mail import send_mail
# Register your models here.






#Actions to use 















class GenresAdmin(admin.ModelAdmin):
    model = Genre



class PlatformsAdmin(admin.ModelAdmin):
    model = Platforms
class DevsAdmin(admin.ModelAdmin):
    model=Developers 

class GamesImagesInline(admin.TabularInline):
    model = GamesImages



class CustomGameAdmin(admin.ModelAdmin):
    list_display = ['user','title', 'price','is_recent', 'payment', 'progression', 'game_status','game_complexity','order_reference']
    actions = ['mark_payment_true', 'change_game_status','set_price','send_custom_email']
    list_filter = ('user','title','created_at','price','game_status','platform')
    
    
    def mark_payment_true(modeladmin, request, queryset):
        queryset.update(payment=True)

    def set_price(self, request, queryset):
        form = SetPriceForm(request.POST or None)
        if form.is_valid():
            price = form.cleaned_data['price']
            queryset.update(price=price)
            self.message_user(request, "Prices updated successfully.")
        else:
            self.message_user(request, "Error: Invalid form submission.", level=messages.ERROR)

    set_price.short_description = "Set Price"

    def send_custom_email(self, request, queryset):
        if 'apply' in request.POST:
            form = EmailForm(request.POST)
            if form.is_valid():
                subject = form.cleaned_data['subject']
                message = form.cleaned_data['message']
                recipients = [game.user.email for game in queryset if game.user.email]
                send_mail(subject, message, 'your@example.com', recipients)
                self.message_user(request, "Email sent successfully.")
                return
        else:
            form = EmailForm()
        return render(request, 'admin/send_custom_email_form.html', context={'form': form})

    send_custom_email.short_description = "Send Custom Email"



class GameAdmin(admin.ModelAdmin):


    
    inlines = [GamesImagesInline]
    list_display=['title','price','is_recent' ,'developer','game_status','is_published']
    list_filter = ('title','created_at','price','game_status','platforms')
    #list_filter = [RecentGameFilter, PublishedGameFilter]

    
    def display_image(self, obj):
        if obj.image:
            return mark_safe('<img src="image_uploads\pfp.jpg" width=100 height=100 />'.format(
                url=obj.image.url,
                width=100,
                height=100,
            ))
        else:
            return '(No image)'

    
class CommentAdmin(admin.ModelAdmin):
    list_display=['user','game','text','approved_comment']
    actions = ['mark_comment_as_approved', 'mark_comment_as_not_approved']

    def mark_comment_as_approved(self, request, queryset):
        queryset.update(approved_comment=True)
    mark_comment_as_approved.short_description = "Mark selected comments as approved"

    def mark_comment_as_not_approved(self, request, queryset):
        queryset.update(approved_comment=False)
    mark_comment_as_not_approved.short_description = "Mark selected comments as not approved"


class ReviewAdmin(admin.ModelAdmin):
    list_display=['user','game','rating']


class FavoriteGamesAdmin(admin.ModelAdmin):
    list_display = ('user', 'game')
    search_fields = ['user__username', 'game__name']
    list_filter = ['user']

admin.site.register(FavoriteGames, FavoriteGamesAdmin)
admin.site.register(Order)
admin.site.register(Game,GameAdmin)
admin.site.register(Platforms,PlatformsAdmin)
admin.site.register(Genre,GenresAdmin)
admin.site.register(Rating,ReviewAdmin)
admin.site.register(Developers,DevsAdmin)
admin.site.register(Comments, CommentAdmin)
admin.site.register(CustomGame,CustomGameAdmin)