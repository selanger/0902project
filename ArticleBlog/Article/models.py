from django.db import models

# Create your models here.

GENDER_LIST = (
    (0,"女"),
    (1,"男")
)
class Author(models.Model):
    name = models.CharField(max_length=32,verbose_name="作者姓名")
    gender = models.IntegerField(choices=GENDER_LIST,verbose_name="性别")
    age = models.IntegerField(verbose_name="年龄")
    email = models.EmailField(verbose_name="邮箱")

    class Meta:
        db_table = "author"



class Type(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField()
    class Meta:
        db_table = "type"

class Article(models.Model):
    title = models.CharField(max_length=32)
    date = models.DateField(auto_now=True)
    content = models.TextField()
    description = models.TextField()
    author = models.ForeignKey(to=Author,on_delete=models.CASCADE)
    type = models.ManyToManyField(to=Type)
    class Meta:
        db_table = "article"







