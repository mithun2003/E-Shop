# Generated by Django 4.1.2 on 2023-02-03 06:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_custom', '0024_product_offered_price'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('product_name',), 'verbose_name': 'My Model', 'verbose_name_plural': 'My Models'},
        ),
    ]