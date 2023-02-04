# Generated by Django 4.1.2 on 2023-01-29 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('admin_custom', '0016_product_is_offers'),
        ('shop', '0005_remove_product_category_delete_category_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cat_Off',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon_name', models.CharField(default=None, max_length=20, null=True)),
                ('offers', models.IntegerField(default=None, null=True)),
                ('category', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_custom.category')),
            ],
        ),
    ]
