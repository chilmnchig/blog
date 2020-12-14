from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import base

import blog.views


urlpatterns = [
    path('', blog.views.blog_list, name='list'),
    path('<int:blog_id>/', blog.views.blog_detail, name='detail'),
    path('addBlog/', blog.views.blog_add, name='add'),
    path('signup/', blog.views.signup, name='signup'),
    path('login/',
         auth_views.LoginView.as_view(template_name="blog/login.html"),
         name='login'
         ),
    path('logout/',
         auth_views.LogoutView.as_view(next_page="list"),
         name='logout'
         ),
    path('accounts/login/', base.RedirectView.as_view(pattern_name="login")),
    path('accounts/profile/',
         base.RedirectView.as_view(pattern_name="user_menu")
         ),
    path('userMenu', blog.views.user_menu, name='user_menu'),
    path('<int:blog_id>/edit', blog.views.edit, name='edit'),
    path('text_list', blog.views.blog_text_list, name='text_list'),
    path('upload/', blog.views.image_upload, name='image_upload'),
    path('image_list', blog.views.image_list, name='image_list'),
]
