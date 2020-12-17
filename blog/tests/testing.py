from django.contrib.auth.models import User

from django.core.files.uploadedfile import SimpleUploadedFile

import blog.models


def factory_blog(**kwargs):
    d = {
        'title': 'ブログテスト',
        'content': 'テスト用です',
        'is_public': True,
    }
    d.update(kwargs)
    return blog.models.Blog.objects.create(**d)


def factory_user(**kwargs):
    d = {
        'username': 'user1',
    }
    password = kwargs.pop('password', None)
    d.update(kwargs)
    user = User(**d)
    if password:
        user.set_password(password)
    user.save()
    return user


def factory_image():
    small_gif = (
     b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
     b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
     b'\x02\x4c\x01\x00\x3b'
    )
    img = SimpleUploadedFile('small.gif', small_gif, content_type='image/gif')
    return img


def factory_content_image(**kwargs):
    img = factory_image()
    d = {
        'content_image': img
    }
    d.update(kwargs)
    if not 'blog' in d:
        d['blog'] = factory_blog()
    return blog.models.ContentImage.objects.create(**d)
