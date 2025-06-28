from django.contrib import admin
from .models import Faq

# Register your models here.

@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ['title', 'body']
    