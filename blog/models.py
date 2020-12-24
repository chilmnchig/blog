from django.db import models
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from urllib.parse import urlencode

from blog.search import search_objects

import re


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'category'
        verbose_name = 'カテゴリー'
        verbose_name_plural = 'カテゴリー'
        ordering = ['name']

    def __str__(self):
        return self.name


class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)
    is_public = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.PROTECT,
                                 blank=True, null=True)
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
            redirect_url = reverse('image_upload')
            parameters = urlencode({'blog': self.id})
            url = f'{redirect_url}?{parameters}'
            return redirect(url)
        else:
            return redirect('detail', blog_id=self.id)

    def __str__(self):
        return self.title

    def sort_content(self):
        self.sort_content = re.split('<html>|</html>', self.content)

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

    @classmethod
    def delete_image(cls, request):
        image_id = request.POST.get('delete_image_id')
        image = get_object_or_404(cls, id=image_id)
        image.delete()
