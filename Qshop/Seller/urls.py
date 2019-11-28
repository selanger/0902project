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
    path("get_code/", get_code),
    path("get_goods/", get_goods),
    path("update_goods/", update_goods),
    path("change_order/", change_order),
    path("order/", order),
    re_path("cachetest/(\d)/", cachetest),
    # path("middletest/", middletest),
    # re_path("middletest/(\w+)/", middletest),
    re_path("middletest/(?P<date>\w+)/", middletest),

]