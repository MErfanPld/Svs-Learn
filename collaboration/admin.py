from django.contrib import admin
from .models import CollaborationRequest

@admin.register(CollaborationRequest)
class CollaborationRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'project_type', 'created_at')
    list_filter = ('project_type', 'contact_method')
    search_fields = ('name', 'email')