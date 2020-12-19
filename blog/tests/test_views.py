from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from datetime import timedelta

from .testing import (factory_blog, factory_user,
                      factory_image, factory_content_image)


class TestBlogList(TestCase):
    def _getTarget(self):
        return reverse('list')

    def test_get(self):
        b1 = factory_blog(published_at=timezone.now())
        b2 = factory_blog(published_at=timezone.now() - timedelta(1))
        b3 = factory_blog(
            is_public=False,
            published_at=timezone.now() - timedelta(2)
        )
        res = self.client.get(self._getTarget())
        self.assertTemplateUsed(res, 'blog/list.html')
        self.assertEqual(len(res.context['blogs']), 2)
        self.assertEqual(res.context['blogs'][0], b1)
        self.assertEqual(res.context['blogs'][1], b2)


class TestBlogListLogIn(TestCase):
    def _getTarget(self):
        return reverse('list')

    def setUp(self):
        self.user = factory_user()
        self.client.force_login(self.user)

    def test_get(self):
        b1 = factory_blog(published_at=timezone.now())
        b2 = factory_blog(published_at=timezone.now() - timedelta(1))
        b3 = factory_blog(
            is_public=False,
            published_at=timezone.now() - timedelta(2)
        )
        res = self.client.get(self._getTarget())
        self.assertTemplateUsed(res, 'blog/list.html')
        self.assertEqual(len(res.context['blogs']), 3)
        self.assertEqual(res.context['blogs'][0], b1)
        self.assertEqual(res.context['blogs'][1], b2)
        self.assertEqual(res.context['blogs'][2], b3)


class TestBlogDetail(TestCase):
    def _getTarget(self, **kwargs):
        return reverse('detail', kwargs=kwargs)

    def test_get(self):
        b1 = factory_blog()
        b2 = factory_blog(is_public=False)
        res1 = self.client.get(self._getTarget(blog_id=b1.id))
        res2 = self.client.get(self._getTarget(blog_id=b2.id))
        self.assertTemplateUsed(res1, 'blog/detail.html')
        self.assertEqual(res1.context['blog'], b1)
        self.assertEqual(res2.status_code, 404)


class TestBlogDetailLogIn(TestCase):
    def _getTarget(self, **kwargs):
        return reverse('detail', kwargs=kwargs)

    def setUp(self):
        self.user = factory_user()
        self.client.force_login(self.user)

    def test_get(self):
        b1 = factory_blog(is_public=False)
        res = self.client.get(self._getTarget(blog_id=b1.id))
        self.assertTemplateUsed(res, 'blog/detail.html')
        self.assertEqual(res.context['blog'], b1)


class TestUserMenu(TestCase):
    def _getTarget(self):
        return reverse('user_menu')

    def setUp(self):
        self.user = factory_user()
        self.client.force_login(self.user)

    def test_get(self):
        res = self.client.get(self._getTarget())
        self.assertTemplateUsed(res, 'blog/userMenu.html')


class TestBlogTextList(TestCase):
    def _getTarget(self):
        return reverse('text_list')

    def setUp(self):
        self.user = factory_user()
        self.client.force_login(self.user)

    def test_get(self):
        b1 = factory_blog(published_at=timezone.now())
        b2 = factory_blog(published_at=timezone.now() - timedelta(1))
        res = self.client.get(self._getTarget())
        self.assertTemplateUsed(res, 'blog/text_list.html')
        self.assertEqual(len(res.context['blogs']), 2)
        self.assertEqual(res.context['blogs'][0], b1)
        self.assertEqual(res.context['blogs'][1], b2)


class TestImageList(TestCase):
    def _getTarget(self):
        return reverse('image_list')

    def setUp(self):
        self.user = factory_user()
        self.client.force_login(self.user)

    def test_get(self):
        b1 = factory_blog(image=factory_image(), published_at=timezone.now())
        b2 = factory_blog(published_at=timezone.now()-timedelta(1))
        b3 = factory_blog(image=factory_image(),
                          published_at=timezone.now()-timedelta(2))
        i1 = factory_content_image(blog=b1)
        i2 = factory_content_image(blog=b2)
        res = self.client.get(self._getTarget())
        self.assertTemplateUsed(res, 'blog/image_list.html')
        self.assertEqual(len(res.context['blogs']), 2)
        self.assertEqual(res.context['blogs'][0], b1)
        self.assertEqual(res.context['blogs'][1], b3)
        self.assertEqual(len(res.context['content_images']), 2)
        self.assertEqual(res.context['content_images'][0], i1)
        self.assertEqual(res.context['content_images'][1], i2)
