from django.urls import path, include

from . import models, views

# Allows for namespacing views using 'app_name:view_name'
app_name='blog'

urlpatterns = [
    path('', views.about, name='about'),
    path('blog/<int:pk>/<slug:slug>', views.view_post, name='view_post')
]
