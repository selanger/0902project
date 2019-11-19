# Generated by Django 2.2.1 on 2019-11-19 09:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Seller', '0006_goods_goods_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='PayOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=32, verbose_name='订单编号')),
                ('order_date', models.DateField(auto_now=True, verbose_name='创建日期')),
                ('order_status', models.IntegerField(choices=[(1, '未支付'), (2, '已支付'), (3, '待发货'), (4, '已发货'), (5, '完成'), (6, '拒收')], verbose_name='订单状态')),
                ('order_total', models.FloatField(verbose_name='订单总价')),
                ('order_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Seller.LoginUser', verbose_name='买家')),
            ],
            options={
                'verbose_name': '订单表',
                'db_table': 'payorder',
            },
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_price', models.FloatField(verbose_name='商品单价')),
                ('goods_count', models.IntegerField(verbose_name='订单商品数量')),
                ('goods_total_price', models.FloatField(verbose_name='商品小计')),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Seller.Goods')),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Buyer.PayOrder')),
            ],
            options={
                'verbose_name': '订单详情表',
                'db_table': 'orderinfo',
            },
        ),
    ]
