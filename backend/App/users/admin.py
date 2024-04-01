from django.contrib import admin
from users.models import user

class UserAdmin(admin.ModelAdmin):
    list_display=['username','email']

# Register your models here.
admin.site.register(user,UserAdmin)