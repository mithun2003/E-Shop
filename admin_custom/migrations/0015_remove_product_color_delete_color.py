# Generated by Django 4.1.2 on 2023-01-27 07:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_custom', '0014_remove_variation_product_product_variation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='color',
        ),
        migrations.DeleteModel(
            name='Color',
        ),
    ]