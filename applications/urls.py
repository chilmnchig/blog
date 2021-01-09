from django.urls import path

from .views import monty_hole


urlpatterns = [
    path('monty_hole/', monty_hole.index, name='index'),
    path('monty_hole/result/', monty_hole.result, name='result'),
]
