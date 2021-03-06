from django.urls import path,re_path
from .views import *

urlpatterns = [
    path("index/",index),
    path("addUser/",addUser),
    path("getData/",getData),
    path("updateUser/",updateUser),
    path("deleteUser/",deleteUser),
    path("doubleLine/",doubleLine),
    path("foreignAdd/",foreignAdd),
    path("foreignGet/",foreignGet),
    path("foreignUpdate/",foreignUpdate),
    path("foreignDelete/",foreignDelete),
    path("choiceDemo/",choiceDemo),
    path("ManyAdd/",ManyAdd),
    path("ManyGet/",ManyGet),
    path("ManyUpdate/",ManyUpdate),
    path("ManyDelete/",ManyDelete),
    path("juheView/",juheView),
    path("FTest/",FTest),
    path("Qtest/",Qtest),
]

