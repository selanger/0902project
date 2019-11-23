# Generated by Django 2.2.1 on 2019-11-23 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Seller', '0006_goods_goods_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='ValidCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=32, verbose_name='验证码内容')),
                ('user', models.CharField(max_length=32, verbose_name='用户')),
                ('date', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
            ],
        ),
    ]
