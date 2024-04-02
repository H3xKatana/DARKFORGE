from django.contrib import admin
from users.models import user,Profile

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'date_joined', 'profile_picture']
    list_filter = ( 'groups', 'date_joined')
    search_fields = ['username']


admin.site.register(user,UserAdmin)
admin.site.register(Profile)