from django.urls import path,re_path
from .views import *

urlpatterns = [
    path("index/",index),
    path("register/", register),
    path("login/", login),
    path("logout/", logout),
    path("goods_list/", goods_list),
    re_path("goods_list/(?P<type>\d{0,1})/(?P<page>\d+)/", goods_list),
    re_path("goods_status/(?P<type>\w+)/(?P<id>\d+)/", goods_status),
    path("personinfo/", PersonInfo),
    path("goods_add/", goods_add),

]