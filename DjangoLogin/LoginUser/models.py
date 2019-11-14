from django.db import models

# Create your models here.

GENDER_LIST = (
    (0,'女'),
    (1,'男')
)
class LoginUser(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=32)
    username = models.CharField(max_length=32)
    # phone_number = models.CharField(max_length=32,null=True,blank=True)
    # age = models.IntegerField(null=True,blank=True)
    # gender = models.IntegerField(choices=GENDER_LIST)
    # address = models.TextField()


    class Meta:
        db_table = "loginuser"


# null=True  针对数据库，可以为空，即 保存在数据库中的时候 可以为空
# blank=True  针对表单，表示在表单中可以不填该字段，对数据库没有任何影响



class Goods(models.Model):
    goods_number = models.CharField(max_length=32,verbose_name="商品编号")
    goods_name = models.CharField(max_length=32,verbose_name="商品名称")
    goods_price = models.FloatField(verbose_name="商品价格")
    goods_count = models.IntegerField(verbose_name="数量")
    goods_location = models.TextField(verbose_name="生产地")
    goods_safe_data = models.IntegerField(verbose_name="保质期")   ##
    goods_pro_time = models.DateField(auto_now=True,verbose_name="生产日期")  ## 生产日期
    goods_status = models.IntegerField(default=1)   ## 0 代表下架   1 代表上架

    class Meta:
        db_table = "goods"













