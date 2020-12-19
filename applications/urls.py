from django.urls import path

import applications.views


urlpatterns = [
    path('monty_hole/', applications.views.index, name='index'),
    path('monty_hole/result/', applications.views.result, name='result'),
]
