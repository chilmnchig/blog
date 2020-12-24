from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from urllib.parse import urlencode

from .testing import (factory_user, factory_blog,
                      factory_content_image, factory_image)
from blog.models import Blog, ContentImage, Category


class TestBlogAdd(TestCase):
    def _getTarget(self):
        return reverse('add')

    def setUp(self):
        self.user = factory_user(password='password')
        self.client.force_login(self.user)

    def test_get(self):
        res = self.client.get(self._getTarget())
        self.assertTemplateUsed(res, 'blog/addBlog.html')
        self.assertIn('form', res.context)

    def test_post_invalid(self):
        res = self.client.post(
            self._getTarget(),
            data={
                'content': '内容'
            }
        )
        self.assertTemplateUsed(res, 'blog/addBlog.html')
        self.assertEqual(res.context['form'].errors['title'],
                         ['このフィールドは必須です。'])

    def test_post_valid(self):
        res = self.client.post(
            self._getTarget(),
            data={
                'title': 'タイトル',
                'content': '内容',
            }
        )
        self.assertEqual(res.status_code, 302)

        self.assertEqual(Blog.objects.count(), 1)
        b = Blog.objects.first()
        self.assertEqual(b.title, 'タイトル')
        self.assertEqual(b.content, '内容')

        self.assertRedirects(res, reverse('detail', kwargs={'blog_id': b.id}))

    def test_post_valid_to_image_upload(self):
        res = self.client.post(
            self._getTarget(),
            data={
                'title': 'タイトル',
                'content': '内容',
                'upload': '保存して写真をアップロードする'
            }
        )
        self.assertEqual(res.status_code, 302)

        self.assertEqual(Blog.objects.count(), 1)
        b = Blog.objects.first()
        self.assertEqual(b.title, 'タイトル')
        self.assertEqual(b.content, '内容')

        redirect_url = reverse('image_upload')
        parameters = urlencode({'blog': b.id})
        url = f'{redirect_url}?{parameters}'
        self.assertRedirects(res, url)


class TestSignUp(TestCase):
    def _getTarget(self):
        return reverse('signup')

    def setUp(self):
        self.user = factory_user()
        self.client.force_login(self.user)

    def test_get(self):
        res = self.client.get(self._getTarget())
        self.assertTemplateUsed(res, 'blog/signup.html')
        self.assertIn('form', res.context)

    def test_post_invalid_empty(self):
        res = self.client.post(
            self._getTarget(),
            data={
                'enter_password': 'password',
                'retype_password': 'password',
            }
        )
        self.assertTemplateUsed(res, 'blog/signup.html')
        self.assertEqual(res.context['form'].errors['username'],
                         ['このフィールドは必須です。'])

    def test_post_invalid_used_username(self):
        res = self.client.post(
            self._getTarget(),
            data={
                'username': 'user1',
                'enter_password': 'password',
                'retype_password': 'password',
            }
        )
        self.assertTemplateUsed(res, 'blog/signup.html')
        self.assertEqual(res.context['form'].errors['username'],
                         ['そのユーザーネームは既に使われてあります'])

    def test_post_invalid_password_small(self):
        res = self.client.post(
            self._getTarget(),
            data={
                'username': 'user1',
                'enter_password': 'pass',
                'retype_password': 'pass',
            }
        )
        self.assertTemplateUsed(res, 'blog/signup.html')
        self.assertEqual(res.context['form'].errors['enter_password'],
                         ['パスワードは5文字以上入力してください'])

    def test_post_invalid_password_incorrespont(self):
        res = self.client.post(
            self._getTarget(),
            data={
                'username': 'user1',
                'enter_password': 'password',
                'retype_password': 'passwor',
            }
        )
        self.assertTemplateUsed(res, 'blog/signup.html')
        self.assertEqual(res.context['form'].errors['retype_password'],
                         ['上とパスワードが一致しません'])

    def test_post_valid(self):
        res = self.client.post(
            self._getTarget(),
            data={
                'username': 'user2',
                'enter_password': 'password2',
                'retype_password': 'password2',
            }
        )
        self.assertEqual(res.status_code, 302)

        self.assertEqual(User.objects.count(), 2)
        u = User.objects.get(username='user2')
        self.assertTrue(u.check_password('password2'))

        self.assertRedirects(res, reverse('list'))


class TestEditIncImage(TestCase):
    def _getTarget(self, **kwargs):
        return reverse('edit', kwargs=kwargs)

    def setUp(self):
        self.user = factory_user()
        self.client.force_login(self.user)
        b = factory_blog()
        factory_content_image(blog=b)

    def test_get(self):
        b = Blog.objects.first()
        img = ContentImage.objects.first()
        res = self.client.get(self._getTarget(blog_id=b.id))
        self.assertTemplateUsed(res, 'blog/edit.html')
        self.assertEqual(res.context['blog_id'], b.id)
        self.assertEqual(res.context['form'].instance, b)
        self.assertEqual(len(res.context['images']), 1)
        self.assertEqual(res.context['images'][0], img)
        self.assertFalse(res.context['confirm'])

    def test_post_edit_invalid(self):
        b = Blog.objects.first()
        img = ContentImage.objects.first()
        res = self.client.post(
            self._getTarget(blog_id=b.id),
            data={
                'title': '',
            }
        )
        self.assertTemplateUsed(res, 'blog/edit.html')
        self.assertEqual(res.context['blog_id'], b.id)
        self.assertEqual(res.context['form'].instance, b)
        self.assertEqual(len(res.context['images']), 1)
        self.assertEqual(res.context['images'][0], img)
        self.assertFalse(res.context['confirm'])
        self.assertEqual(res.context['form'].errors['title'],
                         ['このフィールドは必須です。'])

    def test_post_edit_valid(self):
        b = Blog.objects.first()
        res = self.client.post(
            self._getTarget(blog_id=b.id),
            data={
                'title': '変更',
                'content': '内容を変えました',
            }
        )
        self.assertEqual(res.status_code, 302)

        self.assertEqual(Blog.objects.count(), 1)
        b = Blog.objects.first()
        self.assertEqual(b.title, '変更')
        self.assertEqual(b.content, '内容を変えました')

        self.assertRedirects(res, reverse('detail', kwargs={'blog_id': b.id}))

    def test_post_delete_image(self):
        b = Blog.objects.first()
        img = ContentImage.objects.first()
        res = self.client.post(
            self._getTarget(blog_id=b.id),
            data={
                'delete_image': '画像を削除する',
                'delete_image_id': img.id,
            }
        )
        self.assertTemplateUsed(res, 'blog/edit.html')
        self.assertEqual(res.context['blog_id'], b.id)
        self.assertEqual(res.context['form'].instance, b)
        self.assertEqual(ContentImage.objects.count(), 0)
        self.assertFalse(res.context['confirm'])

    def test_post_request_delete(self):
        b = Blog.objects.first()
        img = ContentImage.objects.first()
        res = self.client.post(
            self._getTarget(blog_id=b.id),
            data={
                'delete': '削除',
            }
        )
        self.assertTemplateUsed(res, 'blog/edit.html')
        self.assertEqual(res.context['blog_id'], b.id)
        self.assertEqual(res.context['form'].instance, b)
        self.assertEqual(len(res.context['images']), 1)
        self.assertEqual(res.context['images'][0], img)
        self.assertEqual(res.context['confirm'], 'error')

    def test_post_delete_confirm(self):
        b = Blog.objects.first()
        img = ContentImage.objects.first()
        res = self.client.post(
            self._getTarget(blog_id=b.id),
            data={
                'confirmed': 'はい'
            }
        )
        self.assertTemplateUsed(res, 'blog/edit.html')
        self.assertEqual(res.context['blog_id'], b.id)
        self.assertEqual(res.context['form'].instance, b)
        self.assertEqual(len(res.context['images']), 1)
        self.assertEqual(res.context['images'][0], img)
        self.assertEqual(res.context['confirm'], 'error')


class TestEditExcImage(TestCase):
    def _getTarget(self, **kwargs):
        return reverse('edit', kwargs=kwargs)

    def setUp(self):
        self.user = factory_user()
        self.client.force_login(self.user)
        factory_blog()

    def test_get(self):
        b = Blog.objects.first()
        res = self.client.get(self._getTarget(blog_id=b.id))
        self.assertTemplateUsed(res, 'blog/edit.html')
        self.assertEqual(res.context['blog_id'], b.id)
        self.assertEqual(res.context['form'].instance, b)
        self.assertEqual(len(res.context['images']), 0)
        self.assertFalse(res.context['confirm'])

    def test_post_edit_invalid(self):
        b = Blog.objects.first()
        res = self.client.post(
            self._getTarget(blog_id=b.id),
            data={
                'title': '',
            }
        )
        self.assertTemplateUsed(res, 'blog/edit.html')
        self.assertEqual(res.context['blog_id'], b.id)
        self.assertEqual(res.context['form'].instance, b)
        self.assertEqual(len(res.context['images']), 0)
        self.assertFalse(res.context['confirm'])
        self.assertEqual(res.context['form'].errors['title'],
                         ['このフィールドは必須です。'])

    def test_post_edit_valid(self):
        b = Blog.objects.first()
        res = self.client.post(
            self._getTarget(blog_id=b.id),
            data={
                'title': '変更',
                'content': '内容を変えました',
            }
        )
        self.assertEqual(res.status_code, 302)

        self.assertEqual(Blog.objects.count(), 1)
        b = Blog.objects.first()
        self.assertEqual(b.title, '変更')
        self.assertEqual(b.content, '内容を変えました')

        self.assertRedirects(res, reverse('detail', kwargs={'blog_id': b.id}))

    def test_post_request_delete(self):
        b = Blog.objects.first()
        res = self.client.post(
            self._getTarget(blog_id=b.id),
            data={
                'delete': '削除',
            }
        )
        self.assertTemplateUsed(res, 'blog/edit.html')
        self.assertEqual(res.context['blog_id'], b.id)
        self.assertEqual(res.context['form'].instance, b)
        self.assertEqual(len(res.context['images']), 0)
        self.assertTrue(res.context['confirm'])

    def test_post_delete_confirm_no(self):
        b = Blog.objects.first()
        res = self.client.post(
            self._getTarget(blog_id=b.id),
            data={
                'confirmed': 'いいえ'
            }
        )
        self.assertTemplateUsed(res, 'blog/edit.html')
        self.assertEqual(res.context['blog_id'], b.id)
        self.assertEqual(res.context['form'].instance, b)
        self.assertEqual(len(res.context['images']), 0)
        self.assertFalse(res.context['confirm'])

    def test_post_delete_confirm_yes(self):
        b = Blog.objects.first()
        res = self.client.post(
            self._getTarget(blog_id=b.id),
            data={
                'confirmed': 'はい'
            }
        )
        self.assertEqual(Blog.objects.count(), 0)
        self.assertRedirects(res, reverse('text_list'))


class TestImageUpload(TestCase):
    def _getTarget(self):
        return reverse('image_upload')

    def setUp(self):
        self.user = factory_user()
        self.client.force_login(self.user)

    def test_get_normal(self):
        res = self.client.get(self._getTarget())
        self.assertTemplateUsed(res, 'blog/addImage.html')
        self.assertIn('form', res.context)

    def test_get_specific(self):
        b = factory_blog()
        res = self.client.get(
            self._getTarget(),
            data={
                'blog': b.id,
            }
        )
        self.assertTemplateUsed(res, 'blog/addImage.html')
        self.assertIn('form', res.context)

    def test_post_invalid(self):
        res = self.client.post(
            self._getTarget(),
            data={}
        )
        self.assertTemplateUsed(res, 'blog/addImage.html')
        self.assertEqual(res.context['form'].errors['blog'],
                         ['このフィールドは必須です。'])

    def test_post_valid(self):
        b = factory_blog()
        img = factory_image()
        res = self.client.post(
            self._getTarget(),
            data={
                'blog': b.id,
                'content_image': img,
            }
        )
        self.assertEqual(res.status_code, 302)

        self.assertEqual(ContentImage.objects.count(), 1)
        uploaded = ContentImage.objects.first()
        self.assertEqual(uploaded.blog, b)

        self.assertRedirects(res, reverse('edit', kwargs={'blog_id': b.id}))


class TestAddCategory(TestCase):
    def _getTarget(self):
        return reverse('add_category')

    def setUp(self):
        self.user = factory_user()
        self.client.force_login(self.user)

    def test_get(self):
        res = self.client.get(self._getTarget())
        self.assertTemplateUsed(res, 'blog/addCategory.html')
        self.assertIn('form', res.context)

    def test_post_invalid(self):
        res = self.client.post(
            self._getTarget(),
            data={}
        )
        self.assertTemplateUsed(res, 'blog/addCategory.html')
        self.assertEqual(res.context['form'].errors['name'],
                         ['このフィールドは必須です。'])

    def test_post_valid(self):
        res = self.client.post(
            self._getTarget(),
            data={
                'name': 'カテゴリー作成'
            }
        )
        self.assertEqual(res.status_code, 302)

        self.assertEqual(Category.objects.count(), 1)
        category = Category.objects.first()
        self.assertEqual(category.name, 'カテゴリー作成')

        self.assertRedirects(res, reverse('user_menu'))
