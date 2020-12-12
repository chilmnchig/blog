from django.db import models
from django.utils import timezone

import re
import requests


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


class ContentImage(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.PROTECT)
    content_image = models.ImageField(upload_to='blog_content_images/')
