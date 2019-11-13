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








