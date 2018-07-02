#!usr/bin/env python
# _*_ coding:utf-8 _*_

from django.urls import path

# 调用login.views里面的方法
from login.views import test, index


urlpatterns = [
    path(r'test/', test),
    path(r'index', index),
]