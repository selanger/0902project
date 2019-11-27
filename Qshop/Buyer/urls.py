from django.urls import path,re_path
from .views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    path("index/",cache_page(200)(index)),
    path("login/",login),
    path("register/",register),
    path("logout/",logout),
    path("base/",base),
    path("goodslist/",goodslist),
    path("person_info/",person_info),
    path("cart/",cart),
    path("user_center_order/",user_center_order),
    path("user_center_site/",user_center_site),
    path("place_order/",place_order),
    path("payorder/",payorderAli),
    path("payresult/",payresult),
    path("add_cart/",add_cart),
    path("change_cart/",change_cart),
    path("delete_cart/",delete_cart),
    path("temptest/",temptest),
    path("place_order_more/",place_order_more),
    path("updateAddress/",updateAddress),
    re_path("goodsdetail/(?P<goods_id>\d+)/",goodsdetail),
]
