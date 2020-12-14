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


class ContentImageAdmin(admin.ModelAdmin):
    list_display = ('blog', 'content_image')


admin.site.register(Blog, BlogAdmin)
admin.site.register(ContentImage, ContentImageAdmin)
