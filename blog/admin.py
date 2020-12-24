from django.contrib import admin

from blog.models import Blog, ContentImage, Category


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


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)


admin.site.register(Blog, BlogAdmin)
admin.site.register(ContentImage, ContentImageAdmin)
admin.site.register(Category, CategoryAdmin)
