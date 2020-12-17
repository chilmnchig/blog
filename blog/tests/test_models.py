from django.test import TestCase

from .testing import factory_blog


class TestBlog(TestCase):
    def test_info_content(self):
        content = ''
        info_content = ''
        for i in range(100):
            content += str(i % 10)
        for i in range(50):
            info_content += str(i % 10)
        info_content += "..."
        b = factory_blog(content=content)
        b.info_content()
        self.assertEqual(b.info_content, info_content)
