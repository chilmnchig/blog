from django.contrib import admin

from blog.models import Blog, ContentImage


class ContentImageInline(admin.TabularInline):
    model = ContentImage
    extra = 0



class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'is_public', 'image')
    ordering = ('-published_at',)
    inlines = [
        ContentImageInline,
    ]



admin.site.register(Blog, BlogAdmin)
