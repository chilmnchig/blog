from django.contrib import admin

from blog.models import Blog

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'is_public')
    ordering = ('-published_at',)
