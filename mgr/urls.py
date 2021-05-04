# -*-coding:utf-8-*-
from django.urls import path

from . import views

app_name = 'mgr'
urlpatterns = [
    path('views', views.dispatcher),
]