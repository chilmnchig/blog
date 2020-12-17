from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from datetime import timedelta

from .testing import factory_blog


class TestSearch(TestCase):
    def _getTarget(self):
        return reverse('list')

    def test_get(self):
        b1 = factory_blog(title='12です', published_at=timezone.now())
        factory_blog(
            title='21です',
            published_at=timezone.now() - timedelta(1),
        )
        res = self.client.get(
            self._getTarget(),
            data={'keyword': '12　す'}
        )
        self.assertTemplateUsed(res, 'blog/list.html')
        self.assertEqual(len(res.context['blogs']), 1)
        self.assertEqual(res.context['blogs'][0], b1)
