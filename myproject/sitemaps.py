from django.contrib.sitemaps import Sitemap
from django.utils import timezone
from django.urls import reverse

from blog.models import Blog


class BlogPostSitemap(Sitemap):
    """
    ブログ記事のサイトマップ
    """
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Blog.objects.filter(is_public=True,
                                   published_at__lte=timezone.now()
                                   ).order_by('-published_at')

    # モデルに get_absolute_url() が定義されている場合は不要
    def location(self, blog):
        return reverse('detail', args=[blog.id])

    def lastmod(self, blog):
        return blog.published_at


class StaticViewSitemap(Sitemap):
    """
    静的ページのサイトマップ
    """
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return ['list']

    def location(self, item):
        return reverse(item)
