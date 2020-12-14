from django.test import TestCase
from django.urls import reverse

from . import models


def factory_blog(**kwargs):
    d = {'title': 'ブログテスト',
         'content': 'テスト用です',
         'is_public': True,
         }
    d.update(kwargs)
    return models.Blog.objects.create(**d)


class TestList(TestCase):
    def _getTarget(self):
        return reverse('list')

    def test_get(self):
        b1 = factory_blog()
        res = self.client.get(self._getTarget())
        self.assertTemplateUsed(res, 'blog/list.html')
        self.assertEqual(len(res.context['blogs']), 1)
        self.assertEqual(res.context['blogs'][0], b1)
