# Generated by Django 2.2.1 on 2019-11-13 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LoginUser', '0002_auto_20191113_1526'),
    ]

    operations = [
        migrations.AddField(
            model_name='loginuser',
            name='username',
            field=models.CharField(default='test', max_length=32),
            preserve_default=False,
        ),
    ]
