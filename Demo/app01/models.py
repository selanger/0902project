from django.db import models

# Create your models here.
class User(models.Model):

    # id = models.AutoField(primary_key=True)  ## 主键
    name = models.CharField(max_length=32,verbose_name="姓名")   ## 名字 字符串
    age = models.IntegerField(verbose_name="年龄")              ## int 年龄
    gender = models.CharField(max_length=4,verbose_name="性别")  ## 性别  int 0 1 string nan nv
    height = models.DecimalField(max_digits=5,decimal_places=2,verbose_name="身高")
    birthday = models.DateField(verbose_name="生日",default="2019-02-01")
    now_time = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.name   ## 返回用户名

    class Meta:
        db_table = "user"
        # ordering = ["-id","name","age"]
        verbose_name = "用户表"   ## 在站点后台中以中文的形式显示表名
        verbose_name_plural = verbose_name   ### 默认以复数显示




class HomeNew(models.Model):
    no = models.CharField(max_length=20)
    price = models.FloatField()
    address = models.TextField()

    class Meta:
        db_table = "homenew"

class Publish(models.Model):

    name = models.CharField(max_length=32,verbose_name="出版社名字")
    address = models.TextField(verbose_name="出版社地址")
    class Meta:
        db_table = "publish"


class Book(models.Model):
    name = models.CharField(max_length=32,verbose_name="书名")
    publish = models.ForeignKey(to=Publish,on_delete=models.CASCADE)
    num = models.IntegerField(default=100,verbose_name="库存量")
    sell_num = models.IntegerField(default=100,verbose_name="已售数量")

    class Meta:
        db_table = "book"


class Person(models.Model):
    name = models.CharField(max_length=32)
    age= models.IntegerField()
    height = models.FloatField()
    birthday = models.DateField(auto_now=True)
    # teacher = models.ManyToManyField(to=Teacher)

    class Meta:
        db_table = "person"

GENDER_LIST = (
    (0,"女"),
    (1,"男")
)
class Teacher(models.Model):
    name = models.CharField(max_length=32)
    # gender = models.IntegerField()  ## 0 代表女  1代表男
    gender = models.IntegerField(choices=GENDER_LIST)
    person = models.ManyToManyField(to=Person)
    ##学科   数学 语文  英语



    class Meta:
        db_table = "teacher"





















