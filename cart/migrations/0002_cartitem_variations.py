# Generated by Django 4.1.2 on 2023-01-14 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_custom', '0006_alter_product_price'),
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='variations',
            field=models.ManyToManyField(blank=True, to='admin_custom.variation'),
        ),
    ]
