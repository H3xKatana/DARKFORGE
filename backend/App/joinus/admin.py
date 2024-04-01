from django.contrib import admin
from .models import CV

# Register your models here.
@admin.register(CV)
class CVAdmin(admin.ModelAdmin):
    list_display = ('user', 'pdf', 'uploaded_at')
    list_filter = ('user', 'uploaded_at')
    