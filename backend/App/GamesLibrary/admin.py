from django.utils.safestring import mark_safe
from django.contrib import admin,messages
from django.utils.translation import ngettext
from .models import Genre,Comments, Game, GamesImages,Rating,Developers,CustomGame
# Register your models here.






#Actions to use 















class GenresAdmin(admin.ModelAdmin):
    model = Genre

class DevsAdmin(admin.ModelAdmin):
    model=Developers 

class GamesImagesInline(admin.TabularInline):
    model = GamesImages



class CustomGameAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'payment', 'progression', 'game_status','game_complexity']
    actions = ['mark_payment_true', 'change_game_status', 'set_price']
    def mark_payment_true(modeladmin, request, queryset):
        queryset.update(payment=True)


    def change_game_status(modeladmin, request, queryset):
        queryset.update(game_status='Draft')

    def set_price(self, request, queryset):
        selected = queryset.count()
        if selected == 1:
            price = request.POST.get('price')
            if price is not None:
                queryset.update(price=price)
                self.message_user(request, "Price successfully updated.")
            else:
                self.message_user(request, "Please enter a valid price.", level=messages.ERROR)
        else:
            self.message_user(request, "Please select exactly one game to set the price.", level=messages.ERROR)

    set_price.short_description = "Set price for selected game(s)"

class GameAdmin(admin.ModelAdmin):
    inlines = [GamesImagesInline]
    list_display=['title','price', 'display_image' ,'developer','game_status','is_published']
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


admin.site.register(Game,GameAdmin)
admin.site.register(Genre,GenresAdmin)
admin.site.register(Rating,ReviewAdmin)
admin.site.register(Developers,DevsAdmin)
admin.site.register(Comments, CommentAdmin)
admin.site.register(CustomGame,CustomGameAdmin)