# Generated by Django 4.1.2 on 2023-02-02 07:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_alter_order_order_total_alter_order_tax'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='product',
        ),
        migrations.RemoveField(
            model_name='order',
            name='product_price',
        ),
        migrations.RemoveField(
            model_name='order',
            name='quantity',
        ),
    ]