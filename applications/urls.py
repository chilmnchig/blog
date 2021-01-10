from django.urls import path

from .views import monty_hole, typing


urlpatterns = [
    path('monty_hole/', monty_hole.index, name='index'),
    path('monty_hole/result/', monty_hole.result, name='result'),
    path('typing/', typing.index, name='typing'),
]
