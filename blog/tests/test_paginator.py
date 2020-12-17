from django.test import TestCase
from django.urls import reverse

from .testing import (factory_blog, factory_user,
                      factory_image, factory_content_image)
from blog.paginator import make_page_info


class TestMakePageInfo(TestCase):
    def test_page_2(self):
        page_info = make_page_info(2, 23)
        self.assertEqual(page_info, [2, 23, range(1, 11)])

    def test_page_near_max(self):
        page_info = make_page_info(38, 40)
        self.assertEqual(page_info, [38, 40, range(31, 41)])

    def test_page_middle(self):
        page_info = make_page_info(7, 38)
        self.assertEqual(page_info, [7, 38, range(2, 12)])

    def test_page_max_small(self):
        page_info = make_page_info(3, 8)
        self.assertEqual(page_info, [3, 8, range(1, 9)])


class TestGetPagination(TestCase):
    def _getTarget(self):
        return reverse('list')

    def test_get_pagination(self):
        for i in range(11):
            factory_blog()
        res = self.client.get(
            self._getTarget(),
            data={'page': '2'}
        )
        self.assertTemplateUsed(res, 'blog/list.html')
        self.assertEqual(len(res.context['blogs']), 5)
        self.assertEqual(res.context['page'], 2)

    def test_invalid(self):
        b1 = factory_blog()
        res1 = self.client.get(
            self._getTarget(),
            data={'page': '100'}
        )
        self.assertTemplateUsed(res1, 'blog/list.html')
        self.assertEqual(len(res1.context['blogs']), 1)
        self.assertEqual(res1.context['blogs'][0], b1)
        self.assertEqual(res1.context['page'], 1)

        res2 = self.client.get(
            self._getTarget(),
            data={'page': 'あいうえお'}
        )
        self.assertTemplateUsed(res2, 'blog/list.html')
        self.assertEqual(len(res2.context['blogs']), 1)
        self.assertEqual(res2.context['blogs'][0], b1)
        self.assertEqual(res2.context['page'], 1)


class TestPageForTwo(TestCase):
    def _getTarget(self):
        return reverse('image_list')

    def setUp(self):
        self.user = factory_user()
        self.client.force_login(self.user)

    def test_normal(self):
        b = factory_blog()
        for i in range(15):
            factory_blog(image=factory_image())
            factory_blog()
        for i in range(23):
            factory_content_image()

        res1 = self.client.get(
            self._getTarget(),
            data={'page': '1'}
        )
        self.assertTemplateUsed(res1, 'blog/image_list.html')
        self.assertEqual(len(res1.context['blogs']), 10)
        self.assertEqual(len(res1.context['content_images']), 20)
        self.assertEqual(res1.context['page'], 1)

        res2 = self.client.get(
            self._getTarget(),
            data={'page': '2'}
        )
        self.assertTemplateUsed(res2, 'blog/image_list.html')
        self.assertEqual(len(res2.context['blogs']), 5)
        self.assertEqual(len(res2.context['content_images']), 3)
        self.assertEqual(res2.context['page'], 2)

    def test_between_lte_imgs(self):
        b = factory_blog()
        for i in range(15):
            factory_blog(image=factory_image())
        for i in range(60):
            factory_content_image(blog=b)

        res = self.client.get(
            self._getTarget(),
            data={'page': '3'}
        )
        self.assertTemplateUsed(res, 'blog/image_list.html')
        self.assertEqual(res.context['blogs'], None)
        self.assertEqual(len(res.context['content_images']), 20)
        self.assertEqual(res.context['page'], 3)

    def test_between_lte_blogs(self):
        b = factory_blog()
        for i in range(35):
            factory_blog(image=factory_image())
        for i in range(10):
            factory_content_image(blog=b)

        res1 = self.client.get(
            self._getTarget(),
            data={'page': '3'}
        )
        self.assertTemplateUsed(res1, 'blog/image_list.html')
        self.assertEqual(len(res1.context['blogs']), 10)
        self.assertEqual(res1.context['content_images'], None)
        self.assertEqual(res1.context['page'], 3)

        res2 = self.client.get(
            self._getTarget(),
            data={'page': '4'}
        )
        self.assertTemplateUsed(res2, 'blog/image_list.html')
        self.assertEqual(len(res2.context['blogs']), 5)
        self.assertEqual(res2.context['content_images'], None)
        self.assertEqual(res2.context['page'], 4)

    def test_invalid(self):
        b = factory_blog()
        for i in range(15):
            factory_blog(image=factory_image())
        for i in range(23):
            factory_content_image(blog=b)

        res1 = self.client.get(
            self._getTarget(),
            data={'page': '3'}
        )
        self.assertTemplateUsed(res1, 'blog/image_list.html')
        self.assertEqual(len(res1.context['blogs']), 10)
        self.assertEqual(len(res1.context['content_images']), 20)
        self.assertEqual(res1.context['page'], 1)

        res2 = self.client.get(
            self._getTarget(),
            data={'page': 'かきくけこ'}
        )
        self.assertTemplateUsed(res2, 'blog/image_list.html')
        self.assertEqual(len(res2.context['blogs']), 10)
        self.assertEqual(len(res2.context['content_images']), 20)
        self.assertEqual(res2.context['page'], 1)
