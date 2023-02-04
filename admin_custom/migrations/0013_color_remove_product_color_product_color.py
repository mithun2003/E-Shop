# Generated by Django 4.1.2 on 2023-01-27 06:40

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('admin_custom', '0012_alter_product_color'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', multiselectfield.db.fields.MultiSelectField(choices=[('Red', 'Red'), ('Black', 'Black'), ('Blue', 'Blue'), ('White', 'White'), ('Green', 'Green')], default='', max_length=1000)),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='color',
        ),
        migrations.AddField(
            model_name='product',
            name='color',
            field=models.ManyToManyField(blank=True, to='admin_custom.color'),
        ),
    ]
