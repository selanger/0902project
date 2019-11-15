"""DjangoLogin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from LoginUser.views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('admin/', admin.site.urls),
    path('loginuser/',include("LoginUser.urls")),
    path("goods_list/",goods_list),
    re_path("goods_list/(?P<type>\d{0,1})/(?P<page>\d+)/",goods_list),
    re_path("goods_list_api/(?P<type>\d{0,1})/(?P<page>\d+)/",goods_list_api),
    re_path("goods_status/(?P<type>\w+)/(?P<id>\d+)/",goods_status),
    path("goodsview/",csrf_exempt(GoodsView.as_view())),
    path("personinfo/",PersonInfo),

]

from rest_framework import routers
router = routers.DefaultRouter()     ## 定义一个  路由集合
router.register("goods",GoodsViewsSet)    ### restful 视图收集路由
router.register("user",UserViewsSet)    ### restful 视图收集路由

urlpatterns += [
    re_path("^API/", include(router.urls))
]

