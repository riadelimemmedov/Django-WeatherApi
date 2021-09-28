from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('',index,name='index'),
    path('delete-city/<str:name>',delete_city,name="delete_city")
]
