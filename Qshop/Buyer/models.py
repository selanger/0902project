from django.db import models
from Seller.models import LoginUser,Goods,UserAddress

# Create your models here.
ORDER_STATUS = (
    (1,'未支付'),
    (2,'已支付'),
    (3,'待发货'),
    (4,'已发货'),
    (5,'完成'),
    (6,'拒收')
)
class PayOrder(models.Model):
    order_number = models.CharField(max_length=32,verbose_name="订单编号")
    order_date = models.DateField(auto_now=True,verbose_name="创建日期")
    order_status = models.IntegerField(choices=ORDER_STATUS,verbose_name="订单状态")
    order_total = models.FloatField(verbose_name="订单总价")
    order_user = models.ForeignKey(to=LoginUser,on_delete=models.CASCADE,verbose_name="买家")
    # order_address = models.IntegerField(verbose_name="订单收货地址",default=1)
    order_address = models.ForeignKey(to=UserAddress,verbose_name="订单收货地址",default=1,on_delete=models.CASCADE)
    class Meta:
        db_table = 'payorder'
        verbose_name = '订单表'

class OrderInfo(models.Model):
    order_id = models.ForeignKey(to=PayOrder,on_delete=models.CASCADE)
    goods = models.ForeignKey(to=Goods,on_delete=models.CASCADE)
    goods_price =  models.FloatField(verbose_name="商品单价")   ## 订单创建的时候商品单价
    goods_count = models.IntegerField(verbose_name="订单商品数量")
    goods_total_price = models.FloatField(verbose_name="商品小计")
    store = models.ForeignKey(to=LoginUser,on_delete=models.CASCADE)
    order_status = models.IntegerField(choices=ORDER_STATUS,verbose_name="订单详情状态",default="1")

    class Meta:
        db_table = 'orderinfo'
        verbose_name = "订单详情表"


"""
- id
- 商品的名字
- 商品的数量
- 商品的单价
- 买家
- 店铺名
- 单件商品的总价
"""
class Cart(models.Model):
    goods = models.ForeignKey(to=Goods,on_delete=models.CASCADE,verbose_name="商品表外键")
    goods_number = models.IntegerField(verbose_name="商品数量")
    cart_user = models.ForeignKey(to=LoginUser,on_delete=models.CASCADE,verbose_name="买家")
    goods_total = models.FloatField(verbose_name="单件商品的总价")
    payorder = models.CharField(default='0',verbose_name="订单表的订单号",max_length=32)

    class Meta:
        db_table = "cart"
        verbose_name = "购物车表"







