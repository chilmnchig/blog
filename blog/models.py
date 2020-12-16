from django.db import models
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect

from blog.search import search_objects

import re


class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)
    is_public = models.BooleanField(default=False)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)

    class Meta:
        db_table = 'blog'
        verbose_name = 'ブログ'
        verbose_name_plural = 'ブログ'
        ordering = ['-published_at']

    def save(self, *args, **kwargs):
        if not self.published_at and self.is_public:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def save_next(self, request):
        if 'upload' in request.POST:
            return redirect('image_upload')
        else:
            return redirect('detail', blog_id=self.id)

    def __str__(self):
        return self.title

    def sort_content(self):
        self.sort_content = re.split('<html>|</html>', self.content)
        if len(self.sort_content) % 2 == 0:
            self.sort_content.append("")

    def info_content(self):
        self.sort_content()
        parts = self.sort_content[::2]
        self.info_content = ''.join(parts)
        if len(self.info_content) > 50:
            self.info_content = self.info_content[:50] + "..."

    @classmethod
    def get_list(cls, request):
        user = request.user
        if user.is_authenticated:
            blogs = cls.objects.order_by('-published_at').all()
        else:
            blogs = cls.objects.filter(is_public=True,
                                       published_at__lte=timezone.now()
                                       ).order_by('-published_at')

        keyword = request.GET.get('keyword')
        if keyword:
            blogs = search_objects(blogs, keyword)

        return blogs

    @classmethod
    def get_detail(cls, request, blog_id):
        user = request.user
        if user.is_authenticated:
            blog = get_object_or_404(cls, id=blog_id)
        else:
            blog = get_object_or_404(cls,
                                     id=blog_id,
                                     is_public=True,
                                     published_at__lte=timezone.now())
        blog.sort_content()
        return blog


class ContentImage(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.PROTECT)
    content_image = models.ImageField(upload_to='blog_content_images/')
