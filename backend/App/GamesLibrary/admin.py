from django.utils.safestring import mark_safe
from django.contrib import admin
from .models import Genre,Comments, Game, GamesImages,Rating,Developers,CustomGame
# Register your models here.

class CustomGameAdmin(admin.ModelAdmin):
    model= CustomGame
class GenresAdmin(admin.ModelAdmin):
    model = Genre

class DevsAdmin(admin.ModelAdmin):
    model=Developers 

class GamesImagesInline(admin.TabularInline):
    model = GamesImages




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