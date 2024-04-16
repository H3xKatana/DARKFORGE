from django.contrib import admin
from .models import Chat
# Register your models here.
class ChatAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'response', 'created_at')
    search_fields = ['user__username', 'message', 'response']
    list_filter = ['created_at']

admin.site.register(Chat, ChatAdmin)