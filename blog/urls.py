from django.contrib import admin
from django.urls import path

import blog.views


urlpatterns = [
    path('', blog.views.blog_list, name='list'),
    path('<int:blog_id>/', blog.views.blog_detail, name='detail')
    # path('add/', blog.views.blog_add, name='add'),
]
