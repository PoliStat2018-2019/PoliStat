from django.urls import path, include

from . import models, views

# Allows for namespacing views using 'app_name:view_name'
app_name='figures'

urlpatterns = [
    path('', views.index, name='index')
]