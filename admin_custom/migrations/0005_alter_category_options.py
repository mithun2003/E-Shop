# Generated by Django 4.1.2 on 2023-01-12 11:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_custom', '0004_alter_product_category_variation'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
    ]