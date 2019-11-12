from django.urls import path
from .views import *

urlpatterns = [
    path("checkuser/",checkuser),
    path("login/",login),
]