# Generated by Django 4.1.2 on 2023-01-28 16:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_alter_cartitem_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='cart.cart'),
        ),
    ]
