## 编写 过滤器
from rest_framework import serializers
from .models import *

class GoodsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:        ###  元类
        model = Goods
        fields = [
            "id",
            "goods_number",
            "goods_name",
            "goods_price",
            "goods_count",
            "goods_location",
            "goods_safe_data",
            "goods_pro_time",
            "goods_status",
        ]   ##  将来restful 要返回的字段



class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:        ###  元类
        model = LoginUser
        fields = [
            "id",
            "email",
            "password",
            "username",
        ]   ##  将来restful 要返回的字段
