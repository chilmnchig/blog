from django.db import models
from django.utils import timezone


class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)
    is_public = models.BooleanField(default=False)

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
