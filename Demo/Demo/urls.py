"""Demo URL Configuration

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
from django.urls import path,re_path,include
from . import views
# from app01 import views as app01views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("index/",views.index),
    path("app01/",include("app01.urls")),
    # path("app01/index/",app01views.index),
    path("hello/",views.hello),
    path("demo01/",views.demo1),
    re_path("^$",views.index),
    re_path("demo/(\d)/",views.demo),
    # re_path("demo02/(\d{4})/(\w*)/",views.demo02),
    re_path("demo02/(?P<year>\d{4})/(?P<city>\w*)/",views.demo02),
    path("tpltest/",views.tpltest),
    path("myindex/",views.myindex),
    path("myindex2/",views.myindex2),
    path("myindex3/",views.myindex3),
    path("tmptest/",views.tmptest),
    path("statictest/",views.statictest),
    path("demotest/",views.demotest),



]
