from django.contrib import admin
from .models import Asset

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin): 
    list_display = ('title', 'owner', 'file_type', 'file_size', 'status', 'created_at')
    list_filter = ('status', 'file_type')
    search_fields = ('title', 'owner__username')