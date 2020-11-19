from django.urls import path

import randomapp.views


urlpatterns = [
    path('random', randomapp.views.perform, name='perform'),
]
