from django.contrib import admin
from users.models import user,Profile,Notification



class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'message', 'timestamp', 'is_read')
    list_filter = ('is_read',)
    search_fields = ('recipient__username', 'message')
    readonly_fields = ('timestamp',)  # Assuming timestamp should not be editable


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'date_joined']
    list_filter = ( 'groups', 'date_joined')
    search_fields = ['username']


admin.site.register(user,UserAdmin)
admin.site.register(Profile)
admin.site.register(Notification,NotificationAdmin)