# -*-coding:utf-8-*-
from django.urls import path

from . import views
from . import manager
from . import articles

app_name = 'mgr'
urlpatterns = [
    path('views', views.dispatcher),
    path('manager', manager.dispatcher),
    path('articles', articles.dispatcher),
]