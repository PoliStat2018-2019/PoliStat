from django.urls import path, include, re_path

from . import models, views

# Allows for namespacing views using 'app_name:view_name'
app_name='figures'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('states/', views.statemap, name='states'),
    path('states/<str:state>/', views.state, name='state'),
    path('states/<str:state>/<int:districtno>/', views.district, name='district')
]