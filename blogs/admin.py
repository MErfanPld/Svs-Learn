from django.contrib import admin
from .models import Blog, CategoryBlog

@admin.register(CategoryBlog)
class CategoryBlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'created_at', 'is_published']
    list_filter = ['category', 'is_published']
    search_fields = ['title', 'content']
