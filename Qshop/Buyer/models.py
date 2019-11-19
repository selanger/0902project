from django.db import models
from Seller.models import LoginUser,Goods

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
    class Meta:
        db_table = 'payorder'
        verbose_name = '订单表'

class OrderInfo(models.Model):
    order_id = models.ForeignKey(to=PayOrder,on_delete=models.CASCADE)
    goods = models.ForeignKey(to=Goods,on_delete=models.CASCADE)
    goods_price =  models.FloatField(verbose_name="商品单价")   ## 订单创建的时候商品单价
    goods_count = models.IntegerField(verbose_name="订单商品数量")
    goods_total_price = models.FloatField(verbose_name="商品小计")

    class Meta:
        db_table = 'orderinfo'
        verbose_name = "订单详情表"




