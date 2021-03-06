"""ArticleBlog URL Configuration

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
from .views import *
from Article.views import login,logout,searchtitle
urlpatterns = [
    path('admin/', admin.site.urls),
    path("index/",index),
    re_path("^$",index),
    path("about/",about,name="aboutnew"),
    path("listpic/",listpic),
    path("newslistpic/",newslistpic),
    re_path("newslistpic/(?P<type>\w+)/(?P<page>\d+)/",newslistpic),
    path("base/",base),
    path("fytest/",fytest),
    # path("addArticle/",addArticle),
    # path("articleDetails/",articleDetails),
    re_path("articleDetails/(?P<id>\d+)/",articleDetails),
    path("ckeditor/",include("ckeditor_uploader.urls")),
    path("requsttest/",requsttest),
    path("reqtest/",reqtest),
    path("search/",search),
    path("reqpost/",reqpost),
    path("register/",register),
    path("ajaxtest/",ajaxtest),
    path("ajaxdemo/",ajaxdemo),
    path("ajaxreq/",ajaxreq),
    path("ajaxregister/",ajaxregister),
    path("ajaxpost/",ajaxpost),
    path("login/",login),
    path("logout/",logout),
    path("searchtitle/",searchtitle),
    path("article/",include("Article.urls")),

]
